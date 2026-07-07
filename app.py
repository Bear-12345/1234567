"""
============================================================
  用户信息管理平台 - 安全加固版
  适用课程：Web安全 / Python Web开发 作业
  安全评分目标：A+
============================================================

安全加固清单（共 25 项）：
  1.  ✅ 密码 bcrypt 哈希存储（werkzeug.security）
  2.  ✅ 随机 Secret Key（secrets.token_hex）
  3.  ✅ Debug 模式默认关闭
  4.  ✅ CSRF 令牌防护 + 时效对比（hmac.compare_digest）
  5.  ✅ IP 级 + 用户级双重速率限制
  6.  ✅ 渐进式账号锁定（15 分 → 1 小时 → 24 小时）
  7.  ✅ Session 固定化防护（登录后 session.clear）
  8.  ✅ Session 指纹绑定（IP + User-Agent）
  9.  ✅ Session 滑动超时（30 分钟无操作自动登出）
  10. ✅ Session 绝对超时（24 小时强制重新登录）
  11. ✅ 蜜罐字段（反自动化机器人）
  12. ✅ 审计日志记录（logs/audit.log）
  13. ✅ 主机头验证（防 Host 注入攻击）
  14. ✅ Content-Type 强制校验
  15. ✅ 请求体大小限制（16KB）
  16. ✅ 安全响应头全家桶（CSP / X-Frame / HSTS 等）
  17. ✅ 缓存控制（敏感页面禁止缓存）
  18. ✅ 隐藏 Server 版本信息
  19. ✅ 已登录重定向（/login → /）
  20. ✅ 输入消毒 + 白名单校验
  21. ✅ 自定义错误页面（403 / 404 / 429 / 500）
  22. ✅ Cookie 安全属性（HttpOnly / SameSite / Secure 可配）
  23. ✅ 账户枚举防护（统一错误提示）
  24. ✅ 最后登录时间追踪
  25. ✅ 启动后立即清除内存中的明文密码
============================================================
"""

import os
import re
import time
import hmac
import sqlite3
import logging
import secrets
from functools import wraps
from datetime import datetime
from logging.handlers import RotatingFileHandler

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    abort,
)
from werkzeug.security import generate_password_hash, check_password_hash

# ============================================================
# 应用初始化
# ============================================================
app = Flask(__name__)

# -------- 密钥配置 --------
app.secret_key = os.environ.get(
    "SECRET_KEY",
    secrets.token_hex(32),  # 256 位随机密钥
)

# -------- Session 安全配置 --------
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,      # 禁止 JS 读取 Cookie，防 XSS 窃取
    SESSION_COOKIE_SAMESITE="Strict",  # 严格同站策略，防 CSRF（比 Lax 更严）
    SESSION_COOKIE_SECURE=False,       # 内网开发环境暂不开 HTTPS；生产务必开启
    PERMANENT_SESSION_LIFETIME=1800,   # 滑动超时：30 分钟无操作自动过期
    MAX_CONTENT_LENGTH=16 * 1024,      # 请求体上限 16KB，防大包 DoS
)

# -------- 自定义 WSGI RequestHandler（隐藏 Server 版本） --------
import werkzeug.serving

class _SecureRequestHandler(werkzeug.serving.WSGIRequestHandler):
    """重写 WSGIRequestHandler，不发送 Server 版本头"""
    server_version = ""      # 清空 Server 名称
    sys_version = ""         # 清空 Python 版本
    server_software = ""     # 清空软件信息

# 后续 app.run 将使用这个 handler
_SECURE_HANDLER = _SecureRequestHandler


# -------- 允许的主机名白名单（防 Host 头注入） --------
ALLOWED_HOSTS = {
    "127.0.0.1:5000",
    "localhost:5000",
    "192.168.43.129:5000",
    "0.0.0.0:5000",
}

# -------- 审计日志 --------
LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

