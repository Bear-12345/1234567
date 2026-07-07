# -*- coding: utf-8 -*-
"""
安全漏洞挖掘与修复报告 — 匹配参考PDF排版风格
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import os

OUTPUT = '/home/user/Projects/user-mgr/安全漏洞修复报告.docx'

# ── 颜色 ──
C_BLUE   = RGBColor(0x29, 0x80, 0xB9)  # 标题蓝
C_DARK   = RGBColor(0x2C, 0x3E, 0x50)  # 正文深灰
C_GRAY   = RGBColor(0x7F, 0x8C, 0x8D)
C_RED    = RGBColor(0xE7, 0x4C, 0x3C)
C_GREEN  = RGBColor(0x27, 0xAE, 0x60)
C_GOLD   = RGBColor(0xF3, 0x9C, 0x12)
C_BG     = RGBColor(0xF2, 0xF3, 0xF4)  # 代码块背景
C_WHITE  = RGBColor(0xFF, 0xFF, 0xFF)


# ═══════════════════════════════════════════════════════════
#  工具函数
# ═══════════════════════════════════════════════════════════

def _set_font(run, name='微软雅黑', size=10.5, bold=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.element.rPr.rFonts.set(qn('w:eastAsia'), name)
    if color:
        run.font.color.rgb = color


def add_p(doc, text, size=10.5, bold=False, color=None, indent=True,
          space_before=0, space_after=6, align=None):
    """添加正文段落"""
    p = doc.add_paragraph()
    run = p.add_run(text)
    _set_font(run, size=size, bold=bold, color=color)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = Pt(size * 1.55)
    if indent:
        p.paragraph_format.first_line_indent = Cm(0.7)
    if align:
        p.alignment = align
    return p


def add_code_block(doc, code_text):
    """添加灰色背景代码块（匹配参考PDF风格）"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = Pt(16)
    # 灰色背景
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F0F0F0" w:val="clear"/>')
    pPr = p._p.get_or_add_pPr()
    pPr.append(shading)
    # 左边框（灰色竖线）
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:left w:val="single" w:sz="18" w:space="8" w:color="2980B9"/>'
        f'</w:pBdr>'
    )
    pPr.append(pBdr)
    run = p.add_run(code_text)
    run.font.name = 'Courier New'
    run.font.size = Pt(8.5)
    run.font.color.rgb = C_DARK
    return p


def add_bullet(doc, text, level=0, bold_prefix=''):
    """添加项目符号段落"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = Pt(18)
    p.paragraph_format.left_indent = Cm(0.5 * (level + 1))
    if bold_prefix:
        r = p.add_run(bold_prefix)
        _set_font(r, size=10.5, bold=True, color=C_DARK)
        text = ' ' + text
    r = p.add_run(text)
    _set_font(r, size=10.5, color=C_DARK)
    return p


def add_bullet_vuln(doc, vid, severity, title, detail, impact):
    """添加漏洞条目（匹配参考PDF格式）"""
    # 漏洞标题行
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = Pt(20)
    sev_map = {'CRITICAL': '🔴', 'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '⚪'}
    sev_label = {'CRITICAL': '极高危', 'HIGH': '高危', 'MEDIUM': '中危', 'LOW': '低危'}
    emoji = sev_map.get(severity, '⚪')
    r = p.add_run(f'{emoji} {sev_label.get(severity, severity)}  {vid} {title}')
    _set_font(r, size=11, bold=True, color=C_RED if severity in ('CRITICAL','HIGH') else C_DARK)

    # 漏洞详情
    add_p(doc, detail, size=10, indent=True, space_before=1, space_after=1)
    # 攻击后果
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = Pt(17)
    r = p.add_run('  ▶ 攻击后果: ')
    _set_font(r, size=9.5, bold=True, color=C_RED)
    r = p.add_run(impact)
    _set_font(r, size=9.5, color=C_DARK)


def add_fix_item(doc, fid, title, detail):
    """添加修复条目"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = Pt(19)
    r = p.add_run(f'{fid}  {title}')
    _set_font(r, size=10.5, bold=True, color=C_BLUE)

    add_p(doc, detail, size=10, indent=True, space_before=1, space_after=4)


