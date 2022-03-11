/*
 * SimpleSerial V2 Template C code
 * Can be freely used to implement ChipWhisperer target binaries.
 *
 * Date: 14th March 2021
 */

#include <stdint.h>
#include <stdlib.h>

#define SS_VER 2

#include "simpleserial/simpleserial.h"

/// This function will handle the 'p' command send from the capture board.
/// It returns the squared version of the scmd given.
/// It does this in approximately equal time, which allows us to see clear
/// differences between different scmd values.
uint8_t handle(uint8_t cmd, uint8_t scmd, uint8_t len, uint8_t *buf)
{
    volatile uint16_t i, j;
    volatile uint32_t cnt;

    cnt = 0;

    trigger_high();
    for(i=0; i<50; i++){
        for(j=0; j<50; j++){
            cnt++;
        }
    }
    trigger_low();

    simpleserial_put('r', 4, (uint8_t*)&cnt);
    return (cnt != 2500);
}

int main(void) {
  // Setup the specific chipset.
  platform_init();
  // Setup serial communication line.
  init_uart();
  // Setup measurement trigger.
  trigger_setup();

  simpleserial_init();

  // Insert your handlers here.
  simpleserial_addcmd('p', 0, handle);

  // What for the capture board to send commands and handle them.
  while (1)
    simpleserial_get();
}
