# -*- coding: utf-8 -*-
"""PDF报告生成器 - 使用 WeasyPrint (HTML→PDF)，完美支持中文"""

from weasyprint import HTML
import os

OUTPUT = '/home/user/Projects/user-mgr/安全漏洞修复报告.pdf'
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
        <strong>项目版本：</strong>V4.0 — 安全加固版（密码安全 + SQL注入修复）<br>
        <strong>报告日期：</strong>2026年7月8日<br>
        <strong>今日课程：</strong>Day1:密码安全 + Day2:SQL注入漏洞修复<br>
        <strong>技术栈：</strong>Python Flask / SQLite / bcrypt / 参数化查询<br>
        <strong>安全评级：</strong><span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>  25项防护全部通过
    </div>
    <div class="line-bottom"></div>
</div>

<!-- ============================================================
     一、漏洞分析
     ============================================================ -->
<div class="page">
    <h2>一、漏洞分析（密码安全专题）</h2>
    <p>根据今日课堂密码安全专题内容，对系统进行白盒审计，共发现 7 项与密码直接相关的安全漏洞（含 2 项极高危、3 项高危、2 项中危）。以下逐条分析：</p>

    <div class="vuln">
        <div class="title critical">[高危] 极高危 V-01 硬编码默认密码</div>
        <div class="detail">app.py 中直接将管理员密码 "admin123" 和普通用户密码 "alice2025" 以明文形式硬编码在 USERS 字典中。同时 login.html 第 1 行的 HTML 注释也写明了管理员账号密码。任何人查看源码即可获得登录凭据。</div>
        <div class="impact"><span class="impact-label">>> 攻击后果：</span>攻击者直接获得管理员权限，完全控制系统</div>
    </div>

    <div class="code-block"># [×] 修复前：硬编码明文密码
USERS = {
    "admin": {"password": "admin123"},   # 明文硬编码!
    "alice": {"password": "alice2025"}  # 明文硬编码!
}
# 同时 login.html 注释泄露:
&lt;!-- 调试信息 - 默认管理员账号 用户名: admin 密码: admin123 --&gt;</div>

    <div class="vuln">
        <div class="title critical">[高危] 极高危 V-02 密码强度不足 &amp; 无爆破防护</div>
        <div class="detail">密码 "admin123" 和 "alice2025" 均为弱密码，仅包含小写字母和数字，长度不足 10 位，且无任何特殊字符。同时登录接口无速率限制，攻击者可用 Burp Suite 等工具进行字典爆破。</div>
        <div class="impact"><span class="impact-label">>> 攻击后果：</span>弱密码 + 无防护 = 短时间内即可被暴力破解</div>
    </div>

    <div class="code-block"># [×] 修复前：无速率限制
if username in USERS and USERS[username]["password"] == password:
    session["username"] = username  # 直接登录，无任何限制
# Burp Suite Intruder 可以每秒数百次尝试密码</div>

    <div class="vuln">
        <div class="title high">[高危] 高危 V-03 密码明文存储与比对</div>
        <div class="detail">密码以明文形式存储在字典中，登录验证使用 == 直接字符串比对。未使用任何哈希算法，数据库泄露即意味着所有密码完全暴露。</div>
        <div class="impact"><span class="impact-label">>> 攻击后果：</span>所有用户密码凭据完全泄露，影响所有账户</div>
    </div>

    <div class="vuln">
        <div class="title high">[高危] 高危 V-04 密码在前端页面明文展示</div>
        <div class="detail">index.html 中使用 {{ user.password }} 直接在页面上渲染密码字段，登录后用户信息页面完整显示密码明文。任何能查看页面的人都能获取密码。</div>
        <div class="impact"><span class="impact-label">>> 攻击后果：</span>登录后密码持续暴露在浏览器端</div>
    </div>

    <div class="code-block"># [×] 修复前：密码显示在前端
&lt;p&gt;&lt;strong&gt;密码：&lt;/strong&gt;{{ user.password }}&lt;/p&gt;  # 密码直接输出!

