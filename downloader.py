from pytube import YouTube

class Downloader:
    def download(self, link):
        youtubeObject = YouTube(link)
        youtubeObject = youtubeObject.streams.get_highest_resolution()

        try:
            youtubeObject.download("E:\\")
        except:
            print("An error occurred")
        print("Download successful")

downloader = Downloader()
downloader.download("https://www.youtube.com/watch?v=6Bmbr0YTMs4&list=PLFa30Ckjce0xTqGN51NJ_PBJynXfRKL1T&index=5")