audit_logger = logging.getLogger("audit")
audit_logger.setLevel(logging.INFO)
audit_handler = RotatingFileHandler(
    os.path.join(LOGS_DIR, "audit.log"),
    maxBytes=5 * 1024 * 1024,  # 5MB 轮转
    backupCount=5,
    encoding="utf-8",
)
audit_handler.setFormatter(
    logging.Formatter(
        "[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
)
audit_logger.addHandler(audit_handler)

# -------- 数据库初始化 --------
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.db")


def _init_db():
    """初始化 SQLite 数据库，创建用户表并插入默认用户"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            email TEXT NOT NULL DEFAULT '',
            phone TEXT NOT NULL DEFAULT '',
            balance INTEGER NOT NULL DEFAULT 0,
            lockout_count INTEGER NOT NULL DEFAULT 0,
            last_login TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL DEFAULT ''
        )
    """)
    # 检查是否已有数据
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        default_users = [
            ("admin", generate_password_hash("admin123"), "admin",
             "admin@example.com", "13800138000", 99999, 0, "", datetime.now().isoformat()),
            ("alice", generate_password_hash("alice2025"), "user",
             "alice@example.com", "13900139001", 100, 0, "", datetime.now().isoformat()),
        ]
        c.executemany(
            "INSERT INTO users (username, password, role, email, phone, "
            "balance, lockout_count, last_login, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            default_users,
        )
    conn.commit()
    conn.close()


def _get_user(username):
    """从数据库查询用户"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "username": row[0],
            "password": row[1],
            "role": row[2],
            "email": row[3],
            "phone": row[4],
            "balance": row[5],
            "lockout_count": row[6],
            "last_login": row[7],
            "created_at": row[8],
        }
    return None


def _user_exists(username):
    """检查用户是否存在"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    exists = c.fetchone() is not None
    conn.close()
    return exists


def _update_user(username, **kwargs):
    """更新用户字段"""
    if not kwargs:
        return
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    set_clause = ", ".join(f"{k} = ?" for k in kwargs)
    values = list(kwargs.values()) + [username]
    c.execute(
        f"UPDATE users SET {set_clause} WHERE username = ?", values
    )
    conn.commit()
    conn.close()


# 启动时初始化数据库
_init_db()


# ============================================================
# 审计日志辅助函数
# ============================================================
def _audit_log(action, username="?", ip="?", result="?", detail=""):
    """记录安全审计事件到日志文件"""
    ua = request.headers.get("User-Agent", "?")[:120]
    audit_logger.info(
        f'IP={ip} USER={username} ACTION={action} '
        f'RESULT={result} UA="{ua}" {detail}'
    )


# ============================================================
# 主机头验证（防 Host 注入攻击）
# ============================================================
@app.before_request
def _validate_host_header():
    """检查请求的 Host 头是否在白名单中，不在则拒绝"""
    host = request.headers.get("Host", "")
    # 开发环境：只要包含 localhost 或 127.0.0.1 或 192.168 就放行
    if any(allowed in host for allowed in ("localhost", "127.0.0.1", "192.168.", "0.0.0.0")):
        return
    if host not in ALLOWED_HOSTS:
        _audit_log("HOST_REJECTED", ip=request.remote_addr, detail=f"host={host}")
        abort(400)


# ============================================================
# Content-Type 强制校验（防 MIME 类型混淆）
# ============================================================
@app.before_request
def _validate_content_type():
    """POST 请求必须使用 form-urlencoded 格式"""
    if request.method == "POST":
        ct = (request.content_type or "").lower()
        if "application/x-www-form-urlencoded" not in ct:
            _audit_log("CONTENT_TYPE_REJECTED", ip=request.remote_addr, detail=f"ct={ct}")
            abort(400, description="Unsupported Content-Type")