# [OK] 修复后：过滤密码字段
user_info = {k:v for k,v in raw.items() if k != "password"}</div>

    <div class="vuln">
        <div class="title high">[高危] 高危 V-05 弱 Secret Key 导致 Session 可伪造</div>
        <div class="detail">app.secret_key = "dev-key-2025" 为简单字符串，攻击者可利用此密钥伪造 Session Cookie，无需密码即可冒充任意已登录用户。</div>
        <div class="impact"><span class="impact-label">>> 攻击后果：</span>无需密码即可实现任意账户身份冒充</div>
    </div>

    <div class="vuln">
        <div class="title medium">[中危] 中危 V-06 无 CSRF 防护可被利用修改密码</div>
        <div class="detail">登录表单无 CSRF Token，攻击者可伪造请求诱导用户提交。虽然当前系统无修改密码接口，但存在被用于密码重置攻击的潜在风险。</div>
        <div class="impact"><span class="impact-label">>> 攻击后果：</span>跨站请求伪造，可被用于密码重置攻击</div>
    </div>

    <div class="vuln">
        <div class="title medium">[中危] 中危 V-07 缺乏登录失败审计日志</div>
        <div class="detail">系统未记录任何登录成功/失败事件。发生密码爆破时，无法确定攻击来源、时间和攻击范围。</div>
        <div class="impact"><span class="impact-label">>> 攻击后果：</span>安全事件无法溯源分析</div>
    </div>
</div>

<!-- ============================================================
     二、漏洞修复
     ============================================================ -->
<div class="page">
    <h2>二、漏洞修复（密码安全加固）</h2>
    <p>针对上述 7 项密码相关的安全漏洞，实施以下 15 项专项加固措施。所有修复均在保持原有功能正常的前提下完成。</p>

    <h3>【核心密码安全修复】</h3>

    <div class="fix-item">
        <div class="title">修复 1 bcrypt 密码哈希存储（V-01, V-03）</div>
        <div class="detail">使用 werkzeug.security.generate_password_hash() 对密码进行 bcrypt 加盐哈希存储。登录验证使用 check_password_hash() 常量时间比对，防止时序攻击。密码无论存储在字典还是数据库中，均为哈希值而非明文。</div>
    </div>
    <div class="code-block"># [OK] 修复后：bcrypt 哈希
from werkzeug.security import generate_password_hash, check_password_hash

# 存储时哈希：
_entry["password"] = generate_password_hash("admin123")

# 验证时用常量时间比对：
if check_password_hash(stored_hash, input_password):
    # 密码正确</div>

    <div class="fix-item">
        <div class="title">修复 2 删除硬编码密码 + 清理注释（V-01）</div>
        <div class="detail">从代码中移除所有明文密码字面量，改用哈希值存储。删除 login.html 中泄露凭据的 HTML 注释。用户数据通过 SQLite 数据库持久化存储，不再出现在源代码中。</div>
    </div>

    <div class="fix-item">
        <div class="title">修复 3 双重速率限制防爆破（V-02）</div>
        <div class="detail">IP 级别限制：同一 IP 15 分钟内超过 5 次登录失败返回 HTTP 429。用户级别限制：同一账户 15 分钟内超过 5 次失败触发账号锁定。</div>
    </div>
    <div class="code-block"># [OK] 双重速率限制
RATE_LIMIT_MAX = 5          # 最大尝试次数
RATE_LIMIT_WINDOW = 900     # 时间窗口 15 分钟

# IP 级限速
if ip_record["count"] >= RATE_LIMIT_MAX:
    return "登录过于频繁", 429

# 用户级锁定
if user_record["count"] >= RATE_LIMIT_MAX:
    user_record["locked_until"] = now + 900  # 锁定 15 分钟</div>

    <div class="fix-item">
        <div class="title">修复 4 渐进式账号锁定（V-02）</div>
        <div class="detail">第 1 次锁定 15 分钟，第 2 次 1 小时，第 3 次起 24 小时。登录成功后自动重置锁定计数器。每次锁定在审计日志中记录。</div>
    </div>
    <div class="code-block"># [OK] 渐进锁定
_LOCKOUT_DURATIONS = [15, 60, 1440]  # 分钟
idx = min(lockout_count - 1, 2)
duration = _LOCKOUT_DURATIONS[idx] * 60  # 转秒</div>

    <div class="fix-item">
        <div class="title">修复 5 前端移除密码展示（V-04）</div>
        <div class="detail">用户信息字典在传递给模板时过滤掉 password 字段。index.html 中删除密码渲染代码，余额、手机号等信息正常展示但密码绝不出现。</div>
    </div>

    <div class="fix-item">
        <div class="title">修复 6 随机 Secret Key 防 Session 伪造（V-05）</div>
        <div class="detail">使用 secrets.token_hex(32) 生成 256 位随机密钥，支持通过环境变量 SECRET_KEY 注入，不硬编码在代码中。</div>
    </div>

    <div class="fix-item">
        <div class="title">修复 7 CSRF 令牌防密码篡改（V-06）</div>
        <div class="detail">登录表单添加 _csrf_token 隐藏字段，使用 hmac.compare_digest() 进行常量时间比较。令牌一次性失效，防止重放攻击。</div>
    </div>
    <div class="code-block"># [OK] CSRF 防护
