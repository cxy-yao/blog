---
layout: default
title: 标签
permalink: /tags/
---

<section class="tags-page">
    <h1 class="section-title reveal"><i class="fas fa-tags"></i> 标签云</h1>
    <div class="tags-cloud reveal">
        {% assign sorted_tags = site.tags | sort %}
        {% for tag in sorted_tags %}
        <a href="#tag-{{ tag[0] }}" class="tag-cloud-item" data-count="{{ tag[1].size }}">
            #{{ tag[0] }} <span>{{ tag[1].size }}</span>
        </a>
        {% endfor %}
    </div>

    <div class="tags-list">
        {% for tag in sorted_tags %}
        <div class="tag-section reveal" id="tag-{{ tag[0] }}">
            <h2 class="tag-name"><i class="fas fa-hashtag"></i> {{ tag[0] }} <span class="tag-count">{{ tag[1].size }} 篇</span></h2>
            <ul class="tag-posts">
                {% for post in tag[1] %}
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
.tags-page { max-width: 900px; margin: 0 auto; }
.tags-cloud {
    display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 48px;
    background: var(--bg-card); border-radius: var(--radius); padding: 32px;
    border: 1px solid var(--glass-border); backdrop-filter: blur(16px);
}
.tag-cloud-item {
    font-size: 0.92rem; color: var(--accent-cyan) !important;
    background: rgba(6,182,212,0.06); padding: 8px 18px; border-radius: 20px;
    font-weight: 500; transition: var(--transition-fast);
    text-decoration: none !important; border: 1px solid rgba(6,182,212,0.1);
}
.tag-cloud-item:hover {
    background: rgba(6,182,212,0.12); border-color: rgba(6,182,212,0.25);
    transform: translateY(-2px);
}
.tag-cloud-item span { font-size: 0.72rem; color: var(--text-muted); margin-left: 4px; }
.tag-cloud-item[data-count="1"] { font-size: 0.82rem; opacity: 0.6; }
.tag-cloud-item[data-count="2"] { font-size: 0.92rem; }
.tag-cloud-item[data-count="3"] { font-size: 1rem; font-weight: 600; }
.tags-list { display: flex; flex-direction: column; gap: 24px; }
.tag-section {
    background: var(--bg-card); border-radius: var(--radius); padding: 28px;
    border: 1px solid var(--glass-border); backdrop-filter: blur(16px);
}
.tag-name {
    font-size: 1.2rem; font-weight: 700; margin-bottom: 18px;
    display: flex; align-items: center; gap: 10px;
}
.tag-name i { color: var(--accent-cyan); }
.tag-count {
    font-size: 0.78rem; color: var(--text-muted); margin-left: auto;
    background: rgba(6,182,212,0.08); padding: 4px 12px; border-radius: 20px;
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
    color: var(--text-muted); font-size: 0.82rem;
    font-family: var(--font-mono); min-width: 100px;
}
.tag-posts a {
    color: var(--text-secondary); font-weight: 500;
    text-decoration: none !important; transition: var(--transition-fast);
}
.tag-posts a:hover { color: var(--accent-blue); }
@media (max-width: 768px) {
    .tag-posts li { flex-direction: column; align-items: flex-start; gap: 4px; }
}
</style>