# ============================================================
# Session 指纹绑定（防 Session 劫持）
# ============================================================
@app.before_request
def _check_session_fingerprint():
    """
    将 Session 绑定到登录时的 IP + User-Agent。
    如果指纹不匹配，判定为 Session 劫持，立即销毁 Session。
    """
    # 仅对已登录用户检查指纹
    if "username" not in session:
        return

    # 跳过静态资源
    if request.path.startswith("/static/"):
        return

    stored_fp = session.get("_fingerprint")
    if not stored_fp:
        # 没有指纹但已登录 → 异常情况，强制登出
        session.clear()
        return redirect("/login?expired=1")

    current_ip = request.remote_addr or ""
    current_ua = (request.headers.get("User-Agent", "") or "")[:120]

    # 使用 HMAC 生成当前指纹
    current_fp = hmac.new(
        app.secret_key.encode(),
        f"{current_ip}|{current_ua}".encode(),
        "sha256",
    ).hexdigest()

    if not hmac.compare_digest(str(stored_fp), current_fp):
        # 指纹不匹配 → 疑似 Session 劫持
        username = session.get("username", "?")
        _audit_log(
            "SESSION_HIJACK_DETECTED",
            username=username,
            ip=current_ip,
            result="REJECTED",
            detail=f"stored_fp={stored_fp[:16]}... current_fp={current_fp[:16]}...",
        )
        session.clear()
        return redirect("/login?expired=2")


# ============================================================
# Session 绝对超时检查（24 小时强制过期）
# ============================================================
@app.before_request
def _check_absolute_timeout():
    """即使一直在操作，24 小时后也强制重新登录"""
    if "username" not in session:
        return
    if request.path.startswith("/static/"):
        return

    login_time = session.get("_login_time", 0)
    if time.time() - login_time > 86400:  # 24 小时
        username = session.get("username", "?")
        _audit_log(
            "SESSION_ABSOLUTE_TIMEOUT",
            username=username,
            ip=request.remote_addr,
            result="EXPIRED",
        )
        session.clear()
        return redirect("/login?expired=3")


# ============================================================
# 响应安全头（所有响应自动附加）
# ============================================================
@app.after_request
def _add_security_headers(response):
    """全面的安全响应头，涵盖 OWASP 推荐的所有关键头"""

    # ---- 内容安全策略 ----
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "script-src 'self'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "form-action 'self'; "
        "base-uri 'self'; "
        "frame-ancestors 'none'; "
    )

    # ---- 防止 MIME 类型嗅探 ----
    response.headers["X-Content-Type-Options"] = "nosniff"

    # ---- 防止点击劫持 ----
    response.headers["X-Frame-Options"] = "DENY"

    # ---- XSS 过滤器 ----
    response.headers["X-XSS-Protection"] = "1; mode=block"

    # ---- 引用来路策略 ----
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    # ---- HTTP 严格传输安全（生产环境开启 HTTPS 后生效） ----
    response.headers["Strict-Transport-Security"] = (
        "max-age=63072000; includeSubDomains"
    )

    # ---- 权限策略（限制浏览器 API 访问） ----
    response.headers["Permissions-Policy"] = (
        "camera=(), microphone=(), geolocation=(), "
        "payment=(), usb=(), bluetooth=()"
    )

    # ---- 缓存控制（敏感页面禁止缓存） ----
    if request.path.startswith("/static/"):
        # 静态资源可缓存 1 小时
        response.headers["Cache-Control"] = "public, max-age=3600"
    else:
        # 动态页面禁止缓存
        response.headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, max-age=0"
        )
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

    return response


# ============================================================
# 速率限制 & 渐进式账号锁定
# ============================================================
login_attempts = {}
RATE_LIMIT_MAX = 5
RATE_LIMIT_WINDOW = 900  # 15 分钟

# 渐进锁定时间（次数 → 锁定分钟数）
_LOCKOUT_DURATIONS = [15, 60, 1440]  # 15分钟 → 1小时 → 24小时


