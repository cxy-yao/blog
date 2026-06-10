---
layout: default
title: 关于我
permalink: /about/
---

<style>
.about-page { max-width: 900px; margin: 0 auto; }
.about-header { text-align: center; padding: 60px 0 40px; }
.about-avatar {
    width: 140px; height: 140px; border-radius: 50%; margin: 0 auto 32px;
    background: var(--gradient-main); display: flex; align-items: center; justify-content: center;
    font-size: 4rem; box-shadow: 0 0 50px rgba(59,130,246,0.3);
    animation: avatar-float 4s ease-in-out infinite;
}
@keyframes avatar-float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}
.about-header h1 {
    font-size: 3rem; font-weight: 900; margin-bottom: 14px;
    background: var(--gradient-main); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.about-role {
    font-size: 1.25rem; color: var(--text-secondary); font-weight: 400; margin-bottom: 16px;
    letter-spacing: 1px;
}
.about-location {
    color: var(--text-muted); font-size: 0.95rem;
}
.about-location i { margin-right: 8px; color: var(--accent-pink); }

.about-section {
    background: var(--bg-card); border-radius: var(--radius); padding: 40px;
    margin-bottom: 24px; border: 1px solid var(--glass-border);
    backdrop-filter: blur(16px); transition: var(--transition);
}
.about-section:hover { border-color: rgba(59,130,246,0.15); }
.about-section h2 {
    font-size: 1.45rem; font-weight: 700; margin-bottom: 28px;
    display: flex; align-items: center; gap: 14px;
}
.about-section h2 i { color: var(--accent-cyan); font-size: 1.3rem; }
.about-section p { color: var(--text-secondary); line-height: 1.9; font-size: 1.02rem; }
.about-section p + p { margin-top: 16px; }

.skills-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
.skill-card {
    background: rgba(0,0,0,0.2); padding: 28px; border-radius: var(--radius-sm);
    text-align: center; transition: var(--transition); border: 1px solid transparent;
}
.skill-card:hover {
    transform: translateY(-6px); background: rgba(0,0,0,0.3);
    border-color: rgba(59,130,246,0.15);
}
.skill-icon { font-size: 2.8rem; margin-bottom: 16px; }
.skill-card h3 { font-size: 1.15rem; font-weight: 700; margin-bottom: 10px; }
.skill-card p { font-size: 0.86rem; color: var(--text-muted); line-height: 1.65; margin: 0; }

.content-topics { display: flex; flex-direction: column; gap: 16px; }
.topic-item {
    display: flex; align-items: center; gap: 20px; padding: 20px;
    background: rgba(0,0,0,0.15); border-radius: var(--radius-sm);
    border: 1px solid transparent; transition: var(--transition);
}
.topic-item:hover {
    background: rgba(0,0,0,0.25); border-color: var(--glass-border);
    transform: translateX(8px);
}
.topic-icon {
    width: 52px; height: 52px; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem; flex-shrink: 0;
}
.topic-info h3 { font-size: 1.1rem; font-weight: 700; margin-bottom: 6px; }
.topic-info p { font-size: 0.9rem; color: var(--text-muted); margin: 0; line-height: 1.6; }

.tech-tags { display: flex; flex-wrap: wrap; gap: 12px; }
.tech-tag {
    padding: 8px 20px; border-radius: 24px; font-size: 0.86rem; font-weight: 500;
    background: rgba(0,0,0,0.2); color: var(--text-secondary);
    border: 1px solid var(--glass-border); transition: var(--transition-fast);
}
.tech-tag:hover {
    background: color-mix(in srgb, var(--tag-color, var(--accent-blue)) 12%, transparent);
    border-color: color-mix(in srgb, var(--tag-color, var(--accent-blue)) 35%, transparent);
    color: var(--tag-color, var(--accent-blue)); transform: translateY(-3px);
}

.contact-links { display: flex; gap: 16px; flex-wrap: wrap; }
.contact-btn {
    display: inline-flex; align-items: center; gap: 12px;
    background: rgba(0,0,0,0.25); color: var(--text-primary);
    padding: 16px 32px; border-radius: var(--radius-sm); font-weight: 600; font-size: 1rem;
    transition: var(--transition); border: 1px solid var(--glass-border);
    text-decoration: none;
}
.contact-btn:hover {
    background: rgba(59,130,246,0.12); border-color: rgba(59,130,246,0.3);
    transform: translateY(-3px);
    box-shadow: 0 8px 28px rgba(59,130,246,0.15);
}
.contact-btn i { font-size: 1.3rem; }

.stats-row {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px;
    margin-bottom: 24px;
}
.stat-card {
    background: var(--bg-card); border-radius: var(--radius); padding: 28px;
    border: 1px solid var(--glass-border); text-align: center;
}
.stat-value {
    font-size: 2.2rem; font-weight: 800;
    background: var(--gradient-main); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 8px;
}
.stat-label { font-size: 0.88rem; color: var(--text-muted); }

@media (max-width: 768px) {
    .about-header h1 { font-size: 2.2rem; }
    .about-avatar { width: 100px; height: 100px; font-size: 2.8rem; }
    .about-section { padding: 28px; }
    .skills-grid { grid-template-columns: 1fr; }
    .stats-row { grid-template-columns: 1fr; }
    .contact-links { flex-direction: column; }
    .contact-btn { width: 100%; justify-content: center; }
}

/* === 写作统计 === */
.writing-stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 32px;
}
.writing-stat-card {
    background: rgba(0,0,0,0.2);
    border-radius: var(--radius-sm);
    padding: 24px 16px;
    text-align: center;
    border: 1px solid var(--glass-border);
    transition: var(--transition);
}
.writing-stat-card:hover {
    border-color: rgba(59,130,246,0.2);
    transform: translateY(-3px);
}
.writing-stat-num {
    font-size: 2rem;
    font-weight: 800;
    background: var(--gradient-main);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 6px;
}
.writing-stat-label {
    font-size: 0.82rem;
    color: var(--text-muted);
}

