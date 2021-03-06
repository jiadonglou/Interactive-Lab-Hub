# Observant Systems


For lab this week, we focus on creating interactive systems that can detect and respond to events or stimuli in the environment of the Pi, like the Boat Detector we mentioned in lecture. 
Your **observant device** could, for example, count items, find objects, recognize an event or continuously monitor a room.

This lab will help you think through the design of observant systems, particularly corner cases that the algorithms need to be aware of.

In Lab 5 part 1, we focus on detecting and sense-making.

In Lab 5 part 2, we'll incorporate interactive responses.


## Prep

1.  Pull the new Github Repo.
2.  Read about [OpenCV](https://opencv.org/about/).
3.  Read Belloti, et al's [Making Sense of Sensing Systems: Five Questions for Designers and Researchers](https://www.cc.gatech.edu/~keith/pubs/chi2002-sensing.pdf)

### For the lab, you will need:

1. Raspberry Pi
1. Raspberry Pi Camera (2.1)
1. Microphone (if you want speech or sound input)
1. Webcam (if you want to be able to locate the camera more flexibly than the Pi Camera)

### Deliverables for this lab are:
1. Show pictures, videos of the "sense-making" algorithms you tried.
1. Show a video of how you embed one of these algorithms into your observant system.
1. Test, characterize your interactive device. Show faults in the detection and how the system handled it.


## Overview
Building upon the paper-airplane metaphor (we're understanding the material of machine learning for design), here are the four sections of the lab activity:

A) [Play](#part-a)

B) [Fold](#part-b)

C) [Flight test](#part-c)

D) [Reflect](#part-d)

---

### Part A
### Play with different sense-making algorithms.

Befor you get started connect the RaspberryPi Camera V2. [The Pi hut has a great explanation on how to do that](https://thepihut.com/blogs/raspberry-pi-tutorials/16021420-how-to-install-use-the-raspberry-pi-camera).  

#### OpenCV
A more traditional to extract information out of images is provided with OpenCV. The RPI image provided to you comes with an optimized installation that can be accessed through python.

Additionally, we also included 4 standard OpenCV examples. These examples include contour(blob) detection, face detection with the ``Haarcascade``, flow detection(a type of keypoint tracking), and standard object detection with the [Yolo](https://pjreddie.com/darknet/yolo/) darknet.

Most examples can be run with a screen (I.e. VNC or ssh -X or with an HDMI monitor), or with just the terminal. The examples are separated out into different folders. Each folder contains a ```HowToUse.md``` file, which explains how to run the python example.

```shell
pi@ixe00:~/openCV-examples $ tree -l
.
├── contours-detection
│   ├── contours.py
│   └── HowToUse.md
├── data
│   ├── slow_traffic_small.mp4
│   └── test.jpg
├── face-detection
│   ├── face-detection.py
│   ├── faces_detected.jpg
│   ├── haarcascade_eye_tree_eyeglasses.xml
│   ├── haarcascade_eye.xml
│   ├── haarcascade_frontalface_alt.xml
│   ├── haarcascade_frontalface_default.xml
│   └── HowToUse.md
├── flow-detection
│   ├── flow.png
│   ├── HowToUse.md
│   └── optical_flow.py
└── object-detection
    ├── detected_out.jpg
    ├── detect.py
    ├── frozen_inference_graph.pb
    ├── HowToUse.md
    └── ssd_mobilenet_v2_coco_2018_03_29.pbtxt
```
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
#### Filtering, FFTs, and Time Series data. (beta, optional)
=======
>>>>>>> Stashed changes

![Alt text](detected_out.jpg?raw=true "Title")

#### Filtering, FFTs, and Time Series data.
>>>>>>> ea626365259eef960dc3aac7816a5b251fa704ab
Additional filtering and analysis can be done on the sensors that were provided in the kit. For example, running a Fast Fourier Transform over the IMU data stream could create a simple activity classifier between walking, running, and standing.

Using the set up from the [Lab 3 demo](https://github.com/FAR-Lab/Interactive-Lab-Hub/tree/Spring2021/Lab%203/demo) and the accelerometer, try the following:

**1. Set up threshold detection** Can you identify when a signal goes above certain fixed values?

**2. Set up averaging** Can you average your signal in N-sample blocks? N-sample running average?

**3. Set up peak detection** Can you identify when your signal reaches a peak and then goes down?

Include links to your code here, and put the code for these in your repo--they will come in handy later.

#### Teachable Machines (beta, optional)
Google's [TeachableMachines](https://teachablemachine.withgoogle.com/train) might look very simple.  However, its simplicity is very useful for experimenting with the capabilities of this technology.

You can train a Model on your browser, experiment with its performance, and then port it to the Raspberry Pi to do even its task on the device.

Here is Adafruit's directions on using Raspberry Pi and the Pi camera with Teachable Machines:

1. [Setup](https://learn.adafruit.com/teachable-machine-raspberry-pi-tensorflow-camera/raspberry-pi-setup)
2. Install Tensorflow: Like [this](https://learn.adafruit.com/running-tensorflow-lite-on-the-raspberry-pi-4/tensorflow-lite-2-setup), but use this [pre-built binary](https://github.com/bitsy-ai/tensorflow-arm-bin/) [the file](https://github.com/bitsy-ai/tensorflow-arm-bin/releases/download/v2.4.0/tensorflow-2.4.0-cp37-none-linux_armv7l.whl) for Tensorflow, it will speed things up a lot.
3. [Collect data and train models using the PiCam](https://learn.adafruit.com/teachable-machine-raspberry-pi-tensorflow-camera/training)
4. [Export and run trained models on the Pi](https://learn.adafruit.com/teachable-machine-raspberry-pi-tensorflow-camera/transferring-to-the-pi)

Alternative less steps option is [here](https://github.com/FAR-Lab/TensorflowonThePi).

#### PyTorch  
As a note, the global Python install contains also a PyTorch installation. That can be experimented with as well if you are so inclined.

### Part B
### Construct a simple interaction.

Pick one of the models you have tried, pick a class of objects, and experiment with prototyping an interaction.
This can be as simple as the boat detector earlier.
Try out different interactions outputs and inputs.
**Describe and detail the interaction, as well as your experimentation.*

For this Lab, I collaborated with Chelsea Luo (cl773)

After trying the models, we have decided to use the object-detection model. We picked my iPhone as the object that we would like to detect. Then we prototyped it by taping the Web-Cam on a bottle of water and look at the wall. We placed a iphone in front of the camera and the Raspbery Pi successfully recoginized and captured the Object. Using what we learned, we want to combine the detection with recognition, which is implemented later in the lab. We plan to use Amazon Rekognition to identify objects.



### Part C
### Test the interaction prototype

Now flight test your interactive prototype and **note your observations**:
For example:
1. When does it what it is supposed to do?
1. When does it fail?
1. When it fails, why does it fail?
1. Based on the behavior you have seen, what other scenarios could cause problems?

What the model is supposed to do is detect and crop the object from a scene. It's constantly capturing the image and will return the coordinates of found object in the image. It can be used as a survilliance camera. For example, when you are out of your home, you can set up the webcam and the program. It will keep tracing objects in the camera. When the someone breaks in by or some objects are moving, the program can automatically save that image. It fails when the background is dark. It fails because the camera does not support night vision. It can also cause problem when the background is too bright. We envisioned such system would be useful in environments such as museums or jewelry stores.



**Think about someone using the system. Describe how you think this will work.**
1. Are they aware of the uncertainties in the system?
1. How bad would they be impacted by a miss classification?
1. How could change your interactive system to address this?
1. Are there optimizations you can try to do on your sense-making algorithm.

User will be aware of the uncertainties in the system because the quality of WebCam is not as good. If the system doesn't work due to the camera's inability to capture good images, the entrie device became useless. In order to address this, we would need to make sure to use a better camera with night vision supported. Because the purpose of the system is more to survilliance instead of recognition at this stage of the lab, we can lower the threshold of classifying an object for now. As long as there's any movements in the camera, it will capture it. However, this could be an issue when we actually need to recognize the object, as it could severely impact by the miss recognition.

### Part D
### Characterize your own Observant system

Now that you have experimented with one or more of these sense-making systems **characterize their behavior**.
During the lecture, we mentioned questions to help characterize a material:
* What can you use X for?
* What is a good environment for X?
* What is a bad environment for X?
* When will X break?
* When it breaks how will X break?
* What are other properties/behaviors of X?
* How does X feel?

**Include a short video demonstrating the answers to these questions.**

https://drive.google.com/file/d/1mb7OkktJgD9h5YfnESLFnkfi2wGTN-6r/view?usp=sharing

![Alt text](sketch.png?raw=true "Title")

To better visualize the system, the sketch illustrates a scenario when the detection and recognition system is used in a jewelry store. In our vision, the system serves as an alarm/recording system to prevent stealing. The system is best used for environments with a lot of movement (ex. customers walking around), as it helps to ensure the location of specific items without causing false alarm. However since the system requires specific lighting and angle to ensure the quality of the capture and recognition, places with natural light might be a bad fit to use it. The system would break when the object is completely covered by the crowds, and to avoid this, the angle of the camera placement is important. The system should merge with the environment well, serving like a hidden surveillance camera.### Part 2.

Following exploration and reflection from Part 1, finish building your interactive system, and demonstrate it in use with a video.

**Include a short video demonstrating the finished result.**

Our system uses WebCamera to detect objects every frame. The image is uploaded directly from Raspberry Pi to Amazon S3 server. Then the program will use Amazon's Rekgonition API and make an object recognition request. The results will show a list of objects detected in the image. If we want to track a iPhone, then the program can only track the location of the iPhone. When the iPhone is moved or stolen, it will record when it happened.

https://drive.google.com/file/d/1ZsQUo7qp0u2HbnOZFeEempm8NdONMOWC/view?usp=sharing

Because we had no prior experience with Amazon API, it took us a lot of time to learn how to connect to the AWS server on Raspberry Pi. And we need to install a older version of AWS CLI.

Jiadong Lou: Responsible for setting up the Amazon API, and code to request Amazon Recokgnition API.

Chelsea Luo: Responsible for reading API documentation, and code to upload images to the Amazon server.
