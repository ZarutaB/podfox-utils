#!/usr/bin/env python3
# Simple utility to convert podfox feed.json file to an XSPF playlist.
# Author: @ZarutaB

import os,sys,argparse,json,time,dicttoxml
from urllib.parse import urlparse
from xml.dom.minidom import parseString

def track_item_func(parent):
  return 'track'

def create_xspf(feeds_file, prefix='./', mp3_only=False):
  track_list = list()
  with open(feeds_file) as f:
    data = json.load(f)

  track_num=1
  for episode in data['episodes']:
    track_title = episode['title']
    track_info = 'Published: ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(episode['published']))
    track_location = prefix + os.path.basename(urlparse(episode['url']).path)
    if not mp3_only or os.path.splitext(urlparse(episode['url']).path)[1][1:].strip().lower() == 'mp3':
        track_list.append(dict(title=track_title, trackNum=track_num, location=track_location, info=track_info))
        track_num = track_num + 1

  print(parseString('<?xml version="1.0" encoding="UTF-8"?><playlist version="1" xmlns="http://xspf.org/ns/0/"><trackList>'\
       + dicttoxml.dicttoxml(track_list, attr_type=False, root=False, item_func=track_item_func).decode(encoding='utf-8', errors='strict')\
       + '</trackList></playlist>').toprettyxml())

def main():
  parser = argparse.ArgumentParser(description='Convert podfox feed.json to an XSPF playlist')
  parser.add_argument('-p', '--prefix',  default='./', help='file path prefix for playlist files, default is ./')
  parser.add_argument('-m', '--mp3',  default=False, help='mp3 files only', action="store_true")
  parser.add_argument('file',  help='feed.json file path to parse')
  args = parser.parse_args()
  create_xspf(args.file, args.prefix, args.mp3)

if __name__ == '__main__':
  main()
