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
    {Fore.RED}          IDOR Auditor v3.1 | Improved tool: interface - fix bugs 
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
    print(f"{Fore.GREEN}0) START AUDIT   {Fore.RED}99) EXIT")


async def app():
    settings = {
        "url": "http://127.0.0.1:5000/story.php?person=",
        "tag": "span[style*='margin-left:2px']",
        "range": [1, 50],
        "semaphore": 10,
        "format": ".txt"
    }

    often_used_tags = {
        "1": ("span[style*='margin-left:2px']", "For this Lab (Default)"),
        "2": ("h1", "Main Heading"),
        "3": (".user-profile", "Common Profile Class"),
        "4": ("#username", "Specific ID Selector")
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

        if option == '2':
            print("\n--- Select Target Pattern ---")

            for key, (selector, desc) in often_used_tags.items():
                print(f"{key}) {desc} -> {Fore.CYAN}{selector}")
            sub_choice = input("\nChoose preset (or type manual): ").strip()
            if sub_choice in often_used_tags:
                settings["tag"] = often_used_tags[sub_choice][0]
            else:
                settings["tag"] = sub_choice

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

        elif option == '0':
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

        elif option == '99':
            print("Bye, thanks for downloading :)")
            break


if __name__ == "__main__":
    asyncio.run(app())
