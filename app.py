
from flask import Flask, render_template
from flask.wrappers import Request
from flask import request
import base64
from main import get_response
import os
import glob

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/3')
def index3():
    return render_template('index_3.html')


@app.route('/response', methods=['GET', 'POST'])
def response():
    response = get_response()
    return response


@app.route('/upload2', methods=['POST'])
def upload():
    data = request.get_json()
    Image1 = data['Image1']
    Image2 = data['Image2']

    delete_all()
    with open("./img/Image1.png", "wb") as fh:
        ImageBin = base64.b64decode(Image1)
        fh.write(ImageBin)
        fh.close()

    with open("./img/Image2.png", "wb") as fh:
        fh.write(base64.b64decode(Image2))
        fh.close()

    response = get_response()
    return response


@app.route('/upload3', methods=['POST'])
def upload3():
    data = request.get_json()
    Image1 = data['Image1']
    Image2 = data['Image2']
    Image3 = data['Image3']

    delete_all()
    with open("./img/Image1.png", "wb") as fh:
        ImageBin = base64.b64decode(Image1)
        fh.write(ImageBin)
        fh.close()

    with open("./img/Image2.png", "wb") as fh:
        fh.write(base64.b64decode(Image2))
        fh.close()

    with open("./img/Image3.png", "wb") as fh:
        fh.write(base64.b64decode(Image3))
        fh.close()

    response = get_response()
    return response


def delete_all():
    files = glob.glob('./img/*.png')
    for f in files:
        os.remove(f)


if __name__ == '__main__':
    app.run(debug=True)
    
    
