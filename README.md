# NoseGoes

## Overview
NoseGoes is an application that allows a user to control their web browser using facial gestures and voice commands. The goal is to make it easier for disabled and paraplegic people to use the internet.

Contributors: Sergei Chestakov, Kaelan Mikowicz

#### Accepted facial gestures:
* Scroll (look up and down)
* Switch tabs (look left and right)
Gestures are implemented by comparing the position of the blue dot at the center of the user's face relative to the readjusting box in the middle, and require a change in tilt/pan of > 10 degrees.

#### Accepted voice commands:
* Open new tabs - "Open tab"
* Navigate to a web page - "Go to *website*" (Appends .com)
* Make a Google search - "Search *query*"
* Navigate to previous page in history - "Go back"
* Navigate to next page in history - "Go Forward"

## Installation
Make sure you are using Python 3.6 or higher

#### Step 1: Clone the repo
```bash
git clone https://github.com/sergeichestakov/NoseGoes.git 
cd NoseGoes
```

#### Step 2: Set up Virtual Environment
```bash
pip3 install virtualenv
virtualenv venv
. venv/bin/activate (MacOS/Linux)
venv\Scripts\activate (Windows)

# Use 'deactivate' to exit virtual environment
```

#### Step 3: Install necessary pip modules
```bash
pip3 install -r requirements.txt
```

#### Step 4: Move geckodriver.log to path
This is the file that Selenium needs to launch Firefox so make sure you have Firefox installed and move geckodriver to a directory in your system path.
To print path you can type:
```bash
echo $PATH
```

## Running
To launch the application simply run
```bash
python3 run.py
```

## To Do
We built the first version of NoseGoes at a 24 hour hackathon, but plan to continue development.

Next Steps include the following in no particular order:
* Refactor code for readability and speed
* Add features including the ability to click on links and interact with the webpage 
* Improve facial gesture implementation and ease of use 
* Replace Google Cloud with other Python modules for using microphone and detecting changes in orientation of the face
* Create an executable for easy download and distribution

Contributions are welcome! Enjoy :blush:

