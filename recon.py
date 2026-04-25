import dns.resolver
import dns.query
import dns.zone
from rich.console import Console

c = Console()

resolver = dns.resolver.Resolver(configure=False)

resolver.nameservers = ["8.8.8.8", "1.1.1.1"]

domain = c.input("Enter The Domain:	")
print("\n\n")

c.print("IPv4:")
try:
	answers = resolver.resolve(domain, "A")
	for rdata in answers:
   	 c.print("- " + rdata.to_text())
	c.print("\n")
except:
   c.print("[ + ] No IP For This Domain")
   
c.print("Owners:")
try:
	owners = resolver.resolve(domain, "NS")
	for owner in owners:
		c.print(f"- {owner}")
	c.print("\n")
except:
	c.print("[ + ] No owner for this domain")

try:
	ans2 = resolver.resolve(domain, "AAAA")
	c.print("IPv6:")
	for rdata in ans2:
		c.print(f"- {rdata.to_text()}")
	c.print("\n")
	
except:
	c.print("[ + ] No IPv6 For This Domain..")


c.print("Mails:")
try:
	mails = resolver.resolve(domain, "MX")
	for mail in mails:
		c.print(f"- {mail}")
	c.print("\n")
except:
	c.print("[ + ] No Mails For This Domain")

c.print("TXTs:")
try:
	txts = resolver.resolve(domain, "TXT")
	for txt in txts:
		c.print(f'- {txt}')
	c.print("\n")
except:
	c.print("[ + ] TXTs Not Found..")

c.print("Server Name:")
try:
	servers = resolver.resolve(f"www.{domain}", "CNAME")
	for server in servers:
		c.print(f"- {server.target}")
	c.print("\n")
except:
	c.print("[ + ] No Server Name Found..")
	c.print("\n")
	
	
try:
    soa = resolver.resolve(domain, "SOA")
    c.print("SOA:")
    for r in soa:
        c.print(f"- Master NS: {r.mname}")
        c.print(f"- Admin Mail: {r.rname}")
    
except:
    c.print("[ + ] No SOA Found")
c.print("\n")

for ns in owners:
    try:
        zone = dns.zone.from_xfr(
            dns.query.xfr(str(ns), domain)
        )
        c.print(f"[ ! ] Zone Transfer ENABLED on {ns}")
        for name, node in zone.nodes.items():
            c.print(name)
    except:
        c.print(f"[ - ] AXFR blocked on {ns}")
        
print("\n")
