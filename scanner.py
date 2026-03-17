from bs4 import BeautifulSoup
from colorama import Fore, init
import asyncio
import aiohttp

init(autoreset=True)


def print_banner():
    banner = f"""{Fore.YELLOW}
    ███████╗ █████╗ ██╗   ██╗██╗██████╗ ██╗   ██╗██╗  ██╗██╗  ██╗ █████╗ 
    ╚══███╔╝██╔══██╗██║   ██║██║██╔══██╗██║   ██║██║  ██║██║  ██║██╔══██╗
      ███╔╝ ███████║██║   ██║██║██████╔╝██║   ██║█████║ ║███████║███████║
     ███╔╝  ██╔══██║╚██╗ ██╔╝██║██╔══██╗██║   ██║██╔══██║██╔══██║██╔══██║
    ███████╗██║  ██║ ╚████╔╝ ██║██║  ██║╚██████╔╝██║  ██║██║  ██║██║  ██║
    ╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
    {Fore.RED}          IDOR Auditor v2.1 | Created by Eugene Zavirukha
    {Fore.RED}          Last update: 17.03.2026 {Fore.YELLOW}- asyncio - fix bugs
    {Fore.RED}          [!] Created for EDUCATION PURPOSES only [!]
    """
    print(banner)


async def main():
    """
        Automates IDOR (Insecure Direct Object Reference) testing over a range of IDs by managing user input,
        environment setup, and asynchronous execution...

        1. User chooses an environment (Local vs Online).
        2. Validates the URL structure.
        3. Initializes a persistent aiohttp.ClientSession for optimized connection pooling.
        4. Dispatches concurrent 'check_id' tasks and aggregates the results using asyncio.gather.
        5. Generates a sanitized .txt report named after the target URL and person range.

        Raises:
            ValueError: If non-integer values are provided for ID range boundaries.
            Exception: Captures and logs errors during the file-writing process.
        """
    semaphore = asyncio.Semaphore(10)

    print_banner()
    print(f"1. Local Lab (127.0.0.1)\n2. Online Target")

    base_url = ""
    # Environment selection
    while not base_url:
        choosing_environment = input(f"{Fore.CYAN}Select environment: ").strip()

        if choosing_environment == "1":
            base_url = "http://127.0.0.1:5000/story.php?person="
        elif choosing_environment == "2":
            user_url = input(
                f"{Fore.YELLOW}Enter target URL (for example: http://site.com/story.php?person=): ").strip()
            if user_url.startswith("http"):
                base_url = user_url
            else:
                print(f"{Fore.RED}[!] URL must start with http:// or https://")
        else:
            print(f"{Fore.RED}[!] Invalid choice.")

    # Id range
    try:
        start_id = int(input(f"{Fore.CYAN}Start ID: "))
        end_id = int(input(f"{Fore.CYAN}End ID: "))
    except ValueError:
        print(f"{Fore.RED}[!] Invalid ID, using default 1-10.")
        start_id, end_id = 1, 10

    print(f"\n{Fore.CYAN}[*] Starting audit on range {start_id} to {end_id}...\n")

    # Async execution
    async with aiohttp.ClientSession() as session:
        tasks = [check_id(session, base_url, uid, semaphore) for uid in range(start_id, end_id + 1)]
        results_raw = await asyncio.gather(*tasks)

    # Filter out None results
    results = [r for r in results_raw if r is not None]

    # Saving logic
    if results:
        save_choice = input(f"\n{Fore.YELLOW}Save results to .txt? (y/n): ").lower().strip()
        if save_choice == 'y':
            # Cleaning file name because of Windows
            clean_filename = (base_url.replace("http://", "").replace("https://", "").replace("/", "_").replace("?",
                                                                                                                "_")
                              .replace(
                "=", "_").replace(":", "_"))
            filename = f"{clean_filename}{start_id}-{end_id}.txt"

            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("\n".join(results))
                print(f"{Fore.CYAN}[*] Saved to: {filename}")
            except Exception as e:
                print(f"{Fore.RED}[!] Save failed: {e}")
    else:
        print(f"\n{Fore.WHITE}[?] No vulnerabilities found to save.")


async def check_id(session, base_url, uid, semaphore):
    """
        Performs an asynchronous HTTP GET request to verify a specific ID for IDOR vulnerabilities.

        Args:
            session (aiohttp.ClientSession): The active aiohttp session used for network requests.
            base_url (str): The target endpoint (for example: 'http://target.com/story.php?person=').
            uid (int): The specific User ID to be appended to the base_url for testing.

        Returns:
            str: A formatted string "ID = Name" if a vulnerability is confirmed and data is parsed.
            None: Returns None if the ID is invalid (404), the page is empty, or a network
                  error occurs.

        Logic:
        - Sends an asynchronous GET request with a 5-second timeout.
        - Inspects the HTTP status code (specifically looking for 200 OK).
        - Utilizes BeautifulSoup to locate sensitive data within a specific <span> tag.
        - Handles aiohttp-specific exceptions (ClientConnectorError, TimeoutError) to
          ensure the global scan loop remains uninterrupted.
          :param uid:
          :param base_url:
          :param session:
          :param semaphore:
        """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    async with semaphore:
        try:
            async with session.get(f"{base_url}{uid}", headers=headers, timeout=5) as res:
                if res.status == 200:
                    html = await res.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    name_tag = soup.find('span', style="margin-left:2px;")
                    name = name_tag.get_text(strip=True) if name_tag else ""
                    if name:
                        print(f"{Fore.GREEN}[+] Vulnerability IDOR CONFIRMED! ID {uid}: {name}")
                        return f"{uid} = {name}"
                    else:
                        print(f"{Fore.WHITE}[.] ID {uid}: Page empty or data missing.")
                elif res.status == 404:
                    print(f"{Fore.YELLOW}[-] ID {uid}: 404 Not Found.")
                else:
                    print(f"{Fore.YELLOW}[?] ID {uid}: Received status code {res.status}")

        except aiohttp.ClientConnectorError:
            print(f"{Fore.RED}\n[!] Connection Error at ID {uid}. Check if the server is running.")
        except asyncio.TimeoutError:
            print(f"{Fore.RED}\n[!] Request Timeout at ID {uid}.")
        except Exception as e:
            print(f"{Fore.RED}[!] An unexpected error occurred at ID {uid}: {e}")
        return None


if __name__ == "__main__":
    asyncio.run(main())
