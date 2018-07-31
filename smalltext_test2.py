from drivers import oled

display = oled.OLED(0, 2, 128, 64)

text = """\
MicroPython is packed full of ad
vanced features such as an inter
active prompt, arbitrary precisi
on integers, closures, list comp
rehension, generators, exception
 handling and more. Yet it is co
mpact enough to fit and run with
in just 256k of code space and 1
6k of RAM.
"""

display.smalltext(text);
display.show()