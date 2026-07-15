# -*- coding: utf-8 -*-
# PDF报告生成器 - 使用 WeasyPrint (HTML→PDF)，完美支持中文

from weasyprint import HTML
import os

OUTPUT = '/home/user/Projects/user-mgr/SQL注入漏洞修复报告.pdf'
FONT_PATH = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'

HTML_CONTENT = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<style>
@font-face {
    font-family: 'zh';
    src: url('FONT_PATH') format('truetype');
}
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
body {
    font-family: 'zh', sans-serif;
    color: #2c3e50;
    line-height: 1.7;
    font-size: 11pt;
}
.page {
    width: 210mm;
    min-height: 297mm;
    padding: 25mm 25mm 20mm 25mm;
    position: relative;
}

/* ===== 封面 ===== */
.cover {
    text-align: center;
    padding-top: 80mm;
}
.cover .line {
    width: 60mm;
    height: 2px;
    background: #2980b9;
    margin: 0 auto 12mm auto;
}
.cover h1 {
    font-size: 32pt;
    color: #2980b9;
    margin-bottom: 6mm;
    letter-spacing: 2px;
}
.cover .subtitle {
    font-size: 20pt;
    color: #2c3e50;
    margin-bottom: 8mm;
}
.cover .url {
    font-size: 12pt;
    color: #95a5a6;
    margin-bottom: 10mm;
}
.cover .divider {
    width: 80mm;
    border: none;
    border-top: 1px solid #ddd;
    margin: 6mm auto;
}
.cover .meta {
    font-size: 11pt;
    line-height: 2.2;
    color: #555;
}
.cover .meta strong {
    color: #2c3e50;
}
.cover .stars {
    font-size: 16pt;
    color: #f39c12;
    letter-spacing: 3px;
}
.cover .line-bottom {
    width: 60mm;
    height: 2px;
    background: #2980b9;
    margin: 10mm auto 0 auto;
}

/* ===== 标题 ===== */
h2 {
    font-size: 17pt;
    color: #2980b9;
    padding-bottom: 3mm;
    border-bottom: 2px solid #2980b9;
    margin: 0 0 5mm 0;
}
h3 {
    font-size: 13pt;
    color: #2c3e50;
    margin: 6mm 0 3mm 0;
}
h4 {
    font-size: 11pt;
    color: #2980b9;
    margin: 4mm 0 2mm 0;
}

/* ===== 正文 ===== */
p {
    text-indent: 2em;
    margin: 0 0 2mm 0;
    font-size: 10pt;
    line-height: 1.8;
}
p.no-indent {
    text-indent: 0;
}
.bold {
    font-weight: bold;
}
.red {
    color: #e74c3c;
}
.green {
    color: #27ae60;
}
.blue {
    color: #2980b9;
}
.gray {
    color: #95a5a6;
}

/* ===== 代码块 ===== */
.code-block {
    background: #f5f5f5;
    border-left: 3px solid #2980b9;
    padding: 3mm 4mm;
    margin: 2mm 0 3mm 5mm;
    font-family: 'Courier New', monospace;
    font-size: 8pt;
    line-height: 1.5;
    white-space: pre;
    overflow-x: auto;
}
td.code {
    font-family: 'Courier New', monospace;
    font-size: 8pt;
    background: #fafafa;
}

/* ===== 漏洞条目 ===== */
.vuln {
    margin: 3mm 0;
}
.vuln .title {
    font-size: 11pt;
    font-weight: bold;
}
.vuln .title.critical, .vuln .title.high {
    color: #e74c3c;
}
.vuln .title.medium {
    color: #e67e22;
}
.vuln .title.low {
    color: #7f8c8d;
}
.vuln .detail {
    text-indent: 2em;
    font-size: 9.5pt;
    margin: 1mm 0 0 5mm;
    line-height: 1.7;
}
.vuln .impact {
    margin: 0.5mm 0 2mm 5mm;
    font-size: 9pt;
}
.vuln .impact-label {
    color: #e74c3c;
    font-weight: bold;
}

/* ===== 修复条目 ===== */
.fix-item {
    margin: 2mm 0;
}
.fix-item .title {
    font-size: 10.5pt;
    font-weight: bold;
    color: #2980b9;
}
.fix-item .detail {
    text-indent: 2em;
    font-size: 9.5pt;
    margin: 0.5mm 0 1mm 5mm;
    line-height: 1.7;
}

