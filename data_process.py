import os
import yt_dlp
from colorama import Fore, Style
from models import Input_data
from pydantic import ValidationError
from tabulate import tabulate
import textwrap
from data_handle import urls

download_folder = os.path.join(os.path.expanduser('~'), 'Downloads', 'video_downloads')

class Data_process:
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
                    if self.downloader(url, 'bestvideo[ext=mp4]') == 'success':
                        break
                    else:
                        continue
            else:
                try:
                    validated_data = Input_data(urls=id.strip())
                    url = str(validated_data.urls)
                    if self.downloader(url, 'bestvideo[ext=mp4]') == 'success':
                        break
                    else:
                        print(f"{Fore.RED + 'ERROR'}: {Style.RESET_ALL + 'Failed to download video'}")
                except ValidationError as exc:
                    print(f"{Fore.RED + 'ERROR'}: {Style.RESET_ALL + exc.errors()[0].get('msg')}")
                    continue