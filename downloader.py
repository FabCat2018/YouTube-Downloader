import os
from itertools import accumulate

from pytube import Playlist, YouTube

from webdriver import WebDriver


class Downloader:

    def download_playlists(self):
        playlists_page = "https://www.youtube.com/@chugga/playlists"

        # Scrape the page for all playlist URLS
        all_playlists = self._get_all_playlists(playlists_page)

        # Filter playlists by keyword
        keyword = "Let's Play"
        playlists_of_interest = list(filter(
            lambda playlist: keyword in playlist.title, all_playlists))

        # Download each playlist of interest into folders with the same name
        # for playlist in playlists_of_interest:
        self.download_playlist(playlists_of_interest[4])

    def download_playlist(self, playlist):
        # Create and move to Playlist folder
        parent_dir = "E:"
        title = playlist.title
        self._move_to_playlist_dir(parent_dir, title)
        print(os.getcwd())

        # Get necessary metadata
        high_res_streams = [video.streams.get_highest_resolution()
                            for video in playlist.videos]

        playlist_size = accumulate(
            [stream.filesize for stream in high_res_streams])
        remaining_drive_space = self._get_remaining_drive_space(parent_dir)
        print(playlist_size)
        print(remaining_drive_space)

        # Download all videos if sufficient space exists on the drive
        # if playlist_size <= remaining_drive_space:
        #     print(f"Downloading: {title}")
            # for stream in high_res_streams:
            #     try:
            #         stream.download(path)
            #     except:
            #         print("An error occurred")

        #     print("Download successful")
        # else:
        #     print("Insufficient space on drive")

    def _get_all_playlists(self, url):
        webdriver = WebDriver()
        webpage = webdriver.get_webpage(url)
        raw_playlists = webdriver.get_all_matching_elements(
            webpage, "ytd-grid-playlist-renderer.ytd-grid-renderer")

        playlists = list(map(lambda playlist: Playlist(webdriver.get_element_attribute(
            playlist, "#video-title", "href")), raw_playlists))

        return playlists

    def _move_to_playlist_dir(self, parent_dir, title):
        path = os.path.join(parent_dir, "/", self._format_title(title))
        os.makedirs(path=path, exist_ok=True)
        os.chdir(path)
        return path

    def _format_title(self, str):
        return str.replace("/", " & ").replace(":", " -")

    def _get_remaining_drive_space(self, drive_path):
        statvfs = os.statvfs(drive_path)
        return statvfs.f_frsize * statvfs.f_bfree


downloader = Downloader()
downloader.download_playlists()
