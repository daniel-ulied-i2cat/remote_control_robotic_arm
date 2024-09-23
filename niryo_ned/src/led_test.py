import time
from rpi_ws281x import PixelStrip, Color, ws

# LED strip configuration:
LED_COUNT = 30       # Number of LED pixels.
LED_PIN = 13         # GPIO pin connected to the pixels (must support PWM!)
LED_FREQ_HZ = 800000 # LED signal frequency in hertz (usually 800kHz)
LED_DMA = 10         # DMA channel to use for generating signal (try 10)
LED_INVERT = True   # True to invert the signal (when using NPN transistor level shift)
LED_BRIGHTNESS = 255 # Set to 0 for darkest and 255 for brightest
LED_CHANNEL = 1      # PWM channel, usually 0 or 1
LED_STRIP = ws.WS2811_STRIP_GRB

# BCM Pin to enable the LED ring
PIN_ENABLE_LED_RING = 27  # BCM pin 27 to enable LED ring

# Initialize GPIO to control enabling of the LED ring (BCM pin 27)
import RPi.GPIO as GPIO

def enable_led_ring(bcm_pin):
    """
    Enable the LED ring by setting BCM pin 27 to HIGH for 5 seconds.
    """
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(bcm_pin, GPIO.OUT)
    GPIO.output(bcm_pin, GPIO.HIGH)

    # Keep the pin enabled for 5 seconds
    time.sleep(5)

    # Disable the LED ring
    GPIO.output(bcm_pin, GPIO.LOW)
    GPIO.cleanup()

# Function to set LEDs to pink color
def set_leds_to_pink(strip):
    """Set all LEDs on the strip to pink (RGB: 255, 0, 255)."""
    pink_color = Color(255, 0, 255)  # Pink color
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, pink_color)
    strip.show()

# Main function
if __name__ == "__main__":
    # Initialize the PixelStrip object
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    
    # Initialize the library (must be called once before other functions)
    strip.begin()
    
    # Enable the LED ring by setting BCM pin 27 high
    enable_led_ring(PIN_ENABLE_LED_RING)
    
    # Set all LEDs to pink
    set_leds_to_pink(strip)
    
    # Keep the LEDs on for 5 seconds
    time.sleep(5)
    
    # Optionally, turn off LEDs after 5 seconds
    strip.setBrightness(0)  # Set brightness to 0 (turns off LEDs)
    strip.show()
