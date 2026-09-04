import requests

USER = "user_posalux"
PASSWORD = "5nZ0i6SzyZgVbutlonger"


url = "https://pdm13-1-codebeamer.connexateurs.com/cb/rest"

r = requests.get(
    url,
    auth=(USER, PASSWORD)
)

print("STATUS =", r.status_code)
print(r.text)