/* === 热力图 === */
.heatmap-wrap {
    background: rgba(0,0,0,0.12);
    border-radius: var(--radius-sm);
    padding: 24px;
    border: 1px solid var(--glass-border);
}
.heatmap-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    font-size: 0.92rem;
    font-weight: 600;
    color: var(--text-secondary);
}
.heatmap-legend {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 0.75rem;
    color: var(--text-muted);
}
.hm-cell {
    width: 13px; height: 13px;
    border-radius: 3px;
    display: inline-block;
    background: rgba(255,255,255,0.04);
}
.hm-lv0 { background: rgba(255,255,255,0.04); }
.hm-lv1 { background: rgba(6,182,212,0.3); }
.hm-lv2 { background: rgba(6,182,212,0.5); }
.hm-lv3 { background: rgba(6,182,212,0.8); }
.hm-lv4 { background: #06b6d4; box-shadow: 0 0 6px rgba(6,182,212,0.4); }

.heatmap-body { display: flex; flex-direction: column; gap: 0; }
.hm-months {
    display: flex;
    padding-left: 32px;
    margin-bottom: 4px;
    font-size: 0.7rem;
    color: var(--text-muted);
}
.hm-months span {
    flex: 1;
    text-align: left;
    white-space: nowrap;
}
.hm-grid {
    display: flex;
    gap: 4px;
}
.hm-labels {
    display: flex;
    flex-direction: column;
    gap: 3px;
    padding-right: 6px;
    padding-top: 0;
    font-size: 0.68rem;
    color: var(--text-muted);
    line-height: 13px;
}
.hm-labels span { height: 13px; }
.hm-cells {
    display: grid;
    grid-template-rows: repeat(7, 13px);
    grid-auto-flow: column;
    gap: 3px;
    flex: 1;
}
.hm-cells .hm-cell { cursor: default; }
.hm-cells .hm-cell:hover {
    outline: 2px solid var(--accent-blue);
    outline-offset: 1px;
    transform: scale(1.15);
    z-index: 2;
    position: relative;
}

@media (max-width: 768px) {
    .writing-stats-row { grid-template-columns: repeat(2, 1fr); }
    .heatmap-wrap { padding: 16px; overflow-x: auto; }
}
</style>

<div class="about-page">
    <div class="about-header reveal">
        <div class="about-avatar">⚡</div>
        <h1>ChenChuLin</h1>
        <p class="about-role">网络工程师 · 技术博主</p>
        <div class="about-location"><i class="fas fa-map-marker-alt"></i> 中国 · AI算力网络方向</div>
    </div>

    <div class="stats-row">
        <div class="stat-card reveal">
            <div class="stat-value">{{ site.posts.size }}</div>
            <div class="stat-label">技术文章</div>
        </div>
        <div class="stat-card reveal">
            <div class="stat-value">5+</div>
            <div class="stat-label">年经验</div>
        </div>
        <div class="stat-card reveal">
            <div class="stat-value">3</div>
            <div class="stat-label">主要领域</div>
        </div>
    </div>

    <!-- 写作统计 + 热力图 -->
    <section class="about-section reveal">
        <h2><i class="fas fa-chart-bar"></i> 写作统计</h2>

        <div class="writing-stats-row">
            <div class="writing-stat-card">
                <div class="writing-stat-num">{{ site.posts.size }}</div>
                <div class="writing-stat-label">总文章</div>
            </div>
            <div class="writing-stat-card">
                <div class="writing-stat-num" id="totalWords">-</div>
                <div class="writing-stat-label">总字数</div>
            </div>
            <div class="writing-stat-card">
                <div class="writing-stat-num" id="firstPostDate">-</div>
                <div class="writing-stat-label">最早文章</div>
            </div>
            <div class="writing-stat-card">
                <div class="writing-stat-num">{{ site.categories.size }}</div>
                <div class="writing-stat-label">分类数</div>
            </div>
        </div>

        <div class="heatmap-wrap">
            <div class="heatmap-header">
                <span>写作热力图</span>
                <span class="heatmap-legend">
                    <span>少</span>
                    <span class="hm-cell hm-lv0"></span>
                    <span class="hm-cell hm-lv1"></span>
                    <span class="hm-cell hm-lv2"></span>
                    <span class="hm-cell hm-lv3"></span>
                    <span>多</span>
                </span>
            </div>
            <div class="heatmap-body">
                <div class="hm-months" id="hmMonths"></div>
                <div class="hm-grid">
                    <div class="hm-labels"><span>一</span><span>三</span><span>五</span><span>日</span></div>
                    <div class="hm-cells" id="hmCells"></div>
                </div>
            </div>
        </div>

        <script id="postDatesData" type="application/json">[
            {% for post in site.posts %}
            {% assign d = post.date | date: '%Y-%m-%d' %}
            {% assign w = post.content | number_of_words %}
            "{{ d }}|{{ w }}"{% unless forloop.last %},{% endunless %}
            {% endfor %}
        ]</script>
    </section>

    <section class="about-section reveal">
        <h2><i class="fas fa-user-astronaut"></i> 关于我</h2>
        <p>资深网络工程师，专注于数据中心网络架构设计与运维。在AI算力网络、大规模Spine-Leaf组网、VXLAN EVPN、BGP/OSPF协议等领域有丰富的实战经验。日常使用华为CE系列、Cisco Catalyst/Nexus、华三S系列交换机。</p>
        <p>这个博客是我的技术笔记本——记录工作中遇到的问题、解决方案、以及对网络技术的思考。所有文章都来自真实项目经验，不是纸上谈兵。</p>
        <p>我相信技术分享的价值，希望通过这些笔记帮助到同样在网络领域奋斗的同行。如果你有任何问题或建议，欢迎随时交流！</p>
    </section>

    <section class="about-section reveal">
        <h2><i class="fas fa-microchip"></i> 核心技能</h2>
        <div class="skills-grid">
            <div class="skill-card">
                <div class="skill-icon">🌐</div>
                <h3>数据中心网络</h3>
                <p>Spine-Leaf架构 · VXLAN EVPN · M-LAG · RoCEv2无损网络</p>
            </div>
            <div class="skill-card">
                <div class="skill-icon">🤖</div>
                <h3>AI算力网络</h3>
                <p>昇腾/NVIDIA集群组网 · PFC+ECN流控 · 参数面/样本面设计</p>
            </div>
            <div class="skill-card">
                <div class="skill-icon">📡</div>
                <h3>路由交换</h3>
                <p>BGP 13步选路 · OSPF区域设计 · IS-IS · 路由策略</p>
            </div>
            <div class="skill-card">
                <div class="skill-icon">🔧</div>
                <h3>自动化运维</h3>
                <p>Python/Netmiko · WSL2工作流 · Shell脚本 · 知识库构建</p>
            </div>
        </div>
    </section>

    <section class="about-section reveal">
        <h2><i class="fas fa-pen-fancy"></i> 博客内容</h2>
        <div class="content-topics">
            <div class="topic-item">
                <div class="topic-icon" style="background: rgba(59,130,246,0.12); color: var(--accent-blue);">
                    <i class="fas fa-server"></i>
                </div>
                <div class="topic-info">
                    <h3>网络工程</h3>
                    <p>华为CE交换机运维、BGP/OSPF协议详解、故障排查方法论</p>
                </div>
            </div>
            <div class="topic-item">
                <div class="topic-icon" style="background: rgba(139,92,246,0.12); color: var(--accent-purple);">
                    <i class="fas fa-cloud"></i>
                </div>
                <div class="topic-info">
                    <h3>数据中心</h3>
                    <p>VXLAN EVPN实战、AI算力网络架构、Spine-Leaf组网</p>
                </div>
            </div>
            <div class="topic-item">
                <div class="topic-icon" style="background: rgba(16,185,129,0.12); color: var(--accent-emerald);">
                    <i class="fab fa-linux"></i>
                </div>
                <div class="topic-info">
                    <h3>Linux运维</h3>
                    <p>WSL2效率工具、Python自动化脚本、知识管理</p>
                </div>
            </div>
            <div class="topic-item">
                <div class="topic-icon" style="background: rgba(245,158,11,0.12); color: var(--accent-amber);">
                    <i class="fas fa-bug"></i>
                </div>
                <div class="topic-info">
                    <h3>故障案例</h3>
                    <p>真实故障排查过程、根因分析、预防措施</p>
                </div>
            </div>
        </div>
    </section>

    <section class="about-section reveal">
        <h2><i class="fas fa-chart-line"></i> 技术栈全景</h2>
        <div class="tech-tags">
            <span class="tech-tag" style="--tag-color: var(--accent-blue)">华为CE12800</span>
            <span class="tech-tag" style="--tag-color: var(--accent-blue)">华为CE8800</span>
            <span class="tech-tag" style="--tag-color: var(--accent-purple)">Cisco Nexus</span>
            <span class="tech-tag" style="--tag-color: var(--accent-purple)">Cisco Catalyst</span>
            <span class="tech-tag" style="--tag-color: var(--accent-emerald)">BGP</span>
            <span class="tech-tag" style="--tag-color: var(--accent-emerald)">OSPF</span>
            <span class="tech-tag" style="--tag-color: var(--accent-emerald)">IS-IS</span>
            <span class="tech-tag" style="--tag-color: var(--accent-cyan)">VXLAN</span>
            <span class="tech-tag" style="--tag-color: var(--accent-cyan)">EVPN</span>
            <span class="tech-tag" style="--tag-color: var(--accent-cyan)">SRv6</span>
            <span class="tech-tag" style="--tag-color: var(--accent-amber)">RoCEv2</span>
            <span class="tech-tag" style="--tag-color: var(--accent-amber)">RDMA</span>
            <span class="tech-tag" style="--tag-color: var(--accent-pink)">Python</span>
            <span class="tech-tag" style="--tag-color: var(--accent-pink)">Netmiko</span>
            <span class="tech-tag" style="--tag-color: var(--accent-pink)">Nornir</span>
            <span class="tech-tag" style="--tag-color: var(--accent-blue)">WSL2</span>
            <span class="tech-tag" style="--tag-color: var(--accent-blue)">Docker</span>
            <span class="tech-tag" style="--tag-color: var(--accent-blue)">Git</span>
        </div>
    </section>

    <section class="about-section reveal">
        <h2><i class="fas fa-paper-plane"></i> 联系方式</h2>
        <div class="contact-links">
            <a href="" target="_blank" class="contact-btn"><i class="fab fa-github"></i> GitHub</a>
            <a href="" target="_blank" class="contact-btn"><i class="fab fa-linkedin"></i> LinkedIn</a>
            <a href="" class="contact-btn"><i class="fas fa-envelope"></i> Email</a>
        </div>
    </section>
</div>

<script>
(function() {
    /* === 获取文章数据 === */
    var dataEl = document.getElementById('postDatesData');
    if (!dataEl) return;
    var raw = JSON.parse(dataEl.textContent || '[]');
    if (!raw.length) return;
    
    var dates = raw.map(function(s) { return s.split('|')[0]; });
    var words = raw.map(function(s) { return parseInt(s.split('|')[1] || '0', 10); });
    var totalWords = words.reduce(function(a,b){return a+b}, 0);
    document.getElementById('totalWords').textContent = totalWords.toLocaleString();
    document.getElementById('firstPostDate').textContent = dates[dates.length - 1];
    
    /* === 构建日期计数 === */
    var counts = {};
    dates.forEach(function(d) { counts[d] = (counts[d] || 0) + 1; });
    
    /* === 确定时间范围（从最早文章到本周日） === */
    var sortedDates = Object.keys(counts).sort();
    var start = new Date(sortedDates[0]);
    var today = new Date();
    
    // 对齐到本周一开始
    var startDay = start.getDay();
    var startMon = new Date(start);
    startMon.setDate(startMon.getDate() - (startDay === 0 ? 6 : startDay - 1));
    
    // 对齐到今天所在周的周日
    var endDay = today.getDay();
    var endSun = new Date(today);
    endSun.setDate(endSun.getDate() + (endDay === 0 ? 0 : 7 - endDay));
    
    /* === 生成月份标签 === */
    var monthsEl = document.getElementById('hmMonths');
    var months = [];
    var cur = new Date(startMon);
    while (cur <= endSun) {
        var m = cur.getMonth();
        if (!months.some(function(x){return x.m === m && x.y === cur.getFullYear()})) {
            // 只记录每个月的首次出现
            months.push({m: m, y: cur.getFullYear(), start: new Date(cur)});
        }
        cur.setDate(cur.getDate() + 7);
    }
    // 计算月份跨度比例
    var totalDays = (endSun - startMon) / (1000 * 60 * 60 * 24);
    monthsEl.innerHTML = '';
    months.forEach(function(mm, i) {
        var span = document.createElement('span');
        var label = ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'][mm.m];
        if (i === 0 || mm.y !== months[i-1].y) label = mm.y + '年' + label;
        span.textContent = label;
        // 计算宽度比例
        var dayOffset = (mm.start - startMon) / (1000 * 60 * 60 * 24);
        var widthPct = (28 / totalDays) * 100;
        // 首个月份按实际剩余空间
        if (i === 0) {
            span.style.marginLeft = '0';
        } else {
            span.style.marginLeft = (dayOffset / totalDays * 100) + '%';
        }
        monthsEl.appendChild(span);
    });
    
    /* === 生成热力网格 === */
    var cellsEl = document.getElementById('hmCells');
    // 计算总周数
    var msPerWeek = 7 * 24 * 60 * 60 * 1000;
    var totalWeeks = Math.ceil((endSun - startMon) / msPerWeek);
    
    // 创建7行 x totalWeeks列 的网格
    var grid = [];
    for (var r = 0; r < 7; r++) {
        grid[r] = [];
        for (var c = 0; c < totalWeeks; c++) {
            grid[r][c] = null;
        }
    }
    
    // 填充日期
    var curDate = new Date(startMon);
    for (var c = 0; c < totalWeeks; c++) {
        for (var r = 0; r < 7; r++) {
            if (curDate > endSun) break;
            var dateStr = curDate.getFullYear() + '-' + 
                String(curDate.getMonth() + 1).padStart(2, '0') + '-' + 
                String(curDate.getDate()).padStart(2, '0');
            var count = counts[dateStr] || 0;
            grid[r][c] = { date: dateStr, count: count };
            curDate.setDate(curDate.getDate() + 1);
        }
    }
    
    // 最大计数
    var maxCount = Math.max.apply(null, Object.values(counts));
    
    // 渲染单元格
    cellsEl.innerHTML = '';
    for (var c = 0; c < totalWeeks; c++) {
        for (var r = 0; r < 7; r++) {
            var cell = document.createElement('div');
            cell.className = 'hm-cell';
            if (grid[r][c]) {
                var level = 0;
                if (grid[r][c].count > 0) {
                    level = Math.min(4, Math.ceil(grid[r][c].count / Math.max(1, maxCount) * 4));
                }
                cell.classList.add('hm-lv' + level);
                cell.title = grid[r][c].date + ' · ' + grid[r][c].count + ' 篇文章';
            } else {
                cell.classList.add('hm-lv0');
            }
            cellsEl.appendChild(cell);
        }
    }
})();
</script>