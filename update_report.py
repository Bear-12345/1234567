# -*- coding: utf-8 -*-
"""Update PDF report for Day5 LFI/RFI"""
with open('/home/user/Projects/user-mgr/generate_pdf_report.py', 'r') as f:
    c = f.read()

start = c.find('<!-- ============================================================\n     封面')
end = c.find('</body>\n</html>')

new_body = '''<!-- ============================================================
     封面
     ============================================================ -->
<div class="page cover">
    <div class="line"></div>
    <h1>用户信息管理平台</h1>
    <div class="subtitle">安全漏洞挖掘与修复报告</div>
    <div class="url">http://10.133.25.94:5000</div>
    <hr class="divider">
    <div class="meta">
        <strong>项目版本：strong>V7.0 - 文件包含漏洞(LFI/RFI)专题<br>
        <strong>报告日期：strong>2026年7月11日<br>
        <strong>今日课程：strong>Day5:文件包含漏洞深度解析<br>
        <strong>技术栈：strong>Python Flask / LFI / RFI / 路径遍历<br>
    </div>
    <div class="line-bottom"></div>
</div>

<div class="page">
    <h2>一、课程背景</h2>
    <p>文件包含漏洞(File Inclusion)是Web安全中的经典漏洞类型，分为LFI(本地文件包含)和RFI(远程文件包含)两种。LFI允许攻击者读取服务器上的任意文件，RFI则允许攻击者远程加载并执行恶意代码。该漏洞通常出现在动态加载页面、模板渲染等功能中。</p>

    <h3>1.1 LFI vs RFI</h3>
    <table>
        <tr><th>类型</th><th>全称</th><th>特点</th><th>危害</th></tr>
        <tr><td>LFI</td><td>本地文件包含</td><td>读取服务器本地文件</td><td>读取系统文件、日志投毒</td></tr>
        <tr><td>RFI</td><td>远程文件包含</td><td>加载远程服务器文件</td><td>远程代码执行、获取shell</td></tr>
    </table>

    <h3>1.2 本次实验环境</h3>
    <table>
        <tr><th>项目</th><th>说明</th></tr>
        <tr><td>目标应用</td><td>基于Flask的用户管理系统</td></tr>
        <tr><td>新增功能</td><td>/page?name=X 动态页面加载</td></tr>
        <tr><td>漏洞类型</td><td>LFI路径遍历漏洞</td></tr>
        <tr><td>测试账号</td><td>admin/admin123</td></tr>
    </table>
</div>

<div class="page">
    <h2>二、漏洞分析</h2>
    <h3>2.1 漏洞代码</h3>
    <div class="code-block">@app.route("/page")
def dynamic_page():
    name = request.args.get("name", "")
    # 直接拼接用户输入的 name 到路径中
    file_path = os.path.join("pages", name)
    # 不校验 ../
    with open(file_path, "r") as f:
        content = f.read()</div>

    <h3>2.2 POC 1: LFI 读取系统文件</h3>
    <div class="code-block">/page?name=../../etc/passwd   -> 读取系统密码文件
/page?name=../../etc/hostname -> 读取主机名
/page?name=../app.py           -> 读取源代码</div>

    <h3>2.3 POC 2: 正常访问帮助中心</h3>
    <div class="code-block">/page?name=help -> 显示帮助中心页面</div>
</div>

<div class="page">
    <h2>三、修复方案</h2>
    <h3>3.1 路径白名单校验</h3>
    <div class="code-block">ALLOWED_PAGES = {"help", "about", "contact"}
if name not in ALLOWED_PAGES:
    return "页面不存在"</div>

    <h3>3.2 路径规范化校验</h3>
    <div class="code-block">real_path = os.path.realpath(os.path.join(PAGES_DIR, name))
if not real_path.startswith(os.path.realpath(PAGES_DIR)):
    return "非法路径"</div>

    <h3>3.3 修复前后对比</h3>
    <table>
        <tr><th>对比项</th><th>修复前</th><th>修复后</th></tr>
        <tr><td>路径处理</td><td>直接拼接</td><td>白名单/规范化校验</td></tr>
        <tr><td>../过滤</td><td>无过滤</td><td>检查是否越界</td></tr>
    </table>
</div>

<div class="page">
    <h2>四、总结</h2>
    <p>文件包含漏洞的核心原因是对用户输入的路径参数缺乏校验。攻击者通过 ../ 跳出限制目录实现LFI。</p>
    <p><strong>安全开发原则：</strong></p>
    <p>1. 永远不要直接将用户输入拼接到文件路径中</p>
    <p>2. 使用白名单限制可访问的文件</p>
    <p>3. 使用 os.path.realpath() 规范化路径后校验范围</p>

    <br>
    <hr style="border: none; border-top: 1px solid #2980b9; width: 60%; margin: 8mm auto;">
    <p style="text-align: center; color: #95a5a6; text-indent: 0;">&mdash; 报告完 &mdash;</p>
    <p style="text-align: center; color: #bbb; font-size: 8pt; text-indent: 0;">报告日期: 2026-07-11 | 课程: 文件包含漏洞 LFI/RFI</p>
</div>'''

c = c[:start] + new_body + '\n' + c[end:]
with open('/home/user/Projects/user-mgr/generate_pdf_report.py', 'w') as f:
    f.write(c)
print('PDF脚本更新完成')