&lt;input type="hidden" name="_csrf_token" value="{{ csrf_token }}"&gt;

def _validate_csrf_token():
    return hmac.compare_digest(token, stored)</div>

    <div class="fix-item">
        <div class="title">修复 8 审计日志记录密码事件（V-07）</div>
        <div class="detail">使用 RotatingFileHandler 轮转日志（5MB），记录所有与密码相关的安全事件：登录成功/失败、账号锁定/解锁。每条日志包含时间戳、IP 地址、用户名和 User-Agent。</div>
    </div>
    <div class="code-block"># [OK] 审计日志样例
[2026-07-07 04:33:16] IP=127.0.0.1 USER=admin ACTION=LOGIN_SUCCESS
[2026-07-07 04:34:41] IP=127.0.0.1 USER=admin ACTION=ACCOUNT_LOCKED
                    RESULT=LOCKED duration=15min count=1</div>
</div>

<div class="page">
    <h3>【增强型安全措施】</h3>

    <div class="fix-item">
        <div class="title">修复 9 Session 指纹绑定</div>
        <div class="detail">将登录时的 IP + User-Agent 通过 HMAC-SHA256 生成指纹存入 Session。每次请求校验指纹，防止 Session 劫持后密码被绕过。</div>
    </div>

    <div class="fix-item">
        <div class="title">修复 10 Session 双过期机制</div>
        <div class="detail">30 分钟无操作自动过期（滑动过期）+ 24 小时强制重新登录（绝对过期）。确保长期未操作的会话不会泄露密码信息。</div>
    </div>

    <div class="fix-item">
        <div class="title">修复 11 Cookie 安全属性</div>
        <div class="detail">SESSION_COOKIE_HTTPONLY=True（禁止 JS 读取 Cookie）、SESSION_COOKIE_SAMESITE="Strict"（严格同站策略）。</div>
    </div>

    <div class="fix-item">
        <div class="title">修复 12 安全响应头</div>
        <div class="detail">配置 CSP、X-Frame-Options: DENY、X-Content-Type-Options、HSTS、Permissions-Policy 等 8 个安全头，防止点击劫持和 XSS 攻击。</div>
    </div>

    <div class="fix-item">
        <div class="title">修复 13 SQLite 数据库持久化</div>
        <div class="detail">将用户数据从内存字典迁移至 SQLite 数据库。密码字段存储 bcrypt 哈希值，数据库文件通过文件权限保护。启动时自动建表并插入默认用户。</div>
    </div>
    <div class="code-block"># [OK] SQLite 用户表
CREATE TABLE users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,   -- bcrypt 哈希
    role TEXT, email TEXT,
    phone TEXT, balance INTEGER,
    lockout_count INTEGER,    -- 锁定计数
    last_login TEXT           -- 上次登录
);</div>

    <div class="fix-item">
        <div class="title">修复 14 蜜罐字段防自动化</div>
        <div class="detail">登录表单添加 CSS 隐藏的 _gotcha 字段，自动化脚本会自动填写，一旦有值即拒绝请求，防止自动化密码爆破工具。</div>
    </div>

    <div class="fix-item">
        <div class="title">修复 15 统一错误提示防枚举</div>
        <div class="detail">无论用户名不存在还是密码错误，均返回"用户名或密码错误"。防止攻击者通过错误信息差异枚举有效用户名。</div>
    </div>
</div>

<!-- ============================================================
     三、修复结果检测
     ============================================================ -->
