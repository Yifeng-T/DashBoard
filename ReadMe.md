Made By Yifeng Tang  
[GitHub](https://github.com/Yifeng-T/DashBoard) Page


# HW4: Dash Board Visulization
## Background
The National Center for Science and Engineering Statistics [NCSES](https://github.com/Yifeng-T/DashBoard) has tons of interesting data sets. Some of the tables from present detailed data on the demographic characteristics, educational history, sources of financial support, and postgraduation plans of doctorate recipients. In this dashboard application, the goal is to analyze and visulize the data realted to *Science and Engineering PhDs awarded in the US*. The application shows details about the data set named "Doctorate-granting institutions, by state or location and major science and engineering fields of study: 2017". Since there are messy headers in the original xlsx file, I have made some changes to the data set. You can access the xlsx file used in the dash board [PHDofEng&Sci](https://github.com/Yifeng-T/DashBoard/blob/main/PHDofEng%26Sci.xlsx).

Click [HERE](https://phd-granting-yifeng-analysis.herokuapp.com/) to open the dash board.  


## Environment
Users could run the dash board on their local machines. You could find the code to build the application [HERE](https://github.com/Yifeng-T/DashBoard/blob/main/app.py). 

==============  
The following are required packages and the versions to run the dashboard:   
dash==2.0.0  
pandas==1.2.2 
numpy==1.20.1  
plotly==5.3.1  
dash_bootstrap_components==0.13.1   

===============  
Make sure dowanload the appropriate packages before runing the application.    
To successfully run the application on locals, you may need to create a virtual environment for this application. You could use [Docker](https://www.docker.com/) to achive that. 

## Features Introduction
The dash board have three parts:  
**OVERVIE OF GRANTING DOCTORS BY STATES**,   
**OVERVIEW OF GRADING DOCTORS BY INSTITUTES AND MAJORS**,   
**OVERVIEW OF GRADING DOCTORS BY FACULTY**

**In the first states part:**  
I created a Choropleth map of US. Users could easily observe the number of fresh graduated PhDs major in sience and engineering by states.   
<br>
![graph3.gif](https://i.loli.net/2021/10/23/mvaoTZtQROc1s4A.gif)  

<br>


**In the second part, there are four plots.**  
The first one is a histogram to show the distribution of number of graduated fresh PhDs in different majors. 
<br>  

![graph4.gif](https://i.loli.net/2021/10/23/4FfW7zoctevYpXu.gif)  

<br>  

The second one is histogram to show the number of fresh PhDs major in different majors in the selected institution. There is a drop-down list on the top of the histogram. Users could either select the school in the list or type the key words of names to find the school.  
![graph5.gif](https://i.loli.net/2021/10/23/ow58lWZfvh1CH2A.gif)  
<br>  

The third and forth include two plots, a pie chart and a stacked histogram. Users could select as many schools and majors as possible to see the ditributions. In the pie chart, users could observe the distributions of graduated PhDs from selected school by selected majors. While in the histogram, users could observe the distribution of number of graduated PhDs by majors in selected schools. The different colors in each bar represent selected majors, and each bar represents one selected school. 
![graph6.gif](https://i.loli.net/2021/10/23/Fs527net9K1ABMg.gif)
<br>  
<br>  

**In the third part**   
There are two histograms to show number of graduated students by majors. One plot is for students gradyated in science field, and anotherone is for engineering field. 
![graph7.gif](https://i.loli.net/2021/10/23/ReG4LIwDamu1783.gif)
<br> 

## Deploy the Dashboard on public web
If you want to deploy your dash board on a public web so that you could share it with  your friends, you could use [Heroku](https://dashboard.heroku.com/apps) to achieve that.   
Before you get started, make sure you’ve installed the Heroku command-line interface [CLI](https://devcenter.heroku.com/articles/heroku-cli) and [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). You can verify that both exist in your system by running these commands at a command prompt (Windows) or at a terminal (macOS, Linux):
```Shell
$ git --version

$ geroku --version
```
The output may change a bit depending on your operating system and the version you have installed, but you shouldn’t get an error.  

When you finished preparation work, we could start to deploy your dash board.
First, please define a variable named server in the code, just below your initialization of the app: (For my dash, I have already defined the server variables on line 162)
```python
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
```
This addition is necessary to run your app using a WSGI server. It’s not advisable to use Flask’s built-in server in production since it won’t able to handle much traffic.  
<br>
Next, in the project’s root directory, create a file called runtime.txt where you’ll specify a Python version for your Heroku app, for example:
```text
python-3.9.1
```
When you deploy your app, Heroku will automatically detect that it’s a Python application and will use the correct buildpack. If you also provide a runtime.txt, then it’ll pin down the Python version that your app will use.

Next, create a requirements.txt file in the project’s root directory where you’ll copy the libraries required to set up your Dash application on a web server. For my application, you need add the following information:  
```text
dash==2.0.0
pandas==1.2.2
gunicorn
numpy==1.20.1
plotly==5.3.1
dash_bootstrap_components==0.13.1
```
dash_bootstrap_components==0.13.1 is a package to read in xlsx file

Then, create a file named Procfile with the following content:
```
web: gunicorn app:server
```
Where app is the name of your dash board py file.   
<br> 

Finally, type the following commands in the cmd: 
```bash
$ git init
$ git add .

$ git commit -m "add application to web"

$ heroku create AppName
git push heroku master
heroku ps:scale web = 1
```
When it set up, you can access the web to share it with your friends. To access your app, copy https://AppName.herokuapp.com/ in your browser and replace AppName with the name you defined in the previous step.

====End



