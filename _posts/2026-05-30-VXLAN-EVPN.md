---
dc-sync: true
dc-source: DC/VXLAN-EVPN分布式网关基础配置.md
layout: post
title: "VXLAN EVPN 分布式网关基础配置"
date: 2026-05-30
categories: [数据中心]
tags: [VXLAN, EVPN, 华为CE, 分布式网关]
excerpt: "VXLAN EVPN分布式网关是数据中心Fabric的核心组件，本文记录华为CE交换机上的基础配置流程。"
---

## 背景

在 Spine-Leaf 架构中，VXLAN EVPN 分布式网关实现了跨 Leaf 节点的三层互通。

## 核心组件

| 组件 | 作用 | 典型设备 |
|------|------|----------|
| Spine | 路由反射器 | CE12800 |
| Leaf | VTEP，分布式网关 | CE6800/CE8800 |
