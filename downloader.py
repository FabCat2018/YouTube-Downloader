from pytube import Channel, Playlist, YouTube

from webdriver import WebDriver


class Downloader:

    def download_playlists(self):
        playlists_page = "https://www.youtube.com/@chugga/playlists"

        # Scrape the page for all playlist URLS, then filter for relevance
        all_playlists = self._get_all_playlists(playlists_page)
        playlists_of_interest = all_playlists

        # Run download for all videos in each playlist, placing into folders with same name

        # Early stop if memory would be exceeded

    def _get_all_playlists(self, url):
        webdriver = WebDriver()
        webpage = webdriver.get_webpage(url)
        playlists = webdriver.get_all_matching_elements(
            webpage, "ytd-grid-playlist-renderer.ytd-grid-renderer")
        print(playlists)

    def _get_stream(self, link):
        youtube_object = YouTube(link)
        youtube_object = youtube_object.streams.get_highest_resolution()

        try:
            youtube_object.download("E:\\")
        except:
            print("An error occurred")
        print("Download successful")


downloader = Downloader()
downloader.download_playlists()
