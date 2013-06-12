import os
from flask import Flask, flash, redirect, render_template, request
from flask import send_from_directory, session, url_for
from werkzeug import secure_filename
from functools import wraps
import helper_methods
import app_settings
import DRD

app = Flask(__name__)
app.config.from_object(app_settings)
app.debug = True # Set to false before deploying!

@app.context_processor
def utility_processor():
    def add_class(title, string):
        if title == string:
            return 'class="active"'
    return dict(add_class=add_class)

def authenticate(func): # http://flask.pocoo.org/snippets/8/
    @wraps(func)
    def call(*args, **kwargs):
        if 'logged_in' in session and session['logged_in'] == True:
            return func(*args, **kwargs)
        else:
            return redirect('login')
    return call

@app.route('/')
@authenticate
def index():
    return render_template('home.html', title = "Home") 

@app.route('/get_started', methods = ['GET','POST'])
@authenticate
def get_started():
    error = None
    if request.method == 'POST':
        # Establish the 'user-uploaded' files and a unique string
        # to temporarily store them on the server:
        lmp_file = request.files['lmps']
        dr_file = request.files['dr']
        load_file = request.files['load']
        dispatch_type = request.form['dispatch_type']
        dispatch_trigger = request.form['dispatch_trigger']
        uuid_string = helper_methods.generateID()
        dr_programs = {
            "P_Event_Length": request.form['P_Event_Length'],
            "L_Event_Length": request.form['L_Event_Length'],
            "I_Event_Length": request.form['I_Event_Length'],
            "R_Event_Length": request.form['R_Event_Length'],
            "P_Number_Events": request.form['P_Number_Events'],
            "L_Number_Events": request.form['L_Number_Events'],
            "I_Number_Events": request.form['I_Number_Events'],
            "R_Number_Events": request.form['R_Number_Events']
            }

        if lmp_file and dr_file and load_file and helper_methods.allowed_files(
                app.config['ALLOWED_EXTENSIONS'],
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

            # get shorter names to pass to DRD module:
            lmp_path = os.path.join(app.config['UPLOAD_FOLDER'], lmp_server_filename)
            dr_path = os.path.join(app.config['UPLOAD_FOLDER'], dr_server_filename)
            load_path = os.path.join(app.config['UPLOAD_FOLDER'], load_server_filename)
            
            # run the algorithm using the three files you just saved to the server:
            try:
                mw_file_path, prices_file_path = helper_methods.run_dr_dispatch(
                    dr_path,
                    lmp_path, 
                    load_path, 
                    dispatch_type, 
                    dispatch_trigger,
                    dr_programs)
            except (OSError, NameError, KeyError, DRD.parsing.ParsingException) as e:
                return render_template(
                    'get_started.html',
                    title='Get Started',
                    error = e)
            return render_template(
                'confirm_files.html',
                title="Confirm Files Submission",
                mw_dispatch_fn=os.path.basename(mw_file_path),
                prices_dispatch_fn = os.path.basename(prices_file_path))
        else:
            error = "The program requires all three files to be present, and all \
                three files must be of type 'text' or 'csv'."
            return render_template('get_started.html', title='Get Started', error=error)
    else:
        return render_template('get_started.html', title="Get Started", error=error)

@app.route('/download_results/<filename>')
@authenticate
def download_results(filename):
    return send_from_directory(app.config['RESULTS_DOWNLOAD_FOLDER'], filename)

@app.route('/download_templates/<filename>')
@authenticate
def download_templates(filename):
    return send_from_directory(app.config['TEMPLATES_DOWNLOAD_FOLDER'], filename)

@app.route('/confirm_files')
@authenticate
def confirm_files(lmps, dr, load):
    return render_template('confirm_files.html', title = "Confirm Files")

@app.route('/template_generator', methods=['GET', 'POST'])
@authenticate
def template_generator():
    if request.method == 'POST':
        form_data = request.form
        bas, dr_programs = helper_methods.parse_template_form_data(form_data)
        dr_levels_filename, lmp_filename, energy_load_filename = \
            helper_methods.create_templates(form_data)
        return render_template(
            'template_instructions.html',
            title="Template Instructions",
            bas = bas,
            dr_programs = dr_programs,
            dr_levels_filename = dr_levels_filename,
            lmp_filename = lmp_filename,
            energy_load_filename = energy_load_filename)
         
    else:
        list_obj = range(11)
        list_obj = map(str, list_obj)
        return render_template(
            'template_generator.html',
            title = "Template Generator",
            ba_field_names=list_obj) 

@app.route('/template_instructions')
@authenticate
def template_instructions():
    return render_template('template_instructions.html', title="Template Instructions")


@app.route('/documentation')
@authenticate
def documentation():
    return render_template('documentation.html', title = "Documentation") 

@app.route('/about')
@authenticate
def about():
    return render_template('about.html', title = "About") 

@app.route('/algorithms')
@authenticate
def algorithms():
    return render_template('algorithms.html', title = "Algorthms") 

@app.route('/contact')
@authenticate
def contact():
    return render_template('contact.html', title = "Contact") 

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        wrong_username = request.form['username'] != app.config['USERNAME']
        wrong_password = request.form['password'] != app.config['PASSWORD']
        if wrong_username or wrong_password:
            error = 'Invalid username or password.'
        else:
            session['logged_in'] = True
            flash('Login successful.')
            return redirect('/')
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("You've been successfully logged out.")
    return redirect('/login')

if __name__ == '__main__':
    app.run() #disable app.debug before pushing to production.
