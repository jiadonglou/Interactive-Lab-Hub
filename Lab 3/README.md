# You're a wizard, Jiadong Lou

<img src="https://pbs.twimg.com/media/Cen7qkHWIAAdKsB.jpg" height="400">

In this lab, we want you to practice wizarding an interactive device as discussed in class. We will focus on audio as the main modality for interaction but there is no reason these general techniques can't extend to video, haptics or other interactive mechanisms. In fact, you are welcome to add those to your project if they enhance your design.


## Text to Speech and Speech to Text

In the home directory of your Pi there is a folder called `text2speech` containing some shell scripts.

```
pi@ixe00:~/text2speech $ ls
Download        festival_demo.sh  GoogleTTS_demo.sh  pico2text_demo.sh
espeak_demo.sh  flite_demo.sh     lookdave.wav

```

you can run these examples by typing 
`./espeakdeom.sh`. Take some time to look at each script and see how it works. You can see a script by typing `cat filename`

```
pi@ixe00:~/text2speech $ cat festival_demo.sh 
#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech

echo "Just what do you think you're doing, Dave?" | festival --tts

```

You can also play audio files directly with `aplay filename`.

After looking through this folder do the same for the `speech2text` folder. In particular, look at `test_words.py` and make sure you understand how the vocab is defined. Then try `./vosk_demo_mic.sh`

## Serving Pages

In Lab 1 we served a webpage with flask. In this lab you may find it useful to serve a webpage for the controller on a remote device. Here is a simple example of a webserver.

```
pi@ixe00:~/$ python server.py
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 162-573-883
```
From a remote browser on the same network, check to make sure your webserver is working by going to [http://ixe00.local:5000]()


## Demo

In the [demo directory](./demo), you will find an example wizard of oz project you may use as a template. **You do not have to** feel free to get creative. In that project, you can see how audio and sensor data is streamed from the Pi to a wizard controller that runs in the browser. You can control what system says from the controller as well.

## Optional

There is an included [dspeech](.dspeech) demo that uses [Mozilla DeepSpeech](https://github.com/mozilla/DeepSpeech) for speech to text. If you're interested in trying it out we suggest you create a seperarate virutalenv. 



# Lab 3 Part 2

Create a system that runs on the Raspberry Pi that takes in one or more sensors and requires participants to speak to it. Document how the system works and include videos of both the system and the controller.

## Prep for Part 2

1. Sketch ideas for what you'll work on in lab on Wednesday.
![Alt text](sketch.jpg?raw=true "Title")

## Share your idea sketches with Zoom Room mates and get feedback

*what was the feedback? Who did it come from?*
Chelsea Luo (cl773): I think it is awesome extension of your previous lab’s work. It would be good to add another sensor to reset the system — like a button or joystick.

## Prototype your system

The system should:
* use the Raspberry Pi 
* use one or more sensors
* require participants to speak to it. 

*Document how the system works*

![Alt text](device.jpg?raw=true "Title")
Lab 3 is built based on my Lab 2 code.

Lab 2 Recap:
For the previous lab, I developed a interactive device that shows current time in different timezones. User can use buttons on the display to switch time zone toward "East" or "West". The background images is displayed for each timezone (with Day Picture or Night Picture depending on local time).

Lab 3 Improvement:
For this week's lab, I implemented the voice recognition algorithm to the exisiting device. A mini USB microphone and QWIIC button are used to record the voice input. When the user press the QWIIC button and hold it, the device will start recording and the button will light green. On the backend, a subprocess is created to call arecord. When the user releases the button, the subprocess is killed and the recording is saved locally as a wav file. 

What user can say/do:
"day" : Switch background picture to day time
"night": Switch background picture to night time
"east": Move to one timezone towards EAST
"west": Move to one timezone towards WEST
"Shanghai"/"Paris"/"Tokyo" : Move to cities' local timezone

*Include videos or screencaptures of both the system and the controller.*
https://drive.google.com/file/d/1uvMaJ4uVw8CkpUMB78AXAFzb1jX_2Mbj/view?usp=sharing

## Test the system
Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard _after_ the interaction, but we recognize that can be hard.)

Answer the following:

### What worked well about the system and what didn't?
The system from Lab 2 was a little bit difficult to navigate because you have to move time zone one at a time. This time the system supports "jumping" directly to the time zone you want to see by using the voice recognition. What didnt' work well is the reaction time. There's always a delay between user input and device output. This delay is due to the latency of speech2text.


### What worked well about the controller and what didn't?
I think the button worked really well. The green light of the button indicates the device is recording, which helps user understand the status of the device. The Mini USB Microphone didn't work well. There are several times that it couldn't recognize the voice.

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?
It's better to let the user know when to speak. For example, a "beep" sound can be implemented to remind user to begin talking. For my device, I simply used the green light to indicate the device is recording. Without the cues, user might be when they shouldn't in a more autonomous version of the system.


### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?
My system can be improved by recognizing more valcabularies and support more time zone searches. I can alsy capture the accerlation of the device. For example, quckly moving the device from left to right can implies change timezone towards east. Quickly moving up and down can switch between day and night. This makes the device more interative than it already is.

