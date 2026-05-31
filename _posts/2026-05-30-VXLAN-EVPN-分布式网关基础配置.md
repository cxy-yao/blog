---
layout: post
title: "VXLAN EVPN 分布式网关基础配置"
date: 2026-05-30
categories: [数据中心]
tags: [VXLAN, EVPN, 华为CE, 分布式网关]
excerpt: "VXLAN EVPN分布式网关是数据中心Fabric的核心组件，本文记录华为CE交换机上的基础配置流程。"
dc-sync: true
dc-source: "DC/VXLAN-EVPN分布式网关基础配置.md"
---

## 背景

在 Spine-Leaf 架构中，VXLAN EVPN 分布式网关实现了跨 Leaf 节点的三层互通。每个 Leaf 交换机都充当 VTEP（VXLAN Tunnel Endpoint），通过 EVPN 控制面学习远端主机路由。

## 拓扑图



## 核心组件

| 组件 | 作用 | 典型设备 |
|------|------|----------|
| Spine | 路由反射器，Underlay 路由 | CE12800 |
| Leaf | VTEP，分布式网关 | CE6800/CE8800 |
| Border Leaf | 外部路由接入 | CE12800 |

## 基础配置步骤

### 1. 配置 NVE 接口

```shell
# 华为 CE 交换机 NVE 接口配置
interface Nve1
 source 10.1.1.1
 vni 10010 head-end peer-list protocol bgp
```

### 2. 配置 EVPN 实例

```shell
evpn vpn-instance evpn1 bd-mode
 route-distinguisher 10.1.1.1:10010
 vpn-target 10010:10010 export-extcommunity
 vpn-target 10010:10010 import-extcommunity
```

### 3. 配置 BD（Bridge Domain）

```shell
bridge-domain 10010
 vxlan vni 10010
 evpn binding vpn-instance evpn1
```

## 验证命令

```shell
display vxlan tunnel all
display evpn vpn-instance all
display bgp evpn all
display mac-address
```
<!-- 更新于 2026-05-30 -->