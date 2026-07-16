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
        <strong>项目版本：</strong>V9.0 - SSRF服务端请求伪造专题<br>
        <strong>报告日期：</strong>2026年7月15日<br>
        <strong>今日课程：</strong>Day7:SSRF服务端请求伪造漏洞深度解析<br>
        <strong>技术栈：</strong>Python Flask / urllib / SSRF / file://协议 / 内网渗透<br>
    </div>
    <div class="line-bottom"></div>
</div>

<div class="page">
    <h2>一、课程背景</h2>
    <p>SSRF(Server-Side Request Forgery，服务端请求伪造)是OWASP Top 10 2021中A10:2021服务端请求伪造类别的重要漏洞类型。SSRF漏洞的核心成因是：服务器在处理用户输入的URL时，未对目标地址做充分的校验和限制，导致攻击者可以利用服务器作为跳板，发起对内网资源的攻击。</p>
    <p>SSRF漏洞之所以危害巨大，是因为它绕过了防火墙的限制。通常情况下，外网攻击者无法直接访问内网服务（如127.0.0.1、10.x.x.x等内网IP），但存在SSRF漏洞的服务器同时拥有外网和内网访问能力，攻击者通过它就可以间接打入内网。</p>

    <h3>1.1 SSRF攻击原理示意图</h3>
    <div class="code-block">攻击者                   存在SSRF的服务器                内网服务
   │                          │                          │
   │  POST /fetch-url          │                          │
   │  url=http://127.0.0.1:80  │                          │
   │─────────────────────────>│                          │
   │                          │  攻击者无法直接访问       │
   │                          │  但服务器可以！           │
   │                          │ ───────────────────────> │
   │                          │                          │
   │                          │ <─────────────────────── │
   │ 返回内网服务的内容        │                          │
   │<─────────────────────────│                          │
   │                          │                          │
   └─ 攻击者通过SSRF成功访问了本机Web服务 ┘</div>

    <h3>1.2 本次新增功能</h3>
    <table>
        <tr><th>功能</th><th>路由</th><th>参数</th><th>说明</th></tr>
        <tr><td>URL抓取</td><td>/fetch-url</td><td>url</td><td>用户提交URL，服务端抓取并返回内容(5000字符限制)</td></tr>
    </table>
</div>

<div class="page">
    <h2>二、漏洞代码分析</h2>

    <h3>2.1 漏洞代码定位</h3>
    <p>文件：app.py，路由 /fetch-url，约第1130行</p>

    <div class="code-block">@app.route("/fetch-url", methods=["POST"])
@login_required
def fetch_url():
    target_url = request.form.get("url", "")
    
    # 【漏洞1】没有校验URL协议
    # 允许 file://、dict://、gopher:// 等危险协议
    
    # 【漏洞2】没有校验目标IP
    # 允许访问 127.0.0.1、10.x.x.x、192.168.x.x 等内网地址
    
    # 【漏洞3】没有做DNS解析校验
    # 攻击者可以用域名指向内网IP绕过简单的IP黑名单
    
    resp = urllib.request.urlopen(target_url, timeout=10)
    content = resp.read()
    return content</div>

    <h3>2.2 漏洞成因分析</h3>
    <table>
        <tr><th style="width:8%">编号</th><th style="width:22%">漏洞</th><th style="width:35%">风险说明</th><th style="width:35%">攻击利用方式</th></tr>
        <tr>
            <td><strong>1</strong></td>
            <td>协议无限制</td>
            <td>允许file://协议读取本地任意文件<br>允许dict://协议操作Redis等</td>
            <td>file:///etc/passwd 读取系统密码文件<br>file:///proc/self/environ 读取环境变量</td>
        </tr>
        <tr>
            <td><strong>2</strong></td>
            <td>内网无限制</td>
            <td>可访问本机和内网所有服务<br>绕过防火墙限制</td>
            <td>http://127.0.0.1:5000 访问本机Web<br>http://10.x.x.x:3306 扫描内网MySQL</td>
        </tr>
        <tr>
            <td><strong>3</strong></td>
            <td>URL无过滤</td>
            <td>可使用重定向绕过简易黑名单</td>
            <td>利用短链接跳转到内网地址<br>利用DNS rebinding绕过IP检查</td>
        </tr>
    </table>
