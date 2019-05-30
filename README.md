# scrapeImages
Python module that scrapes Google Image Search images, stores them to specified local directory, and optionally adds VGG image classification model prediction to the filename.

# Requirements: 
## Python 3.7
### w/ the following packages:
#### bs4, requests, re, urllib, os, argparse, sys, json
### (optional) packages for running VGG image classification model:
### tensorflow, keras, matplotlib, numpy

# Instructions
To run this module, download 'scrapeImages.py' to your local drive, open up command line, then enter:

  python scrapeImages.py --search [SEARCH TERM] --num_images [# OF IMAGES TO DOWNLOAD] --directory [DIRECTORY TO SAVE IMAGE FILES TO] --prediction ['1' if you'd like VGG predictions to be included in filename, otherwise '0']
  
# note: code inspired by https://stackoverflow.com/questions/20716842/python-download-images-from-google-image-search
