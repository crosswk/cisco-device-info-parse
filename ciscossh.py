from concurrent.futures import ThreadPoolExecutor


class Ciscossh:
    """用于连接思科路由器交换机和防火墙"""

    def __init__(self, host_ip, username, password, enable_password='', device_type='cisco_ios'):
        self.host_ip = host_ip
        self.username = username
        self.password = password
        self.enable_password = enable_password
        self.device_type = device_type

    def connect_host(self):
        from netmiko import ConnectHandler
        from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

        try:
            cisco_device = {
                'device_type': self.device_type,
                'host':  self.host_ip,
                'username': self.username,
                'password': self.password,
                'secret': self.enable_password
            }
            device_connect = ConnectHandler(**cisco_device)
            device_connect.enable()
            return device_connect

        except NetmikoAuthenticationException:
            return "authentication error"
        except NetmikoTimeoutException:
            return "host unreachable"
        except Exception as e:
            return f"unknown error: {str(e)}"

    def get_device_info_regex(self):
        """使用正则解析从show version中获取hostname、version和系统类型，并返回vendor和mgmt_ip信息"""
        output = self.send_command("show version")

        # 检查连接是否成功
        if isinstance(output, str) and output in ["authentication error", "host unreachable"] or output.startswith(
                "unknown error"):
            # 返回描述性字符串日志信息
            return {"error": f"Failed to connect to device: {output}"}

        import re
        try:
            hostname_match = re.search(r"^(\S+) uptime is", output, re.MULTILINE)
            version_match = re.search(r'Version\s*(.+?)[\s|,|[]', output)
            system_type_match = re.search(r"Cisco IOS[\w -]*(XE)?", output)

            hostname = hostname_match.group(1) if hostname_match else "Unknown"
            version = version_match.group(1) if version_match else "Unknown"
            system_type = "iosxe" if system_type_match and "XE" in system_type_match.group(
                0) else "ios" if system_type_match else "Unknown"

            # 转换版本号格式
            version = re.sub(r'\b0+(\d)', r'\1', version)

            # 新增字段 vendor 和 mgmt_ip
            vendor = "Cisco"
            mgmt_ip = self.host_ip

            return {
                "mgmt_ip": mgmt_ip,
                "hostname": hostname,
                "vendor": vendor,
                "ostype": system_type,
                "version": version,
            }
        except Exception as e:
            # 返回解析错误的日志信息
            return {"error": f"Error parsing 'show version' output: {str(e)}"}

    def send_command(self, command):
        device_connect = self.connect_host()
        if isinstance(device_connect, str):
            return device_connect
        return_info = device_connect.send_command(command, delay_factor=5)
        return return_info


def connect_devices(file_path, username, password, enable_password='', max_threads=10):
    """从文件中读取IP列表，并使用多线程连接设备，返回成功获取信息的设备字典列表"""
    try:
        # 读取设备IP列表
        with open(file_path, 'r', encoding='utf-8') as f:
            host_list = [line.strip() for line in f.readlines()]

        successful_devices = []

        # 定义处理单个设备的逻辑
        def process_device(host):
            my_device = Ciscossh(host, username, password, enable_password)
            result = my_device.get_device_info_regex()
            if "error" not in result:
                successful_devices.append(result)
            else:
                print(f"无法连接到设备 {host}: {result['error']}")

        # 使用多线程连接设备
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            executor.map(process_device, host_list)

        return successful_devices

    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
        return []

# 测试代码
if __name__ == "__main__":
    results = connect_devices(file_path="hosts_ip.txt", username="admin", password="cisco", enable_password="", max_threads=100)
    print("成功获取设备信息:", results)
