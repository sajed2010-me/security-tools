import requests
target_url = str(input('Insert full correct Url (including http:// or https://) Please: '))
while True:
    # noinspection PyUnusedLocal,PyRedeclaration
    cleaned = target_url.strip() #used in if conditions below
    if ' ' in cleaned:
        print('There may be an extra space in the URL, please remove it.')
        target_url = str(input('Insert full correct Url: '))
        cleaned = target_url.strip()
        continue
    if cleaned == '':
        print('Where is the URL!')
        target_url = str(input('Insert full correct Url, pretty please: '))
        cleaned = target_url.strip()
        continue
    if not cleaned.startswith(('http://', 'https://')):
        print('You still forgot the scheme or a part of it  (http:// or https://)! The URL you entered is not a valid URL.')
        target_url = str(input('Insert full correct Url (WITH http:// or https://): '))
        cleaned = target_url.strip()
        continue

    break

security_headers = {
    "Server": "reveals server info (usually identifies the web server software, e.g., Apache, Nginx)",
    "X-Frame-Options": "prevents clickjacking by controlling whether this page can be embedded in an iframe",
    "X-Powered-By": " reveals backend tech stack (e.g., PHP, ASP.NET) — useful for attackers ",  # e.g., "ASP.NET, PHP" – can leak server‑side stack info
    "Strict-Transport-Security": "forces the browser to use HTTPS only (HSTS), mitigating downgrade attacks",
    "X-Content-Type-Options": "prevents MIME‑type sniffing; usually set to 'nosniff' to avoid content‑type confusion",
    "Content-Security-Policy": "HIGH RISK if missing or misconfigured; prevents XSS and other injection attacks by whitelisting allowed sources"
}
with requests.Session() as session:
    try:
        session.max_redirects = 15
        response = session.get(cleaned, timeout=10)
        for header in security_headers:
            if header in response.headers:
                print(f'{header}: {response.headers[header]}')
            else:
                print(f'{header}: MISSING, {security_headers[header]}.')

    except requests.exceptions.ConnectionError:
        print('Connection Error occurred.')
    except requests.exceptions.Timeout:
        print('Connection Timeout occurred.')
    except requests.exceptions.InvalidURL:
        print('Invalid URL, Please make sure url is correct.')
         
