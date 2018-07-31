from drivers import oled
from drivers import wemos

display = oled.OLED(wemos.D3, wemos.D4, 128, 64)

display.clear()
display.graphic('/graphics/yingyang.txt')
display.show()
