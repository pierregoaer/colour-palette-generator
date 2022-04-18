from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import colorgram
import ast
import os


UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


filename = None


@app.route('/')
def index():
    # delete all the images in UPLOAD_FOLDER since we do not want to store them after upload
    # could be improved
    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, f))
    return render_template('index.html', file=None, colours=None)


@app.route('/', methods=['POST'])
def upload_file():
    global filename
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_path = f"{UPLOAD_FOLDER}/{filename}"
        num_colours = int(request.form['colours'])
        extracted_colours = colorgram.extract(file_path, num_colours)
        img_colours = []
        for colour in extracted_colours:
            rgb = (colour.rgb.r, colour.rgb.g, colour.rgb.b)
            new_colour = [rgb, "#" + ('%02x%02x%02x' % rgb).upper()]
            img_colours.append(new_colour)
        return render_template('index.html', file=filename, colours=img_colours)
        
        # extracted_colours = colorgram.extract(uploaded_file, 10)
        # img_colours = []
        # for colour in extracted_colours:
        #     rgb = (colour.rgb.r, colour.rgb.g, colour.rgb.b)
        #     new_colour = [rgb, "#" + '%02x%02x%02x' % rgb]
        #     img_colours.append(new_colour)

        # for idx, colour in enumerate(extracted_colors):
        #     img_colours[idx] = {
        #         "rgb": (colour.rgb.r, colour.rgb.g, colour.rgb.b),
        #         "hex": '%02x%02x%02x' % (colour.rgb.r, colour.rgb.g, colour.rgb.b)
        #     }

        # print(img_colours)
        # return redirect(url_for('colour_palette', img_colours=img_colours))
        # return redirect(url_for('colour_palette', filename=filename))


# @app.route('/colours/<img_colours>')
# def colour_palette(img_colours):
#     # redirect(url_for()) effectively returns a URL, a list is then converted into a string
#     img_colours = ast.literal_eval(img_colours)
#     # print(type(img_colours))
#     return render_template('palette.html', colours=img_colours)


# @app.route('/colours/')
# def colour_palette():
#     return render_template('palette.html', colours=img_colours)


# @app.route('/colours/<filename>')
# def colour_palette(filename):
#     file_path = f"{UPLOAD_FOLDER}/{filename}"
#     extracted_colours = colorgram.extract(file_path, 10)
#     img_colours = []
#     for colour in extracted_colours:
#         rgb = (colour.rgb.r, colour.rgb.g, colour.rgb.b)
#         new_colour = [rgb, "#" + '%02x%02x%02x' % rgb]
#         img_colours.append(new_colour)
#     return render_template('palette.html', file=filename, colours=img_colours)


if __name__ == "__main__":
    app.run(debug=True)
