from drivers import oled

display = oled.OLED(4, 5, 64, 48)

display.clear()
display.text("Hello")
display.show()