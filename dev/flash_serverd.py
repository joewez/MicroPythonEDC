#
# Basic PicoWeb application for serving up content in a sub-folder
#
import ure as re
import picoweb
import oled

# sub-folder we will serve conent from
rootdir = "wwwroot/"

# count and display response count
display = oled.OLED(4, 5, 64, 48)

def show(fname):
    display.clear()
    display.smalltext('Resource:')
    display.smalltext(fname, 0, 6)
    display.show()

# handle the root URL
def index(req, resp):
    show('index.html')
    yield from app.sendfile(resp, rootdir + "index.html")

# handle all other resource (file) requests
def file(req, resp):
    fname = req.url_match.group(1)
    show(fname)
    yield from app.sendfile(resp, rootdir + fname)

# define the picoweb routing table
ROUTES = [
    ("/", index),
    (re.compile("^/(.+)"), file),
]

# setup the logging that is used by picoweb
import logging
logging.basicConfig(level=logging.DEBUG)

# run the server
app = picoweb.WebApp(None, ROUTES)
app.run(host="0.0.0.0", port=80)
