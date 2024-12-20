# cisco-device-info-parse
使用 Netmiko 和多线程快速收集思科网络设备（路由器、交换机、防火墙）的信息，包括主机名、版本、操作系统类型等。

此项目使用 Python 和 `Netmiko` 库，通过 SSH 协议连接思科网络设备（路由器、交换机、防火墙），并快速收集设备的基本信息，例如主机名、操作系统版本和类型等。使用多线程加速了信息收集的过程。

## 功能特性

*   **支持多种思科设备：** 可以连接运行 Cisco IOS 和 IOS XE 的设备。
*   **多线程加速：** 使用多线程并发连接多个设备，提高信息收集效率。
*   **自动解析设备信息：** 通过正则表达式解析 `show version` 命令的输出，提取关键信息。
*   **错误处理：** 对连接错误、身份验证失败和解析错误进行了处理，并返回描述性的错误信息。
*   **简洁的输出：** 返回一个字典列表，每个字典包含一个设备的信息，方便后续处理。

## 使用方法

1.  **环境准备：**
    *   确保你已经安装了 Python 3.6 或更高版本。
    *   安装 `netmiko` 库：
        ```bash
        pip install netmiko
        ```
2.  **准备设备 IP 列表：**
    *   创建一个名为 `hosts_ip.txt` 的文件，每行包含一个思科设备的 IP 地址。例如：
        ```
        192.168.1.1
        192.168.1.2
        10.0.0.10
        ```
3.  **运行脚本：**
    *   将 `ciscossh.py` 文件和 `hosts_ip.txt` 文件放在同一个目录下。
    *   修改 `ciscossh.py` 文件中的用户名、密码和 enable 密码（如果需要）。
    *   运行以下命令：
        ```bash
        python ciscossh.py
        ```

## 代码说明

*   **`ciscossh.py`:**
    *   `Ciscossh` 类封装了与单个思科设备的连接和信息收集操作。
    *   `connect_host()` 方法负责建立 SSH 连接。
    *   `get_device_info_regex()` 方法发送 `show version` 命令，并使用正则表达式解析结果。
    *   `send_command()` 方法发送命令并返回结果。
    *   `connect_devices()` 函数读取设备列表，并使用多线程连接设备并获取信息。
*   **`hosts_ip.txt`:** 包含需要连接的设备的 IP 地址列表。

## 示例输出
成功获取设备信息: [{'mgmt_ip': '192.168.1.1', 'hostname': 'sw1', 'vendor': 'Cisco', 'ostype': 'iosxe', 'version': '17.9.3'}, {'mgmt_ip': '192.168.1.2', 'hostname': 'sw2', 'vendor': 'Cisco', 'ostype': 'ios', 'version': '15.2(7)E2'}]


## 注意事项
*   确保你的 Python 环境安装了 `netmiko` 库。
*   请替换 `ciscossh.py` 文件中的占位符用户名、密码和 enable 密码为你的实际信息。
*   请确保你拥有访问目标思科设备的权限。
*   如果设备数量较多，请适当调整 `max_threads` 参数。
