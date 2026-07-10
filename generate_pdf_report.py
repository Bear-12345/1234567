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
        <strong>今日课程：</strong>Day4:权限提升与业务逻辑漏洞深度解析<br>
        <strong>技术栈：</strong>Python Flask / IDOR / 水平越权 / 参数篡改<br>
    </div>
    <div class="line-bottom"></div>
</div>

<!-- ============================================================
     一、课程背景
     ============================================================ -->
<div class="page">
    <h2>一、课程背景</h2>
    <p>权限提升漏洞和业务逻辑漏洞是OWASP Top 10 2021中排名第一的"访问控制失效"（A01:2021-Broken Access Control）的核心内容。与SQL注入等传统漏洞不同，这两类漏洞更侧重于应用程序的"权限设计缺陷"和"业务流程缺陷"，往往不依赖特定的技术绕过，而是利用系统自身功能的逻辑漏洞。</p>

    <h3>1.1 权限提升漏洞（IDOR/越权）</h3>
    <p>权限提升（Privilege Escalation）指攻击者通过某种手段，获取到本不属于自己的更高权限。在Web应用中，最常见的表现形式是IDOR（Insecure Direct Object Reference，不安全的直接对象引用），即攻击者通过修改URL参数中的用户标识符（如 user_id），越权访问其他用户的数据。</p>

    <h3>1.2 业务逻辑漏洞</h3>
    <p>业务逻辑漏洞是指应用程序在处理业务流程时，由于对业务规则的校验不严谨，导致攻击者可以通过非预期的操作方式获取利益。典型的例子包括：充值金额可以为负、商品数量可以为负、积分可以无限刷等。这类漏洞不涉及传统的注入或绕过技术，而是利用系统"没想到"的操作路径。</p>

    <h3>1.3 本次实验环境</h3>
    <table>
        <tr><th>项目</th><th>说明</th></tr>
        <tr><td>目标应用</td><td>基于Flask的用户管理系统</td></tr>
        <tr><td>已有功能</td><td>登录、注册、搜索、头像上传、个人中心、充值</td></tr>
        <tr><td>本次新增</td><td>个人中心（/profile）、充值（/recharge）</td></tr>
        <tr><td>漏洞类型</td><td>IDOR越权漏洞 + 业务逻辑漏洞</td></tr>
    </table>
</div>

<!-- ============================================================
     二、漏洞分析与复现
     ============================================================ -->
<div class="page">
    <h2>二、漏洞分析与复现</h2>

    <h3>2.1 漏洞1：IDOR水平越权漏洞</h3>
    <p class="red bold">风险等级：高危 | CWE-639：通过用户控制的密钥绕过授权</p>

    <h4>2.1.1 漏洞代码分析</h4>
    <p>个人中心路由直接从URL参数获取 user_id，未验证当前登录用户与被查询用户是否匹配：</p>
    <div class="code-block">@app.route("/profile")
def profile():
    # 漏洞：user_id 从 URL 参数获取，用户可任意修改
    user_id = request.args.get("user_id")
    
    # 直接根据传入的ID查询，不验证身份
    user = db.query("SELECT * FROM users WHERE id = " + user_id)
    return render_template("profile.html", user=user)</div>

    <h4>2.1.2 攻击复现步骤</h4>
    <div class="code-block">步骤1：登录普通用户 alice (密码 alice2025)
步骤2：访问自己的个人中心
  GET /profile?user_id=2
  → 正常显示 alice 的资料

步骤3：修改URL参数为 admin 的ID
  GET /profile?user_id=1
  → 系统返回 admin 的资料！
  → 越权成功！普通用户看到了管理员的余额和手机号</div>

    <h4>2.1.3 漏洞原理</h4>
    <p>该漏洞属于典型的"不安全的直接对象引用"（IDOR）。系统在对用户数据进行操作时，完全依赖前端传入的 user_id 参数来定位数据归属，而没有在后端校验当前登录用户是否有权访问该数据。攻击者只需要遍历 user_id 参数值（1、2、3、4...），就可以获取系统中所有用户的个人信息。</p>
</div>

<div class="page">
    <h3>2.2 漏洞2：业务逻辑漏洞（金额可为负）</h3>
    <p class="red bold">风险等级：高危 | CWE-841：业务流程处理不当</p>

    <h4>2.2.1 漏洞代码分析</h4>
    <p>充值接口直接接收 amount 参数用于更新余额，未校验金额的正负，且使用f-string拼接SQL：</p>
    <div class="code-block">@app.route("/recharge", methods=["POST"])
