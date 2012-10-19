import os
from flask import Flask, request, redirect, render_template, url_for, send_from_directory
from werkzeug import secure_filename 
from dr_dispatch_wrapper import run_dr_dispatch

UPLOAD_FOLDER = 'user_uploads'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('home.html', title = "Home") 

@app.route('/get_started', methods = ['GET','POST'])
def get_started():
    if request.method == 'POST':
        print request.files['lmps'].filename
        print request.files['dr'].filename
        print request.files['load'].filename
        file = request.files['lmps']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print filename
            run_dr_dispatch(
                "user_uploads/WECC_Common Case Reference DR.csv",
                "user_uploads/WECC_Common Case LMPs_20120130.csv",
                "user_uploads/WECC_Hourly Energy Load.csv",
                "Inflexible")
            return render_template('confirm_files.html',title="Confirm Files Submission")
    else:
        return render_template('get_started.html', title="Get Started")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/confirm_files')
def confirm_files(lmps, dr, load):
    return render_template('confirm_files.html', title = "Confirm Files")

@app.route('/help')
def help():
    return render_template('help.html', title = "Help") 

@app.route('/about')
def about():
    return render_template('about.html', title = "About") 

@app.route('/contact')
def contact():
    return render_template('contact.html', title = "Contact") 

if __name__ == '__main__':
    app.run(debug=True) #disable this before pushing to production
