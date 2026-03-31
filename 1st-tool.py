import request
target_url = str(input('Insert Url: '))
while target_url == '' or not target_url.startswith(('http://', 'https://')):
    target_url = str(input('Insert full correct Url (including http:// or https://) Please: '))
headers = {
    "server": "reveals server info (usually identifies the web server software, e.g., Apache, Nginx)",
    "X-Frame-Options": "prevents clickjacking by controlling whether this page can be embedded in an iframe",
    "X-Powered-By": " reveals what tech the server uses, helps attackers ",  # e.g., "ASP.NET, PHP" – can leak server‑side stack info
    "Strict-Transport-Security": "forces the browser to use HTTPS only (HSTS), mitigating downgrade attacks",
    "X-Content-Type-Options": "prevents MIME‑type sniffing; usually set to 'nosniff' to avoid content‑type confusion",
    "Content-Security-Policy": "HIGH RISK if missing or misconfigured; prevents XSS and other injection attacks by whitelisting allowed sources"
}
with requests.session() as session:
    try:
        response = session.get(target_url, timeout=10)
        for header in headers:
            if header in response.headers:
                print(f'{header}: {response.headers[header]}')
            else:
                print(f'{header}: MISSING, {headers[header]}.')

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        print('Connection error/possible wrong domain or Timeout occurred.')
         
