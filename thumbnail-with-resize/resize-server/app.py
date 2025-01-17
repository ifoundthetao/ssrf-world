from flask  import Flask, request
import subprocess 

app = Flask(__name__)

@app.route("/", methods=["POST"])
def main():
    if "b64_image" in request.values:
        imageData = request.values.get('b64_image').strip()

        commandToRun  = "echo '%s' " % (imageData)
        commandToRun += "| base64 -d > img.png "
        commandToRun += "; convert img.png -geometry 200x resized-img.png "
        commandToRun += "; base64 resized-img.png "
        commandToRun += "| tr -d '\\n' > resized-img.b64"
    
        subprocess.Popen(commandToRun
                , stdout=subprocess.PIPE
                , shell=True
        ).communicate()
        resizedImage = open('resized-img.b64', 'r').read()

    else:
        defaultImage = open('no-img.txt', 'r')
        resizedImage = defaultImage.read()
        defaultImage.close()
    return resizedImage

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=4000)