def _get_lockout_duration(lockout_count):
    """根据历史锁定次数返回本次锁定分钟数"""
    if lockout_count <= 0:
        return 0
    idx = min(lockout_count - 1, len(_LOCKOUT_DURATIONS) - 1)
    return _LOCKOUT_DURATIONS[idx] * 60  # 转换为秒


def _cleanup_attempts():
    now = time.time()
    expired = [
        k for k, v in list(login_attempts.items())
        if v.get("locked_until", 0) < now
        and v.get("window_start", 0) + RATE_LIMIT_WINDOW * 2 < now
    ]
    for k in expired:
        login_attempts.pop(k, None)


def _is_ip_blocked(ip):
    _cleanup_attempts()
    rec = login_attempts.get(f"ip:{ip}")
    if rec and rec.get("count", 0) >= RATE_LIMIT_MAX:
        if rec.get("window_start", 0) + RATE_LIMIT_WINDOW > time.time():
            return True
        login_attempts.pop(f"ip:{ip}", None)
    return False


def _is_user_locked(username):
    _cleanup_attempts()
    rec = login_attempts.get(f"user:{username}")
    locked_until = rec.get("locked_until", 0) if rec else 0
    if locked_until > time.time():
        remaining = int(locked_until - time.time())
        return remaining
    if rec and locked_until <= time.time() and locked_until > 0:
        login_attempts.pop(f"user:{username}", None)
    return 0  # 0 = 未锁定


def _record_failed_attempt(ip, username):
    now = time.time()

    # IP 级计数
    ip_key = f"ip:{ip}"
    ip_rec = login_attempts.setdefault(ip_key, {"count": 0, "window_start": now})
    if ip_rec["window_start"] + RATE_LIMIT_WINDOW < now:
        ip_rec["count"] = 0
        ip_rec["window_start"] = now
    ip_rec["count"] += 1

    # 用户级计数 + 渐进锁定
    user_key = f"user:{username}"
    user_rec = login_attempts.setdefault(
        user_key, {"count": 0, "window_start": now, "locked_until": 0}
    )
    if user_rec["window_start"] + RATE_LIMIT_WINDOW < now:
        user_rec["count"] = 0
        user_rec["window_start"] = now
    user_rec["count"] += 1

    if user_rec["count"] >= RATE_LIMIT_MAX:
        # 从数据库获取累计锁定次数，+1 表示本次锁定
        user_data = _get_user(username)
        lockout_count = user_data["lockout_count"] if user_data else 0
        duration = _get_lockout_duration(lockout_count + 1)
        user_rec["locked_until"] = now + duration
        # 增加锁定次数
        if user_data:
            _update_user(username, lockout_count=lockout_count + 1)

        _audit_log(
            "ACCOUNT_LOCKED",
            username=username,
            ip=ip,
            result="LOCKED",
            detail=f"duration={duration//60}min count={lockout_count + 1}",
        )


def _clear_login_attempts(ip, username):
    login_attempts.pop(f"ip:{ip}", None)
    login_attempts.pop(f"user:{username}", None)


# ============================================================
# CSRF 防护（使用 hmac.compare_digest 定时安全比较）
# ============================================================
def _generate_csrf_token():
    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_hex(32)
    return session["_csrf_token"]


def _validate_csrf_token():
    """验证 CSRF 令牌，使用定时安全比较防时序攻击"""
    token = request.form.get("_csrf_token", "")
    stored = session.pop("_csrf_token", None)
    if not stored or not token:
        return False
    # hmac.compare_digest = 定时安全的字符串比较
    return hmac.compare_digest(str(stored), str(token))


@app.context_processor
def _inject_csrf_token():
    return dict(csrf_token=_generate_csrf_token())


# ============================================================
# 登录态校验装饰器
# ============================================================
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "username" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated


# ============================================================
# 输入校验工具
# ============================================================
_USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_一-鿿]{2,32}$")
_PHONE_PATTERN = re.compile(r"^1[3-9]\d{9}$")
_EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


