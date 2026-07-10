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
    <div class="url">http://10.133.25.191:5000</div>
    <hr class="divider">
    <div class="meta">
        <strong>项目版本：</strong>V6.0 — 权限提升 + 业务逻辑漏洞专题<br>
        <strong>报告日期：</strong>2026年7月10日<br>
        <strong>今日课程：</strong>Day4:权限提升与业务逻辑漏洞深度解析<br>
        <strong>技术栈：</strong>Python Flask / IDOR / 水平越权 / 参数篡改 / SQL注入<br>
        <strong>作者：</strong>Bear<br>
    </div>
    <div class="line-bottom"></div>
</div>

<!-- ============================================================
     一、课程背景与知识概述
     ============================================================ -->
<div class="page">
    <h2>一、课程背景与知识概述</h2>
    <p>权限提升漏洞和业务逻辑漏洞是OWASP Top 10 2021中排名第一的"访问控制失效"（A01:2021-Broken Access Control）的核心内容。与SQL注入、XSS等传统注入类漏洞不同，这两类漏洞更侧重于应用程序的"权限模型设计缺陷"和"业务流程校验缺陷"，攻击者不需要使用复杂的编码技巧，往往只需要修改URL中的一个数字或表单中的一个字段值，就能获得不正当的访问权限或经济利益。</p>

    <h3>1.1 权限提升漏洞（IDOR/越权）</h3>
    <p><strong>定义：</strong>权限提升（Privilege Escalation）指攻击者通过某种手段，获取到本不属于自己的更高权限或他人数据。在Web应用中，最常见的表现形式是IDOR（Insecure Direct Object Reference，不安全的直接对象引用）。</p>
    <p><strong>IDOR原理：</strong>当应用程序直接使用用户提供的输入（如URL参数、表单字段）来访问数据库中的对象（如用户资料、订单记录），且没有验证当前用户是否有权访问该对象时，就产生了IDOR漏洞。攻击者只需修改参数值（如将 user_id=2 改为 user_id=1），就能访问其他用户的数据。</p>
    <p><strong>分类：</strong></p>
    <p>（1）水平越权：攻击者访问同级别其他用户的数据（如普通用户A查看普通用户B的资料）</p>
    <p>（2）垂直越权：攻击者访问更高级别用户的功能或数据（如普通用户执行管理员操作）</p>

    <h3>1.2 业务逻辑漏洞</h3>
    <p><strong>定义：</strong>业务逻辑漏洞是指应用程序在处理业务流程时，由于对业务规则的校验不严谨，导致攻击者可以通过非预期的操作方式获取利益。</p>
    <p><strong>常见类型：</strong></p>
    <p>（1）金额/数量可为负：充值、转账、下单等涉及数值操作的接口未校验正负</p>
    <p>（2）越权操作：未验证当前用户是否有权执行某操作</p>
    <p>（3）重放攻击：同一请求可重复提交导致多次扣款/充值</p>
    <p>（4）条件竞争：多线程同时操作同一资源导致数据不一致</p>
    <p>（5）顺序绕过：跳过某些步骤直接执行后续操作</p>

    <h3>1.3 本次实验环境</h3>
    <table>
        <tr><th style="width:25%">项目</th><th style="width:75%">说明</th></tr>
        <tr><td>目标应用</td><td>基于Python Flask框架的用户信息管理平台</td></tr>
        <tr><td>数据库</td><td>SQLite 3，使用data/users.db存储用户数据</td></tr>
        <tr><td>已有功能</td><td>登录、注册、搜索、头像上传、个人中心、充值</td></tr>
        <tr><td>本次新增功能</td><td>/profile（个人中心查看）、/recharge（余额充值）</td></tr>
        <tr><td>漏洞类型</td><td>IDOR水平越权漏洞 + 业务逻辑漏洞（金额负值）</td></tr>
        <tr><td>测试账号</td><td>admin/admin123（管理员，余额99999）、alice/alice2025（普通用户，余额100）</td></tr>
    </table>
