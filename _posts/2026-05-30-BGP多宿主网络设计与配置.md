---
layout: post
title: BGP 多宿主网络设计与配置
date: 2026-05-30
categories:
  - 路由交换
tags:
  - BGP
  - eBGP
  - iBGP
  - 路由协议
excerpt: BGP多宿主网络设计，通过多个ISP连接提高网络可用性和负载均衡。
---

## 概述

BGP（Border Gateway Protocol）是互联网的核心路由协议，用于在不同自治系统（AS）之间交换路由信息。多宿主（Multihoming）设计通过连接多个ISP来提高网络可靠性。

## 拓扑图

![[辅助文件/BGP多宿主拓扑图.excalidraw|800]]

## 设计要素

### 1. 自治系统规划

| AS编号 | 网络类型 | 用途 |
|--------|----------|------|
| 65001 | 企业网络 | 内部办公网络 |
| 65002 | ISP网络 | 主要互联网连接 |
| 65003 | 数据中心 | 服务器托管 |
| 64512 | 互联网 | 公共网络 |

### 2. BGP 会话类型

- **eBGP**：不同AS之间的BGP会话（External BGP）
- **iBGP**：同一AS内部的BGP会话（Internal BGP）

### 3. 路由策略

```shell
# 华为 CE 交换机 BGP 配置示例
bgp 65001
 router-id 10.1.1.1
 peer 10.2.2.2 as-number 65002
 peer 172.16.0.1 as-number 65003
 
 address-family ipv4 unicast
  network 192.168.10.0 255.255.255.0
  peer 10.2.2.2 enable
  peer 172.16.0.1 enable
```

## 多宿主优势

1. **高可用性**：一个ISP故障时，流量可切换到另一个ISP
2. **负载均衡**：在多个ISP之间分配流量
3. **路径优化**：选择最优路径降低延迟
4. **带宽聚合**：增加总带宽容量

## 注意事项

- 正确配置 BGP 认证（MD5）
- 使用 Route-Map 控制路由通告
- 配置 BFD 快速检测故障
- 监控 BGP 邻居状态和路由表变化

## 验证命令

```shell
display bgp peer
display bgp routing-table
display bgp paths
```
<!-- 更新于 2026-05-30 -->
