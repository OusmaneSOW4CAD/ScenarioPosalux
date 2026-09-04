import requests

urls = [
    "https://pdm13-1-codebeamer.connexateurs.com/cb/rest",
    "https://pdm13-1-codebeamer.connexateurs.com/cb/rest/user",
    "https://pdm13-1-codebeamer.connexateurs.com/cb/rest/project",
    "https://pdm13-1-codebeamer.connexateurs.com/cb/rest/configuration"
]

for url in urls:
    try:
        r = requests.get(url, timeout=10)
        print(url)
        print(r.status_code)
        print("-" * 50)
    except Exception as e:
        print(url, e)
