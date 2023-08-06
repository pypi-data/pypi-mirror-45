# Pi7447
7447 lib for raspberry pi

# Install
`pip install pi7447`

# Usage example
```
import pi7447
import time
import RPi.GPIO as gpio
gpio.setmode(gpio.BCM)

IC7447_INPUT_A = 2
IC7447_INPUT_B = 3
IC7447_INPUT_C = 4
IC7447_INPUT_D = 17

sevenSegmentSisplay = pi7447.IC7447(IC7447_INPUT_A,IC7447_INPUT_B,IC7447_INPUT_C,IC7447_INPUT_D)

#show 1 to 9
for i in range(10):
    sevenSegmentSisplay.show(i)
    time.sleep(0.5)

#turn off display
sevenSegmentSisplay.off()
```