def recharge():
    amount = request.form.get("amount")
    user_id = request.form.get("user_id")
    
    # 漏洞1：没有校验 amount 是否为正数
    # 漏洞2：直接拼接 SQL 语句
    sql = f"UPDATE users SET balance = balance + {amount} WHERE id = {user_id}"
    db.execute(sql)</div>

    <h4>2.2.2 攻击复现步骤</h4>
    <div class="code-block">步骤1：登录任意用户
步骤2：正常充值 100 元
  POST /recharge
  user_id=1&amount=100
  → 余额从 99999 变为 100099

步骤3：恶意提交负值 -100000
  POST /recharge  
  user_id=1&amount=-100000
  → 余额从 100099 变为 99 元！
  → 攻击者"盗刷"了系统的钱（将余额减少）</div>

    <h4>2.2.3 漏洞原理</h4>
    <p>该漏洞同时涉及两个安全问题：（1）业务逻辑缺陷——充值功能的设计假设用户只会输入正数，但未在服务端做任何校验，攻击者提交负数即可"反向扣款"；（2）SQL注入漏洞——使用f-string拼接SQL语句，攻击者可以在 amount 中注入恶意SQL代码。两者叠加，严重性极高。</p>

    <h3>2.3 漏洞危害总结</h3>
    <table>
        <tr><th>漏洞</th><th>攻击路径</th><th>影响范围</th><th>危害等级</th></tr>
        <tr>
            <td>IDOR越权</td>
            <td>遍历user_id参数</td>
            <td>所有用户的手机、邮箱、余额泄露</td>
            <td class="red bold">高危</td>
        </tr>
        <tr>
            <td>业务逻辑漏洞</td>
            <td>amount设为负值</td>
            <td>任意用户的余额可被篡改</td>
            <td class="red bold">高危</td>
        </tr>
    </table>
</div>

<!-- ============================================================
     三、修复方案
     ============================================================ -->
<div class="page">
    <h2>三、修复方案</h2>

    <h3>3.1 修复IDOR漏洞</h3>
    <p>核心原则：<strong>永远从服务端session获取用户身份，绝不信任客户端传入的用户标识。</strong></p>

    <div class="code-block">/// 修复后代码
@app.route("/profile")
@login_required
def profile():
    // 从 session 获取当前登录用户
    username = session.get("username")
    
    // 根据用户名查询用户信息
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    return render_template("profile.html", user=user)

// 修复要点：
// 1. 不从URL参数获取 user_id
// 2. 从 session 获取已登录的用户身份
// 3. 用户只能查询自己的数据</div>

    <h3>3.2 修复业务逻辑漏洞</h3>
    <p>核心原则：<strong>所有涉及金钱的业务操作必须校验数值范围，且使用参数化查询防止SQL注入。</strong></p>

    <div class="code-block">/// 修复后代码
@app.route("/recharge", methods=["POST"])
@login_required
def recharge():
    username = session.get("username")
    amount = int(request.form.get("amount", "0"))
    
    // 修复1：校验金额必须为正数
    if amount <= 0:
        return "充值金额必须大于0"
    
    // 修复2：使用参数化查询防止SQL注入
    c.execute(
        "UPDATE users SET balance = balance + ? WHERE username = ?",
        (amount, username)
    )
    return redirect("/profile")</div>

    <h3>3.3 修复前后代码对比</h3>
    <table>
        <tr><th style="width:18%">对比项</th><th style="width:41%">修复前（存在漏洞）</th><th style="width:41%">修复后（安全）</th></tr>
        <tr>
            <td><strong>用户身份来源</strong></td>
            <td class="code">URL参数: user_id=1</td>
            <td class="code">Session: session["username"]</td>
        </tr>
        <tr>
            <td><strong>权限校验</strong></td>
            <td class="code">无校验，直接查询</td>
            <td class="code">只能查自己的数据</td>
        </tr>
        <tr>
            <td><strong>金额校验</strong></td>
            <td class="code">不校验正负</td>
            <td class="code">amount > 0</td>
        </tr>
        <tr>
            <td><strong>SQL语句</strong></td>
            <td class="code">f"WHERE id = {user_id}"</td>
            <td class="code">WHERE username = ?</td>
        </tr>
    </table>
</div>

<!-- ============================================================
     四、修复后验证
     ============================================================ -->