</div>

<!-- ============================================================
     二、漏洞代码分析
     ============================================================ -->
<div class="page">
    <h2>二、漏洞代码分析</h2>

    <h3>2.1 漏洞1：IDOR水平越权漏洞</h3>
    <p class="red bold">风险等级：高危 | CWE-639：通过用户控制的密钥绕过授权</p>

    <h4>2.1.1 漏洞位置</h4>
    <p>文件：app.py，路由 /profile</p>
    <p>行号：约第900行</p>

    <h4>2.1.2 漏洞代码</h4>
    <div class="code-block">@app.route("/profile")
@login_required
def profile():
    # 个人中心  - 存在IDOR漏洞
    # 【漏洞】user_id 从URL参数获取，用户可以任意修改
    user_id = request.args.get("user_id", "")
    
    # 【漏洞】直接根据传入的ID查询数据库，不验证身份
    user = _get_user_by_id(user_id)
    
    return render_template("profile.html", user=user)</div>

    <h4>2.1.3 漏洞成因分析</h4>
    <p>（1）身份标识来源错误：用户的身份标识（user_id）应从服务端的 session 中获取，而不是从客户端传来的 URL 参数中获取。session 中的数据由服务器签名保护，用户无法篡改；而 URL 参数用户可以随意修改。</p>
    <p>（2）缺少权限校验：即使需要通过 user_id 查询，也应在查询前校验当前登录用户是否与目标 user_id 匹配。例如先查出当前用户自己的 user_id，再与目标 user_id 对比。</p>
    <p>（3）未设置最小权限原则：系统在设计时没有遵循"用户只能访问自己的数据"这一基本原则。</p>

    <h4>2.1.4 攻击原理示意图</h4>
    <div class="code-block">正常访问：
  浏览器 → GET /profile?user_id=2 → 服务器查询ID=2 → 返回alice的资料 ✅

越权攻击：
  浏览器 → GET /profile?user_id=1 → 服务器查询ID=1 
  → 返回admin的资料！（越权成功！）❌
  
  【原因】服务器没有检查"当前登录的用户是alice(ID=2)"
  为什么能查到admin(ID=1)的资料</div>
</div>

<div class="page">
    <h3>2.2 漏洞2：业务逻辑漏洞（金额负值）</h3>
    <p class="red bold">风险等级：高危 | CWE-841：业务流程处理不当</p>

    <h4>2.2.1 漏洞位置</h4>
    <p>文件：app.py，路由 /recharge</p>
    <p>行号：约第918行</p>

    <h4>2.2.2 漏洞代码</h4>
    <div class="code-block">@app.route("/recharge", methods=["POST"])
@login_required
def recharge():
    # 充值 - 存在业务逻辑漏洞
    user_id = request.form.get("user_id", "")
    amount = request.form.get("amount", "0")
    
    # 【漏洞1】没有校验 amount 是否为正数
    # 攻击者可提交 amount=-100000 实现"反向扣款"
    
    # 【漏洞2】使用 f-string 拼接 SQL，存在SQL注入
    sql = f"UPDATE users SET balance = balance + {amount} WHERE id = {user_id}"
    c.execute(sql)</div>

    <h4>2.2.3 漏洞成因分析</h4>
    <p>（1）缺乏输入校验：开发者在设计充值功能时，默认地认为用户"只会"输入正数，而忘记了攻击者可以输入负数。这是典型的"信任用户输入"的安全误区。所有涉及金钱、积分、数量等数值型操作的接口，必须在服务端校验数值的范围和正负。</p>
    <p>（2）SQL语句拼接：使用 f-string 直接将 amount 拼接到 SQL 语句中，既存在SQL注入风险，又使得 amount 的值可以在 SQL 层面被执行任意操作。amount=-100000 会变成 balance = balance + -100000，相当于 balance = balance - 100000。</p>
    <p>（3）未使用参数化查询：参数化查询不仅防止SQL注入，也强制数据与代码分离，使数据库能够正确区分"数据"和"代码"。</p>
