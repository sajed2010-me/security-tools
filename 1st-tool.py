import requests
from concurrent.futures import ThreadPoolExecutor
import os.path
import time
from colorama import Fore, Back, Style, init
init(autoreset=True)
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
                print('Sorry, file not found.')
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
        continue




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
            with ThreadPoolExecutor(max_workers=100) as executor:
                with open('recon_tool_results_file.txt', mode='w', encoding='utf-8') as file:

                    responses = executor.map(lambda url:session.get(url, timeout=10), file_urls)
                    start = time.time()


                    for response, link in zip(responses, file_urls):
                        end = time.time()
                        time_taken = end - start
                        result = response.status_code
                        print(f'Status code is: {result}')
                        file.write(f'Status code is: {result}\n')
                        print(f"==PRESENT HEADERS== in {link} ")
                        file.write(f"==PRESENT HEADERS== in {link}\n")
                        for header in security_headers:
                            if header in response.headers:
                                if header == 'Server' or header == 'X-Powered-By':
                                    print(Fore.BLUE + Style.BRIGHT + f'{header}({header_severity[header]}) is PRESENT: {response.headers[header]}')
                                    file.write(f'{header}({header_severity[header]}) is PRESENT: {response.headers[header]}\n')
                                else:
                                    print(Fore.GREEN + Style.BRIGHT + f'{header}({header_severity[header]}) is PRESENT: {response.headers[header]}')
                                    file.write(f'{header}({header_severity[header]}) is PRESENT: {response.headers[header]}\n')
                        print(f"== MISSING HEADERS== in {link}")
                        file.write(f"==MISSING HEADERS== in {link}\n")
                        for header in security_headers:
                            if header not in response.headers:
                                if header_severity[header] == 'Severity: Low':
                                    print(Fore.BLUE + Style.BRIGHT + f'{header}({header_severity[header]}) is MISSING: {security_headers[header]}')
                                    file.write(f'{header}({header_severity[header]}) is MISSING: {security_headers[header]}\n')
                                elif header_severity[header] == 'Severity: Medium':
                                    print(Fore.YELLOW + Style.BRIGHT + f'{header}({header_severity[header]}) is MISSING: {security_headers[header]}')
                                    file.write(f'{header}({header_severity[header]}) is MISSING: {security_headers[header]}\n')
                                elif header_severity[header] == 'Severity: High':
                                    print(Fore.RED + Style.BRIGHT + f'{header}({header_severity[header]}) is MISSING: {security_headers[header]}')
                                    file.write(f'{header}({header_severity[header]}) is MISSING: {security_headers[header]}')
                                elif header_severity[header] == 'Severity: Low/Medium':
                                    print(Fore.YELLOW + Style.BRIGHT + f'{header}({header_severity[header]}) is MISSING: {security_headers[header]}')
                                    file.write(f'{header}({header_severity[header]}) is MISSING: {security_headers[header]}\n')
                        print(f'Time taken is: {time_taken} seconds')
                        file.write(f'Time taken is: {time_taken} seconds\n')
        elif choice == "l":
            with open('recon_tool_results_link.txt', mode='w', encoding='utf-8') as file:
                start = time.time()
                response = session.get(cleaned, timeout=10)
                print(f"==PRESENT HEADERS== in {cleaned} ")
                file.write(f"==PRESENT HEADERS== in {cleaned}\n")
                end = time.time()
                time_taken = end - start
                for header in security_headers:
                    if header in response.headers:
                        if header == 'Server' or header == 'X-Powered-By':
                            print(Fore.BLUE + Style.BRIGHT + f'{header}({header_severity[header]}) is PRESENT: {response.headers[header]}')
                            file.write(f'{header}({header_severity[header]}) is PRESENT: {response.headers[header]}\n')
                        else:
                            print(Fore.GREEN + Style.BRIGHT + f'{header}({header_severity[header]}) is PRESENT: {response.headers[header]}')
                            file.write(f'{header}({header_severity[header]}) is PRESENT: {response.headers[header]}\n')


                print(f"==MISSING HEADERS== in {cleaned} ")
                file.write(f"==MISSING HEADERS== in {cleaned}\n")
                for header in security_headers:
                    if header not in response.headers:
                        if header_severity[header] == 'Severity: Low':
                            print(Fore.BLUE + Style.BRIGHT + f'{header}({header_severity[header]}) is MISSING: {security_headers[header]}')
                            file.write(f'{header}({header_severity[header]}) is MISSING: {security_headers[header]}\n')
                        elif header_severity[header] == 'Severity: Medium':
                            print(Fore.YELLOW + Style.BRIGHT + f'{header}({header_severity[header]}) is MISSING: {security_headers[header]}')
                            file.write(f'{header}({header_severity[header]}) is MISSING: {security_headers[header]}\n')
                        elif header_severity[header] == 'Severity: High':
                            print(Fore.RED + Style.BRIGHT + f'{header}({header_severity[header]}) is MISSING: {security_headers[header]}')
                            file.write(f'{header}({header_severity[header]}) is MISSING: {security_headers[header]}')
                        elif header_severity[header] == 'Severity: Low/Medium':
                            print(Fore.YELLOW + Style.BRIGHT + f'{header}({header_severity[header]}) is MISSING: {security_headers[header]}')
                            file.write(f'{header}({header_severity[header]}) is MISSING: {security_headers[header]}\n')

                print(f'Time taken is: {time_taken} seconds')
                file.write(f'Time taken is: {time_taken} seconds\n')
    except requests.exceptions.ConnectionError:
        print('Connection Error occurred.')
    except requests.exceptions.Timeout:
        print('Connection Timeout occurred.')
    except requests.exceptions.InvalidURL:
        print('Invalid URL, Please make sure url is correct.')
    except KeyboardInterrupt:
        print('Action interrupted.')
         
