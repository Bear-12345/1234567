# -*- coding: utf-8 -*-
"""PDF报告生成器 - 使用 WeasyPrint (HTML→PDF)，完美支持中文"""

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
    <div class="url">http://192.168.43.129:5000</div>
    <hr class="divider">
    <div class="meta">
        <strong>项目版本：</strong>V4.0 — SQL注入漏洞修复专题<br>
        <strong>报告日期：</strong>2026年7月8日<br>
        <strong>今日课程：</strong>Day2:SQL注入漏洞挖掘与修复<br>
        <strong>技术栈：</strong>Python Flask / SQLite / 参数化查询 / POC验证<br>
        <strong>安全评级：</strong><span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>  25项防护全部通过
    </div>
    <div class="line-bottom"></div>
</div>

<!-- ============================================================
     一、SQL注入漏洞专题
     ============================================================ -->
<div class="page">
    <h2>一、SQL注入漏洞专题</h2>
    <p>第2天课程内容为 SQL 注入漏洞的挖掘与修复。系统在上次迭代中新增了注册和搜索功能，但使用了 f-string 字符串拼接 SQL 语句，故意留下了注入漏洞。</p>

    <h3>4.1 漏洞位置</h3>
    <table>
        <tr><th>功能</th><th>路由</th><th>漏洞代码</th></tr>
        <tr><td>用户注册</td><td>/register</td><td class="code">f"INSERT INTO users VALUES ('{username}',...)"</td></tr>
        <tr><td>用户搜索</td><td>/search</td><td class="code">f"SELECT ... WHERE username LIKE '%{keyword}%'"</td></tr>
    </table>

    <h3>4.2 POC 验证（注入成功）</h3>

    <h4>POC 1：UNION 注入</h4>
    <div class="code-block"># 输入
keyword = ' UNION SELECT 1,'inj','inj@x.com','138'--

# 生成的 SQL
SELECT * FROM users WHERE username LIKE '%' UNION SELECT 1,'inj','inj@x.com','138'--%'

# 结果：搜索结果中出现 "inj" 用户 ✅</div>

    <h4>POC 2：OR 万能条件</h4>
    <div class="code-block"># 输入
keyword = ' OR '1'='1

# 生成的 SQL
SELECT * FROM users WHERE username LIKE '%' OR '1'='1%' OR email LIKE '%' OR '1'='1%'

# 结果：返回 users 表中全部用户数据 ✅</div>

    <h4>POC 3：注册功能注入</h4>
    <div class="code-block"># 输入
username = hacker', 'pass', 'h@x.com', '123')--

# 生成的 SQL
INSERT INTO users VALUES ('hacker', 'pass', 'h@x.com', '123')--',...)

# 结果：恶意数据写入数据库 ✅</div>

    <h3>4.3 修复方案</h3>
    <p>将 f-string 拼接 SQL 改为<strong>参数化查询</strong>（Prepared Statement），根本性防止 SQL 注入：</p>

    <div class="code-block">// ❌ 修复前：f-string 拼接（存在注入）
sql = f"SELECT ... WHERE username LIKE '%{keyword}%'"

// ✅ 修复后：参数化查询（安全）
sql = "SELECT ... WHERE username LIKE ?"
cursor.execute(sql, (like_pattern,))</div>

    <h3>4.3 修复前后代码对比</h3>
    <table>
        <tr><th style="width:15%">功能</th><th style="width:42%">修复前（f-string拼接）</th><th style="width:43%">修复后（参数化查询）</th></tr>
        <tr>
            <td><strong>注册</strong></td>
            <td class="code">f"INSERT INTO users VALUES ('{username}','{password}','{email}','{phone}')"</td>
            <td class="code">sql = "INSERT INTO users VALUES (?,?,?,?)"<br>cursor.execute(sql, (username,password,email,phone))</td>
        </tr>
        <tr>
            <td><strong>搜索</strong></td>
            <td class="code">f"SELECT ... WHERE username LIKE '%{keyword}%'"</td>
            <td class="code">sql = "SELECT ... WHERE username LIKE ?"<br>cursor.execute(sql, (like_pattern,))</td>
        </tr>
    </table>

    <h3>4.4 Burp Suite 测试方法</h3>
    <p>使用 Burp Suite 抓包后修改 keyword 参数测试注入：</p>
    <div class="code-block">1. 登录后拦截 GET /search?keyword=admin 请求
2. 发送到 Repeater
3. 修改 keyword 参数值测试注入：
   admin' OR '1'='1          → 返回全部用户
   ' UNION SELECT 1,2,3,4--  → 返回自定义数据</div>

    <h3>4.5 修复后验证</h3>
    <table>
        <tr><th>测试</th><th>修复前</th><th>修复后</th></tr>
        <tr><td>POC 1 UNION 注入</td><td>返回 "inj" 数据</td><td class="green bold">[OK] 注入无效，搜索结果为0</td></tr>
        <tr><td>POC 2 OR 万能条件</td><td>返回全部用户</td><td class="green bold">[OK] 注入无效，正常搜索</td></tr>
        <tr><td>POC 3 注册注入</td><td>SQL代码被执行</td><td class="green bold">[OK] 注入内容成为普通用户名</td></tr>
    </table>
</div>

<!-- ============================================================
     二、总结
     ============================================================ -->
<div class="page">
    <h2>二、总结</h2>
    <p class="no-indent">本次SQL注入漏洞修复专题，针对注册和搜索功能中的 f-string 拼接SQL漏洞进行了全面修复：</p>

    <table>
        <tr>
            <th>课程内容</th>
            <th>受影响功能</th>
            <th>漏洞类型</th>
            <th>修复措施</th>
        </tr>
        <tr>
            <td>SQL注入</td>
            <td>注册 / 搜索</td>
            <td>f-string拼接SQL</td>
            <td>参数化查询(Prepared Statement)</td>
        </tr>
    </table>

    <p style="margin-top: 4mm;">核心原理：参数化查询将 SQL 语句与用户输入的数据分离，数据库先编译 SQL 结构（SELECT、INSERT 等），再将用户输入作为"纯数据"填入。即使用户输入包含恶意 SQL 代码，也不会被数据库执行，从根源消除注入风险。</p>

    <br>
    <hr style="border: none; border-top: 1px solid #2980b9; width: 60%; margin: 8mm auto;">
    <p style="text-align: center; color: #95a5a6; text-indent: 0;">&mdash; 报告完 &mdash;</p>
    <p style="text-align: center; color: #bbb; font-size: 8pt; text-indent: 0;">报告日期: 2026-07-08 | 课程: SQL注入漏洞修复 | 安全标准: OWASP</p>
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
