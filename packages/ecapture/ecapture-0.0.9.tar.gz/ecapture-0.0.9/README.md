# ecapture
## Image Capture Demo

First run the following command in a cmd window
~~~
pip install opencv-python
~~~

Then, run 
~~~
pip install ecapture
~~~
Create a new python script

Open the script

Import the module
~~~python
from ecapture import ecapture as ec
~~~ 
Capture using webcam
~~~python
(ec.capture(0,False,"img.jpg"))
~~~
The capture function takes three arguments:
  
  Camera index(first connected webcam will be of index 0. The next webcam will be of index 1)
  
  Window name (It can be a variable or a string. If you don't wish to see the window, type False)
   
   ~~~python
   ec.capture(0,False,"img.jpg")
   ~~~
  
  Save name (It can be a variable or a string. If you don't wish to save the image, type False)
  ~~~python
  ec.capture(0,"test",False)
  ~~~
The full code
~~~python
from ecapture import ecapture as ec

ec.capture(0,"test","img.jpg")
~~~
## Video Capture Demo
Create a new python script

Open the script

Import the module
~~~python
from ecapture import ecapture as ec
~~~ 
Capture the video using webcam
~~~python
ec.vidcapture(0,"Video","Demo.avi","q")
~~~
The vidcapture function takes four arguments:
  
  Camera index(first connected webcam will be of index 0. The next webcam will be of index 1)
  
  Window name (It can be a variable or a string)
   
   ~~~python
   ec.vidcapture(0,"Video","Demo.avi","q")
   ~~~
  
  Save name (It can be a variable or a string. If you don't wish to save the image, type False)
  ~~~python
  ec.vidcapture(0,"Video",False,"q")
  ~~~
  
  Exit key (The key you press to stop recording the video. It can be ("q", "x", "a" or any other letter))
  ~~~python
  ec.vidcapture(0,"Video","Demo.avi","x")
  ~~~
The full code
~~~python
from ecapture import ecapture as ec

ec.vidcapture(0,"Video","Demo.avi","q")
~~~
