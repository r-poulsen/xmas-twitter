#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from gpiozero import LEDBoard
from random import choice
from json import JSONDecoder
from time import sleep
import argparse

# Add your own key, token and associated secrets here:
consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""

# The GPIO for the tree LEDs and the star LED.  For some reason 3 seems to do nothing.
tree = LEDBoard(*range(4,28),pwm=True)
star = LEDBoard(2,pwm=True)

# Add more languages if you like.
words = {}
words['en'] = {}
words['en']['star'] = ['MerryXmas', 'MerryChristmas' ]
words['en']['tree'] = ['Xmas', 'Christmas']
words['da'] = {}
words['da']['star'] = ['GodJul', u'GlædeligJul', 'GlaedeligJul' ]
words['da']['tree'] = ['Jul' ]

retry=0

class StdOutListener(StreamListener):
    def on_data(self, data):
        global retry
        retry=0
        post=JSONDecoder().decode(data)
        try:
            if ( args.debug ):
                print( post['user']['name'] + ' @' +post['user']['screen_name'] + ' ' + post['created_at'] )
                print(post['text'] + "\n")
            for tag in post['entities']['hashtags']:
                if ( tag['text'].lower() in monitor_words['star']):
                    star.blink(on_time = args.star_on_time, fade_out_time = args.star_off_time, n = args.star_twinkle )
                elif ( tag['text'].lower() in monitor_words['tree']):
                    choice(tree).blink(on_time = args.tree_on_time, fade_out_time = args.tree_off_time, n = args.tree_twinkle )
        except KeyError, e:
            # Happens sometimes.  Uncomment the print and exit statements to dig into it
            print('KeyError - reason "%s"' % str(e))
            # print(data)
            # exit(1)
        return True

    def on_error(self, status_code):
        global retry
        print(status_code)
        retry+=1
        sleep(retry)
        return True

    def on_timeout(self):
        global retry
        print('Timeout...')
        retry+=1
        sleep(retry)
        return True

parser = argparse.ArgumentParser(description='A Twitter-powered Christmas tree.')
parser.add_argument('--lang',
                    help='comma-seperated list of languages (Supported: ' + ','.join( words ) +') Default en.',
                    default='en' )
parser.add_argument('--star-on-time',
                    help='star LED fade-in seconds. Default 0.',
                    metavar='N',type=int, default=0 )
parser.add_argument('--star-off-time',
                    help='star LED fade-out seconds. Default 5.',
                    metavar='N',type=int, default=5 )
parser.add_argument('--star-twinkle',
                    help='star LED blink (i.e. on/off cycles). Default 1.',
                    metavar='N',type=int, default=1 )
parser.add_argument('--tree-on-time',
                    help='tree LEDs fade-in seconds. Default 0.',
                    metavar='N',type=int, default=0 )
parser.add_argument('--tree-off-time',
                    help='tree LEDs fade-out seconds. Default 5.',
                    metavar='N',type=int, default=5 )
parser.add_argument('--tree-twinkle',
                    help='tree LEDs blink (i.e. on/off cycles). Default 1.',
                    metavar='N',type=int, default=1 )
parser.add_argument('--language-filter',
                    default=False, action='store_true',
                    help='enable Twitter language filter. Fewer hits, but maybe more accurate. Default not enabled.' )
parser.add_argument('--debug',
                    default=False, action='store_true',
                    help='enable debugging.  Your terminal should probably support something like UTF-8 and emojis. Default not enabled.' )

args = parser.parse_args()

monitor_words = {}
monitor_tags = []

for lang in args.lang.split(','):
    for ledgroup in (['star', 'tree']):
        monitor_words[ledgroup] = {}
        if ( lang in words ):
            for word in words[lang][ledgroup]:
                monitor_words[ledgroup][word.lower()] = "1"
                monitor_tags.append('#'+word)
        else:
            print('Language '+l+' not supported!')
            exit(1)

l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)
if( args.language_filter ):
    stream.filter(track=monitor_tags, languages=args.lang.split(','))
else:
    stream.filter(track=monitor_tags)

