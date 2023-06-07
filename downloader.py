import numpy as np
import os
import psutil

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
        for playlist in playlists_of_interest.reverse():
            self.download_playlist(playlist)

    def download_playlist(self, playlist):
        # Create and move to Playlist folder if not already exists
        parent_dir = "E:"
        title = playlist.title
        playlist_dir = self._get_new_playlist_dir(parent_dir, title)
        cwd = os.getcwd()
        if not playlist_dir == cwd:
            return

        print(cwd)

        # Get necessary metadata
        high_res_streams = [video.streams.get_highest_resolution()
                            for video in playlist.videos]

        playlist_size = np.sum(
            [stream.filesize for stream in high_res_streams])
        remaining_drive_space = self._get_remaining_drive_space(parent_dir)
        print("Playlist Size: " + playlist_size)
        print("Remaining Space: " + remaining_drive_space)

        # Download all videos if sufficient space exists on the drive
        if playlist_size <= remaining_drive_space:
            print(f"Downloading: {title}")
            for stream in high_res_streams:
                try:
                    stream.download(playlist_dir)
                except:
                    print("An error occurred")

            print("Download successful")
        else:
            print("Insufficient space on drive")

    def _get_all_playlists(self, url):
        webdriver = WebDriver()
        webpage = webdriver.get_webpage(url)
        raw_playlists = webdriver.get_all_matching_elements(
            webpage, "ytd-grid-playlist-renderer.ytd-grid-renderer")

        playlists = list(map(lambda playlist: Playlist(webdriver.get_element_attribute(
            playlist, "#video-title", "href")), raw_playlists))

        return playlists

    def _get_new_playlist_dir(self, parent_dir, title):
        # Create new playlist directory if not already present
        path = os.path.join(parent_dir, "/", self._format_title(title))
        if not os.path.exists(path):
            os.makedirs(name=path)
            os.chdir(path)
        return path

    def _format_title(self, str):
        return str.replace("/", " & ").replace(":", " -")

    def _get_remaining_drive_space(self, drive_path):
        return psutil.disk_usage(drive_path).free


downloader = Downloader()
downloader.download_playlists()
