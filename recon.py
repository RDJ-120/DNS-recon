import os, re, socket, argparse, sys, threading, requests, time
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


def tr(domain):
    url = f"https://{domain}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    try:
        rr = requests.get(url, headers=headers, timeout=5)
        if rr.status_code < 400:
            return "https"
    except requests.exceptions.RequestException:
        pass

    try:
        url = f"http://{domain}"
        rr = requests.get(url, headers=headers, timeout=5)
        if rr.status_code < 400:
            return "http"
    except requests.exceptions.RequestException:
        pass

    return "dead"

def ps(domain, path, ty, headers):
    if ty not in ("http", "https"):
        print(Colorate.Horizontal(Colors.red_to_purple, "[ * ] Invalid Scheme!"))
        return

    url = f"{ty}://{domain}{path}"
    dead = ["not found", "suspended", "this domain is for sale", "domain expired", "account suspended", "parked"]

    try:
        rr = requests.get(url, headers=headers, timeout=5, allow_redirects=False)

        if 200 <= rr.status_code < 300:
            if not any(kw in rr.text.lower() for kw in dead):
                pf(url, rr.status_code)

        elif rr.status_code in (301, 302, 307, 308):
            loc = rr.headers.get("Location", "")
            if loc and not any(kw in loc.lower() for kw in ["parkingcrew", "sedo", "godaddy"]):
                pf(url, rr.status_code)

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

    url = f"{ty}://{sub}.{domain}"
    dead = ["not found", "suspended", "this domain is for sale", "domain expired", "account suspended", "parked"]

    try:
        rr = requests.get(url, headers=headers, timeout=5, allow_redirects=False)

        if 200 <= rr.status_code < 300:
            if not any(kw in rr.text.lower() for kw in dead):
                pf(url, rr.status_code)

        elif rr.status_code in (301, 302, 307, 308):
            loc = rr.headers.get("Location", "")
            if loc and not any(kw in loc.lower() for kw in ["parkingcrew", "sedo", "godaddy"]):
                pf(url, rr.status_code)

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
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠊⠁⠀⠀⠀⢀⡿⡸⢿⣶⣖⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣆⢻⣿⣷⠃⠀⠀⠀⠀⠀⠀⢀⠠⠐⠈⢄⡈⡐⢀⠂⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢂⠐⡈⠴⠡⠎⡜⢂⠡⠀⠀⠀⠀⠀⠀⠀
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
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡁⢪⡼⠫⢚⡁⢀⡴⠃⢠⠋⠀⠀⡜⣿⡿⠘⣬⣇⠠⠀⠀⠂⠑⡔⠂⠌⡠⠘⢠⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡔⡩⢀⣴⡟⠀⠘⢁⡆⠀⠀⠀⠀⢧⢹⣧⠀⡄⣿⢠⡐⠀⠀⠀⠈⠈⠐⠀⠡⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠁⠲⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠄⢃⠤⢶⡿⣿⣿⡂⠀⠋⠀⠀⠀⠀⠀⠘⣿⡜⡈⢷⡈⠇⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠐⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠃⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⠇⠂⠜⢈⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""


resolver = dns.resolver.Resolver(configure=False)

resolver.nameservers = ["8.8.8.8", "1.1.1.1"]

parser = argparse.ArgumentParser()
parser.add_argument("domain", help="Domain to recon(without \"https://\"\nex. google.com")
parser.add_argument("-a", "--all", help="Scan All IP ports after get data & sub domains checker & sub paths checker", action="store_true")
parser.add_argument("-po", "--ports", help="Scan All IP ports.", action="store_true")
parser.add_argument("-pa", "--paths", help="Scan Paths in URL..", action="store_true")
parser.add_argument("-d", "--domains", help="Scan Sub-domains in URL.", action="store_true")

c = Console()

def ax(domain, owners):
    for ns in owners:
        try:
            zone = dns.zone.from_xfr(
                dns.query.xfr(str(ns), domain)
            )
            r(f"[ + ] Zone Transfer ENABLED on {ns}")

            for name, node in zone.nodes.items():
                r(f"- {name}")

        except:
            r(f"[ - ] AXFR blocked on {ns}")

