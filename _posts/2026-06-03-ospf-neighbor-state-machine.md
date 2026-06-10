---
layout: post
title: "OSPF 邻居状态机全解析"
date: 2026-06-03 20:00:00 +0800
categories: [网络工程, 路由交换]
tags: [OSPF, IGP, 路由协议, 排错]
---

## OSPF 邻居状态机

OSPF（Open Shortest Path First）是目前园区网和数据中心使用最广泛的 IGP 协议之一。理解 OSPF 的邻居状态机是排错的基础。

## 八种邻居状态

```
 Down
   │
   ▼
  Init ◄────── Hello 收到
   │
   ▼
  2-Way ←─── 双向通信建立
   │
   ├─── DR/BDR 选举（广播网络）
   │
   ▼
  ExStart ─── DD 报文协商主从关系
   │
   ▼
  Exchange ── 交换 LSA 头部信息
   │
   ▼
  Loading ─── 请求完整 LSA
   │
   ▼
   Full ───── 邻接关系完全建立 ✅
```

### 1. Down
初始状态，接口上没有任何 OSPF 活动。

### 2. Init
接口收到 Hello 报文，但自己的 Router-ID 不在对方的 Hello 报文中。

### 3. 2-Way
双方都看到了对方的 Router-ID——**双向通信建立**。
- 广播网络中选举 DR/BDR
- P2P 网络直接进入 ExStart

### 4. ExStart
主从协商阶段，通过 DD 报文确定 Master/Slave。

### 5. Exchange
互相交换 DD 报文（LSA 摘要信息），比较 LSDB。

### 6. Loading
发现缺少的 LSA，发送 LSR 请求完整信息。

### 7. Full ✅
LSDB 完全同步，邻接关系建立成功。

## 常见故障排错

### 邻居卡在 Init
```
R1# show ip ospf neighbor
Neighbor ID    Pri   State       Dead Time   Address
2.2.2.2         1   INIT/      -          10.0.0.2
```
**可能原因**：单方向收到 Hello，对端未收到自己的 Hello。
**排查**：
- 接口 IP 是否在同一网段
- ACL 是否过滤了 OSPF（224.0.0.5/6）
- MTU 不一致

### 邻居卡在 2-Way
```
R1# show ip ospf neighbor
Neighbor ID    Pri   State       Dead Time   Address
2.2.2.2         1   2WAY/      -          10.0.0.2
```
**原因**：广播网络中双方都认为对方不是 DR。
**解决**：配置 `ip ospf priority` 确保 DR 选举。

### 邻居卡在 ExStart/Exchange
**可能原因**：
- MTU 不匹配（最常见！）
- DD 报文被丢弃或损坏

## 排错常用命令

```bash
# 查看邻居状态
display ospf peer        # 华为
show ip ospf neighbor    # 思科

# 查看接口 OSPF 参数
display ospf interface   # 华为
show ip ospf interface   # 思科

# 查看 LSDB
display ospf lsdb        # 华为
show ip ospf database    # 思科

# 调试 OSPF 报文
debug ip ospf packet     # 思科
```

## 总结

OSPF 邻居状态机是排错的指南针——看到状态就知道问题出在哪一阶段。建议在实验环境中亲手验证每种状态的变化过程。