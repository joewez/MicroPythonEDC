import bitmapfont
from shields import matrixled_shield
from shields import dht11_shield
import machine
import utime

# Configuration:
DISPLAY_WIDTH  = 8      # Display width in pixels.
DISPLAY_HEIGHT = 8       # Display height in pixels.
SPEED          = 10.0    # Scroll speed in pixels per second.

def display_dht():
    # Initialize LED matrix.
    matrix = matrixled_shield.MatrixLED_Shield()

    # create object to retrieve the temp
    dht_shield = dht11_shield.DHT11_Shield()

    def get_message():
        tempC, tempF, humidity = dht_shield.read_data()
        tempF -= 5.0
        message = 'Temp:{0} F Humidity:{1}%'.format(tempF, humidity)
        print(message)
        return message

    # Initialize font renderer using a helper function to flip the Y axis
    # when rendering so the origin is in the upper left.
    def matrix_pixel(x, y):
        matrix.pixel(x, DISPLAY_HEIGHT-1-y, 1)

    # create the renderer object
    with bitmapfont.BitmapFont(DISPLAY_WIDTH, DISPLAY_HEIGHT, matrix_pixel) as bf:

        # initialize global state:
        message = get_message()
        message_width = bf.width(message)
        pos = DISPLAY_WIDTH                 # X position of the message start.
        speed_ms = SPEED / 1000.0           # Scroll speed in pixels/ms.
        last = utime.ticks_ms()             # Last frame millisecond tick time.

        # Main loop:
        while True:

            # Compute the time delta in milliseconds since the last frame.
            current = utime.ticks_ms()
            delta_ms = utime.ticks_diff(current, last)
            last = current

            # Compute position using speed and time delta.
            pos -= speed_ms*delta_ms
            if pos < -message_width:
                message = get_message()
                message_width = bf.width(message)
                pos = DISPLAY_WIDTH

            # Clear the matrix and 
            matrix.clear()

            # Draw the text at the current position.
            bf.text(message, int(pos), 0)

            # Update the matrix LEDs.
            matrix.show()

            # Sleep a bit to give USB mass storage some processing time (quirk
            # of SAMD21 firmware right now).
            utime.sleep_ms(20)

display_dht()