#!/usr/bin/env python3
"""Jekyll blog local preview builder — full Liquid template support."""
import os, re, markdown
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

BLOG_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BLOG_DIR, '_site')

def parse_frontmatter(content):
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if not m: return {}, content
    fm = {}
    for line in m.group(1).strip().split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            k, v = k.strip(), v.strip()
            if v.startswith('[') and v.endswith(']'):
                fm[k] = [t.strip().strip('"\'') for t in v[1:-1].split(',') if t.strip()]
            else:
                fm[k] = v.strip('"')
    return fm, m.group(2)

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f: return f.read()

def render_layout_chain(layout_name, page, site, content, layouts_dir):
    """Recursively render layout chain (layout -> default)."""
    path = os.path.join(layouts_dir, f'{layout_name}.html')
    if not os.path.exists(path): return content
    html = read_file(path)
    # Parse frontmatter
    fm, body = parse_frontmatter(html)
    if body:
        body = body.replace('{{ content }}', content)
    else:
        body = html.replace('{{ content }}', content)
    
    # If this layout has a parent, render it
    parent = fm.get('layout')
    if parent:
        return render_layout_chain(parent, page, site, body, layouts_dir)
    return body

def liquid_render(html, page, site, posts_data):
    """Full Liquid template rendering."""
    result = html
    
    # === Site variables ===
    result = result.replace('{{ site.title }}', site.get('title', ''))
    result = result.replace('{{ site.description }}', site.get('description', ''))
    result = result.replace('{{ site.author }}', site.get('author', ''))
    result = result.replace('{{ site.posts.size }}', str(len(posts_data)))
    result = result.replace('{{ site.categories.size }}', str(len(site.get('categories', {}))))
    result = result.replace('{{ site.tags.size }}', str(len(site.get('tags', {}))))
    result = result.replace('{{ site.time | date: "%Y" }}', str(datetime.now().year))
    
    # === Page variables ===
    result = result.replace('{{ page.title | default: site.title }}', page.get('title', site.get('title', '')))
    result = result.replace('{{ page.description | default: site.description }}', site.get('description', ''))
    result = result.replace('{{ page.title }}', page.get('title', ''))
    result = result.replace('{{ page.date | date: "%Y年%m月%d日" }}', page.get('date', ''))
    
    # === Conditional: {% if page.url == '/xxx/' %}active{% endif %} ===
    url = page.get('url', '/')
    def replace_active(m):
        target = m.group(1)
        return 'active' if url == target else ''
    result = re.sub(r"\{%\s*if\s+page\.url\s*==\s*'([^']+)'\s*%\}active\{%\s*endif\s*%\}", replace_active, result)
    
    # === Categories conditional block ===
    def replace_cat_block(m):
        cats = page.get('categories_list', [])
        inner = m.group(1)
        if not cats: return ''
        out = ''
        for cat in cats:
            out += inner.replace('{{ cat }}', cat)
        return out
    result = re.sub(r'\{%\s*if\s+page\.categories\.size\s*>\s*0\s*%\}(.*?)\{%\s*endif\s*%\}', replace_cat_block, result, flags=re.DOTALL)
    
    # === Tags loop ===
    def replace_tag_loop(m):
        tags = page.get('tags', [])
        inner = m.group(1)
        out = ''
        for tag in tags:
            out += inner.replace('{{ tag }}', tag)
        return out
    result = re.sub(r'\{%\s*for\s+tag\s+in\s+page\.tags\s*%\}(.*?)\{%\s*endfor\s*%\}', replace_tag_loop, result, flags=re.DOTALL)
    
    # === Categories loop (for category tags in post meta) ===
    def replace_cat_loop(m):
        cats = page.get('categories_list', [])
        inner = m.group(1)
        out = ''
        for cat in cats:
            out += inner.replace('{{ cat }}', cat)
        return out
    result = re.sub(r'\{%\s*for\s+cat\s+in\s+page\.categories\s*%\}(.*?)\{%\s*endfor\s*%\}', replace_cat_loop, result, flags=re.DOTALL)
    
    # === Categories page: sorted categories loop ===
    categories = site.get('categories', {})
    def replace_sorted_cats(m):
        body = m.group(1)
        out = ''
        for idx, (cat_name, cat_posts) in enumerate(sorted(categories.items())):
            cat_block = body
            cat_block = cat_block.replace('{{ category[0] }}', cat_name)
            cat_block = cat_block.replace('{{ category[1].size }}', str(len(cat_posts)))
            # forloop.index starts at 1
            cat_block = cat_block.replace('{{ forloop.index | minus: 1 | times: 0.1 }}', str(idx * 0.1))
            # Inner loop
            def replace_cat_inner_loop(inner_m):
                inner = inner_m.group(1)
                iout = ''
                for p in cat_posts:
                    iout += inner.replace('{{ post.date | date: "%Y-%m-%d" }}', p.get('date', '')).replace('{{ post.url }}', p['url']).replace('{{ post.title }}', p.get('title', ''))
                return iout
            cat_block = re.sub(r'\{%\s*for\s+post\s+in\s+category\[1\]\s*%\}(.*?)\{%\s*endfor\s*%\}', replace_cat_inner_loop, cat_block, flags=re.DOTALL)
            out += cat_block
        return out
    result = re.sub(r'\{%\s*for\s+category\s+in\s+sorted_categories\s*%\}(.*?)\{%\s*endfor\s*%\}', replace_sorted_cats, result, flags=re.DOTALL)
    
    # === Tags page: sorted tags loop ===
    tags_dict = site.get('tags', {})
    def replace_sorted_tags(m):
        body = m.group(1)
        out = ''
        for idx, (tag_name, tag_posts) in enumerate(sorted(tags_dict.items())):
            tag_block = body
            tag_block = tag_block.replace('{{ tag[0] }}', tag_name)
            tag_block = tag_block.replace('{{ tag[1].size }}', str(len(tag_posts)))
            tag_block = tag_block.replace('{{ forloop.index | minus: 1 | times: 0.1 }}', str(idx * 0.1))
            def replace_tag_inner_loop(inner_m):
                inner = inner_m.group(1)
                iout = ''
                for p in tag_posts:
                    iout += inner.replace('{{ post.date | date: "%Y-%m-%d" }}', p.get('date', '')).replace('{{ post.url }}', p['url']).replace('{{ post.title }}', p.get('title', ''))
                return iout
            tag_block = re.sub(r'\{%\s*for\s+post\s+in\s+tag\[1\]\s*%\}(.*?)\{%\s*endfor\s*%\}', replace_tag_inner_loop, tag_block, flags=re.DOTALL)
            out += tag_block
        return out
    result = re.sub(r'\{%\s*for\s+tag\s+in\s+sorted_tags\s*%\}(.*?)\{%\s*endfor\s*%\}', replace_sorted_tags, result, flags=re.DOTALL)
    
    # === Posts loop (home page) — direct HTML generation ===
    cat_class_map = {'网络工程': 'cat-network', '数据中心': 'cat-datacenter', 'Linux': 'cat-linux'}
    
    def replace_posts_loop(m):
        out = ''
        for idx, post in enumerate(posts_data):
            cats = post.get('categories', [])
            cat = cats[0] if cats else ''
            cat_class = cat_class_map.get(cat, 'cat-default')
            cat_span = f'<span class="post-card-category {cat_class}">{cat}</span>' if cat else ''
            tags_html = ''.join(f'<span class="tag-pill">#{t}</span>' for t in post.get('tags', [])[:4])
            tags_div = f'<div class="post-card-tags">{tags_html}</div>' if tags_html else ''
            # Strip markdown: headers, code blocks, bold, links, etc.
            raw_excerpt = post.get('excerpt', '')
            raw_excerpt = re.sub(r'```[^`]*', '', raw_excerpt)  # code blocks (open/close)
            raw_excerpt = re.sub(r'`[^`]+`', '', raw_excerpt)  # inline code
            raw_excerpt = re.sub(r'#{1,6}\s*', '', raw_excerpt)  # headers
            raw_excerpt = re.sub(r'\*\*([^*]+)\*\*', r'\1', raw_excerpt)  # bold
            raw_excerpt = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', raw_excerpt)  # links
            raw_excerpt = re.sub(r'^\s*>\s*', '', raw_excerpt, flags=re.MULTILINE)  # blockquotes
            raw_excerpt = re.sub(r'^\s*[-*+]\s+', '', raw_excerpt, flags=re.MULTILINE)  # lists
            raw_excerpt = re.sub(r'\|', ' ', raw_excerpt)  # table pipes
            raw_excerpt = re.sub(r'-{3,}', '', raw_excerpt)  # horizontal rules / table separator
            raw_excerpt = re.sub(r'\n+', ' ', raw_excerpt).strip()  # collapse newlines
            raw_excerpt = re.sub(r'\s{2,}', ' ', raw_excerpt)  # collapse spaces
            excerpt = raw_excerpt[:120]
            out += f'''
        <article class="post-card reveal" style="animation-delay: {idx * 0.08}s">
            <div class="post-card-header">
                <time><i class="far fa-calendar-alt"></i> {post.get('date', '')}</time>
                {cat_span}
            </div>
            <h3 class="post-card-title"><a href="{post['url']}">{post.get('title', '')}</a></h3>
            <p class="post-card-excerpt">{excerpt}...</p>
            {tags_div}
            <a href="{post['url']}" class="read-more">阅读全文 <span class="arrow">→</span></a>
        </article>'''
        return out
    result = re.sub(r'\{%\s*for\s+post\s+in\s+site\.posts\s*%\}(.*?)\{%\s*endfor\s*%\}', replace_posts_loop, result, flags=re.DOTALL)
    
    # === Assign tags (for sorted categories) ===
    result = re.sub(r'\{%\s*assign\s+\w+\s*=\s*site\.\w+\s*\|\s*sort\s*%\}', '', result)
    
    # === Clean up remaining liquid tags ===
    result = re.sub(r'\{%.*?%\}', '', result)
    result = re.sub(r'\{\{.*?\}\}', '', result)
    
    return result