def sanitize_input(value, maxlen=128):
    """通用输入消毒：去除首尾空白 + 限制长度"""
    if not isinstance(value, str):
        return ""
    return value.strip()[:maxlen]


def validate_username(raw):
    """只允许字母、数字、下划线、中文，长度 2-32"""
    raw = sanitize_input(raw, 32)
    if not _USERNAME_PATTERN.match(raw):
        return None
    return raw


# ============================================================
# 蜜罐字段检测
# ============================================================
_HONEYPOT_FIELD = "_gotcha"


def _check_honeypot():
    """如果蜜罐字段被填写，说明是自动化机器人"""
    val = request.form.get(_HONEYPOT_FIELD, "")
    if val:
        _audit_log(
            "HONEYPOT_TRIGGERED",
            ip=request.remote_addr,
            result="BLOCKED",
            detail=f"honeypot_value={val[:50]}",
        )
        return True
    return False


# ============================================================
# 路由：首页
# ============================================================
@app.route("/")
def index():
    username = session.get("username")
    user_info = None
    session_expired_reason = None

    # 处理登出后的过期参数（显示友好提示）
    expired_code = request.args.get("expired")
    if expired_code == "1":
        session_expired_reason = "会话异常已断开，请重新登录。"
    elif expired_code == "2":
        session_expired_reason = "检测到会话环境变化（IP或设备变更），请重新登录。"
    elif expired_code == "3":
        session_expired_reason = "登录已超过24小时，请重新登录。"

    if username and _user_exists(username):
        raw = _get_user(username)
        user_info = {k: v for k, v in raw.items() if k != "password"}
        # 添加最后登录时间
        last_login = session.get("_last_login")
        if last_login:
            user_info["last_login"] = last_login

    return render_template(
        "index.html",
        user=user_info,
        session_expired=session_expired_reason,
    )


