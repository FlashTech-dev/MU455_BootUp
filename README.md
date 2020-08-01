# BootUp Sentiment Analysis App


# Problem Statement
In current scenario, most of the social media platforms can be seen with the proliferation in usage of code mixed text. Code mixed data is an important challenge of natural language processing, as its characteristics widely vary from the traditional structures of standard languages. In such scenario, context aware sentiment analysis of the social media data becomes a challenge. Here comes a need for standard solution which can take feed of Social Media Data that has code mixed language statements. Handle multiple code mixed languages and perform sentiment analysis further. Sentiment analysis should give results such as, "Positive", "Negative" and "Neutral". Language: English, Hindi, Kannada, Bengali, Urdu etc.

# Team
* Karan Wagh
* Dipak Patil
* Tejashree Salvi
* Kaif Tamboli
* Sakshi Chaudhari
* Pratik Temkar

# Installation
* Delete any previously cloned repo. (If any)
	`boot-up`
* Clone the repository.
    `git clone https://github.com/TeamBootUp/boot-up`
* Go to the repository.
	`cd boot-up`
* Create a virtual environment.
	`virtualenv -p "[path to python37.exe]" python3.7`
	See below for instructions.
* Activate virtual environment.
	`python3.7\Scripts\activate`
* Install packages.
	`pip install -r requirements.txt`
* Go to app directory.
    `cd app`
* For Password Reset Functionality, add environment variables:
	`EMAIL_USER: email_address`
	`EMAIL_PASS: email_password`
	Avoid if not using password reset!!
* Migrate DB.
	`python manage.py migrate`
* Run server.
	`python manage.py runserver`
* Visit site at:
	`127.0.0.1:8000`

# Install Python 3.7 and create virtual environment for the same.
* Download Python 3.7 
	`https://www.python.org/ftp/python/3.7.5/python-3.7.5-amd64.exe`
* Install using the installer.
* In the start menu search for Python 3.7. In the option `Python 3.7 (64-bit)` right-click and go to file location. There is a shortcut with the same name `Python 3.7 (64-bit)`. Right-click on it and go to properties. In the properties, copy the value in the `Target` field.
* In the boot-up folder, create virtual environment
	`virtualenv -p [the value copied above] python3.7`
* Activate the virtual environment.
	`python3.7\Scripts\activate`

	