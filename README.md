# ChenChuLin 的技术博客

> 网络工程师的技术笔记 — 数据中心、AI算力网络、路由交换、Linux运维

## 🚀 在线访问

**https://cxy-yao.github.io/blog/**

## 📁 项目结构

```
├── _config.yml          # Jekyll 配置
├── _layouts/            # HTML 模板
│   ├── default.html     # 基础布局
│   └── home.html        # 首页布局
├── _posts/              # 文章目录 (Markdown)
├── assets/              # 静态资源
├── about.md             # 关于页面
├── categories.md        # 分类页面
├── tags.md              # 标签页面
└── build_preview.py     # 本地预览脚本
```

## ✍️ 添加文章

在 `_posts/` 目录创建 Markdown 文件，格式：`YYYY-MM-DD-slug.md`

```markdown
---
layout: post
title: "文章标题"
date: 2026-05-29
categories: [网络工程]
tags: [BGP, OSPF, VXLAN]
---

正文内容...
```

## 🛠️ 本地开发

```bash
# 克隆仓库
git clone https://github.com/cxy-yao/blog.git
cd blog

# 启动本地预览 (端口 8791)
python3 build_preview.py
```

## 🎨 设计特点

- 🌙 深色主题 (`#0a0e1a`)
- ✨ Canvas 粒子动画
- 🪟 毛玻璃效果导航栏
- 📱 响应式布局
- 🔤 Pacifico 字体 Logo

## 📄 License

MIT © ChenChuLin