import tinyweb

# Create web server application
app = tinyweb.webserver()

@app.route('/')
async def index(req, resp):
    await resp.send_file('index.html')

@app.route('/<fn>')
async def html(req, resp, fn):
    await resp.send_file('/wwwroot/{}'.format(fn))

@app.route('/<sb>/<fn>')
async def content(req, resp, sb, fn):
    await resp.send_file('/wwwroot/{}/{}'.format(sb, fn))

app.run(host='0.0.0.0', port=80)