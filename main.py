import yt_dlp
from tabulate import tabulate
from colorama import Fore, Back, Style
import os
from pydantic import BaseModel, AnyUrl, ValidationError
import textwrap

'''
channel
availabilty
original_url
fulltitle
duration_string
'''
urls = []
download_folder = os.path.join(os.path.expanduser('~'), 'Downloads', 'video_downloads')

class Input_data(BaseModel):
    urls: AnyUrl | None = None

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
class Data_process:
    def __init__(self):
        pass 
    
    def get_info(self, url: str):
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    def get_url_info(self):
        print("Enter a video id in list or a url directly")
        print("To cancel operation, use command 'cancel'")
        info = None
        thr = True
        while thr:
            id = input("get_url_info-> ")
            if id.strip() == '':
                print(f"{Fore.RED + 'ERROR'}: {Style.RESET_ALL + 'URL cannot be empty'}")
                continue
            elif id.strip() == 'cancel':
                print(f"{Fore.GREEN + 'SUCCESS'}: {Style.RESET_ALL + 'Operation cancelled'}")
                break
            elif id.strip().isdigit():
                if len(urls) < 1:
                    print(f"{Fore.RED + 'ERROR'}: {Style.RESET_ALL + 'No videos in the list'}")
                elif int(id) < 1 or int(id) > len(urls):
                    print(f"{Fore.RED + 'ERROR'}: {Style.RESET_ALL + 'Invalid index'}")
                else:
                    info = self.get_info(urls[int(id)-1])
            else:
                try:
                    validated_data = Input_data(urls=id.strip())
                    info = self.get_info(str(validated_data.urls))
                except ValidationError as exc:
                    print(f"{Fore.RED + 'ERROR'}: {Style.RESET_ALL + exc.errors()[0].get('msg')}")
                    continue
            if info:
                data = {
                    'original_url': info.get('original_url', 'N/A'), 
                    'title': info.get('title', 'N/A'), 
                    'duration_string': info.get('duration_string', 'N/A'),
                    'description': info.get('description', 'N/A'),
                    'view_count': info.get('view_count', 'N/A'),
                    'categories': info.get('categories', 'N/A'),
                    'thumbnail': info.get('thumbnail', 'N/A'),
                    'upload_date': info.get('upload_date', 'N/A'),
                    'like_count': info.get('like_count', 'N/A'),
                    'dislike_count': info.get('dislike_count', 'N/A'),
                    'comment_count': info.get('comment_count', 'N/A'),
                    'chapters': info.get('chapters'),
                    'channel': info.get('channel'),
                    'channel_url': info.get('channel_url', 'N/A'),
                    'channel_subscriber_count': info.get('channel_follower_count', 'N/A'),
                }
                wrapper = textwrap.TextWrapper(width=70)
                data_table = [
                    ['Original URL', data.get('original_url')],
                    ['Title', data.get('title')],
                    ['Duration', data.get('duration_string')],
                    ['View Count', data.get('view_count')],
                    ['Upload Date', data.get('upload_date')],
                    ['Like Count', data.get('like_count')],
                    ['Dislike Count', data.get('dislike_count')],
                    ['Comment Count', data.get('comment_count')],
                    ['Categories', ', '.join(data.get('categories', []))],
                    ['Thumbnail', data.get('thumbnail', 'N/A')],
                    ['Description', data.get('description')],
                    ['Channel', data.get('channel')],
                    ['Channel URL', data.get('channel_url')],
                    ['Subscribers', data.get('channel_subscriber_count')],
                ]
                print("\n")
                print(tabulate(data_table, headers=["Query", "Response"]))
                print("\n")
                return
            
    def downloader(self, url, format):
        ydl_opts = {
            'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
            #'format': format
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                #info_dict = self.get_info(str(url))
                # Print available formats (optional for debugging)
                #for f in info_dict['formats']:
                #    print(f"Format: {f['format']} - {f['filesize']}")
                # Proceed to download
                ydl.download(url)
                print(f"{Fore.GREEN + 'SUCCESS'}: {Style.RESET_ALL + 'Download completed'}")
                return "success"
        except yt_dlp.utils.DownloadError as e:
            print(f"{Fore.RED + 'ERROR'}: {Style.RESET_ALL + str(e)}")
            return "error"
    
    def download_video(self):
        print("Enter a video id in list or a url directly")
        print("To cancel operation, use command 'cancel'")
        thr = True
        while thr:
            id = input("download_video-> ").lower()
            if id.strip() == '':
                print(f"{Fore.RED + 'ERROR'}: {Style.RESET_ALL + 'URL cannot be empty'}")
                continue
            elif id.strip() == 'cancel':
                print(f"{Fore.GREEN + 'SUCCESS'}: {Style.RESET_ALL + 'Operation cancelled'}")
                break
            elif id.strip().isdigit():
                if len(urls) < 1:
                    print(f"{Fore.RED + 'ERROR'}: {Style.RESET_ALL + 'No videos in the list'}")
                elif int(id) < 1 or int(id) > len(urls):
                    print(f"{Fore.RED + 'ERROR'}: {Style.RESET_ALL + 'Invalid index'}")
                    continue
                else:
                    url = urls[int(id)-1]
                    if Data_process().downloader(url, 'bestvideo[ext=mp4]') == 'success':
                        break
                    else:
                        continue
            else:
                try:
                    validated_data = Input_data(urls=id.strip())
                    url = str(validated_data.urls)
                    if Data_process().downloader(url, 'bestvideo[ext=mp4]') == 'success':
                        break
                    else:
                        print(f"{Fore.RED + 'ERROR'}: {Style.RESET_ALL + 'Failed to download video'}")
                except ValidationError as exc:
                    print(f"{Fore.RED + 'ERROR'}: {Style.RESET_ALL + exc.errors()[0].get('msg')}")
                    continue

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