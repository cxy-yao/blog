---
layout: post
title: "VXLAN EVPN 分布式网关基础配置"
date: 2026-05-30
categories: [数据中心]
tags: [VXLAN, EVPN, 华为CE, 分布式网关]
excerpt: "VXLAN EVPN分布式网关是数据中心Fabric的核心组件，本文记录华为CE交换机上的基础配置流程。"
---

## 背景

在 Spine-Leaf 架构中，VXLAN EVPN 分布式网关实现了跨 Leaf 节点的三层互通。每个 Leaf 交换机都充当 VTEP（VXLAN Tunnel Endpoint），通过 EVPN 控制面学习远端主机路由。

## 核心组件

| 组件 | 作用 | 典型设备 |
|------|------|----------|
| Spine | 路由反射器，Underlay 路由 | CE12800 |
| Leaf | VTEP，分布式网关 | CE6800/CE8800 |
| Border Leaf | 外部路由接入 | CE12800 |

## 基础配置步骤

### 1. 配置 NVE 接口

```shell
interface Nve1
 source 10.1.10.1
 vni 10010 head-end peer-list protocol bgp
```

### 2. 配置 BD（Bridge Domain）

```shell
bridge-domain 10
 vxlan vni 10010
#
evpn vpn-instance evpn1 bd-mode
 route-distinguisher 10.1.10.1:10
 vpn-target 65000:10 export-extcommunity
 vpn-target 65000:10 import-extcommunity
```

### 3. 配置分布式网关（IRB 接口）

```shell
interface Vbdif10
 ip binding vpn-instance tenant1
 ip address 192.168.10.1 255.255.255.0
 arp collect host-information
 mac-address 0000-5e00-0101
```

## 验证命令

```shell
display vxlan tunnel all
display evpn vpn-instance verbose
display arp vbdif 10
display mac-address bridge-domain 10
```

## 注意事项

- Anycast Gateway 的 MAC 地址在所有 Leaf 上必须一致
- `arp collect host-information` 用于 EVPN ARP 代理
- IRB 接口的 IP 地址在各 Leaf 上也必须一致（Anycast 模式）

> 更新于 2026-05-30，验证通过




