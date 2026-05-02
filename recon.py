import os, re, socket, argparse, sys, threading, requests, time, json, random
from rich.console import Console
from rich.markdown import Markdown
from rich.theme import Theme
from pystyle import Colorate, Colors
import dns.resolver
import dns.query
import dns.zone
from user_agent import generate_user_agent

def p(text):
    print(Colorate.Horizontal(Colors.cyan_to_blue, text))

def r(text):
    print(Colorate.Horizontal(Colors.red_to_yellow, text))

domains = [
    "www", "mail", "ftp", "smtp", "pop", "imap", "ns1", "ns2", "ns3", "ns4",
    "vpn", "m", "mobile", "api", "dev", "stage", "staging", "test", "uat",
    "beta", "alpha", "admin", "portal", "dashboard", "panel", "cpanel", "whm",
    "webmail", "autodiscover", "autoconfig", "remote", "gateway", "ssh",
    "cdn", "static", "assets", "media", "img", "images", "video", "files",
    "download", "downloads", "upload", "uploads", "storage", "backup",
    "db", "database", "sql", "mysql", "redis", "mongo", "elastic", "postgres",
    "cache", "memcache", "queue", "mq", "rabbitmq", "kafka", "zookeeper",
    "auth", "login", "sso", "oauth", "id", "identity", "account", "accounts",
    "pay", "payment", "payments", "shop", "store", "cart", "checkout",
    "blog", "news", "forum", "community", "support", "help", "docs", "wiki",
    "status", "monitor", "metrics", "grafana", "kibana", "prometheus", "nagios",
    "secure", "ssl", "git", "gitlab", "github", "svn", "jira", "confluence",
    "jenkins", "ci", "cd", "build", "deploy", "k8s", "kubernetes", "docker",
    "registry", "repo", "repository", "nexus", "artifactory", "sonar",
    "internal", "intranet", "corp", "office", "owa", "exchange", "sharepoint",
    "ldap", "ad", "dc", "proxy", "firewall", "router", "switch", "nas",
    "aws", "azure", "gcp", "cloud", "s3", "bucket", "lambda", "functions",
    "app", "apps", "application", "web", "frontend", "backend", "microservice",
    "graphql", "rest", "grpc", "websocket", "socket", "ws", "wss",
    "old", "new", "v1", "v2", "v3", "v4", "legacy", "sandbox", "demo",
    "preview", "preprod", "prod", "production", "live", "uat", "qa",
    "mx", "mx1", "mx2", "smtp1", "smtp2", "relay", "outbound", "inbound",
    "webdisk", "cpcontacts", "cpcalendars", "whois", "rdp", "citrix",
    "api2", "api-v1", "api-v2", "api-v3", "api-dev", "api-staging",
    "crm", "erp", "hrm", "cms", "lms", "ecommerce", "marketplace",
    "office365", "teams", "slack", "zoom", "meet", "webex",
    "search", "elastic-search", "solr", "sphinx",
    "logs", "logging", "splunk", "datadog", "newrelic",
    "vault", "secrets", "config", "configs", "settings",
    "bastion", "jump", "jumphost", "mgmt", "management",
    "analytics", "tracking", "tag", "gtm", "pixel",
    "partner", "partners", "affiliate", "reseller",
    "dev1", "dev2", "test1", "test2", "stage1", "stage2",
    "lab", "labs", "research", "poc", "prototype",
    "mail2", "mail3", "smtp2", "smtp3", "mx3", "mx4",
    "waf", "fw", "lb", "loadbalancer", "haproxy", "nginx",
    "phpmyadmin", "pma", "adminer", "pgadmin",
    "ftp2", "sftp", "ftps", "rsync",
    "ntp", "snmp", "syslog", "radius",
    "api-gateway", "apigw", "kong", "traefik",
    "storybook", "design", "figma", "prototype",
    "investor", "ir", "careers", "jobs", "hr",
    "legal", "privacy", "terms", "compliance",
    "data", "datalake", "warehouse", "bi", "reporting",
    "ml", "ai", "model", "inference", "training",
    "notification", "push", "email", "sms", "otp",
    "image", "thumb", "resize", "compress",
    "hook", "webhook", "webhooks", "callback",
    "token", "jwt", "session", "cookie",
    "health", "ping", "alive", "ready", "live",
]