</div>

<div class="page">
    <h2>三、攻击复现（POC）</h2>

    <h3>3.1 POC 1：正常URL抓取</h3>
    <p>作为对照基准，先测试正常的外部网站访问：</p>
    <div class="code-block">请求：
POST /fetch-url
url=http://www.baidu.com

响应：
状态码: 200
内容: 百度首页的HTML代码
（说明：URL抓取功能正常工作）</div>

    <h3>3.2 POC 2：SSRF内网服务扫描</h3>
    <p>攻击者通过SSRF扫描本机开放端口，探测内网服务：</p>
    <div class="code-block">请求1：POST /fetch-url  url=http://127.0.0.1:5000/
结果：状态码 200，抓取到本机Web首页 ✅
说明：SSRF成功！外网攻击者无法直接访问127.0.0.1
      但通过SSRF可以访问本机的Web服务

请求2：POST /fetch-url  url=http://127.0.0.1:3306
结果：连接失败（MySQL不返回HTTP）
说明：通过超时/报错信息判断端口是否开放

请求3：POST /fetch-url  url=http://10.133.25.156:5000/
结果：状态码 200，抓取到内网Web页面
说明：SSRF可访问同网段其他服务</div>

    <h3>3.3 POC 3：file://协议读取系统文件</h3>
    <p>最危险的SSRF攻击方式——利用file://协议直接读取服务器文件：</p>
    <div class="code-block">请求：POST /fetch-url  url=file:///etc/passwd

响应：
状态码: 200
内容:
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
...

说明：成功读取到服务器系统密码文件！
攻击者可进一步尝试读取：
- /etc/shadow      → 密码哈希值
- /root/.bash_history → 命令历史
- /etc/nginx/nginx.conf → 服务器配置
- /root/.ssh/id_rsa   → SSH私钥</div>
</div>

<div class="page">
    <h2>四、SSRF高级攻击场景</h2>

    <h3>4.1 云服务器元数据攻击</h3>
    <p>如果服务器部署在云平台（AWS、阿里云、腾讯云等），SSRF可以读取云服务器的元数据，获取临时访问凭证：</p>
    <div class="code-block">// AWS云元数据
http://169.254.169.254/latest/meta-data/
http://169.254.169.254/latest/meta-data/iam/security-credentials/admin

// 阿里云元数据
http://100.100.100.200/latest/meta-data/
http://100.100.100.200/ram/security-credentials/

// 腾讯云元数据
http://metadata.tencentyun.com/latest/meta-data/</div>

    <h3>4.2 内网服务攻击</h3>
    <div class="code-block">// Redis未授权访问
url=http://127.0.0.1:6379

// Elasticsearch
url=http://127.0.0.1:9200/_cat/indices

// Docker API
url=http://127.0.0.1:2375/containers/json

// MySQL
url=http://127.0.0.1:3306</div>

    <h3>4.3 SSRF结合其它漏洞</h3>
    <table>
        <tr><th>组合攻击</th><th>说明</th><th>严重程度</th></tr>
        <tr><td>SSRF + file://</td><td>读取服务器敏感文件（密码、密钥、配置）</td><td class="red bold">极高</td></tr>
        <tr><td>SSRF + Redis</td><td>利用gopher://协议攻击内网Redis，写入SSH密钥</td><td class="red bold">极高</td></tr>
        <tr><td>SSRF + 云元数据</td><td>获取云平台临时凭证，控制整个云账号</td><td class="red bold">极高</td></tr>
        <tr><td>SSRF + 端口扫描</td><td>扫描内网开放端口，绘制内网拓扑</td><td class="red bold">高</td></tr>
    </table>
</div>

<div class="page">
    <h2>五、修复方案</h2>

    <h3>5.1 方案一：协议白名单</h3>
    <p>严格限制允许访问的URL协议，杜绝file://等危险协议：</p>
    <div class="code-block">from urllib.parse import urlparse

