from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import colorgram
from PIL import Image
import os


UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    # delete all the images in UPLOAD_FOLDER since we do not want to store them after upload
    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, f))
    return render_template('index.html', img_data=None, colours=None)


@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        filename = secure_filename(uploaded_file.filename)
        # resize image before saving to increase speed by 10 when uploading large images (> 20 megapixels)
        uploaded_file = Image.open(uploaded_file)
        uploaded_file.thumbnail((1500, 1500))

        # save to static/images (temporarily, images are deleted on page reload)
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # extract colours from image
        file_path = f"{UPLOAD_FOLDER}/{filename}"
        num_colours = int(request.form['colours'])
        extracted_colours = colorgram.extract(file_path, num_colours)
        extracted_colours = colorgram.extract(uploaded_file, num_colours)

        # create array of extracted colours with rgb and hex code
        img_colours = []
        for colour in extracted_colours:
            rgb = (colour.rgb.r, colour.rgb.g, colour.rgb.b)
            new_colour = [rgb, "#" + ('%02x%02x%02x' % rgb).upper()]
            img_colours.append(new_colour)
        return render_template('index.html', colours=img_colours, img_data=filename)
    else:
        return render_template('index.html', img_data=None, colours=None)


if __name__ == "__main__":
    app.run(debug=True)

# HTML for image
# <img src="{{ url_for('static', filename='images/' + img_data) }}" class="uploaded-image">