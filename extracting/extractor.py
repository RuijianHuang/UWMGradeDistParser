import abc
from utils import tabula
import requests
from bs4 import BeautifulSoup, SoupStrainer
import os
import urllib

DATA_PATH = '../data'

class Extractor(object):
  __metaclass__ = abc.ABCMeta

  def __init__(self, source_url):
    self.source_url = source_url

  @abc.abstractmethod
  def get_columns(self, context):
    pass

  @abc.abstractmethod
  def is_data_set(self, url):
    pass

  @abc.abstractmethod
  def download_name(self, url):
    pass

  @abc.abstractmethod
  def extract_data(self, context, contents):
    pass

  def execute(self):
    results = []

    urls = self.get_download_urls()
    print('Found %d urls...' % len(urls))

    for url in urls:
      print('Downloading: %s' % url)
      file_path = self.download_file(url)
      print('Downloaded to: %s' % file_path)
      context = {
        "url": url,
        "file_path": file_path
      }

      print('Converting: %s' % file_path)
      contents = tabula.execute(file_path, self.get_columns(context))
      data = self.extract_data(context, contents)
      results += data

    return results

  def get_download_urls(self):
    page = requests.get(self.source_url)
    links = BeautifulSoup(page.text, 'html.parser', parse_only=SoupStrainer('a'))

    urls = []

    # iterate all links on the page
    for link in links:
      if not link.has_attr('href'):
        continue

      url = link['href']

      if self.is_data_set(url):
        urls.append(url)

    return urls

  def download_file(self, url):
    if not os.path.isdir(DATA_PATH):
      os.makedirs(DATA_PATH)
    name = self.download_name(url)
    file_path = '%s/%s' % (DATA_PATH, name)
    urllib.request.urlretrieve(url, file_path)
    return file_path
