from flask  import Flask, request
from selenium import webdriver
import requests
import base64

app = Flask(__name__)

@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    if request.method == 'POST':
        if "username" in request.values and "password" in request.values:
            username = request.values.get('username')
            password = request.values.get('password')
            if username == 'admin' and password == 'admin':
                returnHtml = '<!doctype html><html><body><h1>Access Granted.  {FLAG:EASY_CREDS}</h1></body></html>'
            else:
                returnHtml = '<!doctype html><html><body><h1>Access Denied!</h1></body></html>'
    else:
        returnHtml = '<!doctype html><html><body><h1>Admins Only!</h1><form method=post>Username: <input type=text name=username><br />Password: <input type=password name=password></form></form></body></html>'

    return returnHtml

@app.route('/', methods=['GET'])
def home_page():
    location = request.args.get('l')
    print("Location: %s" % (location))
    options = webdriver.ChromeOptions()

    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('user-agent=ThumbCrawler')

    options.binary_location="/usr/bin/chromium-browser"

    driver = webdriver.Chrome(options=options)
    driver.get(location)
    base64Image = driver.get_screenshot_as_base64()
    driver.close()
    return "<!doctype html><html><body><img src='data:image/png;base64, " + base64Image + "'></body></html>"

if __name__ == '__main__':
    app.run(debug=False, port=5000)


