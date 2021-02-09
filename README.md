# InfoVis Assignment #

This repo contains the first assignment for the course Information Visualization. Students need to create one visualization using html/js/d3 and one visualization using the python package Bokeh.


---

## Running the app within Docker container ##

1) Install docker via: https://docs.docker.com/engine/install/
2) Move the docker-compose.yml up 1 directory (so from the InfoVis-Framework-2021 directory it is in now to the directory that contains the InfoVis-Framework-2021 directory)
3) Run "docker-compose build" in your terminal from the directory that is 1 up from the InfoVis-Framework-2021 directory
4) Run "docker-compose up" to start the docker container you just build
5) Navigate to localhost:5000 to access the app

**Note**: in order to get any new changes you make in the app to display in your browser, you will need to stop the app (ctrl+c), rebuild it (step 3) and rerun it (step 4). After some time as you rebuild the app multiple times, it's advisable to clean up some of the old docker containers by running the command "docker system prune".

---

## Running the app outside Docker container ##


## Requirements ##

See the requirements.txt file
You can automatically install all the requirements by running: pip install -r requirements.txt

## How it works ##

You can get the app to run in your local browser by following the steps below.

### Linux & Mac ###

* The app can be started by running: bash start_app.sh
* The app can then be accessed by navigating to http://127.0.0.1:5000/

### Windows ###

* Type the following in your terminal when using windows CMD: set FLASK_ENV=development **OR** when using windows powershell: $env:FLASK_ENV=development **OR** conda env config vars set FLASK_ENV=development (when using anaconda powershell)
* Followed by: python run.py
* The app can then be accessed by navigating to http://127.0.0.1:5000/

