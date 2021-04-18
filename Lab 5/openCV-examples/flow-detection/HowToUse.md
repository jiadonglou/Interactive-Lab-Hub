## How to use

Use the terminal with ssh login or the XTerm or UXTerm over VNC viewer to run one of the following commands.


### If you use VNC or X11 (e.g. ssh -X pi@...)
In these cases you can run this example with a live video stream.

```python optical_flow.py slow_traffic_small.mp4 window```

or to use the webcam

```python optical_flow.py 0 window```


### Comandline only (e.g. ssh pi@...)
If no video screen is avalible we can run these examples with 'noWindow'.
The first 'w' of noWindow needs to be uppercase.

To stop processing new images press CTRL+C. 

```python optical_flow.py slow_traffic_small.mp4 noWindow```

or to use the webcam

```python optical_flow.py 0 noWindow```