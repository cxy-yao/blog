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
            <a href="{{ site.github_url }}" target="_blank" class="contact-btn"><i class="fab fa-github"></i> GitHub</a>
            <a href="https://www.linkedin.com/in/chenchulin/" target="_blank" class="contact-btn"><i class="fab fa-linkedin"></i> LinkedIn</a>
            <a href="mailto:{{ site.email | default: 'chenchulin@example.com' }}" class="contact-btn"><i class="fas fa-envelope"></i> Email</a>
        </div>
    </section>
</div>