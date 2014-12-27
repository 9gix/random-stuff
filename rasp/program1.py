#!/usr/local/bin/python
"""
Sample Raspberry Program on 4 LED with 4 Switch

NOTE: Add The following line in /etc/rc.local to autorun the program on startup:
sudo python /home/pi/workspace/random-stuff/rasp/program1.py &

@author: Eugene
"""

import RPi.GPIO as GPIO
import time
import random

# Set GPIO pinout numbering system
GPIO.setmode(GPIO.BCM)

# Input GPIO
I1 = 15
I2 = 17
I3 = 18
I4 = 22
input_list = [I1, I2, I3, I4]
GPIO.setup(input_list, GPIO.IN)

# Output GPIO
O1 = 23
O2 = 24
O3 = 25
O4 = 27
output_list = [O1, O2, O3, O4]
GPIO.setup(output_list, GPIO.OUT)

# Turn off All output
GPIO.output(output_list, 0)


# initialize constant value
DELAY = 0.5


# Program 1:
def prog1():
    """Blinking LED one by one"""
    for o in output_list:
        time.sleep(DELAY)
        GPIO.output(o, not GPIO.input(o))

# Program 2:
counter = 0
def prog2():
    """4-bit Binary Counter"""
    time.sleep(DELAY)
    global counter
    bin_counter = list(format(counter, '04b'))
    bin_counter.reverse()
    counter_output = [output_list[i] for i, out in enumerate(bin_counter) if int(out)]
    GPIO.output(output_list, 0)
    GPIO.output(counter_output, 1)
    counter = 0 if counter >= 15 else counter + 1


# Program 3:
output_led = 0
def prog3():
    """Blink in order"""
    time.sleep(DELAY)
    global output_led
    GPIO.output(output_list, 0)
    GPIO.output(output_list[output_led], 1)
    output_led = 0 if output_led >= 3 else output_led + 1
    

# Program 4:
def prog4():
    """Random Blinking"""
    time.sleep(0.05)
    for i in output_list:
        new_val = random.randint(0, 1)
        GPIO.output(i, new_val)


def main():
    prog = [prog1, prog2, prog3, prog4]
    try:
        while True:
            in_state = [GPIO.input(i) for i in input_list]
            
            if all(in_state):
                break
            
            in_high = [i for i, state in enumerate(in_state) if state == GPIO.HIGH]
            in_low = [i for i, state in enumerate(in_state) if state == GPIO.LOW]

            # Execute program with respect to the input state
            for i in in_high:
                prog[i]()

    except KeyboardInterrupt:
        print("Terminating Program, Good Bye!!!")
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