ALLOWED_SCHEMES = {"http", "https"}

def validate_url(url):
    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError("不支持的协议类型")
    return True</div>

    <h3>5.2 方案二：内网IP黑名单</h3>
    <p>DNS解析后检查目标IP是否为内网地址：</p>
    <div class="code-block">import socket
import ipaddress

PRIVATE_RANGES = [
    ipaddress.IPv4Network("127.0.0.0/8"),     # 本机回环
    ipaddress.IPv4Network("10.0.0.0/8"),      # 10段内网
    ipaddress.IPv4Network("172.16.0.0/12"),   # 172段内网
    ipaddress.IPv4Network("192.168.0.0/16"),  # 192.168段内网
    ipaddress.IPv4Network("169.254.0.0/16"),  # 云元数据
    ipaddress.IPv4Network("100.64.0.0/10"),   # 运营商级NAT
]

def check_ip(target_url):
    parsed = urlparse(target_url)
    host = socket.gethostbyname(parsed.hostname)
    for r in PRIVATE_RANGES:
        if ipaddress.IPv4Address(host) in r:
            raise ValueError("禁止访问内网地址")
    return True</div>

    <h3>5.3 方案三：URL域名白名单</h3>
    <div class="code-block">ALLOWED_DOMAINS = [
    "example.com",
    "api.example.com",
    "www.safe-site.com",
]

def check_domain(target_url):
    parsed = urlparse(target_url)
    domain = parsed.hostname
    if domain not in ALLOWED_DOMAINS:
        raise ValueError("不允许访问的域名")
    return True</div>

    <h3>5.4 修复前后对比</h3>
    <table>
        <tr><th style="width:12%">对比项</th><th style="width:44%">修复前</th><th style="width:44%">修复后</th></tr>
        <tr>
            <td><strong>协议限制</strong></td>
            <td>无限制，file://、dict://等均可使用</td>
            <td>仅允许 http:// 和 https://</td>
        </tr>
        <tr>
            <td><strong>内网IP</strong></td>
            <td>无限制，可访问127.0.0.1、10.x.x.x等</td>
            <td>DNS解析后检查IP，禁止内网地址</td>
        </tr>
        <tr>
            <td><strong>域名验证</strong></td>
            <td>不验证域名</td>
            <td>通过白名单或正则校验域名</td>
        </tr>
        <tr>
            <td><strong>重定向</strong></td>
            <td>不限制重定向</td>
            <td>限制重定向次数或检查重定向目标</td>
        </tr>
        <tr>
            <td><strong>内容长度</strong></td>
            <td>5000字符限制</td>
            <td>5000字符限制（保留）</td>
        </tr>
    </table>
</div>

<div class="page">
    <h2>六、修复后验证测试</h2>

    <table>
        <tr><th style="width:8%">序号</th><th style="width:25%">测试场景</th><th style="width:32%">测试请求</th><th style="width:15%">修复前</th><th style="width:20%">修复后</th></tr>
        <tr>
            <td>1</td>
            <td>正常外部网站</td>
            <td>url=http://www.baidu.com</td>
            <td>状态码200</td>
            <td class="green bold">[OK] 状态码200</td>
        </tr>
        <tr>
            <td>2</td>
            <td>本机Web服务</td>
            <td>url=http://127.0.0.1:5000/</td>
            <td class="red bold">成功抓取</td>
            <td class="green bold">[OK] 禁止内网</td>
        </tr>
        <tr>
            <td>3</td>
            <td>读取系统文件</td>
            <td>url=file:///etc/passwd</td>
            <td class="red bold">读取成功</td>
            <td class="green bold">[OK] 协议不允许</td>
        </tr>
        <tr>
            <td>4</td>
            <td>内网段扫描</td>
            <td>url=http://10.133.25.1:5000/</td>
            <td class="red bold">可探测</td>
            <td class="green bold">[OK] 禁止内网</td>
        </tr>
        <tr>
            <td>5</td>
            <td>云元数据</td>
            <td>url=http://169.254.169.254/</td>
            <td class="red bold">可访问</td>
            <td class="green bold">[OK] 禁止内网</td>
        </tr>
        <tr>
            <td>6</td>
            <td>未登录访问</td>
            <td>无Cookie请求</td>
            <td>跳转登录</td>
            <td class="green bold">[OK] 跳转登录</td>
        </tr>
    </table>

    <h3>服务端日志记录</h3>
    <div class="code-block">[SSRF漏洞] 用户 admin 请求抓取URL: http://www.baidu.com
