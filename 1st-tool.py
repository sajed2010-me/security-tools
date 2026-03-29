import requests
target_url = str(input('Insert Url: '))
headers = ['server', 'X-Frame-Options', 'X-Powered-By', 'Strict-Transport-Security', 'X-Content-Type-Options', 'Content-Security-Policy' ]
with requests.session() as session:
     response = session.get(target_url)
     for header in headers:
        if header in response.headers:
         print(f'{header}: {response.headers[header]}')
        else:
            print(f'{header}: MISSING, POTENTIAL SECURITY ISSUE.')