/* ===== 表格 ===== */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 3mm 0;
    font-size: 9pt;
}
th {
    background: #2980b9;
    color: white;
    padding: 1.5mm 2mm;
    text-align: center;
    font-weight: bold;
}
td {
    padding: 1.2mm 2mm;
    border: 1px solid #ddd;
    text-align: left;
}
tr:nth-child(even) {
    background: #f8f9fa;
}

/* ===== 测试结果 ===== */
.test-result {
    margin: 1.5mm 0;
    padding-left: 5mm;
}
.test-result .label {
    font-weight: bold;
}
.test-result .pass {
    color: #27ae60;
    font-weight: bold;
}

/* ===== 页脚 ===== */
.footer {
    text-align: center;
    color: #bbb;
    font-size: 8pt;
    margin-top: 10mm;
    padding-top: 5mm;
    border-top: 1px solid #2980b9;
}

/* ===== 检测点 ===== */
.check-point {
    margin: 1.5mm 0 1.5mm 5mm;
    font-size: 9.5pt;
}
.check-point .num {
    font-weight: bold;
    color: #2c3e50;
}
.check-point .arrow {
    color: #95a5a6;
}
</style>
</head>
<body>

<!-- ============================================================
     封面
     ============================================================ -->
<div class="page cover">
    <div class="line"></div>
    <h1>用户信息管理平台</h1>
    <div class="subtitle">安全漏洞挖掘与修复报告</div>
    <div class="url">http://10.133.25.156:5000</div>
    <hr class="divider">
    <div class="meta">
        <strong>项目版本：</strong>V8.0 - XSS与CSRF漏洞专题<br>
        <strong>报告日期：</strong>2026年7月14日<br>
        <strong>今日课程：</strong>Day6:XSS跨站脚本与CSRF跨站请求伪造<br>
        <strong>技术栈：</strong>Python Flask / XSS / CSRF / 越权<br>
    </div>
    <div class="line-bottom"></div>
</div>

<div class="page">
    <h2>一、课程背景</h2>
    <p>XSS(跨站脚本攻击)和CSRF(跨站请求伪造)是两类经典的Web安全漏洞。XSS利用网站未对用户输入进行过滤的缺陷，向页面中注入恶意脚本代码；CSRF则利用网站未验证请求来源的缺陷，诱使用户在不知情的情况下执行非自愿的操作。</p>

    <h3>1.1 XSS(跨站脚本攻击)</h3>
    <p>XSS攻击者将恶意脚本注入到网页中，当其他用户访问该页面时，脚本会在他们的浏览器中执行。XSS分为三种类型：存储型(数据持久化在服务器上)、反射型(恶意脚本在URL中)和DOM型(基于前端DOM操作)。</p>

    <h3>1.2 CSRF(跨站请求伪造)</h3>
    <p>CSRF攻击者构造一个恶意页面，当已登录用户访问该页面时，会在用户不知情的情况下向目标网站发送请求，执行非用户意愿的操作。CSRF的核心成因是网站没有验证请求的合法性来源。</p>

    <h3>1.3 本次实验环境</h3>
    <table>
        <tr><th>项目</th><th>说明</th></tr>
        <tr><td>目标应用</td><td>基于Flask的用户管理系统</td></tr>
        <tr><td>新增功能</td><td>/change-password 修改密码(无CSRF、无原密码校验)</td></tr>
        <tr><td>漏洞类型</td><td>CSRF + 越权(可修改任意用户密码)</td></tr>
        <tr><td>测试账号</td><td>admin/admin123</td></tr>
    </table>
</div>

<div class="page">
    <h2>二、漏洞分析</h2>

    <h3>2.1 漏洞代码</h3>
    <div class="code-block">@app.route("/change-password", methods=["POST"])
@login_required
def change_password():
    username = request.form.get("username", "")
    new_password = request.form.get("new_password", "")
    # 漏洞1: 无CSRF Token校验
    # 漏洞2: 无原密码验证
    # 漏洞3: 可修改任意用户的密码(越权)
    sql = f"UPDATE users SET password = '{new_password}' WHERE username = '{username}'"
    c.execute(sql)</div>

    <h3>2.2 漏洞列表</h3>
    <table>
        <tr><th>漏洞类型</th><th>风险</th><th>说明</th></tr>
        <tr><td>CSRF</td><td class="red bold">高危</td><td>未验证Token，攻击者可伪造密码修改请求</td></tr>
        <tr><td>越权</td><td class="red bold">高危</td><td>已登录用户可修改任意人的密码</td></tr>
        <tr><td>无原密码</td><td class="red bold">高危</td><td>不需要知道原密码即可修改</td></tr>
        <tr><td>SQL注入</td><td class="red bold">高危</td><td>f-string拼接SQL语句</td></tr>
    </table>

    <h3>2.3 POC验证</h3>
    <div class="code-block">// POC 1: admin登录后修改alice的密码