common_ports = {
    20:  {"service": "FTP-Data",     "description": "File Transfer Protocol (data transfer)"},
    21:  {"service": "FTP-Control",  "description": "File Transfer Protocol (control)"},
    22:  {"service": "SSH",          "description": "Secure Shell (remote login)"},
    23:  {"service": "Telnet",       "description": "Unencrypted remote login"},
    25:  {"service": "SMTP",         "description": "Simple Mail Transfer Protocol"},
    53:  {"service": "DNS",          "description": "Domain Name System"},
    67:  {"service": "DHCP-Server",  "description": "Dynamic Host Configuration Protocol (server)"},
    68:  {"service": "DHCP-Client",  "description": "Dynamic Host Configuration Protocol (client)"},
    69:  {"service": "TFTP",         "description": "Trivial File Transfer Protocol"},
    80:  {"service": "HTTP",         "description": "HyperText Transfer Protocol"},
    110: {"service": "POP3",         "description": "Post Office Protocol v3"},
    119: {"service": "NNTP",         "description": "Network News Transfer Protocol"},
    123: {"service": "NTP",          "description": "Network Time Protocol"},
    137: {"service": "NetBIOS-NS",   "description": "NetBIOS Name Service"},
    138: {"service": "NetBIOS-DGM",  "description": "NetBIOS Datagram Service"},
    139: {"service": "NetBIOS-SSN",  "description": "NetBIOS Session Service"},
    143: {"service": "IMAP",         "description": "Internet Message Access Protocol"},
    161: {"service": "SNMP",         "description": "Simple Network Management Protocol"},
    179: {"service": "BGP",          "description": "Border Gateway Protocol"},
    389: {"service": "LDAP",         "description": "Lightweight Directory Access Protocol"},
    443: {"service": "HTTPS",        "description": "HTTP Secure (SSL/TLS)"},
    445: {"service": "SMB",          "description": "Server Message Block"},
    465: {"service": "SMTPS",        "description": "Secure SMTP"},
    500: {"service": "ISAKMP",       "description": "IPSec Key Management"},
    587: {"service": "SMTP-Submission","description": "Mail submission port"},
    636: {"service": "LDAPS",        "description": "Secure LDAP"},
    993: {"service": "IMAPS",        "description": "Secure IMAP"},
    995: {"service": "POP3S",        "description": "Secure POP3"},
    1433: {"service": "MSSQL",       "description": "Microsoft SQL Server"},
    1521: {"service": "Oracle-DB",   "description": "Oracle Database"},
    2049: {"service": "NFS",         "description": "Network File System"},
    2082: {"service": "cPanel",      "description": "cPanel (HTTP)"},
    2083: {"service": "cPanel-SSL",  "description": "cPanel (HTTPS)"},
    2086: {"service": "WHM",         "description": "Web Host Manager (HTTP)"},
    2087: {"service": "WHM-SSL",     "description": "Web Host Manager (HTTPS)"},
    3306: {"service": "MySQL",       "description": "MySQL Database"},
    3389: {"service": "RDP",         "description": "Remote Desktop Protocol"},
    5432: {"service": "PostgreSQL",  "description": "PostgreSQL Database"},
    5900: {"service": "VNC",         "description": "Virtual Network Computing"},
    6379: {"service": "Redis",       "description": "Redis Database"},
    8080: {"service": "HTTP-Alt",    "description": "Alternative HTTP port"},
    8443: {"service": "HTTPS-Alt",   "description": "Alternative HTTPS port"},
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
                status = "Open"
                status_col = Colors.green_to_cyan
            else:
                status = "Closed"
                status_col = Colors.red_to_yellow

            if status == "Open":
                print(
                    Colorate.Horizontal(
                        Colors.cyan_to_blue,
                        f"[ {ip} ] "
                    )
                    + f" Status: "
                    + Colorate.Horizontal(status_col, status)
                    + f"  -  Port: "
                    + Colorate.Horizontal(Colors.blue_to_cyan, str(port))
                    + f"  -  Service: "
                    + Colorate.Horizontal(Colors.purple_to_blue, info['service'])
                    + f"  -  Description: "
                    + Colorate.Horizontal(Colors.purple_to_red, info['description'])
                )

    except socket.timeout:
        print(
            Colorate.Horizontal(
                Colors.green_to_cyan,
                f"[ {ip} ] Status: Filtered - Port: {port}"
            )
        )
        
 
def track(ip):
    url = f"http://ip-api.com/json/{ip}?fields=66846719"
    data = requests.get(url).json()

    for k, v in data.items():
        if k == "query":
            continue

        print(
            Colorate.Horizontal(Colors.blue_to_cyan, str(k)) +
            " : " +
            Colorate.Horizontal(Colors.red_to_yellow, str(v))
        )

def scanports(ipaddress, start, end):
	ports = range(int(start), int(end))
	x = 0
	if 1==1:
		ip = ipaddress
		max_threads = 120
		threadings = []
		for port in ports:
		    t = threading.Thread(target=scan_port, args=(ip, port))
		    t.start()
		    threadings.append(t)
		    if len(threadings) >= max_threads:
		        for th in threadings:
		            th.join()
		            threadings = []

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
	
	p("• IPv4:")
	try:
		main = socket.gethostbyname(domain)
		r(f"- {main}")
		ans = resolver.resolve(domain, "A")
		for one in ans:
			r(f"- {one}")
	except:
		pass
	
	p("\n• IPv6:")
	try:
		ans = resolver.resolve(domain, "AAAA")
		for one in ans:
			r(f"- {one}")
	except:
		r("[ * ] IPv6 Not Found")
	
	p("\n• Owners:")
	try:
		owners = resolver.resolve(domain, "NS")
		for one in owners:
			r(f"- {one}")
	except:
	    owners = False
	    r("[ * ] No Owners Found")
	
	p("\n• Mails:")
	try:
		ans = resolver.resolve(domain, "MX")
		for one in ans:
			r(f"- {one}")
	except:
		r("[ * ] No Mails Found")
	
	p("\n• TXT:")
	try:
		ans = resolver.resolve(domain, "TXT")
		for one in ans:
			r(f"- {one}")
	except:
		r("[ * ] No TXT Found")
		
	p('\n• Servers:')
	try:
		ans = resolver.resolve(f"www.{domain}", "CNAME")
		for one in ans:
			r(f"- {one}")
	except:
		r("[ * ] No Server Names Found")
		
	p("\n• SOA:")
	try:
	   	soa = resolver.resolve(domain, "SOA")
	   	for n in soa:
	   	   	r(f"- Master NS: {n.mname}")
	   	   	r(f"- Admin Mail: {n.rname}")
	except:
		r("[ + ] No SOA Found")
		
	
	if owners:
	    p("\n• AXFR:")
	    ax(domain, owners)
	else:
	    pass
	
        	
if len(sys.argv) == 1:
    print(Colorate.Horizontal(Colors.green_to_cyan, banner))
    domain = c.input("[white][ [cyan]+ [white]] Enter The Domain:   ")
    ports = c.input("[white][ [cyan]+ [white]] Ports Scan?[ Y - N ]:   ")
    paths1 = c.input("[white][ [cyan]+ [white]] Paths Scan?[ Y - N ]:   ")
    domains1 = c.input("[white][ [cyan]+ [white]] Sub-domains Scan?[ Y - N ]:   ")
    a = c.input("[white][ [cyan]+ [white]] Full Recon?[ Y - N ]:   ")
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
    args = parser.parse_args()
    domain = args.domain
    a = args.all
    ports = args.ports
    paths1 = args.paths
    domains1 = args.domains
    
print(Colorate.Horizontal(Colors.green_to_cyan, banner))
if "https://" in domain:
    domain = domain.split("https://")[1]
if "www." in domain:
    domain = domain.split("www.")[1]
    
domain = domain.split("/")[0]
ip = socket.gethostbyname(domain)

rec = Markdown("# Starting Recon...")
c.print(rec, style="cyan")

recon(domain)

print("\n\n\n")
tra = Markdown("# Starting Tracker...")
c.print(tra, style="cyan")
track(ip)
        
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
