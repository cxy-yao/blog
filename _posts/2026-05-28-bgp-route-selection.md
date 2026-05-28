---
layout: post
title: "BGP路由选择算法13步详解与实战调优"
date: 2026-05-28
categories: 网络工程
tags: [BGP, 路由协议, DC网络, 华为]
---

BGP选路不是只看MED，13步算法每一步都可能影响流量走向。本文逐条拆解，配合实际配置说明如何精确控制路径。

<!--more-->

## BGP选路概述

当BGP收到多条去往同一目的前缀的路由时，按以下13步顺序逐条比较，**一旦某步能分出胜负，立即选择，不再继续**：

## 第1步：Weight（权重，Cisco私有）

```bash
# Cisco设备专用，华为不支持
# 本地始发路由Weight=32768，学习到的为0
# 值越大越优先
```

> **注意**：华为CE交换机没有Weight属性，这一步直接跳过。

## 第2步：Local Preference（本地优先级）

```bash
# 默认值100，越大越优先
# 在IBGP邻居间传递，不出AS

# 华为配置：设置LP为200（优先走这条)
route-policy LP-SET permit node 10
 apply local-preference 200

# 应用到IBGP邻居入方向
bgp 12100
 peer 10.1.10.1 route-policy LP-SET import
```

**实战场景**：多出口数据中心，通过LP控制出站流量走主链路。

## 第3步：本地始发优先

优先级顺序：
1. `network` 命令发布的路由
2. `aggregate-address` 聚合路由
3. `import` 引入的路由

本地始发的路由始终优于从邻居学到的。

## 第4步：AS Path长度

```bash
# AS路径越短越优先
# 可以用prepend人为加长路径

# 让这条路径不被优先选择（prepend 3次)
route-policy AS-PREPEND permit node 10
 apply as-path 65001 65001 65001 additive

bgp 12100
 peer 203.0.113.1 route-policy AS-PREPEND export
```

**实战场景**：双ISP接入，用AS-PREPEND引导流量走主ISP。

## 第5步：Origin类型

优先级：`IGP(i)` > `EGP(e)` > `Incomplete(?)`

```bash
# network命令产生 i
# redistribute引入产生 ?
# 一般不需要手动调整
route-policy ORIGIN-SET permit node 10
 apply origin igp
```

## 第6步：MED（多出口鉴别器）

```bash
# 值越小越优先
# 默认从邻居AS学到的MED才比较
# 跨AS默认不比较MED（可配置强制比较)

# 设置MED
route-policy MED-SET permit node 10
 apply cost 100

# 强制比较所有邻居的MED（华为)
bgp 12100
 compare-med always
```

> **注意**：`compare-med always` 可能导致路由黑洞，慎用。建议只在同一邻居AS的路由间比较。

## 第7步：EBGP优于IBGP

EBGP路由 > IBGP路由 > Local路由

这条很直觉：外部学到的路由优先于内部学到的。

## 第8步：到下一跳的IGP度量值

```bash
# 到NEXT_HOP的IGP cost越小越优先
# 这就是为什么OSPF cost能影响BGP选路

# 查看到下一跳的cost
display ip routing-table 10.1.10.1
```

**实战场景**：Spine-Leaf架构中，调整OSPF cost让BGP选择最优Spine。

## 第9-13步：高级属性

```bash
# 第9步：Cluster List长度（RR环境)
# 越短越优先

# 第10步：Originator ID
# 比较Router ID

# 第11步：IP地址比较
# 选择来自较小IP地址的邻居

# 第12步：ECMP等价多路径
# 以上都相同时负载均衡
bgp 12100
 maximum load-balancing 4

# 第13步：最大前缀限制下的选择
```

## 实战调优案例：AI算力网络Spine-Leaf

```bash
# 场景：12台Leaf，2台Spine
# 需求：Leaf1通过Spine1访问Leaf2，Spine2作为备份

# Spine1的Leaf侧配置（低LP=备份)
route-policy BACKUP-LP permit node 10
 apply local-preference 80

# Spine2的Leaf侧配置（默认LP=100=主路径)
# 不需要额外配置，默认值即为主路径
```

## 选路排障命令

```bash
# 查看BGP路由详情（含所有属性)
display bgp routing-table 10.110.1.0/24

# 查看为什么选了这条路由
display bgp routing-table 10.110.1.0/24 verbose

# 对比两条路由的属性
display bgp routing-table 10.110.1.0/24 longer-match

# 查看被抑制的路由
display bgp routing-table suppressed
```

---

> **总结**：BGP选路是一条决策链，前6步（Weight → LP → 本地始发 → AS Path → Origin → MED）是日常调优最常用的。理解每一步的权重，就能精确控制数据中心的流量走向。