// 不需要知道alice的原密码
POST /change-password
username=alice&new_password=hacked123
// 结果: alice的密码被改为 hacked123

// POC 2: CSRF攻击(构造恶意页面)
&lt;form action="http://目标/change-password" method="POST"&gt;
    &lt;input name="username" value="admin"&gt;
    &lt;input name="new_password" value="csrf_hacked"&gt;
&lt;/form&gt;
&lt;script&gt;document.forms[0].submit()&lt;/script&gt;
// 受害用户只要访问这个页面,密码就被改了</div>
</div>

<div class="page">
    <h2>三、修复方案</h2>

    <h3>3.1 添加CSRF Token验证</h3>
    <div class="code-block">// 在表单中添加CSRF Token
&lt;input type="hidden" name="_csrf_token" value="{{ csrf_token }}"&gt;

// 在服务端验证
if request.form.get("_csrf_token") != session.get("_csrf_token"):
    return "CSRF攻击拦截"</div>

    <h3>3.2 验证原密码</h3>
    <div class="code-block">old_password = request.form.get("old_password", "")
if not check_password_hash(user["password"], old_password):
    return "原密码错误"</div>

    <h3>3.3 从Session获取用户身份</h3>
    <div class="code-block"># 不从表单取username
username = session.get("username")
# 只能修改自己的密码</div>

    <h3>3.4 修复前后对比</h3>
    <table>
        <tr><th>对比项</th><th>修复前</th><th>修复后</th></tr>
        <tr><td>CSRF Token</td><td>无</td><td>有Token校验</td></tr>
        <tr><td>原密码</td><td>不需要</td><td>必须验证原密码</td></tr>
        <tr><td>用户身份</td><td>从表单获取</td><td>从Session获取</td></tr>
        <tr><td>SQL语句</td><td>f-string拼接</td><td>参数化查询</td></tr>
    </table>
</div>

<div class="page">
    <h2>四、修复后验证</h2>
    <table>
        <tr><th>测试</th><th>修复前</th><th>修复后</th></tr>
        <tr><td>admin修改alice密码</td><td class="red bold">成功(越权)</td><td class="green bold">[OK] 只能修改自己的</td></tr>
        <tr><td>无CSRF Token提交</td><td class="red bold">成功</td><td class="green bold">[OK] 被拦截</td></tr>
        <tr><td>不输原密码直接改</td><td class="red bold">成功</td><td class="green bold">[OK] 必须输入原密码</td></tr>
    </table>
</div>

<div class="page">
    <h2>五、总结</h2>
    <p>CSRF和XSS是Web安全中最常见的客户端攻击方式。CSRF的核心问题是"这个请求是用户自愿发出的吗"，XSS的核心问题是"这段内容是用户输入的吗"。</p>
    <p><strong>安全开发原则：</strong></p>
    <p>1. 所有涉及数据修改的请求必须验证CSRF Token</p>
    <p>2. 密码修改必须验证原密码</p>
    <p>3. 用户身份从Session获取，不从客户端传入的参数获取</p>
    <p>4. 所有SQL操作使用参数化查询</p>

    <br>
    <hr style="border: none; border-top: 1px solid #2980b9; width: 60%; margin: 8mm auto;">
    <p style="text-align: center; color: #95a5a6; text-indent: 0;">&mdash; 报告完 &mdash;</p>
    <p style="text-align: center; color: #bbb; font-size: 8pt; text-indent: 0;">报告日期: 2026-07-14 | 课程: XSS与CSRF漏洞修复</p>
</div>
</body>
</html>
"""


def build():
    # 替换字体路径占位符
    html = HTML_CONTENT.replace('FONT_PATH', FONT_PATH)

    # 生成 PDF
    HTML(string=html).write_pdf(OUTPUT)
    size_kb = os.path.getsize(OUTPUT) / 1024
    print(f'[OK] PDF 已生成: {OUTPUT}')
    print(f'     大小: {size_kb:.1f} KB')


if __name__ == '__main__':
    build()