[SSRF漏洞] 抓取成功: http://www.baidu.com -> 状态码200

[SSRF漏洞] 用户 admin 请求抓取URL: http://127.0.0.1:5000/
[SSRF漏洞] 抓取成功: http://127.0.0.1:5000/ -> 状态码200

[SSRF漏洞] 用户 admin 请求抓取URL: file:///etc/passwd
[SSRF漏洞] 抓取成功: file:///etc/passwd -> 状态码200</div>
</div>

<div class="page">
    <h2>七、总结与安全开发指南</h2>

    <h3>7.1 漏洞归纳</h3>
    <table>
        <tr><th>漏洞类型</th><th>OWASP Top 10</th><th>根因</th><th>攻击难度</th><th>危害等级</th></tr>
        <tr>
            <td>SSRF</td>
            <td>A10:2021 SSRF</td>
            <td>未校验URL协议和目标IP</td>
            <td>低（提交恶意URL即可）</td>
            <td class="red bold">极高</td>
        </tr>
        <tr>
            <td>file://读取</td>
            <td>A10:2021 SSRF</td>
            <td>允许危险协议</td>
            <td>极低（直接改协议头）</td>
            <td class="red bold">极高</td>
        </tr>
    </table>

    <h3>7.2 SSRF防御六原则</h3>
    <table>
        <tr><th style="width:6%">#</th><th style="width:28%">原则</th><th style="width:66%">说明</th></tr>
        <tr><td><strong>1</strong></td><td>协议白名单</td><td>只允许 http/https，禁止 file://、dict://、gopher:// 等协议</td></tr>
        <tr><td><strong>2</strong></td><td>IP黑名单/白名单</td><td>DNS解析后检查目标IP，禁止访问内网地址和云元数据地址</td></tr>
        <tr><td><strong>3</strong></td><td>域名白名单</td><td>如果业务允许，限定只访问特定域名</td></tr>
        <tr><td><strong>4</strong></td><td>禁止重定向</td><td>关闭或限制自动重定向，防止跳转绕过</td></tr>
        <tr><td><strong>5</strong></td><td>最小响应原则</td><td>不对用户返回完整响应内容，仅返回必要数据</td></tr>
        <tr><td><strong>6</strong></td><td>使用安全库</td><td>使用成熟的HTTP客户端库，避免直接使用urllib的低级API</td></tr>
    </table>

    <h3>7.3 学习心得</h3>
    <p>通过本次SSRF漏洞实验，我深刻认识到：服务器发起的请求同样需要严格校验。许多开发者会关注用户输入的安全性问题（如SQL注入、XSS），却容易忽略"服务器作为客户端"时的安全风险。SSRF漏洞告诉我们，任何涉及URL处理的功能都必须假设用户会提交最恶意的输入——包括file://读系统文件、内网IP扫描、云元数据窃取等。</p>
    <p>修复SSRF的核心思路是"最小权限原则"：只给URL抓取功能最小的权限——只允许http/https协议、只允许访问公网IP、只返回必要的内容。层层设防，才能既保证业务功能正常，又防止被攻击者利用。</p>

    <br>
    <hr style="border: none; border-top: 1px solid #2980b9; width: 60%; margin: 8mm auto;">
    <p style="text-align: center; color: #95a5a6; text-indent: 0;">&mdash; 报告完 &mdash;</p>
    <p style="text-align: center; color: #bbb; font-size: 8pt; text-indent: 0;">报告日期: 2026-07-15 | 课程: SSRF服务端请求伪造漏洞修复 | 安全标准: OWASP A10:2021</p>
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
