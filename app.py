from flask import Flask, render_template, request,flash, redirect, url_for,send_from_directory
import Segmentation
from werkzeug.utils import secure_filename
import os
# change static folder to render photos from other directories
UPLOAD_FOLDER = 'static/uploaded_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            print(request.url)
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return render_template('file_upload.html')

@app.route('/uploads/<name>')
def download_file(name):
    print('in download function')
    fullpath = app.config["UPLOAD_FOLDER"]+'/'+name
    # ans = recognition.prediction(fullpath) : Use this for recognition
    segmented_path = Segmentation.segment(fullpath) # send file for the segmentation
    data =[name, segmented_path] # name contains original filename only
    return render_template("results.html", data=data)

if __name__ == '__main__':
    app.run(debug=True, port=8000)