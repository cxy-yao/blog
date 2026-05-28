---
layout: post
title: "WSL2网络工程师效率工具箱"
date: 2026-05-28
categories: Linux
tags: [WSL2, 效率工具, Python, 网络自动化]
---

在WSL2环境下搭建一套网络工程师的效率工具链——从SSH管理到自动化脚本，从网络抓包到文档写作，全流程覆盖。

<!--more-->

## 基础环境配置

### WSL2网络注意事项

```bash
# WSL2使用NAT网络，IP会变化
# 查看WSL2 IP
hostname -I

# 端口映射到Windows（从外部访问WSL服务)
# Windows PowerShell执行：
netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=8080 connectaddress=$(wsl hostname -I | cut -d' ' -f1)
```

### 必装工具清单

```bash
# 网络工具
sudo apt install -y mtr-tiny nmap tcpdump iperf3 netcat-openbsd

# SSH管理
sudo apt install -y openssh-client autossh

# Python环境
sudo apt install -y python3-pip python3-venv
python3 -m venv ~/venvs/nettools
source ~/venvs/nettools/activate
pip install netmiko paramiko napalm nornir

# 其他工具
sudo apt install -y jq htop tree fzf ripgrep bat
```

## SSH连接管理

### SSH Config优化

```bash
# ~/.ssh/config
Host spine1
    HostName 192.168.17.10
    User admin
    IdentityFile ~/.ssh/id_rsa
    ServerAliveInterval 30
    ServerAliveCountMax 3
    
Host leaf*
    ProxyJump spine1
    User admin
    
# 通配符匹配
Host 192.168.17.*
    User admin
    StrictHostKeyChecking no
```

### sshpass批量管理

```bash
# 安装
sudo apt install sshpass

# 批量执行命令
for host in spine1 leaf1 leaf2; do
    echo "=== $host ==="
    sshpass -p 'password' ssh -o StrictHostKeyChecking=no admin@$host "display version | include Version"
done
```

## Python网络自动化

### Netmiko批量配置

```python
from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor

devices = [
    {"device_type": "huawei", "host": "192.168.17.10", 
     "username": "admin", "password": "pass"},
    {"device_type": "huawei", "host": "192.168.17.11",
     "username": "admin", "password": "pass"},
]

def config_device(device):
    conn = ConnectHandler(**device)
    output = conn.send_command("display version | include Version")
    conn.disconnect()
    return f"{device['host']}: {output.strip()}"

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(config_device, devices))
    for r in results:
        print(r)
```

### Nornir框架

```python
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

result = nr.run(
    task=netmiko_send_command,
    command_string="display interface brief"
)
print_result(result)
```

## 网络诊断工具

### mtr路由追踪

```bash
# 持续追踪路径质量
mtr -r -c 100 10.1.10.1

# 输出解读：
# Loss%  — 丢包率
# Snt    — 发包数
# Last/Avg — 延迟
```

### tcpdump抓包

```bash
# 抓取BGP报文（端口179)
sudo tcpdump -i eth0 port 179 -nn -v

# 抓取OSPF报文（协议号89)
sudo tcpdump -i eth0 proto 89 -nn

# 抓取VXLAN封装（UDP 4789)
sudo tcpdump -i eth0 udp port 4789 -nn

# 保存pcap文件（用Wireshark分析)
sudo tcpdump -i eth0 -w capture.pcap -c 1000
```

### iperf3带宽测试

```bash
# 服务端
iperf3 -s -p 5201

# 客户端（TCP测试)
iperf3 -c 10.1.10.1 -p 5201 -t 30 -P 4

# 客户端（UDP测试，100Mbps)
iperf3 -c 10.1.10.1 -p 5201 -u -b 100M
```

## 文档与知识管理

### Markdown写作

```bash
# 推荐：直接用VSCode + Markdown Preview Enhanced
code ~/workspace/

# 命令行转换
pandoc input.md -o output.html --standalone
```

### 知识库构建

```bash
# 目录结构建议
knowledge-base/
├── 01-网络基础/
│   ├── TCP-IP协议栈.md
│   └── 以太网技术.md
├── 02-路由交换/
│   ├── OSPF配置指南.md
│   └── BGP详解.md
├── 03-数据中心/
│   ├── VXLAN-EVPN.md
│   └── Spine-Leaf架构.md
└── 04-故障案例/
    ├── BGP路由泄露.md
    └── OSPF邻居震荡.md
```

## 自动化脚本集

### 设备健康检查

```bash
#!/bin/bash
# health_check.sh — 批量设备巡检
HOSTS="spine1 leaf1 leaf2 leaf3"
DATE=$(date +%Y%m%d)
REPORT="health_report_${DATE}.txt"

for host in $HOSTS; do
    echo "=== $host ===" >> $REPORT
    sshpass -p 'pass' ssh admin@$host "
        display cpu-usage
        display memory-usage
        display interface brief | include down
        display logbuffer | tail 10
    " >> $REPORT 2>&1
    echo "" >> $REPORT
done
echo "Report saved to $REPORT"
```

### 配置备份

```bash
#!/bin/bash
# backup_config.sh — 自动备份配置到Git
BACKUP_DIR=~/config-backup
cd $BACKUP_DIR

for host in spine1 leaf1 leaf2; do
    sshpass -p 'pass' ssh admin@$host "display saved-configuration" > ${host}.cfg
done

git add -A
git commit -m "Config backup $(date +%Y-%m-%d_%H:%M)"
git push
```

## tmux多窗口管理

```bash
# 安装
sudo apt install tmux

# 创建网络运维session
tmux new-session -s netops -d
tmux send-keys -t netops "ssh spine1" C-m
tmux split-window -h -t netops
tmux send-keys -t netops "ssh leaf1" C-m
tmux split-window -v -t netops
tmux send-keys -t netops "mtr 10.1.10.1" C-m
tmux attach -t netops
```

---

> **总结**：WSL2是网络工程师的理想工作环境——原生Linux工具、SSH无缝连接、Python自动化一应俱全。关键配置：1) SSH Config简化连接 2) Netmiko/Nornir自动化 3) tmux多窗口 4) 知识库结构化管理。