def build():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    layouts_dir = os.path.join(BLOG_DIR, '_layouts')
    
    # Read config
    config = {}
    cfg_path = os.path.join(BLOG_DIR, '_config.yml')
    if os.path.exists(cfg_path):
        for line in read_file(cfg_path).split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and ':' in line:
                k, v = line.split(':', 1)
                config[k.strip()] = v.strip().strip('"')
    
    site = {
        'title': config.get('title', 'ChenChuLin的博客'),
        'description': config.get('description', ''),
        'author': config.get('author', 'ChenChuLin'),
    }
    
    # Build posts
    posts_dir = os.path.join(BLOG_DIR, '_posts')
    posts_data = []
    categories = {}
    tags_dict = {}
    
    for fname in sorted(os.listdir(posts_dir), reverse=True):
        if not fname.endswith('.md'): continue
        content = read_file(os.path.join(posts_dir, fname))
        fm, body = parse_frontmatter(content)
        
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})', fname)
        if date_match: fm['date'] = date_match.group(1)
        
        slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', fname).replace('.md', '')
        fm['url'] = f"/{fm.get('date', '').replace('-', '/')}/{slug}/"
        
        # Parse categories
        cats = fm.get('categories', '')
        if isinstance(cats, str): cats = [cats] if cats else []
        fm['categories'] = cats
        fm['categories_list'] = cats
        
        # Parse tags
        post_tags = fm.get('tags', [])
        if isinstance(post_tags, str):
            post_tags = [t.strip() for t in post_tags.strip('[]').split(',') if t.strip()]
        fm['tags'] = post_tags
        
        # Render markdown with fenced_code, tables, and TOC (heading IDs)
        md = markdown.Markdown(extensions=['fenced_code', 'tables', 'toc'])
        fm['html'] = md.convert(body)
        fm['excerpt'] = re.sub(r'<[^>]+>', '', body[:400]).strip()
        
        posts_data.append(fm)
        for cat in cats: categories.setdefault(cat, []).append(fm)
        for tag in post_tags: tags_dict.setdefault(tag, []).append(fm)
    
    site['categories'] = categories
    site['tags'] = tags_dict
    
    # Build each post page
    for post in posts_data:
        page = dict(post)
        page['categories_list'] = post.get('categories', [])
        html = render_layout_chain('post', page, site, post['html'], layouts_dir)
        html = liquid_render(html, page, site, posts_data)
        
        post_dir = os.path.join(OUTPUT_DIR, post['url'].strip('/'))
        os.makedirs(post_dir, exist_ok=True)
        with open(os.path.join(post_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
    
    # Build home page
    home_content = read_file(os.path.join(layouts_dir, 'home.html'))
    _, home_body = parse_frontmatter(home_content)
    home_html = render_layout_chain('default', {'url': '/', 'title': ''}, site, home_body, layouts_dir)
    home_html = liquid_render(home_html, {'url': '/', 'title': ''}, site, posts_data)
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(home_html)
    
    # Build about page
    about_content = read_file(os.path.join(BLOG_DIR, 'about.md'))
    about_fm, about_body = parse_frontmatter(about_content)
    about_html = render_layout_chain('default', {'url': '/about/', 'title': '关于我'}, site, about_body, layouts_dir)
    about_html = liquid_render(about_html, {'url': '/about/', 'title': '关于我'}, site, posts_data)
    about_dir = os.path.join(OUTPUT_DIR, 'about')
    os.makedirs(about_dir, exist_ok=True)
    with open(os.path.join(about_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(about_html)
    
    # Build categories page
    cats_content = read_file(os.path.join(BLOG_DIR, 'categories.md'))
    cats_fm, cats_body = parse_frontmatter(cats_content)
    cats_html = render_layout_chain('default', {'url': '/categories/', 'title': '分类'}, site, cats_body, layouts_dir)
    cats_html = liquid_render(cats_html, {'url': '/categories/', 'title': '分类'}, site, posts_data)
    cats_dir = os.path.join(OUTPUT_DIR, 'categories')
    os.makedirs(cats_dir, exist_ok=True)
    with open(os.path.join(cats_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(cats_html)
    
    # Build tags page
    tags_content = read_file(os.path.join(BLOG_DIR, 'tags.md'))
    tags_fm, tags_body = parse_frontmatter(tags_content)
    tags_html = render_layout_chain('default', {'url': '/tags/', 'title': '标签'}, site, tags_body, layouts_dir)
    tags_html = liquid_render(tags_html, {'url': '/tags/', 'title': '标签'}, site, posts_data)
    tags_dir = os.path.join(OUTPUT_DIR, 'tags')
    os.makedirs(tags_dir, exist_ok=True)
    with open(os.path.join(tags_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(tags_html)
    
    print(f"✓ Built {len(posts_data)} posts")
    print(f"✓ Categories: {list(categories.keys())}")
    print(f"✓ Tags: {len(tags_dict)} tags")
    print(f"✓ Output: {OUTPUT_DIR}")

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=OUTPUT_DIR, **kw)
    def do_GET(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            idx = os.path.join(path, 'index.html')
            if os.path.exists(idx):
                self.path = self.path.rstrip('/') + '/index.html'
        super().do_GET()
    def log_message(self, format, *args):
        pass  # Suppress logs

if __name__ == '__main__':
    build()
    PORT = 8791
    print(f"\n🌐 Preview: http://localhost:{PORT}")
    HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
