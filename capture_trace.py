import numpy as np
import chipwhisperer as cw
import time

# Setup our capture and target boards.
########################################
scope = cw.scope()
scope.default_setup()

# Basic setup for the glitching
scope.glitch.clk_src = "clkgen" # set glitch input clock
scope.glitch.output = "clock_xor" # glitch_out = clk ^ glitch
scope.glitch.trigger_src = "ext_single" # glitch only after scope.arm() called

scope.io.hs2 = "glitch" # output glitch_out on the clock line
print(scope.glitch)

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

# Define measurement values
########################################
width_values =  np.arange(4.5, 5.5, 0.001) # 4.5 - 5.5 with steps of 0.001
offset_values = np.arange(7.5, 8.5, 0.01) # 7.5 - 8.5 with steps of 0.01

glitch_values = []

# Generate a tuple value for all possible combinations
for wvalue in width_values:
    for ovalue in offset_values:
        if (ovalue != 0.0 and wvalue != 0.0):
            glitch_values.append((wvalue, ovalue))
########################################

# Parameters
########################################
# Other parameters. These need to be refined.
# First put them to broadranges and then progressively refine
scope.glitch.ext_offset = 8 # started at 2
scope.glitch.repeat = 1 # started at 100

expected_sum = 2500

scope.adc.timeout = 0.1

rounds_per_point = 1 # Perform one measurement per tuple
########################################

# Perform attacks
########################################
import struct

glitch_outputs = []

# Reset the device
reboot_flush()
for glitch_setting in glitch_values:
    scope.glitch.width = glitch_setting[0]
    scope.glitch.offset = glitch_setting[1]

    glitch_outputs.append({
        "width": glitch_setting[0],
        "offset": glitch_setting[1],
        "resets": 0, # number of resets needed
        "successes": [], # All sum values where it different from the expected sum
    })

    for i in range(rounds_per_point):
        if scope.adc.state:
            print("Trigger still high!")
            glitch_outputs[-1]["resets"] += 1

            reboot_flush()

        scope.arm()

        target.send_cmd('p', 0x00, bytearray([]))

        ret = scope.capture()

        val = target.simpleserial_read_witherrors('r', 4, glitch_timeout=10)

        if ret:
            print('Timeout - no trigger')
            glitch_outputs[-1]["resets"] += 1

            reboot_flush()
        else:
            if val['valid'] is False:
                glitch_outputs[-1]["resets"] += 1
            else:
                if val['payload'] is None:
                    print(val['payload'])
                    continue
                output_sum = struct.unpack("<I", val['payload'])[0]

                if output_sum != expected_sum: #for loop check
                    print("🐙 Succesful attack (output value: {})".format(output_sum))
                    glitch_outputs[-1]["successes"].append(output_sum)
                else:
                    # We don't care about the times were it did not produce
                    # errors.
                    continue

print("Done glitching")
########################################

# Disconnect from the Chipwhisperer device
########################################
scope.dis()
target.dis()
########################################

# Plot the data
########################################
import matplotlib.pylab as plt

symbols = [
    ('x', '#ff0000'),
    ('^', '#00ff00'),
    ('o', '#0000ff'),
    ('P', '#ffff00'),
    ('d', '#ff00ff')
]
elems = dict()

for glitch_output in glitch_outputs:
    # https://www.geeksforgeeks.org/how-to-count-the-frequency-of-unique-values-in-numpy-array/
    # Get a tuple of unique values 
    # and their frequency in
    # numpy array
    unique, frequency = np.unique(glitch_output["successes"], 
                                  return_counts = True) 
      
    # convert both into one numpy array 
    # and then transpose it
    count = np.asarray((unique,frequency)).T

    for el, freq in count:
        if not (str(el) in elems):
            elems[str(el)] = []

        elems[str(el)].append((glitch_output["width"], glitch_output["offset"], freq))

for i, b in enumerate(elems.items()):
    if (i >= len(symbols)):
        print("Too many options. Breaking.")
        break;

    x = list(map(lambda x: x[0], b[1]))
    y = list(map(lambda x: x[1], b[1]))
    s = list(map(lambda x: x[2] * 10, b[1]))

    plt.scatter(x, y, s=s, c=symbols[i][1], alpha=0.5, marker=symbols[i][0], label=b[0])

plt.xlabel("Width")
plt.ylabel("Offset")
plt.legend(loc='upper left')

plt.show()
########################################