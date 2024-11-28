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