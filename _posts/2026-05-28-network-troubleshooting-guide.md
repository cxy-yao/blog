---
layout: post
title: "网络故障排查结构化方法论"
date: 2026-05-28
categories: 网络工程
tags: [故障排查, 运维方法论, 网络排障]
---

网络故障不可怕，可怕的是没有章法。本文介绍一套四步结构化排障流程，配合常见故障的根因链，帮你快速定位问题。

<!--more-->

## 四步排障法

```
收集信息 → 隔离范围 → 定位根因 → 验证修复
```

### 第一步：收集信息

```bash
# 1. 确认故障现象
#    - 哪些业务受影响？
#    - 什么时间开始的？
#    - 影响范围（单机/单网段/全网)?

# 2. 检查设备状态
display cpu-usage
display memory-usage
display interface brief | include down|err
display logbuffer | include ERROR|CRITICAL

# 3. 检查变更记录
display configuration changes
# 有没有人刚改过配置？
```

### 第二步：隔离范围

```bash
# 逐层排除，从物理层开始
# L1 物理层：接口UP/DOWN？光模块正常？
display interface 100GE1/0/1 | include line protocol
display transceiver interface 100GE1/0/1

# L2 数据链路层：MAC学习？VLAN正确？
display mac-address interface 100GE1/0/1
display vlan brief

# L3 网络层：路由可达？下一跳正确？
display ip routing-table 10.110.1.1
ping -a 10.1.10.11 10.110.1.1

# L4+ 应用层：端口可达？
tcping 10.110.1.1 22
```

### 第三步：定位根因

关键思路：**看日志、看计数器、看状态机**

```bash
# 日志是第一线索
display logbuffer | include %Jun 28
display trapbuffer

# 接口计数器暴露链路质量
display interface 100GE1/0/1 | include error|CRC|drop

# 协议状态机揭示邻居问题
display bgp peer | include Idle|Connect|Active
display ospf peer brief
```

### 第四步：验证修复

```bash
# 修复后必须验证
# 1. 协议状态恢复正常
display bgp peer  # 应该全是Established

# 2. 业务恢复正常
ping -c 100 10.110.1.1  # 连续ping确认稳定

# 3. 监控一段时间
display interface 100GE1/0/1 | include rate  # 流量是否正常
```

## 常见故障根因链

### 故障1：接口频繁UP/DOWN

```
现象：接口反复flapping
├─ 物理层原因
│  ├─ 光模块老化（检查收发光功率)
│  ├─ 光纤弯曲/断裂（检查OTDR)
│  └─ 端口硬件故障（换端口排除)
├─ 协议层原因
│  ├─ BFD误触发（调整检测间隔)
│  └─ STP TC震荡（检查是否有环路)
└─ 对端原因
   └─ 对端设备重启/掉电
```

```bash
# 排查命令
display transceiver interface 100GE1/0/1  # 光功率
display logbuffer | include LINK           # 链路事件
display stp tc-bpdu statistics             # TC报文统计
```

### 故障2：BGP邻居无法建立

```
现象：BGP邻居状态卡在Active/Connect
├─ 连接层问题
│  ├─ TCP 179端口不通（ACL过滤?)
│  ├─ LoopBack不可达（路由缺失?)
│  └─ MTU不匹配（分片导致TCP重传)
├─ 配置问题
│  ├─ AS号配错
│  ├─ Router-ID冲突
│  └─ 密码不匹配
└─ 资源问题
   └─ BGP进程内存不足
```

```bash
# 排查命令
display bgp peer 10.1.10.1 verbose  # 查看邻居详情
tcping 10.1.10.1 179                 # 测试TCP连通性
display acl 3001                     # 检查ACL是否阻断
display bgp error                    # BGP错误计数
```

### 故障3：VXLAN业务不通

```
现象：二层业务跨VXLAN不通
├─ Underlay问题
│  ├─ VTEP LoopBack不可达
│  └─ UDP 4789被ACL阻断
├─ Overlay问题
│  ├─ EVPN邻居未建立
│  ├─ VNI-BD映射错误
│  └─ NVE接口source IP错误
├─ 接入侧问题
│  ├─ VLAN-BD绑定错误
│  └─ 接口PVID不匹配
└─ 主机侧问题
   ├─ IP/掩码配错
   └─ 网关MAC不匹配
```

```bash
# 排查命令
ping -vpn-instance default 10.1.10.12  # 测试VTEP可达
display bgp evpn peer                   # EVPN邻居
display vxlan vni                       # VNI映射
display mac-address remote              # 远端MAC学习
display interface nve1                  # NVE接口状态
```

### 故障4：OSPF邻居震荡

```
现象：OSPF邻居频繁Up/Down
├─ Hello报文问题
│  ├─ Hello/Dead间隔不匹配
│  ├─ 区域ID不一致
│  ├─ 认证密码错误
│  └─ 接口MTU < 1500（DBD报文被丢弃)
├─ 网络问题
│  ├─ 链路质量差（丢包导致Hello超时)
│  └─ 带宽不足（LSA泛洪占满带宽)
└─ 资源问题
   └─ OSPF进程CPU占用过高
```

```bash
# 排查命令
display ospf peer 10.1.10.1 verbose  # 邻居详情
display ospf interface GE1/0/1        # 接口OSPF参数
display ospf error                    # OSPF错误计数
```

## 排障工具箱速查

| 场景 | 工具 | 命令 |
|------|------|------|
| 链路质量 | ping | `ping -c 100 -i 0.01 目标` |
| 路径追踪 | tracert | `tracert -a 源IP 目标IP` |
| 端口测试 | tcping | `tcping 目标 端口` |
| 抓包分析 | mirror | `observe-port interface 100GE1/0/50` |
| 配置对比 | diff | `display configuration changes` |
| 流量分析 | NetStream | `display ip netstream cache` |

## 排障文档模板

```markdown
## 故障报告

**时间**：2026-05-28 14:30
**现象**：Leaf-1下挂服务器无法访问Spine-1 LoopBack
**影响范围**：Leaf-1所有服务器
**根因**：OSPF邻居因MTU不匹配震荡，导致路由缺失
**处理过程**：
1. 14:30 发现故障，ping测试确认
2. 14:35 display ospf peer发现邻居DOWN
3. 14:40 检查接口MTU，发现对端MTU=1400
4. 14:45 修改对端MTU为1500，邻居恢复
5. 14:50 业务恢复正常
**预防措施**：入网检查清单增加MTU校验项
```

---

> **总结**：排障四步法（收集→隔离→定位→验证）适用于所有网络故障。关键原则：1) 先看日志再动手 2) 从下往上逐层排查 3) 修复后必须验证 4) 记录故障报告积累经验。
