import os
import secret

# Upload and download folders should be, relative to this file, one level deeper.
path_to_this_file = os.path.abspath(__file__)
parent_directory_to_this_file = os.path.dirname(path_to_this_file)

UPLOAD_FOLDER   = os.path.join(parent_directory_to_this_file, 'user_uploads')
DOWNLOAD_FOLDER = os.path.join(parent_directory_to_this_file, 'user_results')

ALLOWED_EXTENSIONS = set(['txt', 'csv'])
USERNAME = secret.username
PASSWORD = secret.password
SECRET_KEY = secret.secret_key
