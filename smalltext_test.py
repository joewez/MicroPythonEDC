from drivers import oled

display = oled.OLED(0, 2, 128, 32)

text = """\
MicroPython is a lean and effici
ent implementation of the Python
3 programming language that incl
udes a small subset of the Pytho
n standard library and is optimi
"""

display.smalltext(text);
display.show()