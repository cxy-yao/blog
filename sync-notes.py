#!/usr/bin/env python3
"""
Obsidian DC 笔记同步到 Jekyll 博客
用法: python3 sync-notes.py
"""

import os
import re
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

# 配置
VAULT_DIR = Path(__file__).parent
POSTS_DIR = VAULT_DIR / "_posts"
ASSETS_DIR = VAULT_DIR / "assets"
EXCLUDE_DIRS = ["辅助文件"]  # 排除的目录

def run_cmd(cmd, cwd=None):
    """运行 shell 命令"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd or VAULT_DIR)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def get_dc_files():
    """从 obsidian-dc 分支获取 DC 文件列表"""
    # 使用 -z 选项来正确处理 Unicode 文件名
    result = subprocess.run(
        ['git', 'ls-tree', '-r', '-z', '--name-only', 'origin/obsidian-dc', '--', 'DC/'],
        capture_output=True, text=True, cwd=VAULT_DIR
    )
    
    files = []
    for line in result.stdout.split('\0'):
        line = line.strip()
        if line and line.endswith('.md'):
            # 跳过排除的目录
            if not any(exclude in line for exclude in EXCLUDE_DIRS):
                files.append(line)
    
    return files

def get_file_content(file_path):
    """从 obsidian-dc 分支获取文件内容"""
    result = subprocess.run(
        ['git', 'show', f'origin/obsidian-dc:{file_path}'],
        capture_output=True, text=True, cwd=VAULT_DIR
    )
    if result.returncode != 0:
        return None
    return result.stdout

def extract_frontmatter(content):
    """提取 frontmatter 和正文"""
    if not content.startswith("---"):
        return {}, content
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    
    frontmatter_text = parts[1].strip()
    body = parts[2].strip()
    
    # 简单解析 frontmatter
    frontmatter = {}
    for line in frontmatter_text.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            frontmatter[key] = value
    
    return frontmatter, body

def convert_obsidian_syntax(body):
    """转换 Obsidian 语法为 Jekyll 语法"""
    # ![[辅助文件/xxx.svg|width]] -> ![xxx](/assets/xxx.svg)
    body = re.sub(
        r'!\[\[辅助文件/([^]|]+)\.svg\|?\d*\]\]',
        r'![\1](/assets/\1.svg)',
        body
    )
    
    # 删除 excalidraw 嵌入
    body = re.sub(r'!\[\[.*\.excalidraw.*\]\]', '', body)
    
    # [[wikilink]] -> [wikilink](wikilink)
    body = re.sub(r'\[\[([^\]]+)\]\]', r'[\1](\1)', body)
    
    return body

def generate_slug(title):
    """生成 URL 友好的 slug"""
    # 保留中文和英文数字，其他替换为 -
    slug = re.sub(r'[^\w\u4e00-\u9fff]', '-', title)
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug[:50] if slug else 'post'

def sync_svg_files():
    """同步 SVG 文件到 assets 目录"""
    result = subprocess.run(
        ['git', 'ls-tree', '-r', '-z', '--name-only', 'origin/obsidian-dc', '--', 'DC/'],
        capture_output=True, text=True, cwd=VAULT_DIR
    )
    
    synced = 0
    for line in result.stdout.split('\0'):
        line = line.strip()
        if line and line.endswith('.svg') and not any(exclude in line for exclude in EXCLUDE_DIRS):
            # 从分支获取 SVG 文件
            svg_content = subprocess.run(
                ['git', 'show', f'origin/obsidian-dc:{line}'],
                capture_output=True, cwd=VAULT_DIR
            )
            if svg_content.returncode == 0:
                svg_name = Path(line).name
                svg_path = ASSETS_DIR / svg_name
                with open(svg_path, 'wb') as f:
                    f.write(svg_content.stdout)
                synced += 1
    
    return synced

def sync_notes():
    """同步笔记"""
    print("🚀 开始同步笔记...")
    print(f"📁 工作目录: {VAULT_DIR}")
    
    # 确保目录存在
    POSTS_DIR.mkdir(exist_ok=True)
    ASSETS_DIR.mkdir(exist_ok=True)
    
    # 获取 DC 文件列表
    dc_files = get_dc_files()
    print(f"📋 找到 {len(dc_files)} 个笔记文件")
    
    if not dc_files:
        print("⚠️  没有找到笔记文件")
        return
    
    synced_posts = []
    
    for file_path in dc_files:
        print(f"\n📝 处理: {file_path}")
        
        # 从分支获取文件内容
        content = get_file_content(file_path)
        if not content:
            print(f"  ❌ 无法读取文件")
            continue
        
        frontmatter, body = extract_frontmatter(content)
        
        # 转换语法
        body = convert_obsidian_syntax(body)
        
        # 获取标题
        title = frontmatter.get('title', '')
        if not title or '<%' in title:  # 处理 Templater 语法
            title = Path(file_path).stem
        
        # 获取日期
        date_str = frontmatter.get('date', '')
        if not date_str:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        # 生成 slug
        slug = generate_slug(title)
        post_filename = f"{date_str}-{slug}.md"
        post_path = POSTS_DIR / post_filename
        
        # 生成 Jekyll frontmatter
        categories = frontmatter.get('categories', '[]')
        tags = frontmatter.get('tags', '[]')
        excerpt = frontmatter.get('excerpt', '')
        
        # 写入 _posts 文件
        with open(post_path, 'w', encoding='utf-8') as f:
            f.write("---\n")
            f.write(f"layout: post\n")
            f.write(f'title: "{title}"\n')
            f.write(f"date: {date_str}\n")
            f.write(f"categories: {categories}\n")
            f.write(f"tags: {tags}\n")
            if excerpt:
                f.write(f'excerpt: "{excerpt}"\n')
            f.write(f"dc-sync: true\n")
            f.write(f'dc-source: "{file_path}"\n')
            f.write("---\n\n")
            f.write(body)
        
        synced_posts.append(post_path)
        print(f"  ✅ -> {post_filename}")
    
    # 同步 SVG 文件
    print("\n📎 同步 SVG 文件...")
    svg_count = sync_svg_files()
    print(f"  同步了 {svg_count} 个 SVG 文件")
    
    # 提交并推送
    print("\n📦 提交更改...")
    run_cmd("git add _posts/ assets/")
    stdout, stderr, rc = run_cmd('git commit -m "sync: 手动同步笔记 {}"'.format(
        datetime.now().strftime('%Y-%m-%d %H:%M')
    ))
    
    if "nothing to commit" in stderr or "nothing to commit" in stdout:
        print("ℹ️  没有新的更改需要提交")
    else:
        print("🚀 推送到 main...")
        stdout, stderr, rc = run_cmd("git push origin main")
        if rc == 0:
            print("✅ 同步完成！")
        else:
            print(f"❌ 推送失败: {stderr}")
    
    print(f"\n📊 同步了 {len(synced_posts)} 篇笔记")

if __name__ == "__main__":
    sync_notes()
