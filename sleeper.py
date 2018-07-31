# template main.py for using the hourly_sleeper library
# must be enabled in boot.py
# Example:
#     from library import HourlySleeper
#     hourly_sleeper = HourlySleeper(4)

import machine
import time

def main():
    try:
        hourly_sleeper()

        # here is where our code would be
        # we need the reset after our code so we enter the deep sleep loop

        machine.reset()
    except Exception:
        machine.reset()

if __name__ == '__main__':
    main()