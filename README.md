# EML_Car
Fun little project to turn an old 1:10 RC car into a self driving car usuing only a single front camera and end-to-end machine learning.  
A full description of the project can be found here: <https://autosys.informatik.haw-hamburg.de/publication/2020riegedaniel/>

## Hardware
This project uses some old rc car platform with a PWM servo and brushed Motor (controlled by an ESC via PWM as well). 
For the processing a raspberry Pi 4 is used in combination with a Google Coral TPU stick. The camera is a simple raspberry pi cam, nothing fancy.
For safety reasons and data recording, the car is still controllable via a remote but not directly. Instead the RC receiver PWM signal is measured by some arduino nano using interrupts (for precise timings not on the pi directly) and then send to the pi via UART. 

## Side note
Yes, the code is completly python even though it is a real time system. Python was chosen just for convenience. 
