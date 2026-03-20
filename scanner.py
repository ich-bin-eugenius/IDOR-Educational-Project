from bs4 import BeautifulSoup
from colorama import Fore
import asyncio
import aiohttp


async def check_id(session, base_url, uid, semaphore, css_tag):
    """
    Performs an asynchronous HTTP GET request with CSS selector-based scraping.

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

                    # Smart Scraping: uses dynamic CSS selector from settings
                    target = soup.select_one(css_tag)
                    name = target.get_text(strip=True) if target else ""

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


async def run_audit(settings):
    """
    Manages the lifecycle of the asynchronous scan.
    """
    semaphore = asyncio.Semaphore(settings["semaphore"])
    start_id, end_id = settings["range"]

    async with aiohttp.ClientSession() as session:
        tasks = [check_id(session, settings["url"], uid, semaphore, settings["tag"])
                 for uid in range(start_id, end_id + 1)]
        results_raw = await asyncio.gather(*tasks)

    return [r for r in results_raw if r is not None]
