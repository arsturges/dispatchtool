import os
from flask import Flask, request, redirect, render_template, url_for, send_from_directory
from werkzeug import secure_filename 
import helper_methods

UPLOAD_FOLDER = os.path.abspath('user_uploads')
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 # 5 megabyte max upload size
        
@app.route('/')
def index():
    return render_template('home.html', title = "Home") 

@app.route('/get_started', methods = ['GET','POST'])
def get_started():
    if request.method == 'POST':
        # establish the 'user-uploaded' fles and a unique string
        # to temporarily store them on the server:
        lmp_file = request.files['lmps']
        dr_file = request.files['dr']
        load_file = request.files['load']
        uuid_string = helper_methods.generateID()

        if lmp_file and dr_file and load_file and helper_methods.allowed_files(
                ALLOWED_EXTENSIONS, 
                lmp_file.filename,
                dr_file.filename,
                load_file.filename):
            # establish filenames to save the 'user' files on the server:
            lmp_server_filename = secure_filename(uuid_string + lmp_file.filename)
            dr_server_filename = secure_filename(uuid_string + dr_file.filename)
            load_server_filename = secure_filename(uuid_string + load_file.filename)

            # save the 'user' files to server using those 'server' filenames:
            lmp_file.save(os.path.join(app.config['UPLOAD_FOLDER'], lmp_server_filename))
            dr_file.save(os.path.join(app.config['UPLOAD_FOLDER'], dr_server_filename))
            load_file.save(os.path.join(app.config['UPLOAD_FOLDER'], load_server_filename))
            # run the algorithm using the three files you just saved to the server:
            lmp_path = os.path.join(app.config['UPLOAD_FOLDER'], lmp_server_filename)
            dr_path = os.path.join(app.config['UPLOAD_FOLDER'], dr_server_filename)
            load_path = os.path.join(app.config['UPLOAD_FOLDER'], load_server_filename)
            
            helper_methods.run_dr_dispatch(
                dr_path,
                lmp_path,
                load_path,
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
