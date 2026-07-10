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
    <div class="url">http://10.133.25.191:5000</div>
    <hr class="divider">
    <div class="meta">
        <strong>项目版本：</strong>V6.0 — 权限提升 + 业务逻辑漏洞专题<br>
        <strong>报告日期：</strong>2026年7月10日<br>
        <strong>今日课程：</strong>Day4:权限提升与业务逻辑漏洞<br>
        <strong>技术栈：</strong>Python Flask / IDOR / 余额操作 / SQL注入<br>
    </div>
    <div class="line-bottom"></div>
</div>

<!-- ============================================================
     一、漏洞分析
     ============================================================ -->
<div class="page">
    <h2>一、漏洞分析</h2>
    <p>在已有功能基础上新增了个人中心和充值功能，由于未做权限校验和业务逻辑检查，存在2个严重漏洞。</p>

    <h3>1.1 新增功能</h3>
    <table>
        <tr><th>功能</th><th>路由</th><th>说明</th></tr>
        <tr><td>个人中心</td><td>/profile?user_id=X</td><td>查看用户资料，user_id来源于URL参数</td></tr>
        <tr><td>充值</td><td>/recharge</td><td>修改余额，amount来源于表单参数</td></tr>
    </table>

    <h3>1.2 漏洞1：IDOR（权限提升）</h3>
    <p class="red bold">风险等级：高危</p>
    <p>个人中心从 URL 参数获取 user_id，但未验证当前登录用户与查询的 user_id 是否匹配。</p>
    <div class="code-block">// 漏洞代码
user_id = request.args.get("user_id")
user = _get_user_by_id(user_id)  // 直接查询，不验证身份

// 攻击方法：修改URL参数
/profile?user_id=1  // 查看admin的资料
/profile?user_id=2  // 查看alice的资料（越权！）
/profile?user_id=3  // 查看任意注册用户的资料</div>

    <h3>1.3 漏洞2：业务逻辑漏洞（金额为负）</h3>
    <p class="red bold">风险等级：高危</p>
    <p>充值接口直接拼接 SQL 更新余额，但未校验 amount 的正负。攻击者可填写负数实现盗刷。</p>
    <div class="code-block">// 漏洞代码
sql = f"UPDATE users SET balance = balance + {amount} WHERE id = {user_id}"
// 没有检查 amount 是否 > 0

// 攻击方法：提交负值
POST /recharge
user_id=1&amount=-100000  // 余额减少10万！
user_id=2&amount=999999   // 给alice加钱</div>
</div>

<!-- ============================================================
     二、修复方案
     ============================================================ -->
<div class="page">
    <h2>二、修复方案</h2>

    <h3>2.1 修复IDOR漏洞</h3>
    <p>从 session 获取当前用户，不允许查询其他用户资料：</p>
    <div class="code-block">// 修复后：从session获取当前用户
@app.route("/profile")
@login_required
def profile():
    username = session.get("username")
    user = _get_user(username)  // 只能查自己
    return render_template("profile.html", user=user)</div>

    <h3>2.2 修复业务逻辑漏洞</h3>
    <p>检查金额必须为正数，使用参数化查询：</p>
    <div class="code-block">// 修复后：校验金额正负
amount = int(request.form.get("amount", "0"))
if amount <= 0:
    return "金额必须为正数"

// 使用参数化查询
c.execute("UPDATE users SET balance = balance + ? WHERE username = ?",
          (amount, session["username"]))</div>
</div>

<!-- ============================================================
     三、POC验证结果
     ============================================================ -->
<div class="page">
    <h2>三、POC验证结果</h2>

    <table>
        <tr><th style="width:15%">POC</th><th style="width:35%">测试方法</th><th style="width:25%">修复前结果</th><th style="width:25%">修复后</th></tr>
        <tr>
            <td><strong>IDOR</strong></td>
            <td>登录admin后访问/profile?user_id=2</td>
            <td class="red bold">查到alice的资料 ✅</td>
            <td class="green bold">只能查自己</td>
        </tr>
        <tr>
            <td><strong>负值充值</strong></td>
            <td>POST amount=-100000</td>
            <td class="red bold">余额减少10万 ✅</td>
            <td class="green bold">拦截负值</td>
        </tr>
    </table>

    <h3>服务端日志记录</h3>
    <div class="code-block">[业务逻辑漏洞] 执行SQL: UPDATE users SET balance = balance + 500 WHERE id = 1
[业务逻辑漏洞] 用户ID 1 余额变动: +500
[业务逻辑漏洞] 执行SQL: UPDATE users SET balance = balance + -100000 WHERE id = 1
[业务逻辑漏洞] 用户ID 1 余额变动: -100000</div>
</div>

<!-- ============================================================
     四、总结
     ============================================================ -->
<div class="page">
    <h2>四、总结</h2>

    <table>
        <tr><th>漏洞类型</th><th>根因</th><th>修复方案</th></tr>
        <tr>
            <td>IDOR（权限提升）</td>
            <td>未验证user_id归属</td>
            <td>从session获取用户身份，而非URL参数</td>
        </tr>
        <tr>
            <td>业务逻辑漏洞</td>
            <td>未校验金额正负 + 拼接SQL</td>
            <td>金额>0校验 + 参数化查询</td>
        </tr>
    </table>

    <p style="margin-top: 4mm;">核心安全原则：</p>
    <p>1. 永远不要信任前端传入的用户标识（user_id应从session获取）</p>
    <p>2. 所有业务操作必须做权限校验（用户只能操作自己的数据）</p>
    <p>3. 数值型字段必须校验范围（金额不能为负）</p>
    <p>4. 所有SQL必须使用参数化查询</p>

    <br>
    <hr style="border: none; border-top: 1px solid #2980b9; width: 60%; margin: 8mm auto;">
    <p style="text-align: center; color: #95a5a6; text-indent: 0;">&mdash; 报告完 &mdash;</p>
    <p style="text-align: center; color: #bbb; font-size: 8pt; text-indent: 0;">报告日期: 2026-07-10 | 课程: 权限提升 + 业务逻辑 | OWASP Top 10: A01/Broken Access Control</p>
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