</div>

<!-- ============================================================
     三、攻击复现（POC）
     ============================================================ -->
<div class="page">
    <h2>三、攻击复现（POC）</h2>

    <h3>3.1 POC 1：IDOR越权攻击</h3>
    <h4>实验目标</h4>
    <p>以普通用户 alice 身份登录，通过修改URL参数查看管理员 admin 的个人信息。</p>

    <h4>实验步骤与结果</h4>
    <table>
        <tr><th style="width:8%">步骤</th><th style="width:37%">操作</th><th style="width:30%">请求</th><th style="width:25%">结果</th></tr>
        <tr>
            <td>1</td>
            <td>以alice身份登录系统</td>
            <td>POST /login<br>username=alice&password=alice2025</td>
            <td>登录成功，获取session</td>
        </tr>
        <tr>
            <td>2</td>
            <td>查看自己的个人中心</td>
            <td>GET /profile?user_id=2</td>
            <td class="green bold">正常显示alice的资料</td>
        </tr>
        <tr>
            <td>3</td>
            <td><strong>修改URL参数查看admin</strong></td>
            <td><strong>GET /profile?user_id=1</strong></td>
            <td class="red bold">⚠️ 成功看到admin的资料！<br>邮箱、手机号、余额全部泄露</td>
        </tr>
        <tr>
            <td>4</td>
            <td>遍历其他用户ID</td>
            <td>GET /profile?user_id=3<br>GET /profile?user_id=4</td>
            <td>可查看所有已注册用户的资料</td>
        </tr>
    </table>

    <h4>攻击结果</h4>
    <p>alice（普通用户，user_id=2）通过将URL参数从 user_id=2 修改为 user_id=1，成功获取了管理员 admin 的个人信息，包括邮箱（admin@example.com）、手机号（13800138000）和当前余额。本次攻击属于水平越权（同级别用户之间越权访问），若进一步结合其他漏洞，可升级为垂直越权（普通用户获取管理员权限）。</p>

    <h3>3.2 POC 2：业务逻辑漏洞攻击</h3>
    <h4>实验目标</h4>
    <p>利用充值接口未校验金额正负的缺陷，通过提交负值实现非预期扣款。</p>

    <h4>实验步骤与结果</h4>
    <table>
        <tr><th style="width:8%">步骤</th><th style="width:37%">操作</th><th style="width:30%">请求</th><th style="width:25%">余额变化</th></tr>
        <tr>
            <td>1</td>
            <td>查看admin当前余额</td>
            <td>GET /profile?user_id=1</td>
            <td>初始余额：99999</td>
        </tr>
        <tr>
            <td>2</td>
            <td>正常充值500元</td>
            <td>POST /recharge<br>user_id=1&amount=500</td>
            <td>99999 + 500 = 100499</td>
        </tr>
        <tr>
            <td>3</td>
            <td><strong>恶意提交负值-100000</strong></td>
            <td><strong>POST /recharge<br>user_id=1&amount=-100000</strong></td>
            <td class="red bold">⚠️ 100499 - 100000 = 499！<br>余额被"盗刷"扣除</td>
        </tr>
    </table>

    <h4>攻击结果</h4>
    <p>攻击者通过提交负值 amount=-100000，成功将admin账户的余额从100499减少到499。这在本质上相当于"盗刷"了系统10万元。如果攻击者反复利用此漏洞，可以将任意用户的余额清零甚至变为负数。与此同时，amount参数还存在SQL注入风险，攻击者可在amount中注入恶意SQL代码获取数据库完全控制权。</p>
</div>

<!-- ============================================================
     四、修复方案
     ============================================================ -->
<div class="page">
    <h2>四、修复方案</h2>

    <h3>4.1 修复IDOR漏洞</h3>
    <p><strong>核心修复原则：永远从服务端session获取用户身份，绝不信任客户端传入的用户标识。</strong></p>

    <h4>修复后代码</h4>
    <div class="code-block">@app.route("/profile")
