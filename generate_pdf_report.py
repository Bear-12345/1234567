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
        <strong>项目版本：</strong>V5.0 — 文件上传漏洞修复专题<br>
        <strong>报告日期：</strong>2026年7月9日<br>
        <strong>今日课程：</strong>Day3:文件上传漏洞深度解析与安全防护<br>
        <strong>技术栈：</strong>Python Flask / 文件上传 / 魔数校验 / UUID重命名<br>
    </div>
    <div class="line-bottom"></div>
</div>

<!-- ============================================================
     一、漏洞分析（文件上传）
     ============================================================ -->
<div class="page">
    <h2>一、漏洞分析（文件上传）</h2>
    <p>在已完成的用户管理系统中新增了头像上传功能。由于最初未做任何安全校验，存在以下4个严重漏洞：</p>

    <h3>1.1 漏洞位置</h3>
    <table>
        <tr><th>功能</th><th>路由</th><th>漏洞代码</th></tr>
        <tr><td>头像上传</td><td>/upload</td><td class="code">file.save(os.path.join(UPLOAD_DIR, file.filename))</td></tr>
    </table>

    <h3>1.2 POC 验证</h3>

    <h4>POC 1：上传 PHP Webshell（高危）</h4>
    <div class="code-block"># 上传一个PHP一句话木马
echo '&lt;?php system($_GET["cmd"]); ?>' > shell.php
curl -F "file=@shell.php" http://目标/upload

# 访问上传后的文件执行命令
curl http://目标/static/uploads/shell.php?cmd=id

# 结果：成功执行系统命令 ✅</div>

    <h4>POC 2：上传 HTML 恶意页面（高危）</h4>
    <div class="code-block"># 上传包含XSS的HTML文件
echo '&lt;script>alert(document.cookie)&lt;/script>' > xss.html
curl -F "file=@xss.html" http://目标/upload

# 用户访问该HTML时，XSS脚本被执行
# 结果：HTML文件可被直接访问 ✅</div>

    <h4>POC 3：路径穿越攻击（中危）</h4>
    <div class="code-block"># 文件名包含 ../ 可穿越到其他目录
curl -F "file=@test.txt;filename=../../evil.txt" http://目标/upload

# 结果：文件被保存到上层目录 ✅</div>

    <h4>POC 4：超大型文件上传（中危）</h4>
    <div class="code-block"># 上传超过限制的大文件
dd if=/dev/zero of=bigfile.bin bs=1M count=20
curl -F "file=@bigfile.bin" http://目标/upload

# 结果：耗尽服务器磁盘空间 ✅</div>
</div>

<!-- ============================================================
     二、修复方案
     ============================================================ -->
<div class="page">
    <h2>二、修复方案</h2>
    <p>针对上述4个漏洞，实施以下4层防护措施：</p>

    <h3>2.1 后缀名白名单</h3>
    <div class="code-block"># 只允许图片后缀
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

# 校验逻辑
if "." not in filename or ext not in ALLOWED_EXTENSIONS:
    return "不支持的文件类型"</div>

    <h3>2.2 MIME 类型校验</h3>
    <div class="code-block"># 只允许图片MIME
ALLOWED_MIMETYPES = {"image/png", "image/jpeg", "image/gif", "image/webp"}

# 校验逻辑
if file.content_type not in ALLOWED_MIMETYPES:
    return "不支持的文件类型"</div>

    <h3>2.3 文件头魔数校验</h3>
    <div class="code-block"># 读取文件头部字节验证真实格式
header = file.read(8)
is_valid = (
    header[:4] == b"\x89PNG" or      # PNG
    header[:2] in (b"\xff\xd8",) or  # JPEG
    header[:3] == b"GIF" or            # GIF
    header[:4] == b"RIFF"              # WEBP
)
if not is_valid:
    return "文件内容不是有效图片"</div>

    <h3>2.4 UUID 重命名防路径穿越</h3>
    <div class="code-block"># 使用UUID重命名文件，彻底杜绝路径穿越
import uuid
safe_filename = f"{uuid.uuid4().hex}.{ext}"
filepath = os.path.join(UPLOAD_DIR, safe_filename)
file.save(filepath)</div>
</div>

<!-- ============================================================
     三、修复前后对比
     ============================================================ -->
<div class="page">
    <h2>三、修复前后对比</h2>

    <table>
        <tr><th style="width:18%">防护层</th><th style="width:41%">修复前</th><th style="width:41%">修复后</th></tr>
        <tr>
            <td><strong>后缀校验</strong></td>
            <td class="code">无校验，任意后缀均可上传</td>
            <td class="code">白名单: png/jpg/jpeg/gif/webp</td>
        </tr>
        <tr>
            <td><strong>MIME校验</strong></td>
            <td class="code">无校验</td>
            <td class="code">仅允许image/*类型</td>
        </tr>
        <tr>
            <td><strong>内容校验</strong></td>
            <td class="code">无校验</td>
            <td class="code">读取文件头魔数验证真实格式</td>
        </tr>
        <tr>
            <td><strong>文件命名</strong></td>
            <td class="code">原始文件名，可路径穿越</td>
            <td class="code">UUID重命名，防穿越</td>
        </tr>
    </table>

    <h3>修复后验证结果</h3>
    <table>
        <tr><th>POC测试</th><th>修复前</th><th>修复后</th></tr>
        <tr><td>PHP webshell</td><td>上传成功并可访问</td><td class="green bold">[OK] 拦截非法后缀</td></tr>
        <tr><td>HTML恶意页面</td><td>上传成功并可访问</td><td class="green bold">[OK] 拦截非法后缀</td></tr>
        <tr><td>正常JPG图片</td><td>上传成功</td><td class="green bold">[OK] UUID重命名保存</td></tr>
    </table>
</div>

<!-- ============================================================
     四、总结
     ============================================================ -->
<div class="page">
    <h2>四、总结</h2>
    <p class="no-indent">文件上传漏洞是Web安全中的经典高风险漏洞，本次修复采用了"纵深防御"策略：</p>

    <table>
        <tr><th>防御层次</th><th>防御手段</th><th>防范的威胁</th></tr>
        <tr><td>第1层</td><td>后缀白名单</td><td>阻止 .php .exe .html 等非图片文件</td></tr>
        <tr><td>第2层</td><td>MIME校验</td><td>阻止 Content-Type 伪造的攻击文件</td></tr>
        <tr><td>第3层</td><td>文件头魔数校验</td><td>阻止改后缀名的虚假图片</td></tr>
        <tr><td>第4层</td><td>UUID重命名</td><td>阻止路径穿越和文件名冲突</td></tr>
    </table>

    <p style="margin-top: 4mm;">核心安全原则：永远不要信任用户输入。文件名、后缀、MIME类型、文件内容都需要层层校验，缺一不可。</p>

    <br>
    <hr style="border: none; border-top: 1px solid #2980b9; width: 60%; margin: 8mm auto;">
    <p style="text-align: center; color: #95a5a6; text-indent: 0;">&mdash; 报告完 &mdash;</p>
    <p style="text-align: center; color: #bbb; font-size: 8pt; text-indent: 0;">报告日期: 2026-07-09 | 课程: 文件上传漏洞 | 防御策略: 纵深防御</p>
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
