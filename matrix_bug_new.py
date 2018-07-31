import urandom
from shields import tm1640_shield

matrix = tm1640_shield.TM1640_Shield()

height = 8
width = 8

x = 0
y = 1

up = 0
right = 1
down = 2
left = 3

head = (urandom.getrandbits(3), urandom.getrandbits(3))
thorax = head
tail = head
stinger = head
direction = urandom.getrandbits(2)
count = 0

while True:

    direction = urandom.getrandbits(2)

    if direction == up:
        newhead = (head[x] + 1, head[y])
    elif direction == right:
        newhead = (head[x], head[y] + 1)
    elif direction == down:
        newhead = (head[x] - 1, head[y])
    elif direction == left:
        newhead = (head[x], head[y] - 1)

    if newhead[x] >= 0 and newhead[x] <= width - 1 and newhead[y] >= 0 and newhead[y] <= height -1:
        
        if newhead != head and newhead != thorax and newhead != tail and newhead != stinger:

            stinger = tail
            tail = thorax
            thorax = head
            head = newhead

            matrix.clear()
            matrix.pixel(head[x], head[y], 1)
            matrix.pixel(thorax[x], thorax[y], 1)
            matrix.pixel(tail[x], tail[y], 1)
            matrix.pixel(stinger[x], stinger[y], 1)
            matrix.show()

            count = 0

        else:
            count += 1
    else:
        count += 1

    if count > 20:
        head = (urandom.getrandbits(3), urandom.getrandbits(3))
        thorax = head
        tail = head
        stinger = head
        direction = urandom.getrandbits(2)
        count = 0

