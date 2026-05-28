---
layout: post
title: "华为CloudEngine交换机运维命令速查手册"
date: 2026-05-28
categories: 网络工程
tags: [华为, CE交换机, 运维, 命令速查]
---

日常运维中最常用的华为CE系列交换机命令，按场景分类整理，直接复制可用。

<!--more-->

## 设备基础信息

```bash
# 查看设备基本信息（型号、版本、运行时间)
display version

# 查看设备序列号（资产登记、报修用)
display esn

# 查看当前配置（筛选关键配置)
display current-configuration | include vlan
display current-configuration | section bgp
display current-configuration | begin interface GE1/0/1

# 查看CPU和内存使用率
display cpu-usage
display memory-usage

# 查看设备温度和电源状态
display temperature all
display power
display fan
```

## 接口管理

```bash
# 查看所有接口状态摘要
display interface brief

# 查看特定接口详细信息（流量、错包、光模块)
display interface 100GE1/0/1

# 查看接口光模块信息（光功率、温度)
display transceiver interface 100GE1/0/1

# 批量查看所有光模块状态
display transceiver brief

# 接口流量统计（判断是否拥塞)
display interface 100GE1/0/1 | include rate

# 清除接口计数器（排查前先清零)
reset counters interface 100GE1/0/1
```

> **运维经验**：光模块收发光功率是排查链路质量的第一步。正常范围：接收光功率 -14dBm ~ 0dBm，发送光功率 0dBm ~ +4dBm。低于 -17dBm 就要注意了。

## VLAN与二层

```bash
# 查看VLAN信息
display vlan brief
display vlan 1001

# 查看MAC地址表
display mac-address
display mac-address vlan 1001
display mac-address interface 100GE1/0/1

# 查看ARP表
display arp all
display arp vlan 1001

# STP状态
display stp brief
display stp interface 100GE1/0/1
```

## 三层路由

```bash
# 查看路由表摘要
display ip routing-table statistics

# 查看特定目的路由
display ip routing-table 10.110.1.1

# 查看BGP邻居状态
display bgp peer
display bgp peer 10.1.10.1 verbose

# 查看BGP路由（VPN实例)
display bgp vpnv4 vpn-instance vrf1 all

# 查看OSPF邻居
display ospf peer brief
display ospf 1 peer

# 查看OSPF LSDB摘要
display ospf lsdb brief

# 查看EVPN路由
display evpn vpn-instance brief
display bgp evpn all
```

## VXLAN / EVPN

```bash
# 查看VXLAN隧道
display vxlan tunnel all

# 查看VNI映射
display vxlan vni
display bridge-domain

# 查看EVPN路由（MAC/IP)
display bgp evpn all | include Type
display bgp evpn route-type 2

# 查看远端MAC学习
display mac-address remote

# 查看NVE接口
display interface nve1

# 排查VXLAN隧道建立问题
display vxlan peer
display bgp evpn peer
```

## 安全与ACL

```bash
# 查看ACL匹配统计
display acl 3001
display traffic-filter statistics interface 100GE1/0/1

# 查看DHCP Snooping绑定表
display dhcp snooping user-bind all

# 查看动态ARP检测统计
display arp anti-attack statistics

# 查看风暴抑制配置
display storm suppression interface 100GE1/0/1
```

## QoS与流量管理

```bash
# 查看端口队列统计
display qos queue-statistics interface 100GE1/0/1

# 查看流量策略绑定
display traffic-policy applied-record

# 查看接口带宽利用率
display interface 100GE1/0/1 | include bandwidth
```

## 常用排障组合

```bash
# 一键排查链路问题
display interface brief | include down
display transceiver brief | include -
display logbuffer | include ERROR

# 排查路由振荡
display trapbuffer | include BGP
display logbuffer | include OSPF
display bgp peer | include Idle|Connect

# 排查MAC漂移
display mac-address flapping record
display trapbuffer | include MAC_FLP
```

## 保存与维护

```bash
# 保存配置
save
save force

# 查看配置差异（修改前必做)
display configuration changes

# 回退配置（重要操作前打快照)
display saved-configuration
startup saved-configuration flash:/backup.cfg

# 定时保存配置（防止遗忘)
schedule save-configuration at 02:00 daily
```

---

> **总结**：运维命令不在于多，在于用对场景。以上命令覆盖了日常80%的运维场景，建议收藏备用。遇到具体问题时，先 `display` 看状态，再 `display logbuffer` 看日志，最后 `display current-configuration` 看配置。
