import os
from colorama import Fore, Style
from tabulate import tabulate
from data_handle import Data_handle, urls
from data_process import Data_process, download_folder

def start():
    print(f"{Fore.CYAN}Welcome to the YouTube URL Manager!{Style.RESET_ALL}")
    print("Use 'help' to see available commands.")
    while True:
        command = (input(">")).lower().strip()
        if command == 'help':
            data = [
                ['help', 'Display this help message'],
                ['exit/quit', 'Terminate the program'],
                ['add', 'Add a new video URL to the list'],
                ['update', 'Update an existing video URL in the list'],
                ['del', 'Delete a url from the list'],
                ['list', 'List all the video URLs in the list'],
                ['st-dir', 'Change download folder'],
                ['get-info', 'Get detailed information about a video'],
                ['-d', 'Download one video from the list or use a url']
            ]
            print("\n")
            print("Available commands:")
            print(tabulate(data, headers=["Command", "Description"]))
            print("\n")
        elif command == 'exit' or command == 'quit':
            print(f"{Fore.GREEN + 'Exiting the program...'}")
            break
        elif command == 'add':
            Data_handle().add_url()
        elif command == 'update':
            Data_handle().update_urls()
        elif command == 'del':
            Data_handle().delete()
        elif command == 'list':
            if len(urls) < 1:
                print("No video urls provided!\nPlease add some videos by using the 'add' command.")
            else:
                rows = []
                for index, url in enumerate(urls, 1):
                    info = Data_process().get_info(str(url))
                    title = info.get('title', 'N/A')

                    rows.append([index, title])
                print(tabulate(rows, headers=['Index', 'URL'], tablefmt='grid'))
        elif command == 'st-dir':
            global download_folder
            print(f"Current download folder: {download_folder}")
            new_folder = input("Enter new download folder path (leave blank to keep the same): ")
            if new_folder != '':
                download_folder = new_folder
                print(f"Changed download folder to: {download_folder}")
            else:
                print("No changes made to download folder.")
        elif command == 'get-info':
            Data_process().get_url_info()
        elif command == '-d':
            Data_process().download_video()
        else:
            print(f"{Fore.RED + 'ERROR'}: {Style.RESET_ALL + 'Invalid command'} {Fore.YELLOW + command}{Style.RESET_ALL}")

if __name__ == '__main__':
    os.makedirs(download_folder, exist_ok=True)
    start()