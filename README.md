# JerseyStrongSchedules
Program that uses webscraping to pull the schedules of Jersey Strong gyms

To run, make sure you have the following packages (all available through pip installations)


requests

pandas

bs4

selenium

lxml

gspread

oauth2client

gspread_dataframe


Then, you ***must*** create a Google Spreadsheet called *Jersey Strong Schedules*, if you choose a different name, you must replace the code on line 28 with what ever you called it.
Next, you have to create a project in the Google Cloud Platform. Call the project anything you like, and once it's all setup, head to the Google APIs Console. Enable the Google Drive API and the Google Sheets API. In the Google Drive API, click the Create Credentials button, and use the following answers for the questions

Which API are you using? **Google Drive API**

Where will you be calling the API from? **Web server**

What data will you be accessing? **Application data**

Are you planning to use this API with App Enginer or Compute Engine? **No, I'm not using them**

Hit the 'What credentials do I need?' button


Create a new service account with those credentials, naming it anything you want.

Give it the role "Projects -> Editor" and go to the next page

Hit the '+CREATE KEY' button and download the JSON file


Take this file and throw it into the directory with main.py, ***rename it*** *client_secret.json*

If you do not rename the file correctly, the code will not work.

This file contains sensitive infomation, so do not share it with anyone

Open that file in a text editor and copy the email in the client email field.

On the spreadsheet you created, hit *SHARE* and paste that email into the people field, giving it editing permisions.



Now, you should be able to run main.py, and the Google Sheet you created should be populated with the needed information.
