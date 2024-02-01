# Babies Action Tracker
Small project to have traceability on actions that a baby does :)

## How to run this project

*Pre-requirement*: You have created a conda environment in your machine by using the yml generated with condas (by running `conda env export > babies_action_tracker.yml`

1. This project has 2 parts: The backend & the mobile app. 
1.1 The backend is built using [Flask](https://flask.palletsprojects.com/en/3.0.x/). In order to run the backend, just move to the backend directory and run `python action_tracker.py`. *Note:* The backend has harcoded my local ip. 
1.2 The mobile app is built using [Kivy](https://kivy.org/) and [buildozer](https://buildozer.readthedocs.io/en/latest/). You can run the the mobile app in your machine by moving to the mobile's directory and running `python main.py`.
1.2.1. In order to build the APK for android, you need to run from the mobile directory `buildozer android clean && buildozer android debug`. Once finished, the apk will be located under the bin folder.
1.2.2. In order to build the app for IOS, you need to ....
