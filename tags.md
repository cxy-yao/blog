---
layout: default
title: 标签
permalink: /tags/
---

<section class="tags-page">
    <h1 class="section-title"><i class="fas fa-tags"></i> 标签云</h1>
    <div class="tags-cloud">
        {% assign sorted_tags = site.tags | sort %}
        {% for tag in sorted_tags %}
        <a href="#tag-{{ tag[0] }}" class="tag-cloud-item" data-count="{{ tag[1].size }}">
            #{{ tag[0] }} <span>{{ tag[1].size }}</span>
        </a>
        {% endfor %}
    </div>

    <div class="tags-list">
        {% for tag in sorted_tags %}
        <div class="tag-section" id="tag-{{ tag[0] }}">
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
.tags-cloud { display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 48px; background: var(--bg-card); border-radius: var(--radius-lg); padding: 32px; border: 1px solid var(--border); backdrop-filter: blur(12px); }
.tag-cloud-item { font-size: 0.95rem; color: var(--accent) !important; background: rgba(34,211,238,0.1); padding: 8px 18px; border-radius: 10px; font-weight: 500; transition: var(--transition); text-decoration: none !important; border: 1px solid transparent; }
.tag-cloud-item:hover { background: rgba(34,211,238,0.2); border-color: var(--accent); transform: translateY(-2px); }
.tag-cloud-item span { font-size: 0.75rem; color: var(--text-muted); margin-left: 4px; }
.tag-cloud-item[data-count="1"] { font-size: 0.85rem; opacity: 0.7; }
.tag-cloud-item[data-count="2"] { font-size: 0.95rem; }
.tag-cloud-item[data-count="3"] { font-size: 1.05rem; font-weight: 600; }
.tags-list { display: flex; flex-direction: column; gap: 24px; }
.tag-section { background: var(--bg-card); border-radius: var(--radius-lg); padding: 28px; border: 1px solid var(--border); backdrop-filter: blur(12px); }
.tag-name { font-size: 1.2rem; font-weight: 700; margin-bottom: 16px; display: flex; align-items: center; gap: 10px; }
.tag-name i { color: var(--accent); }
.tag-count { font-size: 0.8rem; color: var(--text-muted); background: rgba(34,211,238,0.12); padding: 3px 10px; border-radius: 12px; margin-left: auto; }
.tag-posts { list-style: none; padding: 0; }
.tag-posts li { display: flex; align-items: center; gap: 16px; padding: 10px 0; border-bottom: 1px solid rgba(51,65,85,0.3); }
.tag-posts li:last-child { border-bottom: none; }
.tag-posts time { color: var(--text-muted); font-size: 0.85rem; font-family: 'JetBrains Mono', monospace; min-width: 100px; }
.tag-posts a { color: var(--text-secondary); font-weight: 500; }
.tag-posts a:hover { color: var(--primary-light); }
@media (max-width: 768px) { .tag-posts li { flex-direction: column; align-items: flex-start; gap: 4px; } }
</style>
