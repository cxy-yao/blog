---
layout: post
title: "AI算力网络架构设计：Spine-Leaf组网要点"
date: 2026-05-28
categories: 数据中心
tags: [AI算力, Spine-Leaf, 网络架构, RoCEv2]
---

AI训练集群对网络的要求与传统数据中心截然不同——低延迟、零丢包、大带宽是硬指标。本文总结AI算力网络Spine-Leaf架构的设计要点。

<!--more-->

## AI训练网络的特殊需求

| 指标 | 传统DC | AI训练集群 |
|------|--------|-----------|
| 东西向带宽 | 10-25Gbps/服务器 | 100-400Gbps/GPU节点 |
| 延迟要求 | <1ms | <10μs（RDMA) |
| 丢包容忍 | 少量可接受 | 零丢包（RoCEv2) |
| 流量模型 | 随机多对多 | All-Reduce同步流量 |

## 网络架构设计

### 三层角色划分

```
┌──────────────────────────────────────────┐
│              Spine Layer                  │
│  AS 12100, LoopBack 10.1.10.1-2         │
│  400GE上行，无状态转发                    │
├────────────┬────────────┬────────────────┤
│   Leaf-1   │   Leaf-2   │    Leaf-12     │
│  AS 12101  │  AS 12102  │   AS 12112    │
│  25/100GE  │  25/100GE  │   25/100GE    │
│  接入GPU节点│  接入存储  │   接入管理    │
└────────────┴────────────┴────────────────┘
```

### 三种网络平面

| 平面 | 网段 | VLAN | 用途 |
|------|------|------|------|
| 参数面（昇腾) | 10.110.x.0/24 | 1001-1099 | GPU通信（HCCP/RoCEv2) |
| 参数面（NVIDIA) | 10.120.x.0/24 | 1101-1199 | NCCL/RDMA通信 |
| 样本面 | 10.130.x.0/24 | 1201-1299 | 数据加载 |
| 业务面 | 81.192.0.0/24 | 2001+ | 推理服务、API |
| 带外管理 | 172.16.0.0/24 | 100 | IPMI/BMC |

## Spine-Leaf互联设计

```bash
# Spine-Leaf点对点互联网段：10.110.101.0/24
# 每条链路一个/30子网

# Spine1 <-> Leaf1: 10.110.101.0/30
# Spine1 <-> Leaf2: 10.110.101.4/30
# Spine2 <-> Leaf1: 10.110.101.8/30
# Spine2 <-> Leaf2: 10.110.101.12/30
```

## RoCEv2无损网络配置

### PFC（优先级流控)

```bash
# 启用PFC，优先级4用于RDMA traffic
dcb pfc enable
dcb pfc priority 4

# 接口应用
interface 100GE1/0/1
 dcb pfc enable
 dcb pfc priority 4
```

### ECN（显式拥塞通知)

```bash
# 配置ECN标记阈值
qos wred ECN-WRED
 color green low-limit 80 high-limit 120 discard-percentage 100
 color yellow low-limit 60 high-limit 100 discard-percentage 100

# 队列调度
interface 100GE1/0/1
 qos queue 4 wred ECN-WRED
```

### DCQCN（数据中心量化拥塞通知)

```bash
# 在拥塞点交换机上配置
# 当队列深度超过阈值，标记CE位
# 发送端收到ECN后降速
```

## 防止微突发的设计

```bash
# 出方向流量整形（避免缓冲区溢出)
interface 100GE1/0/1
 qos car cir 80000 cbs 10000

# 入方向风暴抑制
interface 100GE1/0/1
 storm suppression broadcast packets 100
 storm suppression multicast packets 100
 storm suppression unicast packets 1000
```

## 网络可靠性设计

### M-LAG（跨设备链路聚合)

```bash
# 配置M-LAG双活
dfs-group 1
 priority 100
 source ip-address 10.1.10.11 peer-ip-address 10.1.10.12

interface Eth-Trunk 10
 trunkport 100GE1/0/1
 trunkport 100GE1/0/2
 mode lacp-static
 dfs-group 1
```

### BFD快速检测

```bash
# BFD for OSPF（毫秒级收敛)
ospf 1
 area 0.0.0.0
  bfd all-interfaces enable

# BFD参数调整
bfd
 min-tx-interval 100
 min-rx-interval 100
 detect-multiplier 3
```

## 监控与告警

```bash
# 接口带宽利用率监控（阈值告警)
snmp-agent trap enable feature-name IFNET
snmp-agent trap enable feature-name BASETRAP

# 流量采样（sFlow/NetStream)
sflow collector 172.16.0.100 port 6343
interface 100GE1/0/1
 sflow sampling-rate 1000
```

## 容量规划参考

| GPU节点规模 | Spine数量 | Leaf数量 | Spine-Leaf带宽 |
|------------|----------|---------|---------------|
| 64台（512卡) | 2 | 4 | 2×400GE |
| 128台（1024卡) | 4 | 8 | 4×400GE |
| 256台（2048卡) | 4 | 12 | 4×400GE |

---

> **总结**：AI算力网络设计的核心是"无损、低延迟、高带宽"。Spine-Leaf架构保证等价路径，PFC+ECN保证零丢包，M-LAG+BFD保证高可用。规划时重点关注参数面网段和VLAN划分，这是最容易出问题的地方。
