# Installation notes for DVH Analytics

## Before you start
Please note this software does not work "out-of-the-box."  The smoothest way to run this software is with 
Docker and [DVH Analytics Docker](https://github.com/cutright/DVH-Analytics-Docker). But if you prefer running the source code, here are some broad strokes:
* Must have a PostgreSQL DB setup prior to use. [PostgreSQL Notes](#PostgreSQL)
* Must initialize import_settings.txt and sql_connection.cfg  
`$ dvh settings` or `$ dvh settings_simple`
* Must import data via the admin GUI or `$ dvh import` prior to running the main Bokeh app.

DVH Analytics relies on Bokeh to create web servers/pages for the GUIs, 
so it's best to follow this guide as this app may not behave in the way you might expect from a traditional python app.


## Pre-requisites
 - [Chrome](https://www.google.com/chrome/browser/desktop/) or [Firefox](https://www.mozilla.org/en-US/firefox/new/)
 - [PostgreSQL](https://www.postgresql.org/) (tested with 9.6)
 - [Python 2.7](https://www.python.org/downloads/release/python-2712/) (python3 not supported)
 - [pip](https://pip.pypa.io/en/stable/installing/) (python package manager)
 - Xcode Command Line Tools (Mac only)  

If any of these are not installed, see [Additional Notes](#additional-notes).  

## Setting up your python environment
DVH Analytics is available via pip install:
~~~~
$ pip install dvh-analytics
~~~~
If you're on Mac or Linux, you may need:
~~~~
$ sudo pip install dvh-analytics
~~~~
And for Linux only, you may need to install freetype prior to pip install dvh-analytics:
~~~~
$ sudo apt-get install libfreetype6-dev
~~~~

## Define directories and connection settings
For a web-based UI, type in the following to access the Settings:
~~~~
$ dvh settings
~~~~
or the following for a command-line based setup:
~~~~
$ dvh settings_simple
~~~~

## Processing test files
To verify all of your settings are valid and installation was successful, type:
~~~~
$ dvh test
~~~~
This will process all dicom files located in the test files folder. If this test passes, then all dependencies are 
successfully installed (e.g., PostgreSQL, Python libraries), import directories are valid, and communication with your 
SQL DB has been established.

## Importing your own data
To import your own data, you can click "Import all from inbox" in the Database Editor tab of the 
[settings GUI](#roi-name-manager-db-editor-and-backup--restore)

Alternatively, to import your own data via command line for more options:
~~~~
$ dvh import
~~~~
Assuming all of the previous steps were successful, all dicom files anywhere within your inbox will be imported 
into the SQL database, then organized by patient ID and moved to the specified imported folder.  Note that by 
default, the code will not import dicom files with Study Instance UIDs that are already in the database.
 
You may force the import regardless of UID conflicts by typing:
~~~~
$ dvh import --force-update
~~~~
If you'd like to import from a directory other than the one in your settings:
~~~~
$ dvh import --start-path /some-absolute-directory-name
~~~~
## ROI Name Manager, DB Editor, and Backup & Restore
Using the 'settings' command will start a Bokeh server and open your default browser to access the ROI Name 
Manager, DB Editor, and Backup & Restore modules.  Be sure to stop the server when you're done by press ctrl + c 
in the command line window.
~~~~
$ dvh admin
~~~~
## Main DVH Analytics view
Type the following to start the Bokeh server:  
~~~~
$ dvh run
~~~~
If Chrome or Firefox is not your default browswer, you'll need to copy and paste the url into Chrome or Firefox.
From within the active terminal, press ctrl + c to stop the Bokeh server.

If you would like to specify an IP or port other than the default 127.0.0.1:5006, use the following when starting
the Bokeh server.  You may be interested in this if you are running from a computer with a static IP and would like
to access this Bokeh server from across your network.
~~~~
$ dvh run --allow-websocket-origin <new IP:port>
~~~~
~~~~
$ dvh run --port <some other port number>
~~~~
These two features work with any of the commands that start web-based UI.

----------------------------------------------------------------------------------------------
## Additional Notes

### Python 2.7  
*(Windows only, Xcode command line tools for mac and Ubuntu both include Python 2.7)*  
Download Python 2.7 (not 3.x) from: https://www.python.org/downloads/windows/

Be sure to include pip in the installation and let the installer update your environment variables.

### Xcode Command Line Tools (Mac Only)
Make sure Xcode command line tools are installed. If the full Xcode package is installed (from the Mac App Store), enter the following into a terminal window:
~~~~
$ xcode-select --install
~~~~

### PostgreSQL
If you are familiar with PostgreSQL and have access to a PostgreSQL DB, you simply need to fill in the
login information by running:
~~~
$ dvh settings_simple --sql
~~~

If you need PostgreSQL, here are some options for each OS.

*Mac OS*  
Simply download the PostgreSQL app: http://postgresapp.com/  
 - Open the app
 - Click "Start"
 - Double-click "postgres" with the cylindrical database icon
 - Type the following in the SQL terminal:
~~~~
create database dvh;
~~~~
Then quit by typing:
~~~~
\q
~~~~

NOTE: You may replace dvh with any database name you wish, but you must update dbname in settings to reflect what 
database name you chose.  

*Ubuntu*  
You probably already have PostgreSQL installed, but if you don't, type the following in a terminal:
~~~~
$ sudo apt-get install postgresql postgresql-client postgresql-contrib libpq-dev
$ sudo apt-get install pgadmin3
~~~~
Upon successful installation, open type 'pgadmin3' in the terminal to open the graphical admin.  
Then, create a user and database of your choice (same instructions found below for Windows)

*Windows*  
Download the installer for BigSQL: https://www.bigsql.org/postgresql/installers.jsp/

 - Be sure to include pgAdmin3 LTS
 - After installation, launch pgAdmin3 LTS from the Windows Start Menu.
   - Right-click localhost and then click connect.
   - Right-click Login Roles and then click New Login Role.
   - Fill in Role name (e.g., dvh), click OK
   - Right-click Databases then click New Database
   - Fill in Name (e.g., dvh), set owner to the Role name you just created. Click OK.


### PIP (python package management):
From a terminal window, type:

*Mac*
~~~~
$ easy_install pip
~~~~

*Ubuntu*
~~~~
$ sudo apt-get install python-pip
~~~~

*Windows*  
Download get-pip.py from here: https://pip.pypa.io/en/stable/installing/  
Then compile:
~~~~
$ python get-pip.py
~~~~

### Security Concerns
Obviously, data intended for an application like this may be sensitive and require HIPPA compliance.  The end user is 
entirely liable for setting up an appropriately secure environment.  Bokeh provides some help 
[here](https://bokeh.pydata.org/en/latest/docs/user_guide/server.html#basic-reverse-proxy-setup)
with regards to a reverse proxy, so that HTTPS may be implemented.

DVH Analytics does provide a loose framework for authentication. There is a parameter 'auth_user_req' located in 
options.py; by default this is set to False.  If set to True, user name and password fields will 
be provided to the user when accessing any of the Bokeh servers in this app.  These credentials will be passed to the check_credentials 
function in auth.py.  By default, this function simply returns True.  The end user must supply their own code 
for authentication.  An example code using python-ldap is provided in auth.py, but requires some editing for each end user's
own implementation.  And please remember, you need to setup HTTPS on your own for this authentication to make any sense,
otherwise user name and passwords will not be encrypted inbetween the web-user and the Bokeh server.

Your SQL DB password is stored as plain text in preferences/sql_connection.cnf.  I realize this is not ideal, but if OS
user authentication is implemented, you don't need a password. Alternatively, you could change permissions on this file
so only you or root can access it, just be sure to run your bokeh serve with sudo if needed.


### Customizations
See options.py if you would like to customize some of the plots in the main app, e.g., colors, font sizes, 
line dash, etc.  These will be editable in settings.py in a future update.  Currently, you need to relaunch your 
Bokeh server after editing options.py.
