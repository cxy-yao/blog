---
layout: default
title: 分类
permalink: /categories/
---

<section class="categories-page">
    <h1 class="section-title"><i class="fas fa-folder-open"></i> 文章分类</h1>
    <div class="categories-grid">
        {% assign sorted_categories = site.categories | sort %}
        {% for category in sorted_categories %}
        <div class="category-card" id="{{ category[0] }}">
            <h2 class="category-name">
                <i class="fas fa-folder"></i> {{ category[0] }}
                <span class="category-count">{{ category[1].size }} 篇</span>
            </h2>
            <ul class="category-posts">
                {% for post in category[1] %}
                <li>
                    <time>{{ post.date | date: "%Y-%m-%d" }}</time>
                    <a href="{{ post.url }}">{{ post.title }}</a>
                </li>
                {% endfor %}
            </ul>
        </div>
        {% endfor %}
    </div>
</section>

<style>
.categories-page { max-width: 900px; margin: 0 auto; }
.categories-grid { display: flex; flex-direction: column; gap: 24px; }
.category-card { background: var(--bg-card); border-radius: var(--radius-lg); padding: 28px; border: 1px solid var(--border); backdrop-filter: blur(12px); transition: var(--transition); }
.category-card:hover { border-color: var(--primary-dark); box-shadow: 0 8px 24px rgba(0,0,0,0.2); }
.category-name { font-size: 1.3rem; font-weight: 700; margin-bottom: 16px; display: flex; align-items: center; gap: 10px; }
.category-name i { color: var(--accent); }
.category-count { font-size: 0.8rem; color: var(--text-muted); background: rgba(99,102,241,0.15); padding: 3px 10px; border-radius: 12px; margin-left: auto; }
.category-posts { list-style: none; padding: 0; }
.category-posts li { display: flex; align-items: center; gap: 16px; padding: 10px 0; border-bottom: 1px solid rgba(51,65,85,0.3); }
.category-posts li:last-child { border-bottom: none; }
.category-posts time { color: var(--text-muted); font-size: 0.85rem; font-family: 'JetBrains Mono', monospace; min-width: 100px; }
.category-posts a { color: var(--text-secondary); font-weight: 500; transition: var(--transition); }
.category-posts a:hover { color: var(--primary-light); }
@media (max-width: 768px) { .category-posts li { flex-direction: column; align-items: flex-start; gap: 4px; } }
</style>
