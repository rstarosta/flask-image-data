import PIL.ExifTags
import PIL.Image
from flask import Flask, request, redirect, flash, jsonify

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'tiff'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            return jsonify(extract_exif_data(file))

    return '''
      <!doctype html>
      <title>Upload new File</title>
      <h1>Upload new File</h1>
      <form method=post enctype=multipart/form-data>
        <p><input type=file name=file>
           <input type=submit value=Upload>
      </form>
      '''


def extract_exif_data(file):
    image = PIL.Image.open(file)
    exif = image._getexif()

    if exif is not None:
        return {
            PIL.ExifTags.TAGS[k]: v
            for k, v in exif.items()
            if k in PIL.ExifTags.TAGS and not isinstance(v, bytes)
        }

    return {"error": "No exif data found"}


if __name__ == "__main__":
    app.run()
