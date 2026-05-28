---
layout: post
title: "VXLAN EVPN数据中心网络实战：从原理到配置"
date: 2026-05-28
categories: 数据中心
tags: [VXLAN, EVPN, 数据中心, 华为CE]
---

VXLAN EVPN已成为数据中心网络的事实标准。本文从控制面到数据面，用真实配置讲清楚VXLAN EVPN的核心机制。

<!--more-->

## 为什么是VXLAN EVPN？

传统数据中心网络的痛点：
- **VLAN数量限制**：4096个VLAN不够用
- **STP收敛慢**：链路故障收敛时间秒级
- **二层扩展性差**：MAC表爆炸、广播风暴

VXLAN EVPN的解决方案：
- **24位VNI**：支持16M逻辑网络
- **三层overlay**：underlay用IP路由，无STP
- **EVPN控制面**：BGP通告MAC/IP路由，减少泛洪

## 架构总览

```
┌─────────────────────────────────────┐
│          Spine (VTEP RR)            │
│    AS 12100 / LoopBack 10.1.10.1   │
├──────────┬──────────┬───────────────┤
│          │          │               │
│  Leaf-1  │  Leaf-2  │    Leaf-N     │
│ AS 12101 │ AS 12102 │  AS 121xx    │
│ VTEP     │ VTEP     │   VTEP       │
└──────────┴──────────┴───────────────┘
     │          │            │
   Server    Server       Server
```

## Underlay配置：OSPF + BGP

### Spine交换机

```bash
# OSPF underlay（建立LoopBack可达性)
router id 10.1.10.1
ospf 1
 area 0.0.0.0
  network 10.1.10.1 0.0.0.0
  network 10.110.101.0 0.0.0.255

# BGP overlay（EVPN地址族)
bgp 12100
 router-id 10.1.10.1
 peer 10.1.10.11 as-number 12101
 peer 10.1.10.12 as-number 12102
 
 ipv4-family unicast
  peer 10.1.10.11 enable
  peer 10.1.10.12 enable
 
 l2vpn-family evpn
  peer 10.1.10.11 enable
  peer 10.1.10.11 reflect-client
  peer 10.1.10.12 enable
  peer 10.1.10.12 reflect-client
```

### Leaf交换机

```bash
# OSPF underlay
router id 10.1.10.11
ospf 1
 area 0.0.0.0
  network 10.1.10.11 0.0.0.0
  network 10.110.101.0 0.0.0.255

# BGP overlay
bgp 12101
 router-id 10.1.10.11
 peer 10.1.10.1 as-number 12100
 
 ipv4-family unicast
  peer 10.1.10.1 enable
  
 l2vpn-family evpn
  peer 10.1.10.1 enable
```

## Overlay配置：VXLAN隧道与BD

### 创建Bridge Domain和VNI映射

```bash
# 创建BD，映射VNI
bridge-domain 1001
 vxlan vni 1001

# 配置NVE接口（VTEP)
interface Nve1
 source 10.1.10.11
 vni 1001 head-end peer-list protocol bgp
```

### 接入侧配置

```bash
# 服务器接入接口
interface 100GE1/0/1
 port link-type trunk
 port trunk allow-pass vlan 1001

# VLAN绑定BD
vlan 1001
 bridge-domain 1001
```

## EVPN路由类型

| 类型 | 用途 | 触发条件 |
|------|------|----------|
| Type-2 (MAC/IP) | MAC+IP绑定通告 | 主机上线、ARP学习 |
| Type-3 (Inclusive) | VTEP成员发现 | VNI配置完成 |
| Type-5 (IP Prefix) | IP前缀路由 | 路由聚合 |

```bash
# 查看EVPN路由
display bgp evpn all

# 查看Type-2路由（MAC/IP)
display bgp evpn route-type 2

# 查看Type-3路由（VTEP列表)
display bgp evpn route-type 3
```

## 分布式网关（IRB）

```bash
# 配置VBDIF接口作为网关
interface Vbdif1001
 ip address 10.110.1.1 255.255.255.0
 mac-address 0000-5e00-0101
 arp collect host-information
```

## 关键排障命令

```bash
# 1. 检查VXLAN隧道状态
display vxlan tunnel all
# 正常状态应为UP

# 2. 检查NVE接口
display interface nve1
# 确认source IP正确

# 3. 检查EVPN邻居
display bgp evpn peer
# 确认Established

# 4. 检查远端MAC学习
display mac-address remote
# 确认远端MAC已学习

# 5. 检查VNI映射
display vxlan vni
# 确认VNI-BD映射正确

# 6. 抓包排查
display capture-packet interface 100GE1/0/1
```

## 常见问题

| 现象 | 可能原因 | 排查命令 |
|------|----------|----------|
| VXLAN隧道DOWN | LoopBack不可达 | `ping 10.1.10.12` |
| MAC未学习到远端 | EVPN邻居异常 | `display bgp evpn peer` |
| 业务不通 | BD-VNI映射错误 | `display vxlan vni` |
| 广播风暴 | ARP抑制未开启 | `display arp suppression` |

---

> **总结**：VXLAN EVPN的核心是"控制面用BGP EVPN通告MAC/IP，数据面用VXLAN封装在IP网络上转发"。配置三步走：Underlay(OSPF) → Overlay(BGP EVPN) → 接入(BD+VNI)。
