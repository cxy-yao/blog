---
layout: default
title: 站点地图
permalink: /sitemap/
description: 博客所有文章的完整列表
---

<style>
.sitemap-header {
    text-align: center; padding: 60px 0 40px;
}
.sitemap-header h1 {
    font-size: 2.8rem; font-weight: 800; margin-bottom: 16px;
    background: var(--gradient-main); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.sitemap-header p { color: var(--text-secondary); font-size: 1.05rem; }

.sitemap-stats {
    display: flex; justify-content: center; gap: 48px;
    margin: 40px 0 60px;
}
.sitemap-stat { text-align: center; }
.sitemap-stat-num {
    display: block; font-size: 2rem; font-weight: 800;
    background: var(--gradient-main); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.sitemap-stat-label { font-size: 0.9rem; color: var(--text-muted); margin-top: 4px; }

.sitemap-tree { max-width: 800px; margin: 0 auto; }

/* 分类节点 */
.tree-category { margin-bottom: 48px; position: relative; }
.tree-category-header {
    display: flex; align-items: center; gap: 14px;
    padding: 20px 28px; margin-bottom: 20px;
    background: var(--bg-card); border: 1px solid var(--glass-border);
    border-radius: var(--radius); cursor: pointer;
    transition: var(--transition-fast); position: relative;
}
.tree-category-header:hover {
    border-color: rgba(59,130,246,0.2); background: var(--bg-card-hover);
    transform: translateX(4px);
}
.tree-category-icon {
    width: 44px; height: 44px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem; flex-shrink: 0;
}
.tree-category-info { flex: 1; }
.tree-category-name {
    font-size: 1.1rem; font-weight: 700; color: var(--text-primary);
}
.tree-category-count {
    font-size: 0.82rem; color: var(--text-muted); margin-top: 2px;
}
.tree-category-toggle {
    color: var(--text-muted); font-size: 0.9rem;
    transition: transform 0.3s ease;
}
.tree-category-header.collapsed .tree-category-toggle {
    transform: rotate(-90deg);
}

/* 文章条目 */
.tree-posts { list-style: none; padding: 0; margin: 0 0 0 20px; border-left: 2px solid var(--glass-border); }
.tree-post {
    position: relative; padding: 14px 0 14px 36px;
    border-bottom: 1px solid rgba(255,255,255,0.03);
}
.tree-post::before {
    content: ''; position: absolute; left: -7px; top: 22px;
    width: 12px; height: 12px; border-radius: 50%;
    background: var(--accent-blue); border: 2px solid var(--bg-primary);
    box-shadow: 0 0 0 2px var(--accent-blue);
}
.tree-post:last-child { border-bottom: none; }
.tree-post-link {
    text-decoration: none; display: block;
    transition: var(--transition-fast);
}
.tree-post-link:hover { transform: translateX(6px); }
.tree-post-title {
    font-size: 0.98rem; font-weight: 600; color: var(--text-primary);
    margin-bottom: 4px;
}
.tree-post-link:hover .tree-post-title { color: var(--accent-blue); }
.tree-post-meta {
    display: flex; gap: 16px; font-size: 0.8rem; color: var(--text-muted);
}
.tree-post-meta i { margin-right: 4px; }
.tree-post-tags {
    display: flex; gap: 6px; margin-top: 6px; flex-wrap: wrap;
}
.tree-post-tag {
    font-size: 0.7rem; padding: 2px 10px; border-radius: 12px;
    background: rgba(6,182,212,0.08); color: var(--accent-cyan);
    border: 1px solid rgba(6,182,212,0.12);
}

@media (max-width: 768px) {
    .sitemap-stats { gap: 24px; flex-wrap: wrap; }
    .tree-posts { margin-left: 12px; }
    .tree-post { padding-left: 28px; }
}
</style>

<div class="sitemap-header">
    <h1>🗺️ 站点地图</h1>
    <p>博客所有文章按分类组织的完整列表</p>
</div>

<div class="sitemap-stats">
    <div class="sitemap-stat">
        <span class="sitemap-stat-num">{{ site.posts.size }}</span>
        <span class="sitemap-stat-label">篇文章</span>
    </div>
    <div class="sitemap-stat">
        <span class="sitemap-stat-num">{{ site.categories.size }}</span>
        <span class="sitemap-stat-label">个分类</span>
    </div>
    <div class="sitemap-stat">
        <span class="sitemap-stat-num">{{ site.tags.size }}</span>
        <span class="sitemap-stat-label">个标签</span>
    </div>
    <div class="sitemap-stat">
        <span class="sitemap-stat-num">{{ site.posts | map: 'content' | join: ' ' | number_of_words | divided_by: 1000 | round: 1 }}k+</span>
        <span class="sitemap-stat-label">总字数</span>
    </div>
</div>

<div class="sitemap-tree" id="sitemapTree">
{% assign sorted_categories = site.categories | sort %}
{% for category in sorted_categories %}
{% assign cat_name = category[0] %}
{% assign cat_posts = category[1] | sort: 'date' | reverse %}
{% assign cat_colors = 'accent-blue,accent-purple,accent-emerald,accent-cyan,accent-amber' | split: ',' %}
{% assign cat_idx = forloop.index0 | modulo: 5 %}
<div class="tree-category">
    <div class="tree-category-header" onclick="toggleCategory(this)">
        <div class="tree-category-icon" style="background: rgba(59,130,246,0.12);">
            {% if cat_name == '网络工程' %}<i class="fas fa-network-wired" style="color: var(--accent-blue)"></i>
            {% elsif cat_name == '数据中心' %}<i class="fas fa-server" style="color: var(--accent-purple)"></i>
            {% elsif cat_name == 'Linux' %}<i class="fab fa-linux" style="color: var(--accent-emerald)"></i>
            {% elsif cat_name == '路由交换' %}<i class="fas fa-route" style="color: var(--accent-cyan)"></i>
            {% else %}<i class="fas fa-file-alt" style="color: var(--accent-amber)"></i>{% endif %}
        </div>
        <div class="tree-category-info">
            <div class="tree-category-name">{{ cat_name }}</div>
            <div class="tree-category-count">{{ cat_posts.size }} 篇文章</div>
        </div>
        <span class="tree-category-toggle">▼</span>
    </div>
    <ul class="tree-posts">
    {% for post in cat_posts %}
        <li class="tree-post">
            <a href="{{ site.baseurl }}{{ post.url }}" class="tree-post-link">
                <div class="tree-post-title">{{ post.title }}</div>
                <div class="tree-post-meta">
                    <span><i class="far fa-calendar-alt"></i> {{ post.date | date: "%Y-%m-%d" }}</span>
                    {% assign word_count = post.content | number_of_words %}
                    <span><i class="far fa-file-alt"></i> ~{{ word_count }} 字</span>
                </div>
                {% if post.tags.size > 0 %}
                <div class="tree-post-tags">
                    {% for tag in post.tags limit:3 %}
                    <span class="tree-post-tag">#{{ tag }}</span>
                    {% endfor %}
                </div>
                {% endif %}
            </a>
        </li>
    {% endfor %}
    </ul>
</div>
{% endfor %}
</div>

<script>
function toggleCategory(header) {
    header.classList.toggle('collapsed');
    var posts = header.nextElementSibling;
    if (posts) {
        posts.style.display = posts.style.display === 'none' ? '' : 'none';
    }
}
// 默认折叠所有分类（留展开第一项）
document.addEventListener('DOMContentLoaded', function() {
    var headers = document.querySelectorAll('.tree-category-header');
    headers.forEach(function(h, i) {
        if (i > 0) {
            h.classList.add('collapsed');
            var list = h.nextElementSibling;
            if (list) list.style.display = 'none';
        }
    });
});
</script>