@login_required
def profile():
    # 个人中心 - 已修复：从session获取用户
    # ✅ 从 session 获取当前登录的用户名
    # session中的数据由服务器签名，用户无法篡改
    username = session.get("username")
    
    # ✅ 根据用户名（不是user_id）查询用户信息
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    
    return render_template("profile.html", user=user)</div>

    <h4>修复要点</h4>
    <table>
        <tr><th style="width:8%">要点</th><th style="width:92%">说明</th></tr>
        <tr><td><strong>1</strong></td><td>删除从URL参数获取 user_id 的代码</td></tr>
        <tr><td><strong>2</strong></td><td>从 session 中获取当前已登录的用户身份</td></tr>
        <tr><td><strong>3</strong></td><td>用户只能查询自己的数据，无法通过修改参数越权</td></tr>
        <tr><td><strong>4</strong></td><td>后续如需扩展（如管理员查看所有用户），应单独增加角色校验</td></tr>
    </table>

    <h3>4.2 修复业务逻辑漏洞</h3>
    <p><strong>核心修复原则：所有涉及金钱的业务操作必须校验数值范围，且使用参数化查询。</strong></p>

    <h4>修复后代码</h4>
    <div class="code-block">@app.route("/recharge", methods=["POST"])
@login_required
def recharge():
    # 充值 - 已修复：校验金额+参数化查询
    # ✅ 从 session 获取当前用户
    username = session.get("username")
    amount = int(request.form.get("amount", "0"))
    
    # ✅ 修复1：校验金额必须为正数
    if amount <= 0:
        return "充值金额必须大于0"
    
    # ✅ 修复2：使用参数化查询防止SQL注入
    c.execute(
        "UPDATE users SET balance = balance + ? WHERE username = ?",
        (amount, username)
    )</div>
</div>

<!-- ============================================================
     五、修复前后代码对比
     ============================================================ -->
<div class="page">
    <h2>五、修复前后代码对比</h2>

    <h3>5.1 个人中心路由（/profile）对比</h3>
    <table>
        <tr><th style="width:12%">对比维度</th><th style="width:44%">修复前（存在漏洞）</th><th style="width:44%">修复后（安全）</th></tr>
        <tr>
            <td><strong>用户来源</strong></td>
            <td class="code">request.args.get("user_id")<br>← 从URL参数获取</td>
            <td class="code">session.get("username")<br>← 从服务器session获取</td>
        </tr>
        <tr>
            <td><strong>权限校验</strong></td>
            <td class="code">无任何权限校验<br>直接根据传入ID查询</td>
            <td class="code">自动权限隔离<br>只能查自己的数据</td>
        </tr>
        <tr>
            <td><strong>查询方式</strong></td>
            <td class="code">f"WHERE id = {user_id}"<br>← f-string拼接SQL</td>
            <td class="code">WHERE username = ?<br>← 参数化查询</td>
        </tr>
        <tr>
            <td><strong>攻击可能性</strong></td>
            <td class="code">修改user_id即可越权<br>注入SQL代码</td>
            <td class="code">无法越权<br>无法注入SQL</td>
        </tr>
    </table>

    <h3>5.2 充值路由（/recharge）对比</h3>
    <table>
        <tr><th style="width:12%">对比维度</th><th style="width:44%">修复前（存在漏洞）</th><th style="width:44%">修复后（安全）</th></tr>
        <tr>
            <td><strong>金额校验</strong></td>
            <td class="code">无校验<br>amount可直接为负</td>
            <td class="code">if amount <= 0: return错误<br>金额必须为正数</td>
        </tr>
        <tr>
            <td><strong>SQL语句</strong></td>
            <td class="code">f"balance + {amount}"<br>← f-string拼接</td>
            <td class="code">balance + ?<br>← 参数化查询</td>
        </tr>
        <tr>
            <td><strong>用户身份</strong></td>
            <td class="code">user_id从表单获取<br>可操作任意用户余额</td>
            <td class="code">username从session获取<br>只能操作自己的余额</td>
        </tr>
        <tr>
            <td><strong>攻击可能性</strong></td>
            <td class="code">amount=-99999扣余额<br>amount=1;DROP TABLE删库</td>
            <td class="code">无法负值操作<br>无法注入SQL</td>
        </tr>
    </table>
