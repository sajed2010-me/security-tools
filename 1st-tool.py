import requests
import os.path
while True:
    choice = str(input("Do you wish to upload a file or input link(f/l): ")).lower()
    if choice == "l":
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

        break

    elif choice == "f":
        file_name = str(input('Insert full correct File Path: '))
        file_urls = []
        while True:
            if os.path.isfile(file_name):
                with open(file_name) as content:
                    for link in content:
                        link = link.strip()
                        if link.startswith(('http://', 'https://')):
                            file_urls.append(link)


                if len(file_urls) == 0:
                    print('Sorry, looks like there were no urls in your file.')
                    break
            else:
                file_name2 = str(input('Would you like to upload another file? (y/n): '))
                if file_name2 == 'y':
                    file_name = str(input('Ready to give this another try?(insert file): '))
                    continue
                else:
                    break
            break
        break
    else:
        choice = str(input('Please choose either f for file upload or l for link(f/l): '))




security_headers = {
    "Server": "reveals server info (usually identifies the web server software, e.g., Apache, Nginx)",
    "X-Frame-Options": "prevents clickjacking by controlling whether this page can be embedded in an iframe",
    "X-Powered-By": " reveals backend tech stack (e.g., PHP, ASP.NET) — useful for attackers ",  # e.g., "ASP.NET, PHP" – can leak server‑side stack info
    "Strict-Transport-Security": "forces the browser to use HTTPS only (HSTS), mitigating downgrade attacks",
    "X-Content-Type-Options": "prevents MIME‑type sniffing; usually set to 'nosniff' to avoid content‑type confusion",
    "Content-Security-Policy": "if missing or misconfigured; prevents XSS and other injection attacks by whitelisting allowed sources",
    "Referrer-Policy": "Controls how much URL info leaks to other sites when a user clicks a link. Missing means full URLs including sensitive params get leaked",
    "Permissions-Policy": "Controls whether the page can access camera, mic, geolocation etc. Missing means no restrictions on feature access",
    "Cross-Origin-Opener-Policy": "Isolates your browsing context from other origins. Missing enables cross-origin attacks like Spectre",
    "Cross-Origin-Resource-Policy": "Controls which origins can load your resources. Missing enables cross-origin data leaks",
    "Cross-Origin-Embedder-Policy": "Works with COOP to enable powerful features safely. Missing limits access to certain browser APIs"
}
header_severity = {
    'Server': 'Severity: Low',
    'X-Frame-Options': 'Severity: Medium',
    'X-Powered-By': 'Severity: Low',
    'Strict-Transport-Security': 'Severity: Medium',
    'X-Content-Type-Options': 'Severity: Low/Medium',
    'Content-Security-Policy': 'Severity: High',
    'Referrer-Policy': 'Severity: Low',
    'Permissions-Policy': 'Severity: Low/Medium',
    'Cross-Origin-Opener-Policy': 'Severity: Medium',
    'Cross-Origin-Resource-Policy': 'Severity: Medium',
    'Cross-Origin-Embedder-Policy': 'Severity: Low/Medium'
}
with requests.Session() as session:
    try:
        session.max_redirects = 15
        if choice == "f":
            for link in file_urls:
                response = session.get(link, timeout=10)
                print(f"==PRESENT HEADERS== in {link} ")
                for header in security_headers:
                    if header in response.headers:
                        print(f'{header}({header_severity[header]}) is PRESENT: {response.headers[header]}')
                print(f"== MISSING HEADERS== in {link}")
                for header in security_headers:
                    if header not in response.headers:
                        print(f'{header}({header_severity[header]}) is MISSING: {security_headers[header]}')
        elif choice == "l":
            response = session.get(cleaned, timeout=10)
            print("==PRESENT HEADERS==")
            for header in security_headers:
                if header in response.headers:
                    print(f'{header}({header_severity[header]}) is PRESENT: {response.headers[header]}')
            print("==MISSING HEADERS==")
            for header in security_headers:
                if header not in response.headers:
                    print(f'{header}({header_severity[header]}) is MISSING: {security_headers[header]}')
    except requests.exceptions.ConnectionError:
        print('Connection Error occurred.')
    except requests.exceptions.Timeout:
        print('Connection Timeout occurred.')
    except requests.exceptions.InvalidURL:
        print('Invalid URL, Please make sure url is correct.')
         
