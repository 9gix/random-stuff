import RPi.GPIO as GPIO

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


if __name__ == '__main__':
    while True:
        GPIO.output([O1, O2, O4], 1)
        GPIO.output(O3, 0)
