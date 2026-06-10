---
layout: post
title: "VXLAN EVPN 入门：为什么数据中心需要它"
date: 2026-06-05 20:00:00 +0800
categories: [网络工程, 数据中心]
tags: [VXLAN, EVPN, 数据中心, Overlay]
---

## 为什么传统网络满足不了数据中心？

传统 VLAN 技术在大规模数据中心面临三大瓶颈：

| 问题 | 原因 | 后果 |
|------|------|------|
| **二层规模限制** | VLAN ID 只有 12 位（4096 个） | 租户隔离上限 |
| **STP 瓶颈** | 生成树阻塞链路，利用率低 | 带宽浪费 50%+ |
| **跨子网迁移难** | VM/容器迁移需改 IP | 运维复杂度高 |

VXLAN + EVPN 正是为了解决这些问题而生。

## VXLAN 基本原理

VXLAN（Virtual Extensible LAN）将二层帧封装在 UDP 报文中传输：

```
┌─────────────────────────────────────────┐
│          外层 IP 头部                      │
├─────────────────────────────────────────┤
│          外层 UDP 头部（目标端口 4789）      │
├─────────────────────────────────────────┤
│          VXLAN 头部（24 位 VNI）           │
├─────────────────────────────────────────┤
│          原始二层帧（MAC + Payload）        │
└─────────────────────────────────────────┘
```

### 关键概念

- **VTEP**（VXLAN Tunnel Endpoint）— 隧道端点，负责封装/解封装
- **VNI**（VXLAN Network Identifier）— 24 位标识符，支持 1600 万+ 租户
- **NVE**（Network Virtualization Edge）— VTEP 的华为术语

## EVPN 控制面

VXLAN 早期使用 Flood-and-Learn 方式，数据面学习 MAC 地址，效率低且依赖组播。

**EVPN（Ethernet VPN，RFC 7432）** 引入 BGP 作为控制面：

```
                    ┌──────────┐
                    │  RR/RR   │
                    └────┬─────┘
                   ╱     │     ╲
             BGP EVPN  BGP EVPN  BGP EVPN
              ╱         │         ╲
         ┌──────┐   ┌──────┐   ┌──────┐
         │VTEP1 │   │VTEP2 │   │VTEP3 │
         └──────┘   └──────┘   └──────┘
```

### EVPN 的五种路由类型（RT-1 ~ RT-5）

| 路由类型 | 作用 |
|---------|------|
| RT-1：Ethernet Auto-Discovery | ESI 多归属 |
| RT-2：MAC/IP Advertisement | MAC/IP 地址通告 |
| RT-3：Inclusive Multicast | BUM 组播成员 |
| RT-4：Ethernet Segment | ES 发现与 DF 选举 |
| RT-5：IP Prefix | 跨子网路由 |

## 分布式网关

VXLAN EVPN 的核心架构——**分布式 anycast 网关**：

```
                        ┌──────┐
                        │Spine │
                        └──┬───┘
                   ┌───────┴────────┐
                   │                │
                ┌──┴──┐          ┌──┴──┐
                │Leaf1│          │Leaf2│
                │GW:  │          │GW:  │
                │.254 │          │.254 │
                └──┬──┘          └──┬──┘
                   │                │
                ┌──┴──┐          ┌──┴──┐
                │VM-A │          │VM-B │
                │.100 │          │.200 │
                └─────┘          └─────┘
```

- 每台 Leaf 充当网关（相同 IP .254）
- VM 迁移后网关不变，实现零中断

## 总结

VXLAN EVPN 是现代数据中心网络的基石，也是 HCIE-DC 认证的核心内容。掌握 Overlay 协议栈将帮助你理解从传统网络到云原生网络的演进路径。
