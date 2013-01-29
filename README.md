dispatchtool
============
Andy Satchwell
Nathan Addy
Andrew Sturges

Installation:
$ git clone https://github.com/arsturges/dispatchtool.git
$ git clone <path to Nathan's attila server to clone dr_dispatch>
$ sudo pip install flask
$ cd dispatchtool
$ python dispatchtool.py

To deploy on server:
$ cd ~
$ git clone git@github.com:arsturges/dispatchtool.git
$ cd /var/www/
$ sudo ln -s ~/dispatchtool dispatchtool
$ # make sure debug is set to False!
$ # make sure secret.py exists
$ sudo /etc/init.d/apache2 restart

To update on server:
$ cd ~
$ git pull

Questions:
* Why is os.path.curdir different when running on server vs. workstation?
* Why is Apache not writing to access.log?
