---
layout: post
title: "BGP 基础：从 AS 到路由选路"
date: 2026-06-01 20:00:00 +0800
categories: [网络工程, 路由交换]
tags: [BGP, 路由协议, 网络基础]
---

## 什么是 BGP？

BGP（Border Gateway Protocol，边界网关协议）是互联网的核心路由协议，用于在不同自治系统（AS）之间交换路由信息。它属于**路径矢量协议**，与 OSPF、IS-IS 等 IGP 协议有本质区别。

### BGP 的特点

- **基于 TCP（端口 179）** — 可靠的传输层保证
- **路径矢量协议** — 通过 AS_PATH 属性记录路径信息
- **丰富的路径属性** — MED、Local Preference、Community 等
- **策略驱动** — 不是找最短路径，而是按策略选路

## BGP 基本概念

### 自治系统（AS）

AS 是拥有统一路由策略的网络集合，每个 AS 有唯一的 ASN（AS Number）：
- **公有 ASN**（1-64511）— 互联网上使用
- **私有 ASN**（64512-65535）— 内部使用

### EBGP 与 IBGP

```
    AS 100                  AS 200
  ┌──────┐                ┌──────┐
  │ R1 ←─┼─── EBGP ──────┼──→ R3 │
  │  ↓   │                │  ↑   │
  │ R2   │                │ R4   │
  └──────┘                └──────┘
     IBGP                    IBGP
```

- **EBGP**：不同 AS 之间的 BGP 会话
- **IBGP**：同一 AS 内部的 BGP 会话

## BGP 路径选择（13 步决策）

BGP 选路是网络工程师必须掌握的核心技能，以下是简化的决策流程：

1. **最高 Weight**（Cisco 专有）
2. **最高 Local Preference** — 出站流量控制
3. **本地起源**（network/aggregate > redistributed）
4. **最短 AS_PATH**
5. **最低 Origin 类型**（IGP < EGP < Incomplete）
6. **最低 MED** — 入站流量控制
7. **EBGP 优先于 IBGP**
8. **最近 IGP 下一跳**
9. **最老 EBGP 路由**
10. **最低 Router-ID**
11. **最短 Cluster-List**
12. **最低 Neighbor Address**

## 基础配置示例

```
router bgp 65001
 bgp router-id 1.1.1.1
 neighbor 10.0.0.2 remote-as 65002
 neighbor 10.0.0.2 description EBGP-to-AS65002
 !
 address-family ipv4
  neighbor 10.0.0.2 activate
  network 192.168.1.0 mask 255.255.255.0
 exit-address-family
```

## 总结

BGP 是互联网的基石，掌握 BGP 对于网络工程师来说是必备技能。下篇文章将深入 BGP 的路径属性操控与流量工程。
