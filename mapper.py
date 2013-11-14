import re
from collections import defaultdict


class MapperException(Exception):
  pass


class Mapper:
  def __init__(self, DNS_SEARCH_REGEX = 1):
    self.name_to_service = defaultdict(lambda: 'DEFAULT')


    if DNS_SEARCH_REGEX:
      self.mode = 'REGEX'
    else:
      self.mode='OTHER'
      MapperException("Select REGEX mode. No other mode available")

    self.loadTypeFiles()

  def loadTypeFiles(self):
    self.loadFile('servicedef/adverts.ini', 'ADVERT')
    self.loadFile('servicedef/background.ini', 'BACKGROUND')
    self.loadFile('servicedef/video.ini', 'VIDEO')
    self.loadFile('servicedef/web.ini', 'WEB')

  def loadFile(self, filename, service):
    f = open(filename, 'r')
    for line in f.readlines():
      self.name_to_service[(line.strip('\n').replace('*', '[\S]*'))] = service

  def createTypePoll(self):
    """For every new search, poll the type with the most
    matches instead of the first match"""
    self.types_poll = defaultdict(int)
    self.types_poll['DEFAULT'] = 0

  def searchType(self, dnsname):
    self.createTypePoll()
    for name, service in self.name_to_service.items():
      found = re.search(name, dnsname)
      if found is not None:
          # if match is found, increment counter of that TYPE
          self.types_poll[service]+=1
    return max(self.types_poll, key=self.types_poll.get)

  def searchTypeByStringMatching(self, dnsname):
    self.createTypePoll()
    for name, service in self.name_to_service.items():
      if name in dnsname:
        self.types_poll[service] += 1
        continue
    return max(self.types_poll, key=self.types_poll.get)