<div class="page">
    <h2>四、修复后验证</h2>

    <h3>4.1 IDOR越权测试</h3>
    <table>
        <tr><th style="width:10%">序号</th><th style="width:30%">测试操作</th><th style="width:30%">预期结果</th><th style="width:30%">实际结果</th></tr>
        <tr>
            <td>1</td>
            <td>alice访问 /profile</td>
            <td>显示alice自己的资料</td>
            <td class="green bold">[OK] 显示alice信息</td>
        </tr>
        <tr>
            <td>2</td>
            <td>alice访问 /profile?user_id=1</td>
            <td>仍然显示alice自己的资料</td>
            <td class="green bold">[OK] 未越权到admin</td>
        </tr>
        <tr>
            <td>3</td>
            <td>admin访问 /profile</td>
            <td>显示admin的资料</td>
            <td class="green bold">[OK] 显示admin信息</td>
        </tr>
    </table>

    <h3>4.2 业务逻辑测试</h3>
    <table>
        <tr><th style="width:10%">序号</th><th style="width:30%">测试操作</th><th style="width:30%">预期结果</th><th style="width:30%">实际结果</th></tr>
        <tr>
            <td>1</td>
            <td>正常充值 amount=100</td>
            <td>余额增加100</td>
            <td class="green bold">[OK] 充值成功</td>
        </tr>
        <tr>
            <td>2</td>
            <td>恶意充值 amount=-99999</td>
            <td>报错：金额必须大于0</td>
            <td class="green bold">[OK] 被拦截</td>
        </tr>
        <tr>
            <td>3</td>
            <td>SQL注入 amount=1;DROP TABLE</td>
            <td>参数化查询拦截</td>
            <td class="green bold">[OK] 安全</td>
        </tr>
    </table>
</div>

<!-- ============================================================
     五、漏洞修复总结
     ============================================================ -->
<div class="page">
    <h2>五、漏洞修复总结</h2>

    <h3>5.1 漏洞类型归纳</h3>
    <table>
        <tr><th>漏洞类型</th><th>OWASP Top 10对应</th><th>CWE编号</th><th>根因</th><th>修复方案</th></tr>
        <tr>
            <td>IDOR/越权</td>
            <td>A01:2021 访问控制失效</td>
            <td>CWE-639</td>
            <td>信任前端传入的用户ID</td>
            <td>从Session获取用户身份</td>
        </tr>
        <tr>
            <td>业务逻辑漏洞</td>
            <td>A01:2021 访问控制失效</td>
            <td>CWE-841</td>
            <td>未校验金额正负</td>
            <td>amount>0 + 参数化查询</td>
        </tr>
    </table>

    <h3>5.2 安全开发原则</h3>
    <p>通过本次漏洞修复，总结出以下安全开发原则：</p>
    <table>
        <tr><th style="width:8%">原则</th><th style="width:92%">说明</th></tr>
        <tr><td><strong>1</strong></td><td><strong>永不信任用户输入</strong>：URL参数、表单数据、Cookie等客户端传入的数据均不可信</td></tr>
        <tr><td><strong>2</strong></td><td><strong>服务端身份验证</strong>：用户身份应从 Session/Token 中获取，而非前端参数</td></tr>
        <tr><td><strong>3</strong></td><td><strong>业务参数校验</strong>：金额、数量等业务数据必须校验范围和正负</td></tr>
        <tr><td><strong>4</strong></td><td><strong>最小权限原则</strong>：用户只能操作属于自己的数据，不能越权</td></tr>
        <tr><td><strong>5</strong></td><td><strong>参数化查询</strong>：所有SQL操作必须使用参数化查询，杜绝拼接</td></tr>
    </table>

    <h3>5.3 本次修复涉及的文件</h3>
    <table>
        <tr><th>文件</th><th>修改内容</th></tr>
        <tr><td>app.py</td><td>/profile路由改为从session获取用户；/recharge增加金额正负校验和参数化查询</td></tr>
        <tr><td>templates/profile.html</td><td>移除user_id隐藏字段，改为从session自动获取</td></tr>
        <tr><td>templates/base.html</td><td>导航栏链接从/profile?user_id=1改为/profile</td></tr>
        <tr><td>templates/index.html</td><td>首页快捷入口从/profile?user_id=1改为/profile</td></tr>
    </table>

    <br>
    <hr style="border: none; border-top: 1px solid #2980b9; width: 60%; margin: 8mm auto;">
    <p style="text-align: center; color: #95a5a6; text-indent: 0;">&mdash; 报告完 &mdash;</p>
    <p style="text-align: center; color: #bbb; font-size: 8pt; text-indent: 0;">报告日期: 2026-07-10 | 课程: 权限提升与业务逻辑漏洞 | 安全标准: OWASP Top 10 (2021) A01</p>
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
