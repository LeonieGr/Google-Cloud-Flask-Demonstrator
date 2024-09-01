## Instructions for deploying a Flask application with Google Cloud

## Prerequisites

Before we start deploying, make sure you meet the following prerequisites:

1. **Google Cloud account**: Make sure you have a Google Cloud account. If you don't have one yet, register on [Google Cloud](https://cloud.google.com/) and take advantage of the free trial period.
2. **Python**: Make sure Python is installed. Flask requires Python 3.7 or higher.
3. **Google Cloud SDK**: Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install).
4. **Flask application**: An already working Flask application.

#1 Create the Flask application

Start by creating a Flask application. It is important to strictly separate the frontend and backend so that the frontend can later be made available online independently of the backend.

### 1.1 Project structure

Structure your application as follows:

```plaintext
my-flask-app/
├── app.py # Main file of the Flask application
├── templates/ # HTML files for the frontend
│ └── index.html
├── static/ # Static files such as CSS, JS, images
│ ├─── styles.css
│ └── script.js
├── config.js # Configuration file for the frontend
├── requirements.txt # List of Python dependencies
└── app.yaml # Configuration file for Google App Engine 
```

### 1.2 Contents of app.py
The actual Flask application is defined in app.py:

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
```

### 1.3 requirements.txt
Create a requirements.txt to manage the dependencies of your Flask app:

```plaintext
Flask==2.1.1
gunicorn==20.1.0
```
### 1.4 app.yaml
The app.yaml file is used to configure the Google App Engine:

```yaml
runtime: python39
entrypoint: gunicorn -b :$PORT app:app

#optional
handlers:
  - url: /static
    static_dir: static

  - url: /.*
    script: auto
```
This configuration specifies that your application will run under the Python 3.9 runtime environment and how static files should be handled. It also defines the entrypoint.

## 2 Set up Google Cloud

### 2.1 Sign in to Google Cloud
Log in to your Google Cloud account and create a new project. This project will be used to host your Flask application.

### 2.2 Install Google Cloud SDK
If you have not yet installed the Google Cloud SDK, download it and install it according to the instructions on the Google Cloud SDK installation page.

### 2.3 Setting up a payment account
Although Google Cloud offers a free trial period, you still need to set up a payment account. This serves as security in case your usage exceeds the free period.

### 2.4 Setting access permissions
Make sure you have the right access permissions to create and manage projects. You can check this under “IAM & Administration” in the Google Cloud Console.

## 3 Deployment of the Flask application

### 3.1 Authentication
Authenticate yourself with your Google Cloud account:

```bash
gcloud auth login
```
### 3.2 Select project
Select the project in which the application is to be deployed

```bash
gcloud config set project [YOUR PROJECT ID]
```
### 3.3 Initialize App Engine
Initialize the App Engine in your project:

```bash
gcloud app create --region=[YOUR-REGION]
```
Select a region that is geographically close to your users to minimize latency.

### 3.4 Deployment
To deploy your application to Google App Engine, execute the following command:

```bash
gcloud app deploy
```
This command takes the app.yaml file and deploys the application to App Engine. The deployment process may take a few minutes.

### 3.5 Display application
Once the deployment has been successfully completed, you can display your application in the browser:



```bash
gcloud app browse
```
This command opens the URL of your deployed application in the default browser.

### 3.6 Access to log information

If unexpected problems occur during the operation of your application, you can retrieve detailed log information to identify the cause:

```bash
gcloud app logs tail -s default
```

## 4. run the backend via LocalTunnel

If you want to run the backend locally on a test basis, you can use LocalTunnel to make it accessible to the Internet.

### 4.1 What is LocalTunnel?
LocalTunnel is a simple tool that allows you to make a local server accessible to the internet. It creates a secure tunnel from your local machine to a publicly accessible URL, which you can then use to test your application externally without fully deploying it. This is particularly useful for testing webhooks, APIs or sharing your local application with others without the need for a full production environment.

### 4.2 Installing LocalTunnel
Install [LocalTunnel](https://pypi.org/project/py-localtunnel/):

```bash
pip3 install py-localtunnel
```
### 4.3 Starting LocalTunnel
Start LocalTunnel and forward the port of your Flask application:

```bash
plt --port 5000
```
LocalTunnel generates a public URL that points to your local server. You can then use this to test the backend.