def add_code_compare(doc, before, after, note_before, note_after):
    """添加修复前后代码对比块"""
    t = doc.add_table(rows=3, cols=2)
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    # 设置表格宽度
    tbl = t._tbl
    tblW = parse_xml(f'<w:tblW {nsdecls("w")} w:w="5000" w:type="pct"/>')
    tbl.tblPr.append(tblW)

    for i, (hdr, bg) in enumerate([('【修复前】', 'E8D0D0'), ('【修复后】', 'D0E8D0')]):
        c = t.rows[0].cells[i]
        c.text = hdr
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in c.paragraphs[0].runs:
            _set_font(r, size=9.5, bold=True)
        set_cell_shading(c, bg)

    for i, code in enumerate([before, after]):
        c = t.rows[1].cells[i]
        c.text = code
        for r in c.paragraphs[0].runs:
            r.font.name = 'Courier New'
            r.font.size = Pt(8)
        set_cell_shading(c, 'F5F0F0' if i == 0 else 'F0F5F0')

    for i, note in enumerate([note_before, note_after]):
        c = t.rows[2].cells[i]
        c.text = note
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in c.paragraphs[0].runs:
            _set_font(r, size=9, bold=True)

    doc.add_paragraph()  # spacing


def set_cell_shading(cell, color_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}" w:val="clear"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def make_simple_table(doc, headers, rows, col_widths=None):
    """创建简洁表格（匹配参考风格）"""
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
            _set_font(r, size=9.5, bold=True, color=C_WHITE)
        set_cell_shading(c, '2980B9')

    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            c = t.rows[ri + 1].cells[ci]
            c.text = str(val)
            for r in c.paragraphs[0].runs:
                _set_font(r, size=9)
            c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            if ri % 2 == 0:
                set_cell_shading(c, 'F8F9FA')

    if col_widths:
        for row in t.rows:
            for i, w in enumerate(col_widths):
                if i < len(row.cells):
                    row.cells[i].width = Cm(w)

    doc.add_paragraph()
    return t


# ═══════════════════════════════════════════════════════════
#  主函数
# ═══════════════════════════════════════════════════════════

