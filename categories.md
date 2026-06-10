---
layout: default
title: 分类
permalink: /categories/
---

<style>
.categories-page { max-width: 1000px; margin: 0 auto; }
.categories-header { text-align: center; margin-bottom: 56px; }
.categories-header h1 {
    font-size: 2.5rem; font-weight: 800; margin-bottom: 12px;
    background: var(--gradient-main); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.categories-header p { color: var(--text-secondary); font-size: 1.1rem; }
.categories-grid {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 24px; margin-bottom: 60px;
}
.category-card {
    background: var(--bg-card); border-radius: var(--radius); padding: 28px;
    border: 1px solid var(--glass-border); backdrop-filter: blur(16px);
    transition: var(--transition); position: relative; overflow: hidden;
}
.category-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: var(--gradient-main); opacity: 0; transition: var(--transition);
}
.category-card:hover {
    transform: translateY(-6px); border-color: rgba(59,130,246,0.2);
    box-shadow: var(--shadow-card), var(--shadow-glow);
}
.category-card:hover::before { opacity: 1; }
.category-icon {
    width: 52px; height: 52px; border-radius: 14px;
    background: var(--gradient-main); display: flex;
    align-items: center; justify-content: center; font-size: 1.4rem;
    margin-bottom: 18px;
}
.category-name {
    font-size: 1.25rem; font-weight: 700; margin-bottom: 8px;
}
.category-count {
    font-size: 0.85rem; color: var(--text-muted); margin-bottom: 20px;
}
.category-posts { list-style: none; padding: 0; }
.category-posts li {
    padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.03);
    transition: var(--transition-fast);
}
.category-posts li:last-child { border-bottom: none; }
.category-posts li:hover { padding-left: 8px; }
.category-posts a {
    color: var(--text-secondary); font-weight: 500; font-size: 0.92rem;
    text-decoration: none !important; transition: var(--transition-fast);
    display: flex; align-items: center; gap: 12px;
}
.category-posts a:hover { color: var(--accent-blue); }
.category-posts time {
    font-size: 0.78rem; color: var(--text-muted); font-family: var(--font-mono);
}

@media (max-width: 768px) {
    .categories-header h1 { font-size: 2rem; }
    .categories-grid { grid-template-columns: 1fr; }
}
</style>

<section class="categories-page">
    <div class="categories-header reveal">
        <h1><i class="fas fa-folder-open"></i> 文章分类</h1>
        <p>浏览不同分类下的技术文章，找到你感兴趣的内容</p>
    </div>

    <div class="categories-grid">
        {% assign sorted_categories = site.categories | sort %}
        {% for category in sorted_categories %}
        {% assign cat_name = category[0] %}
        {% assign cat_posts = category[1] %}
        <div class="category-card reveal" style="animation-delay: {{ forloop.index | minus: 1 | times: 0.1 }}s">
            <div class="category-icon">
                {% if cat_name == '网络工程' %}<i class="fas fa-network-wired"></i>
                {% elsif cat_name == '数据中心' %}<i class="fas fa-server"></i>
                {% elsif cat_name == 'Linux' %}<i class="fab fa-linux"></i>
                {% elsif cat_name == '路由交换' %}<i class="fas fa-route"></i>
                {% else %}<i class="fas fa-file-alt"></i>{% endif %}
            </div>
            <h2 class="category-name">{{ cat_name }}</h2>
            <div class="category-count">{{ cat_posts.size }} 篇文章</div>
            <ul class="category-posts">
                {% for post in cat_posts limit:5 %}
                <li>
                    <a href="{{ post.url }}">
                        <time>{{ post.date | date: "%Y-%m-%d" }}</time>
                        <span>{{ post.title }}</span>
                    </a>
                </li>
                {% endfor %}
                {% if cat_posts.size > 5 %}
                <li>
                    <a href="#cat-section-{{ cat_name }}" class="text-accent-blue">
                        查看更多 →
                    </a>
                </li>
                {% endif %}
            </ul>
        </div>
        {% endfor %}
    </div>
</section>