paths = [
    "/admin", "/admin/", "/administrator", "/admin/login", "/admin/dashboard",
    "/admin/index.php", "/admin/admin.php", "/admin/login.php",
    "/admin/panel", "/admin/control", "/admin/cp", "/admin/manage",
    "/admin/config", "/admin/settings", "/admin/users", "/admin/user",
    "/panel", "/cpanel", "/whm", "/webadmin", "/siteadmin",
    "/backend", "/superadmin", "/root", "/master", "/owner",
    "/manager", "/management", "/control", "/controlpanel",

    "/wp-admin", "/wp-login.php", "/wp-config.php", "/wp-config.php.bak",
    "/wp-content", "/wp-content/uploads", "/wp-content/plugins",
    "/wp-content/themes", "/wp-includes", "/wp-json", "/wp-json/wp/v2/users",
    "/xmlrpc.php", "/wp-cron.php", "/wp-settings.php",
    "/wordpress/wp-admin", "/wordpress/wp-login.php", "/gallery.php",

    "/phpmyadmin", "/phpmyadmin/", "/phpMyAdmin", "/phpMyAdmin/",
    "/pma", "/pma/", "/myadmin", "/mysql", "/mysqladmin",
    "/adminer", "/adminer.php", "/adminer/", "/db", "/database",
    "/pgadmin", "/pgadmin4", "/mongo", "/redis",

    "/index.php", "/index.php/admin", "/login.php", "/admin.php",
    "/config.php", "/configuration.php", "/settings.php", "/setup.php",
    "/install.php", "/installer.php", "/update.php", "/upgrade.php",
    "/test.php", "/info.php", "/phpinfo.php", "/php.php",
    "/shell.php", "/cmd.php", "/webshell.php", "/c99.php", "/r57.php",
    "/upload.php", "/uploader.php", "/file.php", "/files.php",
    "/backup.php", "/db.php", "/database.php", "/sql.php",
    "/connect.php", "/connection.php", "/db_connect.php",
    "/ajax.php", "/api.php", "/request.php", "/process.php",
    "/register.php", "/signup.php", "/forgot.php", "/reset.php",
    "/search.php", "/query.php", "/find.php", "/results.php",
    "/error.php", "/404.php", "/403.php", "/500.php",
    "/redirect.php", "/go.php", "/link.php", "/redir.php",
    "/download.php", "/get.php", "/fetch.php",
    "/user.php", "/users.php", "/profile.php", "/account.php",
    "/payment.php", "/pay.php", "/order.php", "/checkout.php",
    "/log.php", "/logs.php", "/logger.php", "/debug.php",
    "/cron.php", "/task.php", "/scheduler.php", "/queue.php",
    "/mail.php", "/send.php", "/sendmail.php", "/mailer.php",
    "/old/index.php", "/backup/index.php", "/test/index.php",
    "/1/index.php", "/2/index.php", "/new/index.php",

    "/api", "/api/v1", "/api/v2", "/api/v3", "/api/v4",
    "/api/v1/users", "/api/v1/admin", "/api/v1/config",
    "/api/v1/login", "/api/v1/register", "/api/v1/token",
    "/api/v2/users", "/api/v2/admin", "/api/v2/config",
    "/graphql", "/graphiql", "/playground", "/graph",
    "/swagger", "/swagger-ui", "/swagger-ui.html", "/swagger.json",
    "/openapi.json", "/openapi.yaml", "/api-docs", "/redoc",
    "/v1", "/v2", "/v3", "/rest", "/rpc", "/soap", "/wsdl",
    "/api/swagger", "/api/docs", "/api/schema",
    "/api/health", "/api/status", "/api/ping",
    "/api/users", "/api/admin", "/api/me", "/api/profile",
    "/api/auth", "/api/login", "/api/logout", "/api/token",
    "/api/register", "/api/signup", "/api/forgot",
    "/api/reset", "/api/verify", "/api/confirm",
    "/api/search", "/api/upload", "/api/download",
    "/api/payment", "/api/order", "/api/product",
    "/api/webhook", "/api/callback", "/api/notify",

    "/.env", "/.env.local", "/.env.production", "/.env.development",
    "/.env.staging", "/.env.test", "/.env.backup", "/.env.old",
    "/.env.example", "/.env.sample", "/.env.bak", "/.env.save",
    "/config.php", "/config.json", "/config.yml", "/config.yaml",
    "/config.xml", "/config.ini", "/config.cfg", "/config.conf",
    "/configuration.php", "/configuration.yml", "/configuration.json",
    "/settings.php", "/settings.json", "/settings.yml",
    "/web.config", "/app.config", "/application.yml",
    "/application.properties", "/bootstrap.yml", "/bootstrap.properties",
    "/database.yml", "/database.json", "/database.php",
    "/secrets.yml", "/secrets.json", "/credentials.json",
    "/credentials.yml", "/.credentials", "/service-account.json",
    "/.git", "/.git/config", "/.git/HEAD", "/.git/index",
    "/.git/COMMIT_EDITMSG", "/.git/logs/HEAD",
    "/.gitignore", "/.gitconfig", "/.gitmodules",
    "/.svn", "/.svn/entries", "/.svn/wc.db",
    "/.htaccess", "/.htpasswd", "/.htusers",
    "/robots.txt", "/sitemap.xml", "/sitemap_index.xml",
    "/crossdomain.xml", "/clientaccesspolicy.xml",
    "/security.txt", "/.well-known/security.txt",
    "/.DS_Store", "/Thumbs.db", "/desktop.ini",
    "/composer.json", "/composer.lock", "/vendor/autoload.php",
    "/package.json", "/package-lock.json", "/yarn.lock",
    "/webpack.config.js", "/webpack.config.ts", "/vite.config.js",
    "/Dockerfile", "/docker-compose.yml", "/docker-compose.yaml",
    "/.dockerignore", "/kubernetes.yml", "/k8s.yml",
    "/.bash_history", "/.bash_profile", "/.bashrc", "/.profile",
    "/.ssh", "/.ssh/id_rsa", "/.ssh/id_rsa.pub", "/.ssh/known_hosts",
    "/.ssh/authorized_keys", "/.aws/credentials", "/.aws/config",

    "/backup", "/backup/", "/backups", "/bak", "/old", "/archive",
    "/backup.zip", "/backup.tar.gz", "/backup.tar", "/backup.rar",
    "/backup.sql", "/backup.sql.gz", "/backup.db",
    "/db.sql", "/dump.sql", "/database.sql", "/data.sql",
    "/site.zip", "/www.zip", "/html.zip", "/htdocs.zip",
    "/public.zip", "/web.zip", "/files.zip", "/uploads.zip",
    "/src.zip", "/source.zip", "/app.zip", "/code.zip",
    "/backup_2023.zip", "/backup_2024.zip", "/backup2024.zip",
    "/db_backup.sql", "/full_backup.zip",
    "/old/", "/old2/", "/new/", "/temp/", "/tmp/",

    "/logs", "/log", "/logs/", "/error.log", "/access.log",
    "/debug.log", "/php_errors.log", "/server.log", "/app.log",
    "/laravel.log", "/storage/logs/laravel.log",
    "/var/log/apache2/access.log", "/var/log/nginx/access.log",
    "/phpinfo.php", "/info.php", "/test.php", "/debug.php",
    "/status", "/server-status", "/server-info", "/nginx_status",
    "/health", "/healthz", "/health-check", "/ping", "/alive", "/ready",
    "/actuator", "/actuator/env", "/actuator/health", "/actuator/info",
    "/actuator/mappings", "/actuator/beans", "/actuator/metrics",
    "/actuator/loggers", "/actuator/httptrace", "/actuator/dump",
    "/trace", "/env", "/beans", "/mappings",

    "/jenkins", "/jenkins/login", "/.jenkins", "/jenkins/api",
    "/gitlab", "/gitlab/admin", "/.travis.yml", "/Jenkinsfile",
    "/Makefile", "/Gruntfile.js", "/Gulpfile.js",
    "/k8s", "/.kube", "/.kube/config", "/deploy", "/deployment",
    "/metrics", "/prometheus", "/grafana", "/kibana",
    "/sonar", "/sonarqube", "/nexus", "/artifactory",
    "/vault", "/consul", "/nomad", "/terraform",
    "/ansible", "/playbook.yml",

    "/login", "/logout", "/signin", "/signout",
    "/signup", "/register", "/forgot-password", "/reset-password",
    "/auth", "/oauth", "/oauth2", "/sso", "/saml", "/cas",
    "/token", "/refresh-token", "/callback", "/verify", "/confirm",
    "/2fa", "/mfa", "/otp", "/totp",
    "/accounts/login", "/accounts/register", "/user/login",

    "/joomla", "/joomla/administrator", "/index.php/administrator",
    "/drupal", "/user/login", "/user/register", "/node",
    "/magento", "/magento/admin", "/index.php/admin",
    "/opencart", "/laravel", "/symfony", "/codeigniter",
    "/storage", "/storage/logs", "/storage/app", "/artisan",
    "/bootstrap/cache", "/.env", "/vendor",
    "/flask", "/django", "/rails", "/spring",

    "/upload", "/uploads", "/files", "/file", "/media",
    "/images", "/img", "/static", "/assets", "/downloads",
    "/attachment", "/attachments", "/content", "/data",
    "/userfiles", "/user-files", "/user_files",
    "/public", "/public/uploads", "/public/files",

    "/console", "/shell", "/terminal", "/cmd", "/exec",
    "/cgi-bin", "/cgi-bin/admin.cgi", "/cgi-bin/test.cgi",
    "/cgi-bin/printenv", "/cgi-bin/env.cgi",
    "/secret", "/secrets", "/private", "/hidden", "/secure",
    "/internal", "/system", "/sys", "/proc",

    "/search", "/find", "/query", "/lookup", "/fetch",
    "/redirect", "/redir", "/goto", "/url", "/link", "/out",
    "/include", "/includes", "/lib", "/library", "/vendor",
    "/cache", "/temp", "/tmp", "/var", "/run",
    "/install", "/installer", "/setup", "/setup.php", "/install.php",
    "/upgrade", "/update", "/patch", "/migrate", "/migration",
]