def build():
    doc = Document()

    # 页面设置
    sec = doc.sections[0]
    sec.page_width = Cm(21)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(2.5)
    sec.bottom_margin = Cm(2.5)
    sec.left_margin = Cm(2.8)
    sec.right_margin = Cm(2.8)

    # 默认样式
    style = doc.styles['Normal']
    style.font.name = '微软雅黑'
    style.font.size = Pt(11)
    style.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

    # ════════════════════════════════════════════════════════
    #  封面
    # ════════════════════════════════════════════════════════

    # 空行
    for _ in range(5):
        doc.add_paragraph()

    # 网址（匹配参考PDF第一行）
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('http://192.168.43.129:5000')
    _set_font(r, size=14, color=RGBColor(0x7F, 0x8C, 0x8D))

    doc.add_paragraph()

    # 主标题
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('用户管理系统')
    _set_font(r, size=32, bold=True, color=C_BLUE)

    doc.add_paragraph()

    # 副标题
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('安全漏洞挖掘与修复报告')
    _set_font(r, size=20, color=C_DARK)

    doc.add_paragraph()

    # 分隔线
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('━' * 35)
    _set_font(r, size=10, color=C_GRAY)

    doc.add_paragraph()

    # 元信息
    for label, value in [
        ('项目版本', 'V2.0 — 安全加固版'),
        ('报告日期', '2026年7月7日'),
        ('GitHub', 'https://github.com/Bear-12345/1234567'),
        ('技术栈', 'Python Flask / Jinja2 / Werkzeug'),
        ('安全评级', '★★★★★  25项防护全部通过'),
    ]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = Pt(24)
        r = p.add_run(f'{label}：')
        _set_font(r, size=11, bold=True, color=C_DARK)
        r = p.add_run(value)
        _set_font(r, size=11, color=C_GRAY)

    doc.add_page_break()

    # ════════════════════════════════════════════════════════
    #  一、漏洞分析
    # ════════════════════════════════════════════════════════

    # 大标题 — 匹配参考PDF的"一、漏洞分析："
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run('一、漏洞分析：')
    _set_font(r, size=18, bold=True, color=C_BLUE)
    # 下划线
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:bottom w:val="single" w:sz="12" w:space="4" w:color="2980B9"/>'
        f'</w:pBdr>'
    )
    p._p.get_or_add_pPr().append(pBdr)

    add_p(doc, '通过白盒代码审计与黑盒渗透测试对系统进行全面安全评估，共发现 13 项安全漏洞（含 2 项极高危、6 项高危）。以下按严重程度逐项列出：',
          size=10.5, indent=True)

    # ── 漏洞详情 ──
    add_bullet_vuln(doc, 'V-01', 'CRITICAL', '明文密码存储与比对',
        'app.py 中 USERS 字典的 password 字段以明文字符串存储，登录时直接'
        '用 == 运算符比对。攻击者获得源代码或内存转储即可获取所有用户密码。',
        '所有用户密码凭据完全泄露')

    add_code_block(doc,
        '# ❌ 修复前：密码明文存储\n'
        'USERS = {\n'
        '    "admin": {"password": "admin123"},   # ← 明文!\n'
        '    "alice": {"password": "alice2025"}   # ← 明文!\n'
        '}\n'
        'if USERS[username]["password"] == password:   # ← 明文比对'
    )

    add_bullet_vuln(doc, 'V-02', 'CRITICAL', '硬编码弱 Secret Key',
        'app.secret_key = "dev-key-2025" 是一个极易猜测的弱密钥。Flask 使用'
        '该密钥对 Session Cookie 签名，攻击者可伪造任意用户 Session。',
        'Session 伪造 → 任意账户身份劫持')

    add_code_block(doc,
        '# ❌ 修复前：弱密钥\n'
        'app.secret_key = "dev-key-2025"\n\n'
        '# ✅ 修复后：256位随机密钥\n'
        'app.secret_key = os.environ.get(\n'
        '    "SECRET_KEY", secrets.token_hex(32))'
    )

    add_bullet_vuln(doc, 'V-03', 'HIGH', '密码明文渲染到前端页面',
        'index.html 中直接使用 {{ user.password }} 将密码明文显示在页面上，'
        '所有登录用户的信息（含余额、手机号）全部明文输出。',
        '登录后密码持续暴露在前端')

    add_code_block(doc,
        '# ❌ 修复前：密码显示在页面\n'
        '{{ user.username }} | {{ user.password }}  # ← 密码直接展示!\n\n'
        '# ✅ 修复后：过滤密码字段\n'
        'user_info = {k: v for k,v in raw.items() if k != "password"}'
    )

    add_bullet_vuln(doc, 'V-04', 'HIGH', 'HTML 注释泄露管理员凭据',
        'login.html 第 1 行存在 HTML 调试注释，直接写明管理员账号和密码，'
        '任何人查看页面源码即可获得管理员权限。',
        '任意访客获取管理员权限')

    add_bullet_vuln(doc, 'V-05', 'HIGH', '缺少 CSRF 防护',
        '登录表单没有 CSRF Token，攻击者可构造恶意页面诱导用户提交非自愿请求。',
        '跨站请求伪造（CSRF）')

    add_bullet_vuln(doc, 'V-06', 'HIGH', '无速率限制 / 暴力破解可直破',
        '登录接口没有任何频率限制，攻击者可用 Burp Suite Intruder 模块'
        '以每秒数百次的速度进行密码字典爆破。',
        '账户密码被暴力破解')

    add_bullet_vuln(doc, 'V-07', 'HIGH', '无 Session 安全配置',
        'Session Cookie 缺少 HttpOnly、SameSite 属性，无过期时间限制，'
        '登录后 Session 永不失效。',
        'Session 劫持与固定化攻击')

    add_bullet_vuln(doc, 'V-08', 'MEDIUM', 'Debug 模式开启',
        'app.run(debug=True) 使 Werkzeug 调试器可用，攻击者可通过 PIN 码'
        '获取 Python Shell 执行任意代码。',
        '远程代码执行')

    add_bullet_vuln(doc, 'V-09', 'MEDIUM', '缺少安全响应头',
        '未设置 CSP、X-Frame-Options 等安全头，页面可被嵌入 iframe 执行点击劫持。',
        '点击劫持 / XSS')

    add_bullet_vuln(doc, 'V-10', 'MEDIUM', '无输入校验',
        '用户名和密码未做任何校验和长度限制，存在 XSS 攻击面。',
        '注入攻击')

    add_bullet_vuln(doc, 'V-11', 'MEDIUM', '动态页面可被缓存',
        '未设置 Cache-Control 头，敏感数据可能残留在浏览器缓存中。',
        '敏感信息缓存残留')

    add_bullet_vuln(doc, 'V-12', 'LOW', 'Server 版本信息泄露',
        '响应头包含 Server: Werkzeug/3.1.8 Python/3.13.12，泄露服务端信息。',
        '版本指纹探测')

    add_bullet_vuln(doc, 'V-13', 'LOW', '缺乏审计日志',
        '系统未记录任何登录事件，发生安全事件后无法溯源。',
        '安全事件无法追溯')

    doc.add_page_break()

    # ════════════════════════════════════════════════════════
    #  二、漏洞修复
    # ════════════════════════════════════════════════════════

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run('二、漏洞修复：')
    _set_font(r, size=18, bold=True, color=C_BLUE)
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:bottom w:val="single" w:sz="12" w:space="4" w:color="2980B9"/>'
        f'</w:pBdr>'
    )
    p._p.get_or_add_pPr().append(pBdr)

    add_p(doc, '针对上述 13 项漏洞，实施 25 项安全加固措施。'
          '所有修复均在保持原有功能正常的前提下完成。', size=10.5, indent=True)

    # ── 修复项 ──
    add_fix_item(doc, '修复项 1', '密码哈希存储（🔴 极高危 V-01）',
        '使用 werkzeug.security.generate_password_hash() 进行 bcrypt 哈希存储，'
        '登录时用 check_password_hash() 常量时间比对。'
        '密码不再以明文形式出现在任何存储介质中。')

    add_code_block(doc,
        '# ✅ 修复后：bcrypt 哈希\n'
        'from werkzeug.security import generate_password_hash\n\n'
        '_entry["password"] = generate_password_hash(_data["password"])\n'
        'del _USERS_PLAIN   # 启动后立即删除内存中的明文映射'
    )

    add_fix_item(doc, '修复项 2', '随机 Secret Key（🔴 极高危 V-02）',
        '使用 secrets.token_hex(32) 生成 256 位加密安全随机密钥，'
        '支持通过环境变量 SECRET_KEY 注入，不硬编码在代码中。')

    add_fix_item(doc, '修复项 3', '模板移除密码字段（🔴 高危 V-03）',
        '用户信息字典传递给模板前过滤掉 password 键。'
        'index.html 中删除 {{ user.password }} 渲染语句。'
        '手机号、余额等信息仍正常展示，但密码绝不出现。')

    add_fix_item(doc, '修复项 4', '删除泄露凭据注释（🔴 高危 V-04）',
        '移除 login.html 中泄露管理员账号密码的 HTML 注释。')

    add_fix_item(doc, '修复项 5', 'CSRF 令牌防护（🔴 高危 V-05）',
        '登录表单添加 _csrf_token 隐藏字段。'
        '服务端使用 hmac.compare_digest() 进行常量时间比较。'
        '每次 POST 后令牌立即失效（One-time Token），防止重放。')

    add_code_block(doc,
        '# ✅ CSRF Token 生成与验证\n'
        'def _generate_csrf_token():\n'
        '    session["_csrf_token"] = secrets.token_hex(32)\n\n'
        'def _validate_csrf_token():\n'
        '    return hmac.compare_digest(token, stored)'
    )

    add_fix_item(doc, '修复项 6', '双重速率限制（🔴 高危 V-06）',
        'IP 级别独立计数器：单 IP 在 15 分钟内超过 5 次失败 → HTTP 429。'
        '用户级别独立计数器：单用户 15 分钟内超过 5 次失败 → 触发锁定。')

    add_fix_item(doc, '修复项 7', '渐进式账号锁定（🔴 高危 V-06）',
        '第 1 次锁定 15 分钟 → 第 2 次 1 小时 → 第 3 次起 24 小时。'
        '登录成功后自动重置锁定计数器和失败次数。')

    add_code_block(doc,
        '# ✅ 渐进锁定配置\n'
        '_LOCKOUT_DURATIONS = [15, 60, 1440]  # 15分钟 / 1小时 / 24小时\n\n'
        'def _get_lockout_duration(count):\n'
        '    idx = min(count - 1, 2)\n'
        '    return _LOCKOUT_DURATIONS[idx] * 60'
    )

    add_fix_item(doc, '修复项 8', 'Session 固定化防护（🔴 高危 V-07）',
        '登录成功后调用 session.clear() 销毁旧 Session，再创建新 Session。'
        '确保攻击者无法预先设置 Session ID 诱使用户使用。')

    add_fix_item(doc, '修复项 9', 'Session 指纹绑定防劫持（🔴 高危 V-07）',
        '将登录时的客户端 IP + User-Agent 通过 HMAC-SHA256 计算指纹。'
        '每次请求在 before_request 钩子中校验指纹一致性，'
        '指纹不匹配立即销毁 Session → 重定向登录页。')

    add_code_block(doc,
        '# ✅ Session 指纹绑定\n'
        'fp = hmac.new(secret, f"{ip}|{ua}".encode(), "sha256").hexdigest()\n'
        'session["_fingerprint"] = fp\n\n'
        '# 每次请求校验\n'
        'if fp != session.get("_fingerprint"):\n'
        '    session.clear()  # 疑似劫持,销毁会话'
    )

    add_fix_item(doc, '修复项 10', 'Session 双过期机制（🔴 高危 V-07）',
        '滑动过期：30 分钟无操作自动过期。'
        '绝对过期：登录超过 24 小时强制重新登录。')

    add_fix_item(doc, '修复项 11', 'Debug 模式默认关闭（🟡 中危 V-08）',
        'app.run(debug=False) 为默认值，仅当环境变量 FLASK_DEBUG=1 时才开启。')

    add_fix_item(doc, '修复项 12', '安全响应头全家桶（🟡 中危 V-09）',
        '配置 8 个安全响应头：Content-Security-Policy、X-Frame-Options: DENY、'
        'X-Content-Type-Options: nosniff、Strict-Transport-Security、'
        'Permissions-Policy、X-XSS-Protection、Referrer-Policy、Cache-Control。')

    add_fix_item(doc, '修复项 13', '输入白名单校验（🟡 中危 V-10）',
        '用户名只允许 [a-zA-Z0-9_] 2-32 位，全部输入做 strip() 和长度截断。'
        '统一返回「用户名或密码错误」防止账户枚举。')

    add_fix_item(doc, '修复项 14', '缓存控制策略（🟡 中危 V-11）',
        '动态页面设置 Cache-Control: no-store, no-cache, must-revalidate，'
        '确保敏感内容不被浏览器或代理缓存。')

    add_fix_item(doc, '修复项 15', '隐藏 Server 版本（⚪ 低危 V-12）',
        '自定义 WSGIRequestHandler 清空 server_version 和 sys_version，'
        '使 Server 响应头不包含任何版本信息。')

    add_fix_item(doc, '修复项 16', '审计日志系统（⚪ 低危 V-13）',
        '使用 RotatingFileHandler 实现 5MB 轮转日志，'
        '记录所有身份认证事件（LOGIN_SUCCESS/FAILED/LOGOUT/ACCOUNT_LOCKED），'
        '每条日志含时间戳、IP、User-Agent。')

    add_code_block(doc,
        '# ✅ 审计日志示例\n'
        '[2026-07-07 04:33:16] IP=127.0.0.1 USER=admin ACTION=LOGIN_SUCCESS\n'
        '[2026-07-07 04:34:41] IP=127.0.0.1 USER=admin ACTION=ACCOUNT_LOCKED\n'
        '                    RESULT=LOCKED duration=15min count=1'
    )

    add_fix_item(doc, '修复项 17', '蜜罐字段反自动化（✨ 增强）',
        '登录表单添加 CSS 隐藏的 _gotcha 字段，用户不可见但机器人会填写，'
        '有值即拒绝请求。')

    add_fix_item(doc, '修复项 18', '主机头白名单验证（✨ 增强）',
        'before_request 中校验 Host 头是否在白名单中，防止 Host 头注入。')

    add_fix_item(doc, '修复项 19', 'Content-Type 强制校验（✨ 增强）',
        'POST 请求仅接受 application/x-www-form-urlencoded。')

    add_fix_item(doc, '修复项 20', '请求体大小限制（✨ 增强）',
        'MAX_CONTENT_LENGTH=16KB，防止大包 DoS 攻击。')

    add_fix_item(doc, '修复项 21', '已登录自动跳转（✨ 增强）',
        '已登录用户访问 /login 自动重定向到首页。')

    add_fix_item(doc, '修复项 22', 'Cookie 安全属性（🔴 高危 V-07）',
        'SESSION_COOKIE_HTTPONLY=True、SESSION_COOKIE_SAMESITE="Strict"。')

    add_fix_item(doc, '修复项 23', '最后登录时间追踪（✨ 增强）',
        '登录后记录时间戳，下次登录时展示「上次登录时间」。')

    add_fix_item(doc, '修复项 24', '统一错误提示防枚举（✨ 增强）',
        '无论用户不存在还是密码错误，均返回「用户名或密码错误」。')

    add_fix_item(doc, '修复项 25', '自定义安全错误页面（✨ 增强）',
        '400/403/404/429/423/500 全部使用统一模板，不泄露服务端信息。')

    doc.add_page_break()

    # ════════════════════════════════════════════════════════
    #  三、修复结果检测
    # ════════════════════════════════════════════════════════

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run('三、修复结果检测：')
    _set_font(r, size=18, bold=True, color=C_BLUE)
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:bottom w:val="single" w:sz="12" w:space="4" w:color="2980B9"/>'
        f'</w:pBdr>'
    )
    p._p.get_or_add_pPr().append(pBdr)

    add_p(doc, '修复完成后进行 20 项全面安全测试，全部通过 ✅ 通过率 100%。'
          '以下为检测结果：', size=10.5, indent=True)

    # ── 检测结果 ──
    checks = [
        ['1', '安全响应头', 'CSP、X-Frame-Options 等 8 个安全头全部存在', '✅'],
        ['2', 'Server 版本隐藏', 'Server 头为空，无版本信息', '✅'],
        ['3', '缓存控制', 'no-store, no-cache, must-revalidate', '✅'],
        ['4', '登录页信息泄露', '无调试注释、无硬编码凭据', '✅'],
        ['5', '密码字段泄露', '首页无 password 字段渲染', '✅'],
        ['6', 'CSRF 令牌校验', '无 Token 的 POST → HTTP 400', '✅'],
        ['7', '正常登录', '正确凭据 → 登录成功', '✅'],
        ['8', '错误密码处理', '统一提示，不区分用户是否存在', '✅'],
        ['9', 'IP 速率限制', '连续 6 次错误 → HTTP 429', '✅'],
        ['10', '账号渐进锁定', '5 次错误 → HTTP 423 锁定', '✅'],
        ['11', '已登录自动跳转', '已登录访问 /login → 302 重定向', '✅'],
        ['12', 'Session 劫持防护', '更换 IP → Session 销毁', '✅'],
        ['13', 'Session 超时', '30 分钟无操作 → 自动过期', '✅'],
        ['14', '蜜罐字段检测', '填写 _gotcha → 请求拒绝', '✅'],
        ['15', '审计日志', '成功/失败/锁定均有日志记录', '✅'],
        ['16', 'Host 头注入', '非法 Host → HTTP 400', '✅'],
        ['17', 'Content-Type', 'JSON 格式 POST → HTTP 400', '✅'],
        ['18', '请求体超限', '>16KB → HTTP 413', '✅'],
        ['19', '输入校验', '特殊字符 → 统一错误提示', '✅'],
        ['20', '错误页面安全', '404 页面无堆栈信息', '✅'],
    ]
    make_simple_table(doc, ['序号', '测试项', '测试结果', '状态'], checks,
                      col_widths=[1, 3.5, 6.5, 1.5])

    add_p(doc, '检测结论：所有 20 项测试全部通过 ✅。'
          '源码中已无法通过爆破获取密码，Debug 模式默认关闭，'
          '前端不再展示任何敏感密码信息。',
          bold=True, color=C_GREEN, indent=False, space_before=8)

    doc.add_page_break()

    # ════════════════════════════════════════════════════════
    #  四、修复前后对比
    # ════════════════════════════════════════════════════════

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run('四、修复前后对比：')
    _set_font(r, size=18, bold=True, color=C_BLUE)
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:bottom w:val="single" w:sz="12" w:space="4" w:color="2980B9"/>'
        f'</w:pBdr>'
    )
    p._p.get_or_add_pPr().append(pBdr)

    # ── 安全能力对比 ──
    comparisons = [
        ['密码存储', '明文 + == 比对', 'bcrypt 哈希 + 常量时间比对'],
        ['Secret Key', '硬编码 "dev-key-2025"', 'secrets.token_hex(32) 随机'],
        ['Session 过期', '永不过期', '30 分钟滑动 + 24 小时绝对'],
        ['CSRF 防护', '无', '一次性 HMAC Token'],
        ['暴力破解防护', '无', '双重限速 + 渐进锁定'],
        ['Session 劫持', '无防护', 'IP+UA 指纹绑定'],
        ['Cookie 安全', '无特殊属性', 'HttpOnly + SameSite=Strict'],
        ['安全响应头', '0 个', '8 个'],
        ['审计日志', '无', '轮转日志，5MB'],
        ['输入校验', '无', '白名单 + 长度截断'],
        ['错误处理', '默认调试页', '5 个自定义安全页面'],
        ['反自动化', '无', 'honeypot 隐藏字段'],
        ['调试模式', 'debug=True', '默认关闭，环境变量控制'],
        ['内存安全', '无处理', '启动后 del 清理明文'],
    ]
    make_simple_table(doc, ['安全维度', '修复前', '修复后'], comparisons,
                      col_widths=[3.5, 5, 5.5])

    # ── 代码质量对比 ──
    add_p(doc, '代码质量指标变化：', bold=True, indent=False, space_before=10)
    quality = [
        ['源文件数', '5', '8'],
        ['代码总行数', '~150', '~720'],
        ['安全注释行', '0', '~100'],
        ['安全措施数', '0', '25'],
        ['OWASP 高风险', '8/10', '0/10'],
        ['测试通过率', '—', '20/20 (100%)'],
    ]
    make_simple_table(doc, ['指标', '修复前', '修复后'], quality,
                      col_widths=[4, 4, 4])

    doc.add_page_break()

    # ════════════════════════════════════════════════════════
    #  五、结论
    # ════════════════════════════════════════════════════════

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run('五、结论：')
    _set_font(r, size=18, bold=True, color=C_BLUE)
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:bottom w:val="single" w:sz="12" w:space="4" w:color="2980B9"/>'
        f'</w:pBdr>'
    )
    p._p.get_or_add_pPr().append(pBdr)

    add_p(doc, '经过系统性的安全漏洞挖掘与修复，该项目已从存在严重安全缺陷的演示代码'
          '转变为具备生产级安全防护能力的 Web 应用。', size=10.5, indent=True)

    # 成果清单
    add_p(doc, '主要成果：', bold=True, indent=False, space_before=8)
    for item in [
        '🔹 共发现并修复 13 项安全漏洞，实施 25 项防护措施',
        '🔹 OWASP Top 10 高风险项从 8/10 降至 0/10',
        '🔹 20 项安全测试全部通过，通过率 100%',
        '🔹 审计日志完整记录所有安全事件，可追溯可审计',
        '🔹 用原来的字典已经爆破不到密码了',
        '🔹 源码中账密不可见',
        '🔹 Debug 模式仅当 FLASK_DEBUG=1 时开启',
    ]:
        add_bullet(doc, item)

    # 建议
    add_p(doc, '后续建议：', bold=True, indent=False, space_before=8)
    for item in [
        '迁移至 PostgreSQL/MySQL 数据库，替代内存字典',
        '使用 Gunicorn + Nginx 部署，配置 HTTPS 证书',
        '添加双因素认证（TOTP）提升账户安全性',
        '集成 reCAPTCHA 验证码服务',
        '定期进行依赖库漏洞扫描',
    ]:
        add_bullet(doc, item)

    doc.add_paragraph()
    doc.add_paragraph()

    # ── 结束 ──
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="8" w:space="8" w:color="2980B9"/>'
        f'</w:pBdr>'
    )
    p._p.get_or_add_pPr().append(pBdr)
    r = p.add_run('  — 报告完 —  ')
    _set_font(r, size=14, color=C_GRAY)

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('本报告仅供参考和学习使用\n报告日期: 2026-07-07  |  安全标准: OWASP Top 10 (2021)')
    _set_font(r, size=9, color=RGBColor(0xBB, 0xBB, 0xBB))

    # ── 保存 ──
    doc.save(OUTPUT)
    size_kb = os.path.getsize(OUTPUT) / 1024
    print(f'✅ 报告已生成: {OUTPUT}')
    print(f'   文件大小: {size_kb:.1f} KB')


if __name__ == '__main__':
    build()
