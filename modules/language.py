import sys, urllib2
from urllib import urlencode
from BeautifulSoup import BeautifulSoup
from pprint import pprint

class Language:
   def translate(self, args):
      """ Translate, using Google, from one lang to another """
      parse_args = args.partition(" ")
      fromlang = parse_args[0].split("|")[0]
      tolang = parse_args[0].split("|")[1]
      text = args[1]

      open = urllib2.build_opener()
      open.addheaders = [("User-agent", "Mozilla/5.0 (X11; U; FreeBSD i686; en-US; rv:1.8.1.9)  Gecko/20071025 Firefox/2.0.0.9")]

      translate = open.open("http://translate.google.com/translate_t?" + 
            urlencode({"sl": fromlang, "tl": tolang}),
            data = urlencode({"hl": "en", "ie": "UTF8", "text": text.encode("utf-8"),
               "sl": fromlang, "tl": tolang})
      )

      soup = BeautifulSoup(translate)
      return soup("span", id="result_box")