</div>

<!-- ============================================================
     六、修复后验证测试
     ============================================================ -->
<div class="page">
    <h2>六、修复后验证测试</h2>

    <h3>6.1 IDOR越权测试</h3>
    <table>
        <tr><th style="width:8%">序号</th><th style="width:25%">测试场景</th><th style="width:27%">测试操作</th><th style="width:20%">预期结果</th><th style="width:20%">实际结果</th></tr>
        <tr>
            <td>1</td>
            <td>alice查看自己的资料</td>
            <td>GET /profile</td>
            <td>显示alice的信息</td>
            <td class="green bold">[OK] 通过</td>
        </tr>
        <tr>
            <td>2</td>
            <td>alice尝试查看admin</td>
            <td>GET /profile?user_id=1</td>
            <td>仍显示alice的信息</td>
            <td class="green bold">[OK] 越权被拦截</td>
        </tr>
        <tr>
            <td>3</td>
            <td>alice尝试查看不存在的ID</td>
            <td>GET /profile?user_id=999</td>
            <td>仍显示alice的信息</td>
            <td class="green bold">[OK] 通过</td>
        </tr>
        <tr>
            <td>4</td>
            <td>admin查看自己的资料</td>
            <td>GET /profile</td>
            <td>显示admin的信息</td>
            <td class="green bold">[OK] 通过</td>
        </tr>
        <tr>
            <td>5</td>
            <td>未登录访问/profile</td>
            <td>GET /profile（无Cookie）</td>
            <td>重定向到登录页</td>
            <td class="green bold">[OK] 通过</td>
        </tr>
    </table>

    <h3>6.2 业务逻辑测试</h3>
    <table>
        <tr><th style="width:8%">序号</th><th style="width:25%">测试场景</th><th style="width:27%">测试操作</th><th style="width:20%">预期结果</th><th style="width:20%">实际结果</th></tr>
        <tr>
            <td>1</td>
            <td>正常充值100元</td>
            <td>POST amount=100</td>
            <td>余额增加100</td>
            <td class="green bold">[OK] 通过</td>
        </tr>
        <tr>
            <td>2</td>
            <td>负值充值</td>
            <td>POST amount=-99999</td>
            <td>报错：金额必须大于0</td>
            <td class="green bold">[OK] 被拦截</td>
        </tr>
        <tr>
            <td>3</td>
            <td>零值充值</td>
            <td>POST amount=0</td>
            <td>报错：金额必须大于0</td>
            <td class="green bold">[OK] 被拦截</td>
        </tr>
        <tr>
            <td>4</td>
            <td>超长字符串</td>
            <td>POST amount=abc</td>
            <td>报错：金额格式错误</td>
            <td class="green bold">[OK] 被拦截</td>
        </tr>
        <tr>
            <td>5</td>
            <td>SQL注入尝试</td>
            <td>POST amount=1;DROP TABLE</td>
            <td>参数化查询拦截</td>
            <td class="green bold">[OK] 安全</td>
        </tr>
    </table>
</div>

<!-- ============================================================
     七、总结与安全开发指南
     ============================================================ -->
