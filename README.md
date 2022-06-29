# ML_Football-Prediction
This is an end-to-end Machine Learning Project from Defining problem to building an app working on the ML model.

This model is for predicting the winner of a football match.(Binary Classification problem as 0 for loss/draw and 1 for win)

Data is collected by web-scrapping this football-stats website. (https://fbref.com/en)

After EDA, and deploying various models, precision of the model is increased by using rolling average method for some feature.
App is created which displays the same results of the model.

Description of files in this repository:

1.FootballPredictions_Notebook.ipynb -Main Jupyter notebook for this project. All processes of data loading,cleaning and model deployment are done in this.

2.app.py -Application file for this project. App is build using Flask and basic html,css.

3.templates/index.html -HTML file for app. (I used inline-css for little styling, you can add static/styles.css file as well for styling)

4.templates/hometeam.html -HTML file for app 2nd page.




