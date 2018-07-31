import bitmapfont
from shields import matrixled_shield
import machine
import utime
import gc
import micropython

# Configuration:
DISPLAY_WIDTH  = 8      # Display width in pixels.
DISPLAY_HEIGHT = 8       # Display height in pixels.
SPEED          = 10.0    # Scroll speed in pixels per second.

def read(file):
    # Initialize LED matrix.
    matrix = matrixled_shield.MatrixLED_Shield()

    # Scroll speed in pixels/ms.
    speed_ms = SPEED / 1000.0

    # Initialize font renderer using a helper function to flip the Y axis
    # when rendering so the origin is in the upper left.
    def matrix_pixel(x, y):
        matrix.pixel(x, DISPLAY_HEIGHT-1-y, 1)

    # create the renderer object
    with bitmapfont.BitmapFont(DISPLAY_WIDTH, DISPLAY_HEIGHT, matrix_pixel) as bf:

        while True:

            f = open(file)
            message = f.readline()
            while message != '':

                message = message.rstrip('\n')

                # init line
                pos = DISPLAY_WIDTH                 # X position of the message start.
                message_width = bf.width(message)   # Message width in pixels.
                last = utime.ticks_ms()             # Last frame millisecond tick time.

                # scroll line
                line_done = False
                while not line_done:
                    # Compute the time delta in milliseconds since the last frame.
                    current = utime.ticks_ms()
                    delta_ms = utime.ticks_diff(current, last)
                    last = current

                    # Compute position using speed and time delta.
                    pos -= speed_ms*delta_ms
                    if pos < -message_width:
                        line_done = True
                    else:
                        # Clear the matrix and 
                        matrix.clear()
                        # Draw the text at the current position.
                        bf.text(message, int(pos), 0)
                        # Update the matrix LEDs.
                        matrix.show()
                
                message = f.readline()
                utime.sleep(1)
                gc.collect()
                micropython.mem_info()

            f.close()
