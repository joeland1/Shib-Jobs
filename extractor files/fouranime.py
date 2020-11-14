from __future__ import unicode_literals

from .common import InfoExtractor
import re

class FourAnimeIE(InfoExtractor):
    _VALID_URL = r'(?:https?://)?(?:www\.)?4anime\.to/(?P<title>.+)-episode-(?P<episode>\d+)\?id=(?P<id>\d+)'

    def _real_extract(self, url):
        name, episode, id = re.match(self._VALID_URL, url).groups()

        webpage = self._download_webpage(url,name+"-episode-"+episode)
        #print(webpage)
        video_url = self._html_search_regex(r'<source src="(.+)" type=\'video/mp4\'', webpage, u'video URL')

        print(video_url)

        return {
            'title': name+"-episode-"+episode,
            'id': '123',
            'url': video_url
        }

class FourAnimePlaylistIE(InfoExtractor):
    _VALID_URL= r'(?:https?://)?(?:www\.)?4anime\.to/anime/(?P<anime_name>.+)'

    def _real_extract(self, url):
        name, = re.match(self._VALID_URL, url).groups()
        webpage = self._download_webpage(url, name+" playlist")
        #video_url = re.search(r'<li><a href="(?https://4anime.to/.*-episode-\d+\/\?id=\d+)".*>\d+</a></li>', webpage).group()
        video_urls = re.findall(r'<li><a href=\"(.*?)\" title=\"\">\d+</a></li>',webpage)
        #video_url = self._html_search_regex(r'<li><a href=\"(.*?)\" title=\"\">\d+</a></li>', webpage, u'PLaylist urls')
        print(video_urls)
        return_arr=[]
        for video in video_urls:
            print(video)
            name, episode, id = re.match(r'(?:https:\/\/)?(?:www\.)?4anime\.to\/(?P<title>.+?)-episode-(?P<episode>\d+?)\/\?id=(?P<id>\d+)', video).groups()
            print(name)
            webpage = self._download_webpage(video, "ep="+str(ctr+1))
            video_url = self._html_search_regex(r'<source src="(.+)" type=\'video/mp4\'', webpage, u'video URL')
            return_arr.append({
                'title': name+"-episode-"+episode,
                'id': '',
                'url': video_url
            })
        return return_arr
