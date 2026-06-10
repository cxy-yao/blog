# ChenChuLin 的博客

🌐 **blog.chulinchen.top** — 网络工程师的技术笔记

## 📁 仓库结构

```
├── main 分支（CF Pages 部署）
│   ├── _config.yml          # Jekyll 配置
│   ├── _layouts/            # 页面模板
│   │   ├── default.html     # 基础布局
│   │   ├── home.html        # 首页
│   │   └── post.html        # 文章详情
│   ├── _posts/              # 博客文章（自动同步自 DC/）
│   ├── assets/              # 静态资源（CSS、SVG）
│   ├── about.md             # 关于页面
│   ├── categories.md        # 分类页面
│   ├── tags.md              # 标签页面
│   └── index.md             # 首页
│
└── obsidian-dc 分支（Obsidian 同步）
    ├── DC/                  # 笔记目录（写在这里）
    │   └── 辅助文件/        # Excalidraw、模板等（不同步到博客）
    └── .obsidian/           # Obsidian 配置（gitignore）
```

## ✍️ 写博客流程

1. 在 Obsidian 中打开 `DC/` 目录
2. 新建或编辑 `.md` 文件
3. 保存后，obsidian-git 插件自动 push 到 `obsidian-dc` 分支
4. GitHub Action 自动同步到 `main` 分支的 `_posts/`
5. Cloudflare Pages 自动构建部署

## 📝 文章格式

```yaml
---
layout: post
title: "文章标题"
date: 2026-01-01
categories: [分类名]
tags: [标签1, 标签2]
excerpt: "摘要文字"
---

正文内容...
```

## 🔧 技术栈

- **博客引擎**: Jekyll 4.4
- **部署**: Cloudflare Pages
- **笔记工具**: Obsidian + obsidian-git
- **图表**: Excalidraw
- **域名**: blog.chulinchen.top
