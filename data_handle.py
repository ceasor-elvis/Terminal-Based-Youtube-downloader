from models import Input_data
from colorama import Fore, Style
from pydantic import ValidationError

urls = []

class Data_handle:
    def __init__(self):
        pass

    def add_url(self):
        print("Enter the URL of the video (or use command 'done' to finish, 'cancel' to cancel the operation.): ")
        outer = True
        while outer:
            input_url = input("add_url-> ")
            if input_url.strip() == 'done':
                if len(urls) > 0:
                    print(f"{Fore.GREEN + 'SUCCESS'}: {Style.RESET_ALL + 'Finished adding urls'}")
                    break
                else:
                    print("No videos entered.")
                    pass
            elif input_url.strip() == 'cancel':
                if len(urls) > 0:
                    print("The urls list contains elements")
                    print("Are you sure you want to cancel [Y/N]")
                    while True:
                        conf = input("confirm cancellation>")
                        if conf.lower().strip() == 'y':
                            urls.clear()
                            print(f"{Fore.GREEN + 'SUCCESS'}: {Style.RESET_ALL + 'Cancelled the operation'}")
                            outer = False
                            break
                        elif conf.lower().strip() == 'n':
                            print("Operation continued.")
                            break
                        else:
                            print("Invalid confirmation")
                            print("Please use either [Y/N]")
                else:
                    print("Operation cancelled.")
                    break
            elif input_url.strip() == '':
                print("No video entered.")
                continue
            else:
                if input_url in urls:
                    print(f"{Fore.YELLOW + 'WARNING'}: {Style.RESET_ALL + f'Video {input_url} already exists in the list'}")
                    print("If done adding urls, leave the space blank and press enter to quit.")
                else:
                    try:
                        validated_data = Input_data(urls=input_url)
                        urls.append(validated_data.urls)
                        print(f"{Fore.GREEN + 'SUCCESS'}: {Style.RESET_ALL + f'Added {input_url} to the list'}")
                    except ValidationError as exc:
                        print(f"{Fore.RED + 'ERROR'}: {Style.RESET_ALL + exc.errors()[0].get('msg')}")
                        continue

    def update_urls(self):
        if len(urls)< 1:
            print(f"{Fore.RED + 'ERROR'}: {Style.RESET_ALL + 'No videos in the list'}")
            return
        thr = True
        while thr:
            id = input("Enter valid video id to update-> ")
            if id.strip().isdigit():
                if id < 1 or id > len(urls):
                    print(f"{Fore.RED + 'ERROR'}: {Style.RESET_ALL + 'Invalid index'}")
                else:
                    for index, url in enumerate(urls, 1):
                        if index == id:
                            cont = True
                            while cont:
                                print("Enter new valid url: ")
                                new_url = input("update url-> ")
                                if new_url.strip() == '':
                                    print(f"{Fore.RED + 'ERROR'}: {Style.RESET_ALL + 'URL cannot be empty'}")
                                else:  
                                    try: 
                                        validated_data = Input_data(urls=new_url)
                                        urls[index-1] = validated_data.urls
                                        print(f"{Fore.GREEN + 'SUCCESS'}: {Style.RESET_ALL + f'Updated URL for index {id}'}")
                                        cont = False
                                        thr = False
                                    except ValidationError as exc:
                                        print(f"{Fore.RED + 'ERROR'}: {Style.RESET_ALL + exc.errors()[0].get('msg')}")
            else:
                if id.strip() == 'cancel':
                    break
                else:
                    print(f"{Fore.RED + 'ERROR'}: {Style.RESET_ALL + 'Invalid id, integer needed'}")
    def delete(self):
        if len(urls) < 1:
            print(f"{Fore.RED + 'ERROR'}: {Style.RESET_ALL + 'No videos in the list'}")
            return
        while True:
            id = input("Enter valid video id to delete-> ")
            if id.strip().isdigit():
                if id < 1 or id > len(urls):
                    print(f"{Fore.RED + 'ERROR'}: {Style.RESET_ALL + 'Invalid index'}")
                else:
                    del urls[id-1]
                    print(f"{Fore.GREEN + 'SUCCESS'}: {Style.RESET_ALL + f'Deleted URL for index {id}'}")
                    break
            else:
                if id.strip() == 'cancel':
                    break
                else:
                    print(f"{Fore.RED + 'ERROR'}: {Style.RESET_ALL + 'Invalid id, integer needed'}")
                    continue