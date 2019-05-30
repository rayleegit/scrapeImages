# scrapeImages
Python module that scrapes Google Image Search images and stores them to specified local directory

# Requirements: 
## Python 3.7
### w/ the following packages:
#### bs4, requests, re, urllib, os, argparse, sys, json

# Instructions
To run this module, download 'scrapeImages.py' to your local drive, open up command line, then enter:

  python scrapeImages.py --search [SEARCH TERM] --num_images [# OF IMAGES TO DOWNLOAD] --directory [YOUR DIRECTORY NAME] --prediction ['1' if you'd like VGG predictions to be included in filename, otherwise '0']
