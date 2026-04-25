# DNS Recon Tool (Python)

## Overview

A simple DNS reconnaissance tool written in Python. It performs multiple
DNS queries on a target domain to gather useful information such as IP
addresses, mail servers, name servers, and more.

The tool uses custom DNS resolvers and provides clean terminal output
using the `rich` library.

------------------------------------------------------------------------

## Features

-   Resolve IPv4 addresses (A records)
-   Resolve IPv6 addresses (AAAA records)
-   Retrieve Name Servers (NS records)
-   Retrieve Mail Servers (MX records)
-   Retrieve TXT records
-   Detect CNAME (Server name)
-   Extract SOA (Start of Authority) information
-   Attempt Zone Transfer (AXFR)
-   Custom DNS resolvers (Google & Cloudflare)

------------------------------------------------------------------------

## Technologies Used

Python 3 dnspython rich

------------------------------------------------------------------------

## Installation

    pip install dnspython rich

------------------------------------------------------------------------

## Usage

    python dns_recon.py

Then enter the target domain when prompted.

------------------------------------------------------------------------

## Example Output

    IPv4:
    - 142.250.x.x

    Owners:
    - ns1.example.com

    IPv6:
    - 2a00:1450:400...

    Mails:
    - mail.example.com

    TXTs:
    - v=spf1 include:_spf.example.com

    Server Name:
    - example.cdn.net

    SOA:
    - Master NS: ns1.example.com
    - Admin Mail: admin.example.com

------------------------------------------------------------------------

## How It Works

1.  A custom DNS resolver is configured using public DNS servers
    (8.8.8.8, 1.1.1.1)
2.  Multiple DNS record types are queried:
    -   A, AAAA
    -   NS
    -   MX
    -   TXT
    -   CNAME
    -   SOA
3.  The tool attempts a Zone Transfer (AXFR) on each name server
4.  Results are printed using formatted output

------------------------------------------------------------------------

## Zone Transfer (AXFR)

The tool attempts to perform a zone transfer: - If successful →
indicates a misconfigured DNS server - If blocked → server is properly
secured

------------------------------------------------------------------------

## Error Handling

-   Handles missing records gracefully
-   Prevents crashes on failed queries
-   Displays informative messages for each failure

------------------------------------------------------------------------

## Requirements

    Python 3.x

------------------------------------------------------------------------

## Security Notes

-   AXFR should be disabled on production servers
-   Public DNS data may be incomplete or cached
-   Always use responsibly and only on authorized targets

------------------------------------------------------------------------

## License

MIT License
