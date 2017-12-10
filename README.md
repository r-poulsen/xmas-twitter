# xmas-twitter
A Twitter-powered Christmas tree

Lights up the LEDs on [the PiHit Raspberry Pi XMas tree](https://thepihut.com/products/3d-xmas-tree-for-raspberry-pi) when certain Christmassy hashtags are used on Twitter.

![Demonstration](demo.gif)

It has language support, but you'll have to add your own language.  The code should be pretty straightforward.

## Install required libs
```
$ sudo apt-get install python-gpiozero python3-gpiozero python-tweepy
```
## Setup
To connect to the Twitter API, you'll need application keys that you generate on https://apps.twitter.com and add to the top of xmas-twitter.py.

## Run on boot
To run on boot, copy the xmaslights.service into /etc/systemd/system, edit the path to the binary and the commandline arguments if you don't go with the defaults and enable the service:
```
$ sudo systemctl daemon-reload
$ sudo systemctl enable xmaslights
```
## Usage
```
usage: xmas-twitter.py [-h] [--lang LANG] [--star-on-time N]
                       [--star-off-time N] [--star-twinkle N]
                       [--tree-on-time N] [--tree-off-time N]
                       [--tree-twinkle N] [--language-filter] [--debug]

A Twitter-powered Christmas tree.

optional arguments:
  -h, --help         show this help message and exit
  --lang LANG        comma-seperated list of languages (Supported: en,da)
                     Default en.
  --star-on-time N   star LED fade-in seconds. Default 0.
  --star-off-time N  star LED fade-out seconds. Default 5.
  --star-twinkle N   star LED blink (i.e. on/off cycles). Default 1.
  --tree-on-time N   tree LEDs fade-in seconds. Default 0.
  --tree-off-time N  tree LEDs fade-out seconds. Default 5.
  --tree-twinkle N   tree LEDs blink (i.e. on/off cycles). Default 1.
  --language-filter  enable Twitter language filter. Fewer hits, but maybe
                     more accurate. Default not enabled.
  --debug            enable debugging. Your terminal should probably support
                     something like UTF-8 and emojis. Default not enabled.

```
