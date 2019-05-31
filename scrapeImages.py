# note: code inspired by https://stackoverflow.com/questions/20716842/python-download-images-from-google-image-search and note: code inspired by https://stackoverflow.com/questions/20716842/python-download-images-from-google-image-search and https://www.learnopencv.com/keras-tutorial-using-pre-trained-imagenet-models/

# import packages
from bs4 import BeautifulSoup
import requests
import re
import urllib.request
from urllib.request import urlopen
from urllib.request import Request
import os
import argparse
import sys
import json


# define BeautifulSoup html parser
def get_soup(url,header):
    req = urllib.request.Request(url, headers=header)
    response = urllib.request.urlopen(req)
    return BeautifulSoup(response,'html.parser')

def main(args):

    parser = argparse.ArgumentParser(description='Scrape Google images')
    parser.add_argument('-s', '--search', default='bananas', type=str, help='search term')
    parser.add_argument('-n', '--num_images', default=10, type=int, help='num images to save')
    parser.add_argument('-d', '--directory', default=os.getcwd(), type=str, help='save directory')
    parser.add_argument('-p', '--prediction', default=1, type=int, help="indicate '1' if you'd like to add VGG prediction to image filename")

    # parse arguments and define variables for them
    args = parser.parse_args()
    query = args.search
    max_images = args.num_images
    save_directory = os.path.join(args.directory, query)
    ## create new save directory if it does not exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    prediction_indicator = args.prediction

    # format query so that it fits into the google search URL we'll connect to
    query= query.split()
    query='+'.join(query)
    url="https://www.google.com/search?tbm=isch&q="+query

    # create this header to "trick" websites into thinking request is coming from browser instead of script
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

    # call BeautifulSoup HTML parser
    soup = get_soup(url,header)

    # initiate pre-trained VGG model
    if prediction_indicator == 1:
        # load VGG model packages
        from keras.preprocessing.image import load_img
        from keras.preprocessing.image import img_to_array
        from keras.applications.imagenet_utils import decode_predictions
        from keras.applications import vgg16
        import numpy as np
        from PIL import Image
        from io import BytesIO
        # initiate model with imagenet weights
        # note: weights are a ~500MB file so it may take a few minutes to download
        vgg_model = vgg16.VGG16(weights='imagenet')

    # initiate list to store image links and image type info
    ActualImages=[]

    # get image link and filetype by taking the 'ou' and 'ity' values from each "rg_meta..." div class line
    for a in soup.find_all("div",{"class":"rg_meta"}):
        link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
        ActualImages.append((link,Type))

    # for each link, get image data and save to file in respective directory
    for i , (img , Type) in enumerate( ActualImages[0:max_images]):
        try:
            # get image data
            req = requests.get(img, headers=header)
            raw_img = req.content

            # if prediction_indicator is 1, VGG prediction will be added to filename
            if prediction_indicator == 1:
                # convert image to numpy format
                numpy_image = img_to_array(Image.open(BytesIO(raw_img)).resize((224, 224)))
                # convert image to batch format
                image_batch = np.expand_dims(numpy_image, axis=0)
                # prepare image for model
                processed_image = vgg16.preprocess_input(image_batch.copy())
                # classify image. output is predicted probabilities
                predictions = vgg_model.predict(processed_image)
                # convert highest probability prediction to class label
                label = decode_predictions(predictions, top=1)
                # define variable for class label to be used in filename
                label = list(label[0][0])[1]

                # save file
                if len(Type)==0:
                    f = open(os.path.join(save_directory , "img" + "_"+ str(i)+ "_"+label+".jpg"), 'wb')
                else:
                    f = open(os.path.join(save_directory , "img" + "_"+ str(i)+ "_"+label+"."+ Type), 'wb')
            else:
                    if len(Type)==0:
                        f = open(os.path.join(save_directory , "img" + "_"+ str(i)+".jpg"), 'wb')
                    else:
                        f = open(os.path.join(save_directory , "img" + "_"+ str(i)+"."+Type), 'wb')
            f.write(raw_img)
            f.close()

        except Exception as e:
            print("could not load : ", img)
            print(e)

# run this code as the main program
if __name__ == '__main__':
    from sys import argv
    try:
        main(argv)
    except KeyboardInterrupt:
        pass
    sys.exit()
