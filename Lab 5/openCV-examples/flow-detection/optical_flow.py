import numpy as np
import cv2
import argparse
import signal
import sys


parser = argparse.ArgumentParser(description='This sample demonstrates Lucas-Kanade Optical Flow calculation. \
                                              The example file can be downloaded from: \
                                              https://www.bogotobogo.com/python/OpenCV_Python/images/mean_shift_tracking/slow_traffic_small.mp4')
parser.add_argument('image', type=str, help='path to image file')
parser.add_argument('window', type=str, help='Should either be "window" or "noWindow"')
args = parser.parse_args()
print(args)

if not args.window=="window" and not args.window=="noWindow":
   print('The second argument should should either be "window" or "noWindow"')
   print('Defaulting to window')
   args.window="window"
elif args.window=="noWindow":
   print("Ok noWindow was set, so I will not render any windows. To stop the the program press CTRL+C.")

print("Opening video",args.image)

def closeEverything():
    cv2.imwrite('flow.png',img)
    cap.release()



def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    closeEverything();
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)



path = None
try:
    path = int(args.image)
    print("You gave just a number. Trying to find the matching webcam.")
except ValueError:
    path = args.image

cap = cv2.VideoCapture(path)

# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors
color = np.random.randint(0,255,(100,3))

# Take first frame and find corners in it
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)

while(1):
    ret,frame = cap.read()
    if not ret:
        break
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # Select good points
    good_new = p1[st==1]
    good_old = p0[st==1]

    # draw the tracks
    for i,(new,old) in enumerate(zip(good_new, good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
        frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
    img = cv2.add(frame,mask)

    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1,1,2)
    if args.window=='window':
        cv2.imshow('optical flow (press q to quit.)',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

closeEverything()
print("Finished analysing video flow. Check out flow.png")

