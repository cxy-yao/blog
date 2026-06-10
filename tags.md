---
layout: default
title: 标签
permalink: /tags/
---

<style>
.tags-page { max-width: 1000px; margin: 0 auto; }
.tags-header { text-align: center; margin-bottom: 56px; }
.tags-header h1 {
    font-size: 2.5rem; font-weight: 800; margin-bottom: 12px;
    background: var(--gradient-main); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.tags-header p { color: var(--text-primary); font-size: 1.1rem; }
.tags-cloud-wrapper {
    background: var(--bg-card); border-radius: var(--radius); padding: 40px;
    border: 1px solid var(--glass-border); backdrop-filter: blur(16px);
    margin-bottom: 60px;
}
.tags-cloud {
    display: flex; flex-wrap: wrap; gap: 12px; justify-content: center;
}
.tag-cloud-item {
    font-size: 0.95rem; color: var(--text-primary);
    background: rgba(255,255,255,0.06); padding: 10px 22px; border-radius: 28px;
    font-weight: 500; transition: var(--transition-fast);
    text-decoration: none !important; border: 1px solid rgba(255,255,255,0.12);
}
.tag-cloud-item:hover {
    background: rgba(59,130,246,0.1); border-color: rgba(59,130,246,0.25);
    color: var(--accent-blue); transform: translateY(-3px);
}
.tag-cloud-item.hot {
    background: rgba(255,255,255,0.08); border-color: rgba(255,255,255,0.15);
    color: var(--text-primary);
}
.tag-cloud-item.hot:hover { background: rgba(236,72,153,0.15); border-color: rgba(236,72,153,0.2); color: var(--accent-pink); }
.tag-cloud-item span { font-size: 0.75rem; color: var(--text-muted); margin-left: 6px; }

.tags-list { display: flex; flex-direction: column; gap: 20px; }
.tag-section {
    background: var(--bg-card); border-radius: var(--radius); padding: 28px;
    border: 1px solid var(--glass-border); backdrop-filter: blur(16px);
    transition: var(--transition);
}
.tag-section:hover { border-color: rgba(59,130,246,0.15); }
.tag-header {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 20px;
}
.tag-name {
    font-size: 1.3rem; font-weight: 700; display: flex; align-items: center; gap: 10px;
}
.tag-name i { color: var(--accent-cyan); }
.tag-count {
    font-size: 0.82rem; color: var(--text-muted);
    background: rgba(59,130,246,0.08); padding: 5px 14px; border-radius: 20px;
}
.tag-posts { list-style: none; padding: 0; }
.tag-posts li {
    display: flex; align-items: center; gap: 16px;
    padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.03);
    transition: var(--transition-fast);
}
.tag-posts li:last-child { border-bottom: none; }
.tag-posts li:hover { padding-left: 8px; }
.tag-posts time {
    color: var(--text-muted); font-size: 0.85rem;
    font-family: var(--font-mono); min-width: 100px;
}
.tag-posts a {
    color: var(--text-primary); font-weight: 500; font-size: 0.95rem;
    text-decoration: none !important; transition: var(--transition-fast);
    flex-grow: 1;
}
.tag-posts a:hover { color: var(--accent-blue); }

@media (max-width: 768px) {
    .tags-header h1 { font-size: 2rem; }
    .tags-cloud-wrapper { padding: 24px; }
    .tag-posts li { flex-direction: column; align-items: flex-start; gap: 6px; }
    .tag-posts time { min-width: auto; }
}
</style>

<section class="tags-page">
    <div class="tags-header reveal">
        <h1><i class="fas fa-tags"></i> 标签云</h1>
        <p>通过标签快速筛选你感兴趣的技术主题</p>
    </div>

    <div class="tags-cloud-wrapper reveal">
        <div class="tags-cloud">
            {% assign sorted_tags = site.tags | sort %}
            {% for tag in sorted_tags %}
            {% assign tag_name = tag[0] %}
            {% assign tag_count = tag[1].size %}
            <a href="#tag-{{ tag_name }}" 
               class="tag-cloud-item {% if tag_count >= 3 %}hot{% endif %}">
                #{{ tag_name }} <span>{{ tag_count }}</span>
            </a>
            {% endfor %}
        </div>
    </div>

    <div class="tags-list">
        {% for tag in sorted_tags %}
        {% assign tag_name = tag[0] %}
        {% assign tag_posts = tag[1] %}
        <div class="tag-section reveal" id="tag-{{ tag_name }}">
            <div class="tag-header">
                <h2 class="tag-name">
                    <i class="fas fa-hashtag"></i> {{ tag_name }}
                </h2>
                <span class="tag-count">{{ tag_posts.size }} 篇文章</span>
            </div>
            <ul class="tag-posts">
                {% for post in tag_posts %}
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