<div class="page">
    <h2>七、总结与安全开发指南</h2>

    <h3>7.1 漏洞归纳</h3>
    <table>
        <tr><th>漏洞类型</th><th>OWASP Top 10</th><th>CWE编号</th><th>根因</th><th>攻击难度</th><th>危害等级</th></tr>
        <tr>
            <td>IDOR/水平越权</td>
            <td>A01:2021 访问控制失效</td>
            <td>CWE-639</td>
            <td>信任前端传入的用户ID</td>
            <td>极低（改URL即可）</td>
            <td class="red bold">高危</td>
        </tr>
        <tr>
            <td>业务逻辑漏洞</td>
            <td>A01:2021 访问控制失效</td>
            <td>CWE-841</td>
            <td>未校验金额正负</td>
            <td>极低（改表单值即可）</td>
            <td class="red bold">高危</td>
        </tr>
    </table>

    <h3>7.2 安全开发五原则</h3>
    <table>
        <tr><th style="width:8%">原则</th><th style="width:22%">名称</th><th style="width:70%">说明</th></tr>
        <tr>
            <td><strong>1</strong></td>
            <td><strong>永不信任用户输入</strong></td>
            <td>URL参数、表单数据、Cookie、HTTP头等所有客户端传入的数据均不可信，必须在服务端进行校验</td>
        </tr>
        <tr>
            <td><strong>2</strong></td>
            <td><strong>服务端身份验证</strong></td>
            <td>用户身份应从 Session/Token 中获取，session数据由服务器签名保护，用户无法篡改</td>
        </tr>
        <tr>
            <td><strong>3</strong></td>
            <td><strong>业务参数校验</strong></td>
            <td>金额、数量、积分等数值型业务数据，必须校验其范围（>0、<=最大值等）和格式</td>
        </tr>
        <tr>
            <td><strong>4</strong></td>
            <td><strong>最小权限原则</strong></td>
            <td>用户只能操作属于自己的数据。每个请求在处理前，都应验证发起者是否有权执行该操作</td>
        </tr>
        <tr>
            <td><strong>5</strong></td>
            <td><strong>参数化查询</strong></td>
            <td>所有数据库操作必须使用参数化查询（Prepared Statement），杜绝任何形式的字符串拼接</td>
        </tr>
    </table>

    <h3>7.3 本次修复涉及的文件清单</h3>
    <table>
        <tr><th>文件路径</th><th>修改内容</th><th>行数变化</th></tr>
        <tr><td>app.py</td><td>/profile路由重写（session替换URL参数）；/recharge增加金额校验和参数化查询</td><td>+30行</td></tr>
        <tr><td>templates/profile.html</td><td>移除user_id隐藏字段</td><td>-1行</td></tr>
        <tr><td>templates/base.html</td><td>导航栏链接从/profile?user_id=1改为/profile</td><td>0行</td></tr>
        <tr><td>templates/index.html</td><td>首页快捷入口链接修改</td><td>0行</td></tr>
    </table>

    <h3>7.4 学习心得</h3>
    <p>通过本次实验，我深刻认识到：安全漏洞并不总是需要高深的技术才能利用。IDOR漏洞只需要修改URL中的一个数字，业务逻辑漏洞只需要在表单中填一个负数——这些操作任何普通用户都能做到。真正的安全防线在于开发者的安全意识：永远假设用户会做最坏的操作，永远在服务端做最严格的校验。</p>
    <p>权限提升和业务逻辑漏洞的修复并不复杂，但它们暴露出的问题——"信任用户输入"和"缺乏权限校验"——却是Web安全中最常见也最危险的设计缺陷。在后续的开发中，我会将"权限校验"和"输入校验"作为每个接口的必选步骤，而不是可有可无的附加项。</p>

    <br>
    <hr style="border: none; border-top: 1px solid #2980b9; width: 60%; margin: 8mm auto;">
    <p style="text-align: center; color: #95a5a6; text-indent: 0;">&mdash; 报告完 &mdash;</p>
    <p style="text-align: center; color: #bbb; font-size: 8pt; text-indent: 0;">报告日期: 2026-07-10 | 课程: 权限提升与业务逻辑漏洞修复 | 安全标准: OWASP Top 10 (2021) A01</p>
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
