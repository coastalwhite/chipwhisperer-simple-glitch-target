import numpy as np
import chipwhisperer as cw

# Setup our capture and target boards.
########################################
scope = cw.scope()
scope.default_setup()
target = cw.target(scope, cw.targets.SimpleSerial2, flush_on_err=False)
########################################

# Reprogram the target
########################################
import os
from chipwhisperer.capture.api.programmers import STM32FProgrammer

# Initiate a new STM32F Program
# STM32 being the ARM microcontroller that we are using
# https://en.wikipedia.org/wiki/STM32#STM32_F3
program = STM32FProgrammer

# Get the path to the current folder
# Adjust accordingly
aes_firmware_dir = os.path.dirname(os.path.realpath(__file__))
aes_hex_path = os.path.join(aes_firmware_dir, r"simpleserial-target-CWLITEARM.hex")

# Apply the program to the actual target
# This allows us to run the hex code on the microcontroller
cw.program_target(scope, program, aes_hex_path)
########################################

# Define a reboot function
########################################
def reboot_flush():
    scope.io.nrst = False
    time.sleep(0.05)
    scope.io.nrst = "high_z"
    time.sleep(0.05)
    #Flush garbage too
    target.flush()
########################################

# Start glitching
########################################
target.send_cmd('g', 0x00, bytearray([0xAB]))

val = target.simpleserial_read_witherrors('r', 4, glitch_timeout=10)#For loop check
valid = val['valid']
if valid:
    response = val['payload']
    raw_serial = val['full_response']
    error_code = val['rv']

print(val)
########################################

# Return the data.
########################################
# Print the returned data
# returned_data = target.read_cmd('r')
# print(returned_data)
# ack = target.read_cmd('e')
#
# import matplotlib.pyplot as plt
#
# # Plot the trace
# plt.plot(trace)
# plt.show()
########################################

scope.dis()
target.dis()