# Web Recon Tool (recon.py)

A multi-module passive and active reconnaissance tool written in Python. Designed for authorized security assessments, it performs DNS enumeration, IP geolocation, TCP port scanning, HTTP path discovery, and subdomain brute-forcing against a target domain from the command line or an interactive prompt.

---

## Features

- **DNS Enumeration** — Resolves A, AAAA, NS, MX, TXT, CNAME, and SOA records using custom resolvers (Google and Cloudflare DNS).
- **AXFR Zone Transfer Testing** — Attempts zone transfers against discovered nameservers to identify misconfigured DNS servers.
- **IP Geolocation Tracking** — Queries ip-api.com for detailed geolocation and ASN data on the resolved IP address.
- **TCP Port Scanning** — Scans all ports from 0 to 9999 using a threaded scanner (120 concurrent threads per batch). Identifies open ports and maps them to known services.
- **HTTP Path Discovery** — Brute-forces over 300 common web paths including admin panels, config files, backup archives, exposed APIs, and sensitive endpoints. Uses randomized User-Agent headers per request.
- **Subdomain Enumeration** — Tests over 200 common subdomain prefixes using threaded HTTP HEAD requests with false-positive filtering.
- **Dual Interface** — Runs interactively with guided prompts when invoked with no arguments, or fully non-interactively via CLI flags.

---

## Requirements

- Python 3.8 or higher
- Internet access to the target and external APIs

---

## Installation

Clone or download the repository, then install dependencies:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install requests rich pystyle dnspython user_agent
```

---

## Usage

![Scan Mode Example](https://github.com/user-attachments/assets/bcf8eeac-93f6-488b-a0db-31a682326b85)

### Interactive Mode

Run the script with no arguments to enter the guided prompt:

```bash
python recon.py
```

You will be asked to provide the target domain and choose which modules to run.

### Command-Line Mode

```bash
python recon.py <domain> [options]
```

#### Positional Argument

| Argument | Description                              |
|----------|------------------------------------------|
| `domain` | Target domain to recon (e.g. `google.com`). Do not include `https://` or `www.` — the tool strips them automatically. |

#### Options

| Flag              | Short | Description                                                                 |
|-------------------|-------|-----------------------------------------------------------------------------|
| `--all`           | `-a`  | Run all modules: port scan, path discovery, and subdomain enumeration.      |
| `--ports`         | `-po` | Scan all TCP ports (0–9999) on the resolved IP address.                     |
| `--paths`         | `-pa` | Brute-force common HTTP paths on the target domain.                         |
| `--domains`       | `-d`  | Enumerate subdomains using a built-in wordlist.                             |

---

## Examples

Run full DNS recon and geolocation only:

```bash
python recon.py example.com
```

Run DNS recon with port scanning:

```bash
python recon.py example.com --ports
```

Run DNS recon with subdomain and path discovery:

```bash
python recon.py example.com --domains --paths
```

Run every module at once:

```bash
python recon.py example.com --all
```

---

## Execution Flow

Regardless of which options are selected, the tool always executes the following in order:

1. Strip `https://`, `www.`, and any trailing path from the provided domain.
2. Resolve the domain to an IP address via `socket.gethostbyname`.
3. Run DNS enumeration (A, AAAA, NS, MX, TXT, CNAME, SOA records).
4. Attempt AXFR zone transfer against all discovered nameservers.
5. Run IP geolocation via ip-api.com.

After the base recon, optional modules run based on the flags provided:

- `--ports` triggers the TCP scanner against the resolved IP.
- `--paths` triggers the HTTP path brute-forcer against the domain.
- `--domains` triggers the subdomain brute-forcer against the domain.
- `--all` triggers all three modules in sequence: ports, paths, domains.

---

## Module Details

### DNS Enumeration

Queries the following record types using `8.8.8.8` and `1.1.1.1` as resolvers:

| Record | Purpose                                      |
|--------|----------------------------------------------|
| A      | IPv4 address(es) for the domain              |
| AAAA   | IPv6 address(es) for the domain              |
| NS     | Authoritative nameservers                    |
| MX     | Mail exchange servers                        |
| TXT    | SPF, DKIM, verification records              |
| CNAME  | Canonical name (server alias) for `www`      |
| SOA    | Start of authority: master NS and admin mail |

### AXFR Zone Transfer

Attempts a DNS zone transfer (AXFR) from each discovered nameserver. If successful, dumps all DNS records in the zone — a critical misconfiguration that exposes the full internal DNS structure.

### IP Geolocation

Queries `ip-api.com` with all available fields enabled. Returns data including country, region, city, ISP, ASN, organization, timezone, and proxy/VPN detection flags.

### Port Scanner

Scans TCP ports 0 through 9999 in batches of 1000 with a 3-second delay between batches. Uses up to 120 concurrent threads per batch. Each open port is matched against a built-in service map covering 40+ well-known ports (SSH, HTTP, MySQL, RDP, Redis, etc.).

### Path Discovery

Iterates a wordlist of 300+ paths covering admin panels, PHP scripts, environment files, Git/SVN metadata, database interfaces, API endpoints, log files, backup archives, framework-specific routes, and DevOps tooling paths. Each request uses a randomized User-Agent and a HEAD check followed by a GET to reduce false positives.

### Subdomain Enumeration

Tests 200+ common subdomain prefixes (e.g. `api`, `dev`, `staging`, `mail`, `vpn`, `k8s`) using threaded HTTP HEAD requests. Filters responses containing "not found", "suspended", or "error" to reduce noise.

---

## Legal Notice

This tool is intended for use on systems and domains you own or have explicit written permission to test. Unauthorized use against third-party infrastructure is illegal and unethical. The author assumes no responsibility for misuse.

---

## Dependencies

| Package     | Purpose                                         |
|-------------|-------------------------------------------------|
| `requests`  | HTTP requests for path and subdomain scanning   |
| `rich`      | Console output formatting and Markdown rendering|
| `pystyle`   | Gradient terminal color output                  |
| `dnspython` | DNS record resolution and zone transfer queries |
| `user_agent`| Random User-Agent string generation             |
