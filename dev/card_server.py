#
# Basic PicoWeb application for serving up content in a sub-folder
#
import ure as re
import picoweb
from shields import microsd_shield

# sub-folder we will serve conent from
rootdir = "wwwroot/"

# handle the root URL
def index(req, resp):
    yield from app.sendfile(resp, rootdir + "index.html")

# handle all other resource (file) requests
def file(req, resp):
    fname = req.url_match.group(1)
    yield from app.sendfile(resp, rootdir + fname)

# define the picoweb routing table
ROUTES = [
    ("/", index),
    (re.compile("^/(.+)"), file),
]

# setup the logging that is used by picoweb
import logging
logging.basicConfig(level=logging.DEBUG)

sd = microsd_shield.MicroSD_Shield()
sd.mount()

# run the server
app = picoweb.WebApp(None, ROUTES)
app.run(host="0.0.0.0", port=80, debug=True)

sd.unmount()
