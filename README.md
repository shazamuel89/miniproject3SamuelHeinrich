### INF601 - Advanced Programming in Python
### Samuel Heinrich
### Mini Project 3


# Analogs - A Song Analysis Forum

## Description

Analogs is a simple song analysis forum built with Flask (a Python web framework) and SQLite
(a lightweight database). Users can register, log in, create analyses of songs, leave comments
on analyses, and manage a personal profile with a username, avatar, and password. The project
demonstrates basic CRUD functionality, user authentication, and file uploads.

## Getting Started

### Dependencies

* Python 3.9 or higher (Windows, macOS, or Linux)
* Basic terminal/command prompt usage
* pip (comes with Python)

All required Python libraries are listed in `requirements.txt` and will be installed in the next step.
 
### Installing
 
* Navigate to the directory that you want to put the project into
* Open a terminal and clone the repository into the directory using the following command:
```
git clone https://github.com/shazamuel89/miniproject3SamuelHeinrich.git
```
* Change directory into the project directory
* Install dependencies using the following command:
```
pip install -r requirements.txt
```
 
### Executing program

* Initialize the database using the following command:
```
flask --app analogs init-db
```
* Run the web server using the following command:
```
flask --app analogs run
```
* Then open a web browser and navigate to `http://127.0.0.1:5000/`

## Help
 
If something breaks with the database or you want to reset to a fresh one, feel free to run the init-db command again, and then restart the app:
```
^c (ctrl + c to stop the server) 
flask --app analogs init-db
flask --app analogs run
```
 
## Authors

Samuel Heinrich
[shazamuel89@gmail.com](mailto:shazamuel89@gmail.com)
 
## Version History
 
* 1.0
    * Initial release of the working application

## License
 
This project is Unlicensed - provided without any license grant.
 
## Acknowledgments
 
Inspiration, code snippets, etc.
* [Flask Documentation](https://flask.palletsprojects.com/en/stable/)
* [Flask Tutorial](https://flask.palletsprojects.com/en/stable/tutorial/)
* [Bootstrap Documentation](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
* [Jinja Documentation](https://jinja.palletsprojects.com/en/stable/)