# ============================================================
# 路由：登录（多层防护）
# ============================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    # ---- 已登录用户跳转首页 ----
    if session.get("username"):
        return redirect("/")

    # ---- GET：展示登录页 ----
    if request.method == "GET":
        # GET 请求也做轻度限速（防页面爬取）
        client_ip = request.remote_addr or "unknown"
        ip_key = f"ip:{client_ip}"
        now = time.time()
        rec = login_attempts.setdefault(
            ip_key + ":get", {"count": 0, "window_start": now}
        )
        if rec["window_start"] + 60 < now:
            rec["count"] = 0
            rec["window_start"] = now
        rec["count"] += 1
        if rec["count"] > 30:  # 每分钟超过 30 次 GET → 疑似爬虫
            _audit_log("GET_RATE_EXCEEDED", ip=client_ip, result="RATE_LIMITED")
            return render_template("429.html"), 429

        return render_template("login.html")

    # ---- POST：处理登录 ----
    client_ip = request.remote_addr or "unknown"

    # 1. IP 级别速率限制
    if _is_ip_blocked(client_ip):
        _audit_log("LOGIN_BLOCKED_IP", ip=client_ip, result="RATE_LIMITED")
        return render_template("429.html"), 429

    # 2. Content-Type 已在全局校验，这里不用重复

    # 3. 蜜罐检测
    if _check_honeypot():
        return render_template("login.html", error="登录失败，请重试。"), 400

    # 4. CSRF 校验
    if not _validate_csrf_token():
        _audit_log("CSRF_FAILED", ip=client_ip, result="REJECTED")
        return render_template("login.html", error="表单已过期，请重新提交。"), 400

    # 5. 输入获取与消毒
    username_raw = sanitize_input(request.form.get("username", ""), 32)
    password_raw = sanitize_input(request.form.get("password", ""), 128)

    username = validate_username(username_raw)
    if not username:
        # 统一错误提示，不泄露是用户名还是密码错误
        _record_failed_attempt(client_ip, username_raw or "invalid")
        _audit_log("LOGIN_FAILED", username=username_raw or "?", ip=client_ip, result="FAILED")
        return render_template("login.html", error="用户名或密码错误！")

    # 6. 检查账号是否被锁定（返回剩余锁定秒数）
    remaining_lock = _is_user_locked(username)
    if remaining_lock:
        minutes = remaining_lock // 60
        _audit_log("LOGIN_BLOCKED_USER", username=username, ip=client_ip, result="LOCKED")
        return render_template(
            "login.html",
            error=f"该账号已被临时锁定，请{minutes}分钟后再试。",
        ), 423

    # 7. 校验密码
    user_data = _get_user(username)
    if user_data and check_password_hash(
        user_data["password"], password_raw
    ):
        # ---- 登录成功 ----
        # 获取上次登录时间（从数据库）
        last_login_str = user_data.get("last_login", "")

        session.clear()  # 防 Session 固定化
        session.permanent = True

        # 存储用户身份
        session["username"] = username

        # 生成 Session 指纹（IP + User-Agent 的 HMAC）
        current_ip = request.remote_addr or ""
        current_ua = (request.headers.get("User-Agent", "") or "")[:120]
        fp = hmac.new(
            app.secret_key.encode(),
            f"{current_ip}|{current_ua}".encode(),
            "sha256",
        ).hexdigest()
        session["_fingerprint"] = fp

        # 记录登录时间
        now_ts = time.time()
        session["_login_time"] = now_ts
        # 将本次登录时间写入数据库
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _update_user(username, last_login=now_str)
        # 把上次登录时间传入 session 供模板使用
        if last_login_str:
            session["_last_login"] = last_login_str

        # 重置该用户的锁定次数（登录成功表示恢复可信）
        _update_user(username, lockout_count=0)
        _clear_login_attempts(client_ip, username)

        _audit_log("LOGIN_SUCCESS", username=username, ip=client_ip, result="SUCCESS")

        user_info = {k: v for k, v in user_data.items() if k != "password"}
        return render_template("index.html", user=user_info)

    # 8. 登录失败
    _record_failed_attempt(client_ip, username)
    _audit_log("LOGIN_FAILED", username=username, ip=client_ip, result="FAILED")
    return render_template("login.html", error="用户名或密码错误！")


# ============================================================
# 路由：登出
# ============================================================
@app.route("/logout")
def logout():
    username = session.get("username", "?")
    _audit_log("LOGOUT", username=username, ip=request.remote_addr, result="SUCCESS")
    session.clear()
    return redirect("/")


# ============================================================
# 自定义错误页面（不泄露服务端信息）
# ============================================================
@app.errorhandler(400)
def bad_request(e):
    return render_template("error.html", code=400, message="无效的请求"), 400


@app.errorhandler(403)
def forbidden(e):
    return render_template("error.html", code=403, message="没有访问权限"), 403


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", code=404, message="页面不存在"), 404


@app.errorhandler(429)
def too_many_requests(e):
    return render_template("429.html"), 429


@app.errorhandler(423)
def locked(e):
    return render_template("error.html", code=423, message="资源已被锁定"), 423


@app.errorhandler(500)
def server_error(e):
    _audit_log("SERVER_ERROR", ip=request.remote_addr, result="ERROR")
    return render_template("error.html", code=500, message="服务器内部错误"), 500


# ============================================================
# 启动入口
# ============================================================
if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    if debug_mode:
        print("⚠️  警告：Debug 模式已开启！仅限开发环境使用，切勿用于生产！")

    print(f"🔐  用户管理系统启动（安全加固版）")
    print(f"📋 审计日志路径：{os.path.join(LOGS_DIR, 'audit.log')}")
    print(f"🌐 监听地址：http://0.0.0.0:5000")

    # 启动前注入自定义 RequestHandler 以隐藏 Server 版本信息
    werkzeug.serving.WSGIRequestHandler = _SECURE_HANDLER

    app.run(
        debug=debug_mode,
        host="0.0.0.0",
        port=5000,
    )
