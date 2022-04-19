from flask import Flask, render_template, request
import colorgram
from PIL import Image

# imports to not save the image but encode it
import base64
import io

# the first version of this project was saving images to the static folder to then serve them
# after some research, I found how to encode images to pass them as argument to the HTML template
# no need to save the images (saving serves no purpose in this case)
# the initla version is initial_version.py


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', img_data=None, colours=None)


@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        # resize image increase speed by 10 when uploading large images (> 20 megapixels)
        uploaded_file = Image.open(uploaded_file)
        uploaded_file.thumbnail((1500, 1500))

        # encode image instead of saving it
        data = io.BytesIO()
        uploaded_file.save(data, "JPEG")
        encoded_img_data = base64.b64encode(data.getvalue())
        decoded_img_data = encoded_img_data.decode('utf-8')
        img_data = f"data:image/jpeg;base64,{decoded_img_data}"

        # extract colours from image
        num_colours = int(request.form['colours'])
        extracted_colours = colorgram.extract(uploaded_file, num_colours)

        # create array of extracted colours with rgb and hex code
        img_colours = []
        for colour in extracted_colours:
            rgb = (colour.rgb.r, colour.rgb.g, colour.rgb.b)
            new_colour = [rgb, "#" + ('%02x%02x%02x' % rgb).upper()]
            img_colours.append(new_colour)
        return render_template('index.html', colours=img_colours, img_data=img_data)
    else:
        return render_template('index.html', img_data=None, colours=None)


if __name__ == "__main__":
    app.run(debug=True)