def pf(url, status_code):
    url_part    = f"[ * ] Found, URL: {url}"
    status_part = f"Status Code: {status_code}"
    print(
        Colorate.Horizontal(Colors.cyan_to_blue,    url_part.ljust(80)) +
        Colorate.Horizontal(Colors.red_to_purple,   status_part)
    )

json_data = {}
json_lock = threading.Lock()

def jset(key, value):
    with json_lock:
        json_data[key] = value

def jadd(key, value):
    with json_lock:
        if key not in json_data:
            json_data[key] = []
        json_data[key].append(value)

def jsave(filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

proxy_pool = []
proxy_lock = threading.Lock()
proxy_idx  = [0]

def load_proxies(filepath):
    proxies = []
    try:
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if not line.startswith("http"):
                        line = "http://" + line
                    proxies.append(line)
    except:
        r(f"[ - ] Failed to load proxies from: {filepath}")
    return proxies

def test_proxy(proxy):
    try:
        start = time.time()
        rr = requests.get(
            "http://ip-api.com/json/",
            proxies={"http": proxy, "https": proxy},
            timeout=8
        )
        latency = time.time() - start
        if rr.status_code == 200:
            return (proxy, round(latency, 3))
    except:
        pass
    return None

def init_proxies(filepath):
    global proxy_pool
    raw = load_proxies(filepath)
    p(f"[ * ] Testing {len(raw)} proxies...")
    results = []
    lock    = threading.Lock()
    threads = []

    def worker(px):
        result = test_proxy(px)
        if result:
            with lock:
                results.append(result)

    for px in raw:
        t = threading.Thread(target=worker, args=(px,), daemon=True)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

    results.sort(key=lambda x: x[1])
    proxy_pool = [item[0] for item in results]
    p(f"[ + ] {len(proxy_pool)} proxies ready — sorted fastest to slowest")
    if not proxy_pool:
        r("[ - ] No working proxies found — proceeding with direct connection")

def get_proxy():
    with proxy_lock:
        if not proxy_pool:
            return None
        px = proxy_pool[proxy_idx[0] % len(proxy_pool)]
        proxy_idx[0] += 1
        return px

def proxies_dict():
    px = get_proxy()
    if not px:
        return None
    return {"http": px, "https": px}

security_headers = {
    "Strict-Transport-Security":         ("HSTS — enforces HTTPS on all connections",                True),
    "X-Content-Type-Options":            ("Prevents MIME-type sniffing attacks",                     True),
    "X-Frame-Options":                   ("Blocks clickjacking via iframe embedding",                True),
    "Content-Security-Policy":           ("Controls which resources the page can load",              True),
    "Referrer-Policy":                   ("Controls referrer info sent in requests",                 True),
    "X-XSS-Protection":                  ("XSS filter for legacy browsers",                          False),
    "Permissions-Policy":                ("Controls browser feature access (mic, camera, etc.)",     False),
    "X-Permitted-Cross-Domain-Policies": ("Controls Adobe cross-domain access",                      False),
    "Cache-Control":                     ("Controls how responses are cached",                       False),
    "Access-Control-Allow-Origin":       ("CORS — defines allowed cross-origin access",              False),
    "Cross-Origin-Embedder-Policy":      ("Prevents loading cross-origin resources without consent", False),
    "Cross-Origin-Opener-Policy":        ("Isolates the browsing context from other origins",        False),
    "Cross-Origin-Resource-Policy":      ("Controls who can load this resource cross-origin",        False),
}

def check_headers(domain):
    hdrs = {
        "User-Agent": generate_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    px       = proxies_dict()
    response = None
    for scheme in ("https", "http"):
        try:
            response = requests.get(
                f"{scheme}://{domain}",
                headers=hdrs,
                timeout=10,
                proxies=px,
                allow_redirects=True
            )
            break
        except:
            pass

    if response is None:
        r("[ - ] Failed to fetch headers")
        return

    p("\n• Security Headers:")
    present = []
    missing = []

    for header, (desc, required) in security_headers.items():
        val = response.headers.get(header)
        if val:
            present.append({"header": header, "value": val, "description": desc})
            print(
                Colorate.Horizontal(Colors.green_to_cyan, f"  [+] {header}") +
                " : " +
                Colorate.Horizontal(Colors.red_to_yellow, val)
            )
            print(Colorate.Horizontal(Colors.cyan_to_blue, f"      └─ {desc}"))
        else:
            missing.append({"header": header, "required": required, "description": desc})
            label = " [REQUIRED — MISSING]" if required else " [missing]"
            col   = Colors.red_to_yellow if required else Colors.purple_to_blue
            print(Colorate.Horizontal(col, f"  [-] {header}{label}"))
            print(Colorate.Horizontal(Colors.cyan_to_blue, f"      └─ {desc}"))

    with json_lock:
        json_data["headers"] = {
            "url":         response.url,
            "status_code": response.status_code,
            "present":     present,
            "missing":     missing,
        }

def tr(domain):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    px = proxies_dict()
    try:
        rr = requests.get(f"https://{domain}", headers=headers, timeout=5, proxies=px)
        if rr.status_code < 400:
            return "https"
    except requests.exceptions.RequestException:
        pass
    try:
        rr = requests.get(f"http://{domain}", headers=headers, timeout=5, proxies=px)
        if rr.status_code < 400:
            return "http"
    except requests.exceptions.RequestException:
        pass
    return "dead"

def ps(domain, path, ty, headers):
    if ty not in ("http", "https"):
        print(Colorate.Horizontal(Colors.red_to_purple, "[ * ] Invalid Scheme!"))
        return

    url  = f"{ty}://{domain}{path}"
    dead = ["not found", "suspended", "this domain is for sale", "domain expired", "account suspended", "parked"]
    px   = proxies_dict()

    try:
        rr = requests.get(url, headers=headers, timeout=5, allow_redirects=False, proxies=px)

        if 200 <= rr.status_code < 300:
            if not any(kw in rr.text.lower() for kw in dead):
                pf(url, rr.status_code)
                jadd("paths", {"url": url, "status_code": rr.status_code})

        elif rr.status_code in (301, 302, 307, 308):
            loc = rr.headers.get("Location", "")
            if loc and not any(kw in loc.lower() for kw in ["parkingcrew", "sedo", "godaddy"]):
                pf(url, rr.status_code)
                jadd("paths", {"url": url, "status_code": rr.status_code})

    except requests.exceptions.ConnectionError:
        pass
    except requests.exceptions.Timeout:
        print(Colorate.Horizontal(Colors.red_to_purple, f"[ * ] Timeout: {url}"))
    except requests.exceptions.RequestException:
        pass

def ds(domain, sub, ty, headers):
    if ty not in ("http", "https"):
        print(Colorate.Horizontal(Colors.red_to_purple, "[ * ] Invalid Scheme!"))
        return

    url  = f"{ty}://{sub}.{domain}"
    dead = ["not found", "suspended", "this domain is for sale", "domain expired", "account suspended", "parked"]
    px   = proxies_dict()

    try:
        rr = requests.get(url, headers=headers, timeout=5, allow_redirects=False, proxies=px)

        if 200 <= rr.status_code < 300:
            if not any(kw in rr.text.lower() for kw in dead):
                pf(url, rr.status_code)
                jadd("subdomains", {"url": url, "status_code": rr.status_code})

        elif rr.status_code in (301, 302, 307, 308):
            loc = rr.headers.get("Location", "")
            if loc and not any(kw in loc.lower() for kw in ["parkingcrew", "sedo", "godaddy"]):
                pf(url, rr.status_code)
                jadd("subdomains", {"url": url, "status_code": rr.status_code})

    except requests.exceptions.ConnectionError:
        pass
    except requests.exceptions.Timeout:
        print(Colorate.Horizontal(Colors.red_to_purple, f"[ * ] Timeout: {url}"))
    except requests.exceptions.RequestException:
        pass

def mp(domain):
    ty = tr(domain)
    if ty == "dead":
        print(Colorate.Horizontal(Colors.red_to_purple, f"[ * ] Dead: {domain}"))
        return

    sem = threading.Semaphore(20)

    def run(path):
        with sem:
            headers = {
                "User-Agent": generate_user_agent(),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }
            ps(domain, path, ty, headers)

    threads = [threading.Thread(target=run, args=(one,), daemon=True) for one in paths]
    for t in threads: t.start()
    for t in threads: t.join()

def md(domain):
    ty = tr(domain)
    if ty == "dead":
        print(Colorate.Horizontal(Colors.red_to_purple, f"[ * ] Dead: {domain}"))
        return

    sem = threading.Semaphore(20)

    def run(sub):
        with sem:
            headers = {
                "User-Agent": generate_user_agent(),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }
            ds(domain, sub, ty, headers)

    threads = [threading.Thread(target=run, args=(one,), daemon=True) for one in domains]
    for t in threads: t.start()
    for t in threads: t.join()

banner = """⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣷⢸⣧⠨⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣤⣄⡾⠱⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⢿⡿⣹⡤⣿⡏⠸⡅⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⣿⠟⣰⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⢈⢷⡡⣧⢻⣿⠖⠣⠣⣤⣀⡀⠀⣠⠶⣿⣿⣿⣿⢕⣾⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠤⣴⣤⣶⣤⣤⣀⡀⠀⠸⢰⠘⡧⢸⠀⠻⡄⢐⠀⠎⠙⢟⣵⠈⠀⣟⢾⡹⢣⣿⡿⣟⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢦⠹⣾⣽⣿⣿⣿⣿⣿⣿⣷⣤⣃⢌⢱⠉⡆⠀⣽⠈⡁⠀⣡⢿⢪⢀⣾⢭⠚⣡⠟⣼⡻⢌⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡉⢶⣷⣦⣼⣉⠟⡿⣿⣿⣿⣿⣿⣿⣷⣜⢇⢣⠀⠈⠚⡄⠀⣿⠋⠆⡞⠋⠈⡔⢎⡞⣱⡛⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠰⡈⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠿⣿⣿⣿⣾⣎⣝⡿⣿⣿⠿⣿⣿⣷⡄⠂⢃⠃⠀⠀⠏⡘⠀⢓⣀⠴⣉⢞⣼⠓⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠐⡀⢃⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣾⡎⢀⢴⠛⡞⠙⣷⡀⢸⠀⣄⢀⣶⢁⠀⡞⠠⡁⣞⡞⠂⠀⠠⣄⣒⢶⣲⣶⣶⣤⣤⣀⡀⠀⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠂⠄⢂⠘⡀⠂⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣍⣀⣁⠙⠳⢤⡉⠻⡝⣧⠎⠀⣟⠘⣴⢞⡼⠐⠀⣕⠼⢃⡰⢌⣳⡼⣽⣾⣿⣿⣿⣿⣿⣿⡿⠃⢀⣏⢷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⡐⠠⢈⠒⡈⠄⠒⡀⠁⠀⠀⠀⠀⣀⣄⠒⡄⠡⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠿⣿⣿⣶⣤⡁⠄⢮⡻⡜⢰⡇⣶⣯⠞⡵⠟⠃⡤⢘⢦⢱⣋⣥⠿⣾⣻⣿⣿⣿⣿⣽⣶⡆⠀⢨⠘⢢⠑⠕⠂⠄⡀⠀⠀⠀⠀⠐⠠⣁⠂⠒⠄⢊⠐⠠⠀⠀⠀⢀⢞⡱⣎⣷⡹⢇⡡⢀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠉⡇⢆⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣶⣾⣷⣽⡻⢿⣿⠛⠦⠁⠁⡄⢸⢹⠏⠀⠠⠒⣁⣊⣡⡘⠮⢗⣾⡿⢿⠿⠛⠛⠉⠉⠉⠉⠉⠀⠀⠡⢂⠌⡠⢉⠐⡀⠂⠄⠀⠀⡘⠠⠄⡈⢁⠊⠄⠌⠀⠁⠀⠀⠄⡈⢲⢩⠖⣿⢻⡵⢢⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠐⠨⣈⠉⠒⠠⠀⠄⠀⠀⠀⠀⢆⠱⢈⠒⡩⢍⡛⠷⣥⣀⠆⢄⠀⣀⡊⠞⠀⠴⠎⠙⠫⣹⣿⣿⣿⣶⣅⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠆⢂⡐⠄⠨⠐⡁⢂⠐⠀⠄⡁⢂⠐⠈⠄⡈⠄⡀⠀⠀⠀⠀⣐⣚⠛⠛⠛⠻⠗⠤⠈⠄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⢮⣀⠁⠌⠀⢀⡢⣉⡔⣂⣅⣊⣔⣡⣊⣵⣒⣢⣍⢹⢡⠻⣿⣦⣼⣄⣤⣨⣖⡿⣿⣿⣿⣿⢻⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠠⠐⠈⠄⡁⢂⠐⡈⠀⠈⠰⡀⢈⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠩⢥⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠱⠀⢠⡿⣳⢿⣿⣿⣿⣿⣿⣿⠿⠟⠋⠉⠉⠉⠃⠁⠙⠻⠽⠿⣿⣿⣿⣮⡘⢿⣿⣽⢷⣽⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠂⠐⠀⠀⠁⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⢁⠣⣿⣿⠿⠟⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⡌⢪⢿⣎⡽⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠠⠀⠀⠀⠀⡁⠌⠙⡙⢛⠒⠦⢀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠊⠁⠀⠀⠀⢀⡿⡸⢿⣶⣖⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣆⢻⣿⣷⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢂⠐⡈⠴⠡⠎⡜⢂⠡⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣄⠉⢿⣏⠷⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⡍⡿⠏⠀⠀⠀⠀⠠⠐⡈⠄⡐⢈⠰⡀⠔⡠⢁⠠⠈⠄⠀⠀⣸⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠐⡠⢁⠒⡀⠂⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⡅⠐⡻⠁⠤⠑⡈⠄⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⢌⡑⠢⠔⡈⠰⢁⢂⠡⠌⢐⠀⠂⠁⠄⠂⠄⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⢀⠂⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡷⠃⠁⢀⠢⠑⡈⡠⣿⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠠⢄⠡⠒⡈⠥⡈⢆⠱⢈⠆⡈⠄⠡⠈⠄⢀⠂⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣀⡤⠤⢖⣞⣯⣵⣤⣂⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⢍⠚⡁⠌⡄⢢⠑⠀⡱⢋⠁⢀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠂⠁⠊⠄⠃⡌⠐⡈⠄⠡⠐⠠⠈⠀⠀⠀⠀⠀⠄⠁⠀⠀⠀⢀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠈⠡⡰⣭⡽⠽⠞⠛⣉⡠⠚⠀⠀⠀⠀⠀⢠⠀⡘⠠⠀⢄⠢⢡⠐⠁⠀⠀⠐⠢⠔⠋⠲⢌⡎⢟⡷⢦⡀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠐⢀⠂⢀⠠⠀⠂⠀⡁⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⡄⠂⠀⠄⠑⣀⡠⢔⡢⠛⠀⠀⠀⠀⠀⠀⠀⢀⢼⣷⣤⡅⠠⠀⠁⢈⠂⠚⠀⠀⢠⠀⠀⠀⠐⠀⠈⢍⡹⢓⠮⣕⠲⠒⡂⣀⣬⠄⡠⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢀⠐⡈⢄⠁⡂⠄⠂⠀⠈⠄⡁⠂⠄⠂⠄⠈⠄⠁⠀⠠⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡀⠀⠄⠀⠠⠉⠀⠁⠀⢀⡐⠰⢄⣀⠀⠀⠀⣀⣵⠿⣛⡫⠁⠐⡀⠘⠂⠁⣀⠀⢸⢸⢐⠀⠀⠐⠤⠤⣄⡀⠉⠚⢆⡋⢆⠑⡈⠉⠄⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡘⢄⠂⢆⡁⢂⠌⡐⠠⠐⠀⠀⠐⡠⠁⠌⡐⠌⡐⢀⠂⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠠⠀⠀⠀⠠⢀⠉⠥⢒⣛⡉⠀⢀⠂⠌⣸⢃⡾⠃⠀⠸⡌⡇⡆⠠⠉⠀⠀⠲⣈⢂⠀⠀⠀⠈⠆⠑⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢆⡘⠤⣉⠦⡐⠌⡐⠠⠁⢂⠐⠈⠀⠀⠐⠠⠐⡈⠄⡀⢂⠠⠀⢁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠶⣾⢡⣮⣜⣶⡛⠌⣠⣿⣧⣈⢐⢋⡀⠄⠈⢰⠰⠀⢡⠸⡆⠠⠀⠄⠒⢠⠈⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢂⠜⡰⢱⠪⠔⡡⠢⠕⠁⠀⠀⠀⠀⠀⠈⠤⢁⡐⠠⠐⠀⡄⢈⠀⠄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠁⠀⣼⣿⣿⡿⣻⢞⣼⠏⠐⠀⠇⠀⡇⠁⠀⠉⡀⢣⠈⠒⢠⠈⢂⠡⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢄⠊⠔⡡⢊⠜⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠂⠔⡁⡍⢆⠈⠄⢂⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⢳⣿⠟⣵⢫⣾⠏⡔⠀⠆⠀⠰⠁⠀⡀⡀⠘⢄⠈⠌⠠⠈⠄⠂⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠐⠈⠄⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠱⡜⢠⠈⠀⠂⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢪⠏⡿⣡⡾⣱⠏⣡⢞⠀⢌⡜⠀⠀⣸⡄⢰⢱⠀⠀⠀⠂⢁⠌⡐⢈⠐⢌⡀⢂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢆⠠⢁⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡔⡩⢀⣴⡟⠀⠘⢁⡆⠀⠀⠀⠀⢧⢹⣧⠀⡄⣿⢠⡐⠀⠀⠀⠈⠈⠐⠀⠡⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠁⠲⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠄⢃⠤⢶⡿⣿⣿⡂⠀⠋⠀⠀⠀⠀⠀⠘⣿⡜⡈⢷⡈⠇⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠐⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠃⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⠇⠂⠜⢈⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""

resolver = dns.resolver.Resolver(configure=False)
resolver.nameservers = ["8.8.8.8", "1.1.1.1"]

parser = argparse.ArgumentParser()
parser.add_argument("domain",          help="Domain to recon (without \"https://\")\nex. google.com")
parser.add_argument("-a",  "--all",    help="Full scan: ports, paths, sub-domains.", action="store_true")
parser.add_argument("-po", "--ports",  help="Scan all IP ports.", action="store_true")
parser.add_argument("-pa", "--paths",  help="Scan paths in URL.", action="store_true")
parser.add_argument("-d",  "--domains",help="Scan sub-domains.", action="store_true")
parser.add_argument("-r",  "--reverse",help="Reverse DNS on resolved IP, run recon on root domain.", action="store_true")
parser.add_argument("-he", "--headers",help="Check security headers.", action="store_true")
parser.add_argument("-pr", "--proxies",help="Proxies file to use (one per line, host:port or proto://host:port).")
parser.add_argument("-j",  "--json",   help="Save results to JSON file. ex: --json=results.json", dest="json")

c = Console()

def get_root(hostname):
    parts = hostname.rstrip(".").split(".")
    if len(parts) >= 2:
        return ".".join(parts[-2:])
    return hostname

def rev(ip):
    rev_data = {"ip": ip}
    try:
        host, aliases, ips = socket.gethostbyaddr(ip)

        print(
            Colorate.Horizontal(Colors.blue_to_cyan, "Hostname") +
            " : " +
            Colorate.Horizontal(Colors.red_to_yellow, host)
        )
        rev_data["hostname"] = host

        if aliases:
            print(
                Colorate.Horizontal(Colors.blue_to_cyan, "Aliases") +
                " : " +
                Colorate.Horizontal(Colors.red_to_yellow, ", ".join(aliases))
            )
            rev_data["aliases"] = aliases

        if ips:
            print(
                Colorate.Horizontal(Colors.blue_to_cyan, "IPs") +
                " : " +
                Colorate.Horizontal(Colors.red_to_yellow, ", ".join(ips))
            )
            rev_data["ips"] = ips

        root = get_root(host)
        rev_data["root_domain"] = root

        p(f"\n[ * ] Root Domain: {root}")
        p("[ * ] Running Recon on Root Domain...")
        recon(root)

    except socket.herror:
        r("[ - ] Name Not Found..")
        rev_data["error"] = "Name Not Found"

    jset("reverse_dns", rev_data)

def ax(domain, owners):
    axfr_data = {}
    for ns in owners:
        ns_str = str(ns)
        try:
            zone = dns.zone.from_xfr(
                dns.query.xfr(ns_str, domain)
            )
            r(f"[ + ] Zone Transfer ENABLED on {ns}")
            records = []
            for name, node in zone.nodes.items():
                r(f"- {name}")
                records.append(str(name))
            axfr_data[ns_str] = {"enabled": True, "records": records}
        except:
            r(f"[ - ] AXFR blocked on {ns}")
            axfr_data[ns_str] = {"enabled": False}
    return axfr_data

common_ports = {
    20:   {"service": "FTP-Data",        "description": "File Transfer Protocol (data transfer)"},
    21:   {"service": "FTP-Control",     "description": "File Transfer Protocol (control)"},
    22:   {"service": "SSH",             "description": "Secure Shell (remote login)"},
    23:   {"service": "Telnet",          "description": "Unencrypted remote login"},
    25:   {"service": "SMTP",            "description": "Simple Mail Transfer Protocol"},
    53:   {"service": "DNS",             "description": "Domain Name System"},
    67:   {"service": "DHCP-Server",     "description": "Dynamic Host Configuration Protocol (server)"},
    68:   {"service": "DHCP-Client",     "description": "Dynamic Host Configuration Protocol (client)"},
    69:   {"service": "TFTP",            "description": "Trivial File Transfer Protocol"},
    80:   {"service": "HTTP",            "description": "HyperText Transfer Protocol"},
    110:  {"service": "POP3",            "description": "Post Office Protocol v3"},
    119:  {"service": "NNTP",            "description": "Network News Transfer Protocol"},
    123:  {"service": "NTP",             "description": "Network Time Protocol"},
    137:  {"service": "NetBIOS-NS",      "description": "NetBIOS Name Service"},
    138:  {"service": "NetBIOS-DGM",     "description": "NetBIOS Datagram Service"},
    139:  {"service": "NetBIOS-SSN",     "description": "NetBIOS Session Service"},
    143:  {"service": "IMAP",            "description": "Internet Message Access Protocol"},
    161:  {"service": "SNMP",            "description": "Simple Network Management Protocol"},
    179:  {"service": "BGP",             "description": "Border Gateway Protocol"},
    389:  {"service": "LDAP",            "description": "Lightweight Directory Access Protocol"},
    443:  {"service": "HTTPS",           "description": "HTTP Secure (SSL/TLS)"},
    445:  {"service": "SMB",             "description": "Server Message Block"},
    465:  {"service": "SMTPS",           "description": "Secure SMTP"},
    500:  {"service": "ISAKMP",          "description": "IPSec Key Management"},
    587:  {"service": "SMTP-Submission", "description": "Mail submission port"},
    636:  {"service": "LDAPS",           "description": "Secure LDAP"},
    993:  {"service": "IMAPS",           "description": "Secure IMAP"},
    995:  {"service": "POP3S",           "description": "Secure POP3"},
    1433: {"service": "MSSQL",           "description": "Microsoft SQL Server"},
    1521: {"service": "Oracle-DB",       "description": "Oracle Database"},
    2049: {"service": "NFS",             "description": "Network File System"},
    2082: {"service": "cPanel",          "description": "cPanel (HTTP)"},
    2083: {"service": "cPanel-SSL",      "description": "cPanel (HTTPS)"},
    2086: {"service": "WHM",             "description": "Web Host Manager (HTTP)"},
    2087: {"service": "WHM-SSL",         "description": "Web Host Manager (HTTPS)"},
    3306: {"service": "MySQL",           "description": "MySQL Database"},
    3389: {"service": "RDP",             "description": "Remote Desktop Protocol"},
    5432: {"service": "PostgreSQL",      "description": "PostgreSQL Database"},
    5900: {"service": "VNC",             "description": "Virtual Network Computing"},
    6379: {"service": "Redis",           "description": "Redis Database"},
    8080: {"service": "HTTP-Alt",        "description": "Alternative HTTP port"},
    8443: {"service": "HTTPS-Alt",       "description": "Alternative HTTPS port"},
}

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            result = s.connect_ex((ip, port))

            info = common_ports.get(
                port,
                {"service": "Unknown", "description": "No description"}
            )

            if result == 0:
                status     = "Open"
                status_col = Colors.green_to_cyan
            else:
                status     = "Closed"
                status_col = Colors.red_to_yellow

            if status == "Open":
                print(
                    Colorate.Horizontal(Colors.cyan_to_blue, f"[ {ip} ] ")
                    + f" Status: "
                    + Colorate.Horizontal(status_col, status)
                    + f"  -  Port: "
                    + Colorate.Horizontal(Colors.blue_to_cyan, str(port))
                    + f"  -  Service: "
                    + Colorate.Horizontal(Colors.purple_to_blue, info['service'])
                    + f"  -  Description: "
                    + Colorate.Horizontal(Colors.purple_to_red, info['description'])
                )
                jadd("ports", {
                    "port":        port,
                    "status":      "Open",
                    "service":     info["service"],
                    "description": info["description"],
                })

    except socket.timeout:
        print(
            Colorate.Horizontal(
                Colors.green_to_cyan,
                f"[ {ip} ] Status: Filtered - Port: {port}"
            )
        )

def track(ip):
    px = proxies_dict()
    try:
        data = requests.get(
            f"http://ip-api.com/json/{ip}?fields=66846719",
            proxies=px,
            timeout=10
        ).json()
    except:
        r("[ - ] Failed to fetch IP info")
        return

    tracker = {}
    for k, v in data.items():
        if k == "query":
            continue
        print(
            Colorate.Horizontal(Colors.blue_to_cyan, str(k)) +
            " : " +
            Colorate.Horizontal(Colors.red_to_yellow, str(v))
        )
        tracker[k] = v

    jset("tracker", tracker)

def scanports(ipaddress, start, end):
    port_range  = range(int(start), int(end))
    ip          = ipaddress
    max_threads = 120
    threadings  = []
    for port in port_range:
        t = threading.Thread(target=scan_port, args=(ip, port))
        t.start()
        threadings.append(t)
        if len(threadings) >= max_threads:
            for th in threadings:
                th.join()
            threadings = []
    for th in threadings:
        th.join()

def mainscan(ipaddress):
    step = 1000
    for start in range(1, 10000, step):
        end = start + step
        scanports(ipaddress, start, end)
        time.sleep(3)

def recon(domain):
    if "https://" in domain:
        domain = domain.split("https://")[1]
    if "www" in domain:
        domain = domain.split("www.")[1]

    rec_data = {
        "ipv4":        [],
        "ipv6":        [],
        "nameservers": [],
        "mx":          [],
        "txt":         [],
        "cname":       [],
        "soa":         None,
        "axfr":        {},
    }
    owners = False

    p("• IPv4:")
    try:
        main = socket.gethostbyname(domain)
        r(f"- {main}")
        ans = resolver.resolve(domain, "A")
        for one in ans:
            addr = str(one)
            r(f"- {addr}")
            if addr not in rec_data["ipv4"]:
                rec_data["ipv4"].append(addr)
    except:
        pass

    p("\n• IPv6:")
    try:
        ans = resolver.resolve(domain, "AAAA")
        for one in ans:
            addr = str(one)
            r(f"- {addr}")
            rec_data["ipv6"].append(addr)
    except:
        r("[ * ] IPv6 Not Found")

    p("\n• Owners:")
    try:
        owners = resolver.resolve(domain, "NS")
        for one in owners:
            ns = str(one)
            r(f"- {ns}")
            rec_data["nameservers"].append(ns)
    except:
        owners = False
        r("[ * ] No Owners Found")

    p("\n• Mails:")
    try:
        ans = resolver.resolve(domain, "MX")
        for one in ans:
            mx = str(one)
            r(f"- {mx}")
            rec_data["mx"].append(mx)
    except:
        r("[ * ] No Mails Found")

    p("\n• TXT:")
    try:
        ans = resolver.resolve(domain, "TXT")
        for one in ans:
            txt = str(one)
            r(f"- {txt}")
            rec_data["txt"].append(txt)
    except:
        r("[ * ] No TXT Found")

    p('\n• Servers:')
    try:
        ans = resolver.resolve(f"www.{domain}", "CNAME")
        for one in ans:
            cname = str(one)
            r(f"- {cname}")
            rec_data["cname"].append(cname)
    except:
        r("[ * ] No Server Names Found")

    p("\n• SOA:")
    try:
        soa = resolver.resolve(domain, "SOA")
        for n in soa:
            r(f"- Master NS: {n.mname}")
            r(f"- Admin Mail: {n.rname}")
            rec_data["soa"] = {"mname": str(n.mname), "rname": str(n.rname)}
    except:
        r("[ + ] No SOA Found")

    if owners:
        p("\n• AXFR:")
        rec_data["axfr"] = ax(domain, owners)

    jset("recon", rec_data)


if len(sys.argv) == 1:
    print(Colorate.Horizontal(Colors.green_to_cyan, banner))
    domain       = c.input("[white][ [cyan]+ [white]] Enter The Domain:                       ")
    proxies_inp  = c.input("[white][ [cyan]+ [white]] Proxies File (blank to skip):           ")
    proxies_file = proxies_inp.strip() if proxies_inp.strip() else None
    json_inp     = c.input("[white][ [cyan]+ [white]] Save to JSON File (blank to skip):      ")
    jsfi    = json_inp.strip() if json_inp.strip() else None
    hdr_inp      = c.input("[white][ [cyan]+ [white]] Check Security Headers? [ Y - N ]:      ")
    headers_check = hdr_inp.lower() == "y"
    rev_inp      = c.input("[white][ [cyan]+ [white]] Reverse DNS? [ Y - N ]:                 ")
    reverse      = rev_inp.lower() == "y"
    a            = c.input("[white][ [cyan]+ [white]] Full Recon? [ Y - N ]:                  ")
    if a.lower() == "n":
        ports    = c.input("[white][ [cyan]+ [white]] Ports Scan? [ Y - N ]:                  ")
        paths1   = c.input("[white][ [cyan]+ [white]] Paths Scan? [ Y - N ]:                  ")
        domains1 = c.input("[white][ [cyan]+ [white]] Sub-domains Scan? [ Y - N ]:            ")
    else:
        ports    = "n"
        paths1   = "n"
        domains1 = "n"

    os.system("clear")

    if a.lower() == "y":
        a = True
    else:
        a = False

    if ports.lower() == "y":
        ports = True
    else:
        ports = False

    if paths1.lower() == "y":
        paths1 = True
    else:
        paths1 = False

    if domains1.lower() == "y":
        domains1 = True
    else:
        domains1 = False

else:
    args          = parser.parse_args()
    domain        = args.domain
    a             = args.all
    ports         = args.ports
    paths1        = args.paths
    domains1      = args.domains
    reverse       = args.reverse
    headers_check = args.headers
    proxies_file  = args.proxies
    jsfi     = args.json

print(Colorate.Horizontal(Colors.green_to_cyan, banner))

if "https://" in domain:
    domain = domain.split("https://")[1]
if "www." in domain:
    domain = domain.split("www.")[1]
domain = domain.split("/")[0]

if proxies_file:
    init_proxies(proxies_file)

jset("domain", domain)

try:
    ip = socket.gethostbyname(domain)
    jset("ip", ip)
except socket.gaierror:
    r("[ - ] Something went wrong...")
    r("[ * ] Check the domain or Internet connection and try again.")
    sys.exit(1)

rec = Markdown("# Starting Recon...")
c.print(rec, style="cyan")
recon(domain)

print("\n\n\n")
tra = Markdown("# Starting Tracker...")
c.print(tra, style="cyan")
track(ip)

if headers_check:
    print("\n\n\n")
    hd = Markdown("# Checking Security Headers...")
    c.print(hd, style="cyan")
    check_headers(domain)

if reverse:
    print("\n\n\n")
    rv = Markdown("# Reverse DNS...")
    c.print(rv, style="cyan")
    rev(ip)

if a:
    print("\n\n\n")
    sp = Markdown("# Scanning Ports...")
    c.print(sp, style="cyan")
    mainscan(ip)
    print("\n\n\n")
    spp = Markdown("# Scanning Paths...")
    c.print(spp, style="cyan")
    mp(domain)
    print("\n\n\n")
    dp = Markdown("# Scanning Sub-Domains...")
    c.print(dp, style="cyan")
    md(domain)

if ports and not domains1 and not paths1:
    print("\n\n\n")
    sp = Markdown("# Scanning Ports...")
    c.print(sp, style="cyan")
    mainscan(ip)

if paths1 and not ports and not domains1:
    print("\n\n\n")
    spp = Markdown("# Scanning Paths...")
    c.print(spp, style="cyan")
    mp(domain)

if domains1 and not ports and not paths1:
    print("\n\n\n")
    dp = Markdown("# Scanning Sub-Domains...")
    c.print(dp, style="cyan")
    md(domain)

if paths1 and ports and not domains1:
    print("\n\n\n")
    sp = Markdown("# Scanning Ports...")
    c.print(sp, style="cyan")
    mainscan(ip)
    print("\n\n\n")
    spp = Markdown("# Scanning Paths...")
    c.print(spp, style="cyan")
    mp(domain)

if paths1 and domains1 and not ports:
    print("\n\n\n")
    spp = Markdown("# Scanning Paths...")
    c.print(spp, style="cyan")
    mp(domain)
    print("\n\n\n")
    dp = Markdown("# Scanning Sub-Domains...")
    c.print(dp, style="cyan")
    md(domain)

if ports and domains1 and not paths1:
    print("\n\n\n")
    sp = Markdown("# Scanning Ports...")
    c.print(sp, style="cyan")
    mainscan(ip)
    print("\n\n\n")
    dp = Markdown("# Scanning Sub-Domains...")
    c.print(dp, style="cyan")
    md(domain)

if ports and domains1 and paths1:
    print("\n\n\n")
    sp = Markdown("# Scanning Ports...")
    c.print(sp, style="cyan")
    mainscan(ip)
    print("\n\n\n")
    spp = Markdown("# Scanning Paths...")
    c.print(spp, style="cyan")
    mp(domain)
    print("\n\n\n")
    dp = Markdown("# Scanning Sub-Domains...")
    c.print(dp, style="cyan")
    md(domain)

if jsfi:
    jsave(jsfi)
    p(f"\n[ + ] Results saved to {jsfi}")
