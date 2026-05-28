---
layout: default
title: 分类
permalink: /categories/
---

<section class="categories-page">
    <h1 class="section-title reveal"><i class="fas fa-folder-open"></i> 文章分类</h1>
    <div class="categories-grid">
        {% assign sorted_categories = site.categories | sort %}
        {% for category in sorted_categories %}
        <div class="category-card reveal" style="animation-delay: {{ forloop.index | minus: 1 | times: 0.1 }}s">
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
.category-card {
    background: var(--bg-card); border-radius: var(--radius); padding: 28px;
    border: 1px solid var(--glass-border); backdrop-filter: blur(16px);
    transition: var(--transition);
}
.category-card:hover { border-color: rgba(59,130,246,0.15); box-shadow: var(--shadow-card); }
.category-name {
    font-size: 1.3rem; font-weight: 700; margin-bottom: 18px;
    display: flex; align-items: center; gap: 12px;
}
.category-name i { color: var(--accent-cyan); }
.category-count {
    font-size: 0.78rem; color: var(--text-muted); margin-left: auto;
    background: rgba(59,130,246,0.1); padding: 4px 12px; border-radius: 20px;
}
.category-posts { list-style: none; padding: 0; }
.category-posts li {
    display: flex; align-items: center; gap: 16px;
    padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.03);
    transition: var(--transition-fast);
}
.category-posts li:last-child { border-bottom: none; }
.category-posts li:hover { padding-left: 8px; }
.category-posts time {
    color: var(--text-muted); font-size: 0.82rem;
    font-family: var(--font-mono); min-width: 100px;
}
.category-posts a {
    color: var(--text-secondary); font-weight: 500;
    text-decoration: none !important; transition: var(--transition-fast);
}
.category-posts a:hover { color: var(--accent-blue); }
@media (max-width: 768px) {
    .category-posts li { flex-direction: column; align-items: flex-start; gap: 4px; }
}
</style>
