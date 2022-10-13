import os
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import numpy as np


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

uploaddir = basedir + "\\static\\"

app.config['UPLOAD_FOLDER'] = uploaddir
image = 'file1.jpg'

im = np.array(Image.open(uploaddir + image))

def get_colours(im):
    width = im.shape[0]
    height = im.shape[1]

    im = im.reshape(-1)

    my_dict = {}
    for i in range(0, im.size - 1, 3):

        tup = str(im[i]).rjust(3, '0') + str(im[i + 1]).rjust(3, '0') + str(im[i + 2]).rjust(3, '0')

        if tup in my_dict:
            my_dict[tup] += 1
        else:
            my_dict[tup] = 1

    dictlist = []
    for key in my_dict:
        temp = [my_dict[key], key]
        dictlist.append(temp)
    # print('start')
    dictlist.sort(key=lambda row: (row[0], row[1]), reverse=True)
    # print(dictlist)
    new_list = dictlist[:10]
    for i in new_list:

        percent = str(round(i[0] / im.size / 3 * 100, 2))
        i[0] = percent

    return new_list


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file1():
    global image
    if request.method == 'POST':
        f = request.files['file']
        print(uploaddir + f.filename)
        f.save(uploaddir + f.filename)
        image = f.filename
        return redirect(url_for("home"))
      # return 'file uploaded successfully'



@app.route("/")
def home():
    global image
    print(uploaddir + image)
    im = np.array(Image.open(uploaddir + image))
    colours_used = get_colours(im)

    return render_template("index.html", image=image, path=uploaddir, colours_used=colours_used)

if __name__ == '__main__':
    app.run(debug=True)
