# How to load a Tensorflow model using OpenCV
# Jean Vitor de Paulo Blog - https://jeanvitor.com/tensorflow-object-detecion-opencv/
# David edited some stuff

import numpy as np
import cv2
import sys
import requests
import time
import boto3
from botocore.exceptions import NoCredentialsError



def upload_to_aws(local_file, bucket, s3_file):

    ACCESS_KEY = 'AKIATSIVDXPQKGK4542J'
    SECRET_KEY = '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'
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        return True
    except FileNotFoundError:
        return False
    except NoCredentialsError:
        return False


def detect_labels(photo, bucket):

    client=boto3.client('rekognition')

    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
        MaxLabels=10)

    output=''
    for label in response['Labels']:

      if label['Confidence'] > 80:
        output=output+label['Name']+" | "
    print("Detected:"+output, end='\r')
    return True


# Load a model imported from Tensorflow
tensorflowNet = cv2.dnn.readNetFromTensorflow('frozen_inference_graph.pb', 'ssd_mobilenet_v2_coco_2018_03_29.pbtxt')

img = None
webCam = False
if(len(sys.argv)>1 and not sys.argv[-1]== "noWindow"):
   try:
      print("I'll try to read your image");
      img = cv2.imread(sys.argv[1])
      if img is None:
         print("Failed to load image file:", sys.argv[1])
   except:
      print("Failed to load the image are you sure that:", sys.argv[1],"is a path to an image?")
else:
   try:
      print("Trying to open the Webcam.")
      cap = cv2.VideoCapture(0)
      if cap is None or not cap.isOpened():
         raise("No camera")
      webCam = True
   except:
      img = cv2.imread("../data/test.jpg")
      print("Using default image.")


while(True):
    if webCam:
        ret, img = cap.read()

    rows, cols, channels = img.shape

    # Use the given image as input, which needs to be blob(s).
    tensorflowNet.setInput(cv2.dnn.blobFromImage(img, size=(300, 300), swapRB=True, crop=False))

    # Runs a forward pass to compute the net output
    networkOutput = tensorflowNet.forward()

    if webCam:
        if sys.argv[-1] == "noWindow":
          api1 = False
          api2 = False
          cv2.imwrite('detected.jpg',img)
          api1 = upload_to_aws('detected.jpg', 'cornelltech', 'detected.jpg')
          while(not api1):
            time.sleep(1)
          photo='detected.jpg'
          bucket='cornelltech'
          api2=detect_labels(photo, bucket)
          while(not api2):
            time.sleep(1)
          continue
        cv2.imshow('detected (press q to quit)',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break
    else:
        break

cv2.imwrite('detected_out.jpg',img)
cv2.destroyAllWindows()


