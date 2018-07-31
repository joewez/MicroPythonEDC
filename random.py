import urandom

def randint(min, max):
    span = max - min
    div = 0x3fffffff // span
    offset = urandom.getrandbits(30) // div
    val = min + offset
    return val
