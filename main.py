import asyncio
from colorama import Fore, init
import scanner
import utils

init(autoreset=True)


def print_banner():
    banner = f"""{Fore.YELLOW}
    ███████╗ █████╗ ██╗   ██╗██╗██████╗ ██╗   ██╗██╗  ██╗██╗  ██╗ █████╗ 
    ╚══███╔╝██╔══██╗██║   ██║██║██╔══██╗██║   ██║██║  ██║██║  ██║██╔══██╗
      ███╔╝ ███████║██║   ██║██║██████╔╝██║   ██║█████║ ║███████║███████║
     ███╔╝  ██╔══██║╚██╗ ██╔╝██║██╔══██╗██║   ██║██╔══██║██╔══██║██╔══██║
    ███████╗██║  ██║ ╚████╔╝ ██║██║  ██║╚██████╔╝██║  ██║██║  ██║██║  ██║
    ╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
    {Fore.RED}          IDOR Auditor v2.3 | ...
    {Fore.RED}          Created by Eugene Zavirukha | Last update: 20.03.2026
    """
    print(banner)


def show_dashboard(s):
    print(f"{Fore.WHITE}{'=' * 50}")
    print(f"1) Target URL:   {Fore.CYAN}{s['url']}")
    print(f"2) CSS Selector: {Fore.CYAN}{s['tag']}")
    print(f"3) ID Range:     {Fore.CYAN}{s['range'][0]} to {s['range'][1]}")
    print(f"4) Semaphore:    {Fore.CYAN}{s['semaphore']} concurrent tasks")
    print(f"5) Format:       {Fore.CYAN}{s['format']}")
    print(f"{Fore.WHITE}{'=' * 50}")
    print(f"{Fore.GREEN}G) START AUDIT   {Fore.RED}Q) EXIT")


async def app():
    settings = {
        "url": "http://127.0.0.1:5000/story.php?person=",
        "tag": "span[style*='margin-left:2px']",
        "range": [1, 50],
        "semaphore": 10,
        "format": ".txt"
    }

    print_banner()
    while True:
        show_dashboard(settings)
        option = input(f"\n{Fore.YELLOW}Option > ").lower().strip()

        if option == '1':
            print(f"\n1. Local (127.0.0.1)\n2. Custom Target")
            choice = input("Select: ")
            if choice == '1':
                settings["url"] = "http://127.0.0.1:5000/story.php?person="
            else:
                target = input("Enter target URL: ").strip()
                if target.startswith("http"): settings["url"] = target

        elif option == '2':
            settings["tag"] = input("Enter CSS Selector (for example: .user-name): ")

        elif option == '3':
            try:
                start = int(input("Start ID: "))
                end = int(input("End ID: "))
                settings["range"] = [start, end]
            except ValueError:
                print(f"{Fore.RED}[!] Numbers only!")

        elif option == '4':
            try:
                settings["semaphore"] = int(input("Max concurrent tasks: "))
            except ValueError:
                pass

        elif option == 'g':
            print(f"\n{Fore.MAGENTA}[*] Audit in progress...")
            results = await scanner.run_audit(settings)

            if results:
                path = utils.save_results(results, settings["url"],
                                         settings["range"][0], settings["range"][1],
                                         settings["format"])
                print(f"{Fore.CYAN}[!] Audit complete. Saved to: {path}")
            else:
                print(f"{Fore.RED}[!] No data leaked.")
            input(f"\n{Fore.WHITE}Press Enter to return...")

        elif option == 'q':
            break


if __name__ == "__main__":
    asyncio.run(app())
