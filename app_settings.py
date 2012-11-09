import os
import secret

UPLOAD_FOLDER = os.path.abspath('user_uploads')
DOWNLOAD_FOLDER = os.path.abspath('user_results')
ALLOWED_EXTENSIONS = set(['txt', 'csv'])
USERNAME = secret.username
PASSWORD = secret.password
SECRET_KEY = secret.secret_key
