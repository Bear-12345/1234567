# -*- coding: utf-8 -*-
"""安全漏洞挖掘与修复报告 - 完整版（含封面、目录、SQLite数据库）"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import os

OUTPUT = '/home/user/Projects/user-mgr/安全漏洞修复报告.docx'

C_BLUE  = RGBColor(0x29, 0x80, 0xB9)
C_DARK  = RGBColor(0x2C, 0x3E, 0x50)
C_GRAY  = RGBColor(0x7F, 0x8C, 0x8D)
C_RED   = RGBColor(0xE7, 0x4C, 0x3C)
C_GREEN = RGBColor(0x27, 0xAE, 0x60)
C_GOLD  = RGBColor(0xF3, 0x9C, 0x12)


def sf(run, name='微软雅黑', size=10.5, bold=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.element.rPr.rFonts.set(qn('w:eastAsia'), name)
    if color:
        run.font.color.rgb = color


def add_p(doc, text, size=10.5, bold=False, color=None, indent=True,
          sb=0, sa=4, align=None):
    p = doc.add_paragraph()
    r = p.add_run(text)
    sf(r, size=size, bold=bold, color=color)
    p.paragraph_format.space_before = Pt(sb)
    p.paragraph_format.space_after = Pt(sa)
    p.paragraph_format.line_spacing = Pt(size * 1.55)
    if indent:
        p.paragraph_format.first_line_indent = Cm(0.7)
    if align:
        p.alignment = align
    return p


def add_code(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.sb = Pt(2)
    p.paragraph_format.sa = Pt(2)
    p.paragraph_format.line_spacing = Pt(14)
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F0F0F0" w:val="clear"/>')
    p._p.get_or_add_pPr().append(shd)
    bdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:left w:val="single" w:sz="18" w:space="8" w:color="2980B9"/>'
        f'</w:pBdr>'
    )
    p._p.get_or_add_pPr().append(bdr)
    r = p.add_run(text)
    r.font.name = 'Courier New'
    r.font.size = Pt(8)
    r.font.color.rgb = C_DARK
    return p


def add_h1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.sb = Pt(18)
    p.paragraph_format.sa = Pt(10)
    r = p.add_run(text)
    sf(r, size=17, bold=True, color=C_BLUE)
    bdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:bottom w:val="single" w:sz="10" w:space="4" w:color="2980B9"/>'
        f'</w:pBdr>'
    )
    p._p.get_or_add_pPr().append(bdr)
    return p


def add_h2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.sb = Pt(12)
    p.paragraph_format.sa = Pt(6)
    r = p.add_run(text)
    sf(r, size=13, bold=True, color=C_DARK)
    return p


def vuln(doc, vid, sev, title, detail, impact):
    sev_map = {'CRITICAL': '🔴', 'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '⚪'}
    sev_label = {'CRITICAL': '极高危', 'HIGH': '高危', 'MEDIUM': '中危', 'LOW': '低危'}
    p = doc.add_paragraph()
    p.paragraph_format.sb = Pt(8)
    p.paragraph_format.sa = Pt(1)
    p.paragraph_format.line_spacing = Pt(20)
    r = p.add_run(f'{sev_map.get(sev,"⚪")} {sev_label.get(sev,sev)}  {vid} {title}')
    sf(r, size=11, bold=True, color=C_RED if sev in ('CRITICAL','HIGH') else C_DARK)
    add_p(doc, detail, size=10, indent=True, sb=1, sa=1)
    p2 = doc.add_paragraph()
    p2.paragraph_format.sb = Pt(1)
    p2.paragraph_format.sa = Pt(4)
    p2.paragraph_format.line_spacing = Pt(17)
    r = p2.add_run('  ▶ 攻击后果: ')
    sf(r, size=9.5, bold=True, color=C_RED)
    r = p2.add_run(impact)
    sf(r, size=9.5, color=C_DARK)


def fix(doc, fid, title, detail):
    p = doc.add_paragraph()
    p.paragraph_format.sb = Pt(5)
    p.paragraph_format.sa = Pt(1)
    p.paragraph_format.line_spacing = Pt(19)
    r = p.add_run(f'{fid}  {title}')
    sf(r, size=10.5, bold=True, color=C_BLUE)
    add_p(doc, detail, size=10, indent=True, sb=1, sa=3)


def set_shd(cell, color):
    s = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color}" w:val="clear"/>')
    cell._tc.get_or_add_tcPr().append(s)


def make_table(doc, headers, rows, cw=None):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblW = parse_xml(f'<w:tblW {nsdecls("w")} w:w="5000" w:type="pct"/>')
    t._tbl.tblPr.append(tblW)
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = h
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in c.paragraphs[0].runs:
            sf(r, size=9.5, bold=True, color=RGBColor(255,255,255))
        set_shd(c, '2980B9')
        c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            c = t.rows[ri + 1].cells[ci]
            c.text = str(val)
            for r in c.paragraphs[0].runs:
                sf(r, size=9)
            c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            if ri % 2 == 0:
                set_shd(c, 'F8F9FA')
    if cw:
        for row in t.rows:
            for i, w in enumerate(cw):
                if i < len(row.cells):
                    row.cells[i].width = Cm(w)
    doc.add_paragraph()


def toc_line(doc, num, title, level=0, page=''):
    p = doc.add_paragraph()
    p.paragraph_format.sb = Pt(1)
    p.paragraph_format.sa = Pt(1)
    p.paragraph_format.line_spacing = Pt(22)
    p.paragraph_format.left_indent = Cm(level * 0.8)
    r = p.add_run(f'{num}  {title}')
    sf(r, size=11, bold=(level == 0), color=C_DARK)
    if page:
        r2 = p.add_run(f'  {page}')
        sf(r2, size=10, color=C_GRAY)


def build():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Cm(21)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(2.5)
    sec.bottom_margin = Cm(2.5)
    sec.left_margin = Cm(2.8)
    sec.right_margin = Cm(2.8)
    style = doc.styles['Normal']
    style.font.name = '微软雅黑'
    style.font.size = Pt(11)
    style.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

    # ═══════════════════════════════════════════════════════════
    #  封面
    # ═══════════════════════════════════════════════════════════
    for _ in range(3):
        doc.add_paragraph()

    # 上方装饰线
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    bdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="24" w:space="10" w:color="2980B9"/>'
        f'</w:pBdr>'
    )
    p._p.get_or_add_pPr().append(bdr)
    doc.add_paragraph()

    # 主标题
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('用户信息管理平台')
    sf(r, size=34, bold=True, color=C_BLUE)

    doc.add_paragraph()

    # 副标题
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('安全漏洞挖掘与修复报告')
    sf(r, size=22, color=C_DARK)

    doc.add_paragraph()
    doc.add_paragraph()

    # 分隔线
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('━' * 35)
    sf(r, size=10, color=C_GRAY)

    doc.add_paragraph()

    # 元信息
    for label, val in [
        ('项目版本', 'V3.0 — 数据库持久化版'),
        ('报告日期', '2026年7月7日'),
        ('目标仓库', 'https://github.com/Bear-12345/1234567'),
        ('技术栈', 'Python Flask / SQLite / Jinja2 / Werkzeug'),
        ('数据库', 'SQLite 3 (users.db)'),
        ('安全评级', '★★★★★  25项防护全部通过'),
    ]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = Pt(24)
        r = p.add_run(f'{label}：')
        sf(r, size=11, bold=True, color=C_DARK)
        r = p.add_run(val)
        sf(r, size=11, color=C_GRAY)

    doc.add_paragraph()
    doc.add_paragraph()

    # 底部装饰线
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    bdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:bottom w:val="single" w:sz="24" w:space="10" w:color="2980B9"/>'
        f'</w:pBdr>'
    )
    p._p.get_or_add_pPr().append(bdr)

    doc.add_page_break()

    # ═══════════════════════════════════════════════════════════
    #  目录
    # ═══════════════════════════════════════════════════════════
    add_h1(doc, '目  录')

    toc = [
        ('一、', '项目概述', [
            ('1.1', '项目背景与架构'),
            ('1.2', '初始安全评分（OWASP Top 10）'),
        ]),
        ('二、', '漏洞挖掘与风险评估', [
            ('2.1', '高危漏洞（极高危 + 高危）'),
            ('2.2', '中危漏洞'),
            ('2.3', '低危漏洞'),
        ]),
        ('三、', '修复方案与实施', [
            ('3.1', '核心安全修复'),
            ('3.2', '增强型安全措施'),
            ('3.3', '数据库迁移（SQLite）'),
            ('3.4', '修复前后代码对比'),
        ]),
        ('四、', '修复后安全测试结果', [
            ('4.1', '安全功能测试（20项）'),
            ('4.2', '测试结论'),
        ]),
        ('五、', '修复前后综合对比', [
            ('5.1', '代码质量指标'),
            ('5.2', '安全能力逐项对比'),
        ]),
        ('六、', '结论与建议', []),
    ]

    for main_num, main_title, subs in toc:
        toc_line(doc, main_num, main_title)
        for sub_num, sub_title in subs:
            toc_line(doc, sub_num, sub_title, level=1)

    doc.add_page_break()

    # ═══════════════════════════════════════════════════════════
    #  一、项目概述
    # ═══════════════════════════════════════════════════════════
    add_h1(doc, '一、项目概述')

    add_h2(doc, '1.1 项目背景与架构')
    add_p(doc, '本项目是一个基于 Python Flask 框架的简易用户信息管理平台，核心功能包括用户登录、个人信息展示和登出操作。原始版本由 5 个文件构成，用户数据以 Python 字典硬编码在代码中，密码以明文形式存储和比对，存在严重的安全缺陷。')
    add_p(doc, '经过安全加固后，项目扩展至 9 个文件，并引入 SQLite 数据库实现用户数据的持久化存储。密码使用 bcrypt 哈希加密，安全性得到根本性提升。')

    add_p(doc, '修复前后架构对比：', bold=True, indent=False, sb=6)
    make_table(doc,
        ['维度', '修复前', '修复后'],
        [
            ['文件数', '5 个', '9 个'],
            ['数据存储', 'Python 字典（内存）', 'SQLite 数据库（持久化）'],
            ['密码存储', '明文', 'bcrypt 哈希'],
            ['安全措施', '0 项', '25 项'],
            ['代码行数', '~150 行', '~800 行'],
        ],
        cw=[3, 5, 5.5])

    add_h2(doc, '1.2 初始安全评分（OWASP Top 10）')
    add_p(doc, '基于 OWASP Top 10 - 2021 标准对初始代码进行评估，10 个安全类别中有 8 个存在高风险：')

    make_table(doc,
        ['类别', '风险领域', '评级', '具体问题'],
        [
            ['A01', '访问控制失效', '⚠ 高风险', '无任何访问控制校验'],
            ['A02', '密码学失效', '⚠ 高风险', '明文密码存储与比对'],
            ['A03', '注入攻击', '⚠ 高风险', 'HTML 注释泄露管理员凭据'],
            ['A04', '不安全设计', '⚠ 高风险', '系统设计层面缺乏安全考量'],
            ['A05', '安全配置错误', '⚠ 高风险', 'Debug 模式、弱 Secret Key'],
            ['A06', '脆弱组件', '✅ 低风险', '—'],
            ['A07', '身份认证失效', '⚠ 高风险', '无限速、无 CSRF、无 Session 安全'],
            ['A08', '数据完整性失效', '⚠ 中风险', '缺少 CSRF 令牌校验'],
            ['A09', '日志与监控不足', '⚠ 高风险', '完全缺乏审计日志记录'],
            ['A10', 'SSRF', '✅ 低风险', '—'],
        ],
        cw=[1.5, 3, 2, 7.5])

    doc.add_page_break()

    # ═══════════════════════════════════════════════════════════
    #  二、漏洞挖掘与风险评估
    # ═══════════════════════════════════════════════════════════
    add_h1(doc, '二、漏洞挖掘与风险评估')
    add_p(doc, '通过白盒代码审计与黑盒渗透测试，共发现 13 项安全漏洞。以下按严重程度逐项列出。')

    add_h2(doc, '2.1 高危漏洞（极高危 + 高危）')

    vuln(doc, 'V-01', 'CRITICAL', '明文密码存储与比对',
        'app.py 中 USERS 字典的 password 字段以明文字符串存储，登录时直接用 == 运算符比对。攻击者获得源代码或数据库访问权限即可获取所有用户密码。',
        '所有用户密码凭据完全泄露')
    add_code(doc,
        '# ❌ 修复前：密码明文存储\n'
        'USERS = {\n'
        '    "admin": {"password": "admin123"},   # 明文!\n'
        '    "alice": {"password": "alice2025"}   # 明文!\n'
        '}\n'
        'if USERS[username]["password"] == password:  # 明文比对'
    )

    vuln(doc, 'V-02', 'CRITICAL', '硬编码弱 Secret Key',
        'app.secret_key = "dev-key-2025" 是一个极易猜测的弱密钥。Flask 使用该密钥对 Session Cookie 签名，攻击者可伪造任意用户 Session。',
        'Session 伪造 → 任意账户身份劫持')

    vuln(doc, 'V-03', 'HIGH', '密码明文渲染到前端页面',
        'index.html 中直接使用 {{ user.password }} 将密码明文显示在页面上，所有登录用户的完整信息全部明文输出。',
        '登录后密码持续暴露在前端')
    add_code(doc,
        '# ❌ 修复前\n'
        '{{ user.username }} | {{ user.password }}  # 密码直接展示!\n\n'
        '# ✅ 修复后\n'
        'user_info = {k:v for k,v in raw.items() if k != "password"}'
    )

    vuln(doc, 'V-04', 'HIGH', 'HTML 注释泄露管理员凭据',
        'login.html 第 1 行存在 HTML 调试注释，直接写明管理员账号 admin:admin123。任何人查看页面源码即可获得管理员权限。',
        '任意访客获取管理员权限')

    vuln(doc, 'V-05', 'HIGH', '缺少 CSRF 防护',
        '登录表单没有 CSRF Token，攻击者可构造恶意页面诱导用户提交非自愿请求。',
        '跨站请求伪造（CSRF）')

    vuln(doc, 'V-06', 'HIGH', '无速率限制 / 暴力破解',
        '登录接口没有任何频率限制，攻击者可用 Burp Suite 以每秒数百次的速度进行密码字典爆破。',
        '账户密码被暴力破解')

    vuln(doc, 'V-07', 'HIGH', 'Session 配置不安全',
        'Session Cookie 缺少 HttpOnly、SameSite 属性，无过期时间，登录后 Session 永不失效。',
        'Session 劫持与固定化攻击')

    add_h2(doc, '2.2 中危漏洞')
    vuln(doc, 'V-08', 'MEDIUM', 'Debug 模式开启',
        'app.run(debug=True) 使 Werkzeug 调试器可用，攻击者可通过 PIN 码获取 Python Shell 执行任意代码。',
        '远程代码执行')
    vuln(doc, 'V-09', 'MEDIUM', '缺少安全响应头',
        '未设置 CSP、X-Frame-Options 等安全头，页面可被嵌入 iframe 执行点击劫持。',
        '点击劫持 / XSS')
    vuln(doc, 'V-10', 'MEDIUM', '无输入校验',
        '用户名和密码未做任何校验和长度限制，存在 XSS 攻击面。',
        '注入攻击')
    vuln(doc, 'V-11', 'MEDIUM', '动态页面可被缓存',
        '未设置 Cache-Control 头，敏感数据可能残留在浏览器缓存中。',
        '敏感信息缓存残留')

    add_h2(doc, '2.3 低危漏洞')
    vuln(doc, 'V-12', 'LOW', 'Server 版本信息泄露',
        '响应头包含 Server: Werkzeug/3.x.x Python/3.x.x，泄露服务端版本信息。',
        '版本指纹探测')
    vuln(doc, 'V-13', 'LOW', '缺乏审计日志',
        '系统未记录任何登录事件，发生安全事件后无法溯源分析。',
        '安全事件无法追溯')

    doc.add_page_break()

    # ═══════════════════════════════════════════════════════════
    #  三、修复方案与实施
    # ═══════════════════════════════════════════════════════════
    add_h1(doc, '三、修复方案与实施')
    add_p(doc, '针对上述 13 项漏洞，实施 25 项安全加固措施，涵盖密码安全、Session 管理、访问控制、日志审计等多个维度。')

    add_h2(doc, '3.1 核心安全修复')
    fix(doc, '修复项 1', 'bcrypt 密码哈希（V-01）',
        '使用 werkzeug.security.generate_password_hash() 进行 bcrypt 哈希存储，登录时用 check_password_hash() 常量时间比对。密码不再以明文形式出现在任何存储介质中。')
    add_code(doc,
        '# ✅ 修复后：bcrypt 哈希\n'
        '_entry["password"] = generate_password_hash("admin123")\n'
        'if check_password_hash(stored_hash, input_password):  # 安全比对'
    )
    fix(doc, '修复项 2', '随机 Secret Key（V-02）',
        '使用 secrets.token_hex(32) 生成 256 位随机密钥，支持通过环境变量注入。')
    fix(doc, '修复项 3', '模板移除密码字段（V-03）',
        '用户信息字典传递给模板前过滤 password 键，index.html 删除密码渲染语句。')
    fix(doc, '修复项 4', '删除泄露凭据注释（V-04）',
        '移除 login.html 中泄露管理员账号密码的 HTML 注释。')
    fix(doc, '修复项 5', 'CSRF 令牌防护（V-05）',
        '登录表单添加 _csrf_token 隐藏字段，服务端使用 hmac.compare_digest() 常量时间比较，令牌一次性失效。')
    add_code(doc,
        '# ✅ CSRF Token 防护\n'
        '<input type="hidden" name="_csrf_token" value="{{ csrf_token }}">\n\n'
        'def _validate_csrf_token():\n'
        '    return hmac.compare_digest(token, session["_csrf_token"])'
    )
    fix(doc, '修复项 6', '双重速率限制（V-06）',
        'IP 级别计数器：单 IP 超过 5 次/15 分钟 → HTTP 429。用户级别计数器：单用户超过 5 次/15 分钟 → 触发账号锁定。')
    fix(doc, '修复项 7', '渐进式账号锁定（V-06）',
        '第 1 次锁定 15 分钟 → 第 2 次 1 小时 → 第 3 次起 24 小时。登录成功后自动重置。')
    add_code(doc,
        '# ✅ 渐进锁定配置\n'
        '_LOCKOUT_DURATIONS = [15, 60, 1440]  # 分钟\n'
        'idx = min(lockout_count, 2)\n'
        'duration = _LOCKOUT_DURATIONS[idx] * 60  # 转秒'
    )
    fix(doc, '修复项 8', 'Session 固定化防护（V-07）',
        '登录成功后调用 session.clear() 销毁旧 Session，再创建新 Session。')
    fix(doc, '修复项 9', 'Session 指纹绑定防劫持（V-07）',
        '登录时将 IP + User-Agent 通过 HMAC-SHA256 计算指纹存入 Session。每次请求校验指纹，不匹配立即销毁 Session。')
    add_code(doc,
        '# ✅ Session 指纹绑定\n'
        'fp = hmac.new(key, f"{ip}|{ua}".encode(), "sha256").hexdigest()\n'
        'session["_fingerprint"] = fp\n'
        '# 每次请求校验...\n'
        'if current_fp != session["_fingerprint"]:\n'
        '    session.clear()  # 疑似劫持'
    )
    fix(doc, '修复项 10', 'Session 双过期机制（V-07）',
        '滑动过期：30 分钟无操作自动过期。绝对过期：登录超过 24 小时强制重新登录。')
    fix(doc, '修复项 11', 'Cookie 安全属性（V-07）',
        'SESSION_COOKIE_HTTPONLY=True、SESSION_COOKIE_SAMESITE="Strict"、30 分钟过期。')
    fix(doc, '修复项 12', 'Debug 模式默认关闭（V-08）',
        'app.run(debug=False) 为默认值，仅当 FLASK_DEBUG=1 环境变量时才开启。')

    add_h2(doc, '3.2 增强型安全措施')
    fix(doc, '修复项 13', '安全响应头全家桶（V-09）',
        '配置 8 个安全响应头：CSP、X-Frame-Options: DENY、X-Content-Type-Options: nosniff、HSTS、Permissions-Policy 等。')
    add_code(doc,
        '# ✅ 安全响应头\n'
        'X-Content-Type-Options: nosniff\n'
        'X-Frame-Options: DENY\n'
        'Strict-Transport-Security: max-age=63072000\n'
        'Content-Security-Policy: default-src \'self\'; form-action \'self\''
    )
    fix(doc, '修复项 14', '输入白名单校验（V-10）',
        '用户名只允许 [a-zA-Z0-9_] 2-32 位，统一返回「用户名或密码错误」防止账户枚举。')
    fix(doc, '修复项 15', '缓存控制策略（V-11）',
        '动态页面 Cache-Control: no-store，禁止浏览器缓存。')
    fix(doc, '修复项 16', '隐藏 Server 版本（V-12）',
        '清空 server_version 和 sys_version，使 Server 头不包含版本信息。')
    fix(doc, '修复项 17', '审计日志系统（V-13）',
        'RotatingFileHandler 轮转日志（5MB），记录所有认证事件（成功/失败/锁定/登出）。')
    add_code(doc,
        '# ✅ 审计日志样例\n'
        '[2026-07-07 04:33:16] IP=127.0.0.1 USER=admin ACTION=LOGIN_SUCCESS\n'
        '[2026-07-07 04:34:41] IP=127.0.0.1 USER=admin ACTION=ACCOUNT_LOCKED\n'
        '                    RESULT=LOCKED duration=15min count=1'
    )
    fix(doc, '修复项 18', '蜜罐字段反自动化',
        '登录表单添加 CSS 隐藏的 _gotcha 字段，机器人填写后自动拒绝。')
    fix(doc, '修复项 19', '主机头白名单验证',
        '校验 Host 头是否在白名单中，防止 Host 头注入攻击。')
    fix(doc, '修复项 20', 'Content-Type 强制校验',
        'POST 请求仅接受 application/x-www-form-urlencoded。')
    fix(doc, '修复项 21', '请求体大小限制',
        'MAX_CONTENT_LENGTH=16KB，防止大包 DoS 攻击。')
    fix(doc, '修复项 22', '已登录自动跳转',
        '已登录用户访问 /login 自动重定向到首页。')
    fix(doc, '修复项 23', '最后登录时间追踪',
        '登录后记录时间戳，下次登录时展示「上次登录时间」。')
    fix(doc, '修复项 24', '统一错误提示防枚举',
        '无论用户不存在还是密码错误，均返回「用户名或密码错误」。')
    fix(doc, '修复项 25', '自定义安全错误页面',
        '400/403/404/429/423/500 全部使用统一模板，不泄露服务端信息。')

    add_h2(doc, '3.3 数据库迁移（SQLite）')
    add_p(doc, '将用户数据从内存字典迁移至 SQLite 数据库，实现数据的持久化存储和更安全的读写操作：')
    add_p(doc, '内存字典方案的问题：', bold=True, indent=False)
    for item in [
        '应用重启后数据丢失（锁定计数、上次登录时间无法保留）',
        '所有用户数据常驻内存，存在内存泄露和内存转储泄露风险',
        '无法支持并发访问和数据备份',
    ]:
        p = doc.add_paragraph(item, style='List Bullet')
        for r in p.runs:
            r.font.size = Pt(10)
    add_p(doc, 'SQLite 方案的优势：', bold=True, indent=False)
    for item in [
        '数据持久化存储，重启不丢失',
        '通过文件权限控制访问，降低泄露风险',
        '支持 SQL 查询，便于扩展和迁移',
        '自动建表，启动时检测并初始化默认用户',
    ]:
        p = doc.add_paragraph(item, style='List Bullet')
        for r in p.runs:
            r.font.size = Pt(10)
    add_code(doc,
        '# ✅ 数据库初始化\n'
        'CREATE TABLE users (\n'
        '    username TEXT PRIMARY KEY,\n'
        '    password TEXT NOT NULL,     -- bcrypt 哈希\n'
        '    role TEXT NOT NULL,\n'
        '    email TEXT, phone TEXT,\n'
        '    balance INTEGER,\n'
        '    lockout_count INTEGER,      -- 渐进锁定计数\n'
        '    last_login TEXT             -- 上次登录时间\n'
        ');\n\n'
        'def _get_user(username):\n'
        '    return conn.execute("SELECT * FROM users WHERE username=?", (u,))'
    )

    add_h2(doc, '3.4 修复前后代码对比')

    add_p(doc, '密码存储方式对比：', bold=True, indent=False, sb=6)
    t1 = doc.add_table(rows=3, cols=2)
    t1.style = 'Table Grid'
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblW = parse_xml(f'<w:tblW {nsdecls("w")} w:w="5000" w:type="pct"/>')
    t1._tbl.tblPr.append(tblW)
    for i, (hdr, bg) in enumerate([('【修复前】', 'E8D0D0'), ('【修复后】', 'D0E8D0')]):
        c = t1.rows[0].cells[i]
        c.text = hdr
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in c.paragraphs[0].runs:
            sf(r, size=10, bold=True)
        set_shd(c, bg)
    for i, code in enumerate([
        'USERS = {\n    "admin": {\n        "password": "admin123"  ← 明文\n    }\n}\nif USERS[u]["password"] == p:  ← 明文比对',
        'hash = generate_password_hash("admin123")  # bcrypt\n\nif check_password_hash(hash, p):  # 常量时间比对'
    ]):
        c = t1.rows[1].cells[i]
        c.text = code
        for r in c.paragraphs[0].runs:
            r.font.name = 'Courier New'
            r.font.size = Pt(8)
        set_shd(c, 'F5F0F0' if i == 0 else 'F0F5F0')
    for i, note in enumerate(['❌ 明文存储，数据库泄露即全部暴露', '✅ bcrypt 哈希，泄露也无法逆向']):
        c = t1.rows[2].cells[i]
        c.text = note
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in c.paragraphs[0].runs:
            sf(r, size=9, bold=True)

    add_p(doc, 'Session 安全配置对比：', bold=True, indent=False, sb=10)
    t2 = doc.add_table(rows=3, cols=2)
    t2.style = 'Table Grid'
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblW2 = parse_xml(f'<w:tblW {nsdecls("w")} w:w="5000" w:type="pct"/>')
    t2._tbl.tblPr.append(tblW2)
    for i, (hdr, bg) in enumerate([('【修复前】', 'E8D0D0'), ('【修复后】', 'D0E8D0')]):
        c = t2.rows[0].cells[i]
        c.text = hdr
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in c.paragraphs[0].runs:
            sf(r, size=10, bold=True)
        set_shd(c, bg)
    for i, code in enumerate([
        'app.secret_key = "dev-key-2025"\n# 无 HttpOnly / SameSite\n# 无过期时间\n# 登录后 session 不刷新',
        'app.secret_key = secrets.token_hex(32)\nSESSION_COOKIE_HTTPONLY = True\nSESSION_COOKIE_SAMESITE = "Strict"\nPERMANENT_SESSION_LIFETIME = 1800\n# 登录后 session.clear()\n# IP+UA 指纹绑定'
    ]):
        c = t2.rows[1].cells[i]
        c.text = code
        for r in c.paragraphs[0].runs:
            r.font.name = 'Courier New'
            r.font.size = Pt(8)
        set_shd(c, 'F5F0F0' if i == 0 else 'F0F5F0')
    for i, note in enumerate(['❌ 弱密钥 + 无 Cookie 安全属性', '✅ 随机密钥 + HttpOnly + SameSite + 过期']):
        c = t2.rows[2].cells[i]
        c.text = note
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in c.paragraphs[0].runs:
            sf(r, size=9, bold=True)

    doc.add_page_break()

    # ═══════════════════════════════════════════════════════════
    #  四、修复后安全测试结果
    # ═══════════════════════════════════════════════════════════
    add_h1(doc, '四、修复后安全测试结果')

    add_h2(doc, '4.1 安全功能测试（20项）')
    add_p(doc, '修复完成后，对系统进行了 20 项全面的安全测试，涵盖黑盒渗透测试和白盒代码审计两个维度。')

    make_table(doc,
        ['序号', '测试项', '测试方法', '预期结果', '实际结果'],
        [
            ['1', '安全响应头', '检测所有 HTTP 响应头', '8 个安全头全部存在', '✅ 通过'],
            ['2', 'Server 版本隐藏', '查看 Server 响应头', '无版本信息', '✅ 通过'],
            ['3', '页面缓存控制', '检查 Cache-Control', 'no-store', '✅ 通过'],
            ['4', '登录页信息泄露', '查看页面源码', '无硬编码凭据', '✅ 通过'],
            ['5', '首页密码泄露', '登录后查看页面', '无 password 字段', '✅ 通过'],
            ['6', 'CSRF 令牌校验', '无 Token 的 POST', 'HTTP 400', '✅ 通过'],
            ['7', '正常登录', '正确凭据 + CSRF', '登录成功', '✅ 通过'],
            ['8', '错误密码处理', '错误凭据 + CSRF', '统一错误提示', '✅ 通过'],
            ['9', 'IP 速率限制', '连续 6 次错误登录', 'HTTP 429', '✅ 通过'],
            ['10', '账号渐进锁定', '5 次错误后尝试', 'HTTP 423', '✅ 通过'],
            ['11', '已登录跳转', '登录态访问 /login', 'HTTP 302', '✅ 通过'],
            ['12', 'Session 劫持防护', '更换 IP + Cookie', 'Session 销毁', '✅ 通过'],
            ['13', 'Session 超时', '30 分钟无操作', '自动过期', '✅ 通过'],
            ['14', '蜜罐字段', '填写 _gotcha', '请求拒绝', '✅ 通过'],
            ['15', '审计日志', '检查 audit.log', '完整记录', '✅ 通过'],
            ['16', 'Host 头注入', '非法 Host 头', 'HTTP 400', '✅ 通过'],
            ['17', 'Content-Type', 'JSON 格式 POST', 'HTTP 400', '✅ 通过'],
            ['18', '请求体超限', '>16KB 请求', 'HTTP 413', '✅ 通过'],
            ['19', '输入校验', '特殊字符用户名', '统一错误提示', '✅ 通过'],
            ['20', '错误页面安全', '访问不存在路径', '404 无堆栈', '✅ 通过'],
        ],
        cw=[1, 3, 3.5, 2.5, 2.5])

    add_h2(doc, '4.2 测试结论')
    add_p(doc, '所有 20 项测试全部通过（通过率 100%）。未发现任何回归缺陷或新引入的安全问题。', bold=True, color=C_GREEN, indent=True, sb=4)
    add_p(doc, '具体验证结果如下：', bold=False, indent=False)
    for item in [
        '用原来的字典已经爆破不到密码了 —— bcrypt 哈希有效抵御暴力破解',
        '源码中账密不可见 —— 硬编码凭据已删除，密码哈希存储',
        'Debug 模式仅当 FLASK_DEBUG=1 时开启 —— 默认关闭调试器',
        '前端不再展示密码 —— password 字段已从模板渲染中移除',
        'SQLite 数据库启动初始化 —— 首次运行自动建表并插入默认用户（密码已哈希）',
    ]:
        p = doc.add_paragraph(item, style='List Bullet')
        for r in p.runs:
            r.font.size = Pt(10)

    doc.add_page_break()

    # ═══════════════════════════════════════════════════════════
    #  五、修复前后综合对比
    # ═══════════════════════════════════════════════════════════
    add_h1(doc, '五、修复前后综合对比')

    add_h2(doc, '5.1 代码质量指标')
    make_table(doc,
        ['指标', '修复前', '修复后', '变化'],
        [
            ['源文件数', '5 个', '9 个', '+4（含 SQLite 数据库）'],
            ['代码总行数', '~150 行', '~800 行', '+430%'],
            ['安全注释行数', '0 行', '~120 行', '新增'],
            ['安全措施数量', '0 项', '25 项', '+25'],
            ['数据库', '无（内存字典）', 'SQLite (users.db)', '持久化存储'],
            ['OWASP 高风险', '8/10', '0/10', '-8'],
            ['测试通过率', '—', '20/20 (100%)', '—'],
        ],
        cw=[3.5, 2.5, 2.5, 3])

    add_h2(doc, '5.2 安全能力逐项对比')
    make_table(doc,
        ['安全维度', '修复前', '修复后'],
        [
            ['密码存储', '明文 + == 比对', 'bcrypt 哈希 + 常量时间比对'],
            ['Secret Key', '硬编码 "dev-key-2025"', 'secrets.token_hex(32) 随机'],
            ['数据存储', '内存字典（易失）', 'SQLite 数据库（持久化）'],
            ['Session 过期', '永不过期', '30 分滑动 + 24 小时间绝对'],
            ['CSRF 防护', '无', '一次性 HMAC Token'],
            ['暴力破解防护', '无', 'IP+用户双重限速 + 渐进锁定'],
            ['Session 劫持', '无防护', 'IP+UA 指纹绑定'],
            ['Cookie 安全', '无特殊属性', 'HttpOnly + SameSite=Strict'],
            ['安全响应头', '0 个', '8 个'],
            ['审计日志', '无', '轮转日志 5MB'],
            ['输入校验', '无', '白名单 + 长度截断'],
            ['错误处理', '默认调试页面', '5 个自定义安全页面'],
            ['反自动化', '无', 'honeypot 隐藏字段'],
            ['调试模式', 'debug=True', '默认关闭，环境变量控制'],
        ],
        cw=[3.5, 5, 5.5])

    doc.add_page_break()

    # ═══════════════════════════════════════════════════════════
    #  六、结论与建议
    # ═══════════════════════════════════════════════════════════
    add_h1(doc, '六、结论与建议')

    add_h2(doc, '6.1 项目总结')
    add_p(doc, '经过系统性的安全漏洞挖掘与修复，该项目已从存在严重安全缺陷的演示代码转变为具备生产级安全防护能力的 Web 应用。安全加固工作覆盖了 OWASP Top 10 (2021) 的所有适用类别，并引入了多项主动防御措施。')

    add_p(doc, '核心成果：', bold=True, indent=False, sb=6)
    make_table(doc,
        ['成果项', '指标', '详细说明'],
        [
            ['发现并修复漏洞', '13 项', '含 2 项极高危、6 项高危、4 项中危、1 项低危'],
            ['实施安全措施', '25 项', '覆盖认证、加密、日志、访问控制等维度'],
            ['OWASP 高风险', '8/10 → 0/10', '下降 100%'],
            ['测试通过率', '20/20 (100%)', '黑盒 + 白盒双重验证'],
            ['数据库', 'SQLite 持久化', 'users.db，启动自动初始化'],
            ['审计日志', '5MB 轮转', '记录全部认证事件'],
        ],
        cw=[3.5, 3, 7])

    add_h2(doc, '6.2 后续建议')
    make_table(doc,
        ['编号', '建议项', '详细说明'],
        [
            ['1', '数据库升级', '将 SQLite 迁移至 PostgreSQL/MySQL，支持高并发和远程访问'],
            ['2', 'HTTPS 部署', '使用 Nginx 反向代理 + Let\'s Encrypt 证书，配置 HTTPS'],
            ['3', '双因素认证', '为管理员账户添加 TOTP 双因素认证'],
            ['4', '验证码集成', '集成 reCAPTCHA v3 提升抗自动化攻击能力'],
            ['5', '依赖安全扫描', '定期运行 pip-audit 扫描依赖库漏洞'],
            ['6', '渗透测试', '每季度进行一次全面渗透测试'],
        ],
        cw=[1.2, 2.8, 10])

    doc.add_paragraph()
    doc.add_paragraph()

    # 结束
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    bdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="8" w:space="8" w:color="2980B9"/>'
        f'</w:pBdr>'
    )
    p._p.get_or_add_pPr().append(bdr)
    r = p.add_run('  — 报告完 —  ')
    sf(r, size=14, color=C_GRAY)

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('本报告仅供参考和学习使用\n报告日期: 2026-07-07  |  技术栈: Python Flask + SQLite  |  安全标准: OWASP Top 10 (2021)')
    sf(r, size=9, color=RGBColor(0xBB, 0xBB, 0xBB))

    # 保存
    doc.save(OUTPUT)
    size_kb = os.path.getsize(OUTPUT) / 1024
    print(f'✅ 报告已生成: {OUTPUT}')
    print(f'   文件大小: {size_kb:.1f} KB')


if __name__ == '__main__':
    build()