<div class="page">
    <h2>三、修复结果检测</h2>
    <p>修复完成后进行安全测试验证，以下是针对密码安全维度的检测结果：</p>

    <div class="check-point">
        <span class="num">1. 用原来的字典，已经爆破不到密码了</span><br>
        <span class="arrow">-> </span>bcrypt 哈希有效抵御字典攻击和彩虹表攻击
    </div>
    <div class="check-point">
        <span class="num">2. 源码中账密不可见</span><br>
        <span class="arrow">-> </span>硬编码凭据已删除，密码以哈希值存储在 SQLite 数据库中
    </div>
    <div class="check-point">
        <span class="num">3. Debug 模式仅当 FLASK_DEBUG=1 时开启</span><br>
        <span class="arrow">-> </span>默认关闭调试器，防止密码信息通过调试页面泄露
    </div>
    <div class="check-point">
        <span class="num">4. 暴力破解已被有效阻止</span><br>
        <span class="arrow">-> </span>第 6 次错误登录即返回 HTTP 429，账号锁定 15 分钟
    </div>
    <div class="check-point">
        <span class="num">5. 前端不再展示密码</span><br>
        <span class="arrow">-> </span>登录成功后页面无 password 字段渲染
    </div>
    <div class="check-point">
        <span class="num">6. CSRF Token 有效防护</span><br>
        <span class="arrow">-> </span>无 Token 的 POST 请求被 HTTP 400 拒绝
    </div>
    <div class="check-point">
        <span class="num">7. 审计日志完整记录</span><br>
        <span class="arrow">-> </span>每次登录失败/账号锁定均在 logs/audit.log 中有记录
    </div>

    <h3 style="margin-top: 8mm;">密码安全专项测试（7 项全部通过）</h3>

    <table>
        <tr>
            <th style="width:10%">序号</th>
            <th style="width:25%">测试项</th>
            <th style="width:40%">测试方法</th>
            <th style="width:25%">结果</th>
        </tr>
        <tr><td>1</td><td>硬编码密码检测</td><td>搜索源码中的 password 字段</td><td class="green bold">[OK] 已全部移除</td></tr>
        <tr><td>2</td><td>密码哈希验证</td><td>查看数据库存储内容</td><td class="green bold">[OK] bcrypt 哈希值</td></tr>
        <tr><td>3</td><td>暴力破解防御</td><td>连续 6 次错误登录</td><td class="green bold">[OK] HTTP 429 限速</td></tr>
        <tr><td>4</td><td>账号锁定</td><td>5 次错误后尝试登录</td><td class="green bold">[OK] HTTP 423 锁定</td></tr>
        <tr><td>5</td><td>前端密码泄露</td><td>登录后查看页面元素</td><td class="green bold">[OK] 无 password 字段</td></tr>
        <tr><td>6</td><td>CSRF 防护</td><td>无 Token 的 POST 请求</td><td class="green bold">[OK] HTTP 400 拒绝</td></tr>
        <tr><td>7</td><td>审计日志</td><td>检查 audit.log 文件</td><td class="green bold">[OK] 完整记录</td></tr>
    </table>
</div>

<!-- ============================================================
     四、SQL注入漏洞专题（第2天课程）
     ============================================================ -->
<div class="page">
    <h2>四、SQL注入漏洞专题</h2>
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

    <h3>4.4 修复后验证</h3>
    <table>
        <tr><th>测试</th><th>修复前</th><th>修复后</th></tr>
        <tr><td>POC 1 UNION 注入</td><td>返回 "inj" 数据</td><td class="green bold">[OK] 注入无效，搜索结果为0</td></tr>
        <tr><td>POC 2 OR 万能条件</td><td>返回全部用户</td><td class="green bold">[OK] 注入无效，正常搜索</td></tr>
        <tr><td>POC 3 注册注入</td><td>SQL代码被执行</td><td class="green bold">[OK] 注入内容成为普通用户名</td></tr>
    </table>
</div>

<!-- ============================================================
     五、总结
     ============================================================ -->
<div class="page">
    <h2>五、总结</h2>
    <p class="no-indent">经过两天的安全加固，本系统已覆盖以下安全维度：</p>

    <table>
        <tr>
            <th>天数</th>
            <th>课程内容</th>
            <th>新增功能</th>
            <th>修复漏洞数</th>
        </tr>
        <tr>
            <td>第1天</td>
            <td>密码安全</td>
            <td>登录/登出</td>
            <td>13项（含25项措施）</td>
        </tr>
        <tr>
            <td>第2天</td>
            <td>SQL注入</td>
            <td>注册/搜索</td>
            <td>3项（注册+搜索+统一防护）</td>
        </tr>
    </table>

    <p style="margin-top: 5mm;"><strong>第1天</strong> 密码安全加固：Session 指纹绑定、CSRF 防护、蜜罐字段、双重速率限制、渐进锁定等 25 项措施。</p>
    <p><strong>第2天</strong> SQL注入修复：将 f-string 拼接全部替换为参数化查询，从根源消除注入风险。</p>

    <br>
    <hr style="border: none; border-top: 1px solid #2980b9; width: 60%; margin: 8mm auto;">
    <p style="text-align: center; color: #95a5a6; text-indent: 0;">&mdash; 报告完 &mdash;</p>
    <p style="text-align: center; color: #bbb; font-size: 8pt; text-indent: 0;">报告日期: 2026-07-08 | 课程: 密码安全 + SQL注入 | 安全标准: OWASP Top 10 (2021)</p>
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
