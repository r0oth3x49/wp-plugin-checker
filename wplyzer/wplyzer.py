import requests
from bs4 import BeautifulSoup
import sys

class WPlyzer:
    
    def __init__(self, url):

        self.http_headers = {'User-agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/47.0 (Chrome)'}

        self.url = url
        self._plugin_dict = {}
        self._plugin_name = None
        self._plugin_version = None
        self._plugin_full_link = None
        self._plugin_split_link = None
        self._plugin_identifier = '/wp-content/plugins/'
        self._theme_dict = {}
        self._theme_name = None
        self._theme_version = None
        self._theme_full_link = None
        self._theme_split_link = None
        self._theme_identifier = '/wp-content/themes/'

    def Request(self):
        try:
            req = requests.get(self.url, headers=self.http_headers)
        except requests.exceptions.MissingSchema:
            sys.exit(0)
            pass
        except requests.exceptions.ConnectionError as e:
            raise e
        else:
            resp = req.text
            return resp

    def _parse_plugins(self, resp):
        soup = BeautifulSoup(resp, 'html.parser')
        linktags = soup.find_all('link')
        for link in linktags:
            self._plugin_full_link = link.get('href')
            if self._plugin_full_link is not None:
                if self._plugin_identifier in self._plugin_full_link:
                    self._plugin_split_link = self._plugin_full_link.split('?')[0] if '?' in self._plugin_full_link else self._plugin_full_link
                    self._plugin_name = self._plugin_split_link.split('/')[5]
                    self._plugin_version = (self._plugin_full_link.split('?')[1]).replace('ver=','') if '?' in self._plugin_full_link else 'Unknown'
                    self._plugin_dict[self._plugin_name] = self._plugin_version
                
        return self._plugin_dict

    def _parse_themes(self, resp):
        soup = BeautifulSoup(resp, 'html.parser')
        linktags = soup.find_all('link')
        for link in linktags:
            self._theme_full_link = link.get('href')
            if self._theme_full_link is not None:
                if self._theme_identifier in self._theme_full_link:
                    self._theme_split_link = self._theme_full_link.split('?')[0] if '?' in self._theme_full_link else self._theme_full_link
                    self._theme_name = self._theme_split_link.split('/')[5]
                    self._theme_version = (self._theme_full_link.split('?')[1]).replace('ver=','') if '?' in self._theme_full_link else 'Unknown'
                    self._theme_dict[self._theme_name] = self._theme_version
                
        return self._theme_dict


