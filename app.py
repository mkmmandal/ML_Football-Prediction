#This app is for Football matches prediction
#User select matchweek  and team and app predicts whether their team or opponent team going to win
from flask import Flask ,render_template,request
import pickle
import pandas as pd
app = Flask(__name__)
#football test data
footballdatadf=pickle.load(open('footballdata.pkl','rb'))

weekdaylist=[]
#fetching matchweek from  the test data
for i in footballdatadf.Round.unique():
    weekdaylist.append(i)
weekdaylist=sorted(weekdaylist)
#These are the columns we need for prediction
columns=['venue_code','opp_code','hour','day_code','GF_rolling','GA_rolling','Sh_rolling','SoT_rolling','Dist_rolling','FK_rolling','PK_rolling','PKatt_rolling']

#This is our trained model we will predict using this model
rfModel=pickle.load(open('rfmodel.pkl','rb'))

#opponent team name is different for some teams,making it correct
class MissingDict(dict):
    __missing__ = lambda self, key: key

map_values = {"Brighton and Hove Albion": "Brighton", "Manchester United": "Manchester Utd", "Newcastle United": "Newcastle Utd", "Tottenham Hotspur": "Tottenham", "West Ham United": "West Ham", "Wolverhampton Wanderers": "Wolves"} 
mapping = MissingDict(**map_values)

#Home page to chose matchweek
@app.route("/",methods=['GET','POST'])
def home_page():
    return render_template('index.html',weekdaylist=weekdaylist)

#Team selection/Prediction page
@app.route("/team",methods=['GET','POST'])
def hometeam_page():
    prediction=''
    match=''
    teams=[]
    team=''
    week=''
    if request.method=='POST':
        week=(request.form['Week'])
        team=request.form['Team']
    #First call to this page loading team data from the selected matchweek
    #User will select team from this list only
    if team == 'ABC':
        teamdata=footballdatadf[footballdatadf['Round']==week]
        for i in teamdata.Team.unique():
            teams.append(i)
    #Second call to this page after selecting the team for prediction
    else:
        winput=footballdatadf[footballdatadf.Round==week]
        input=winput[winput.Team==team]
        #Getting both sides of the game and showing only 1 result for both the cases
        #In some cases results are different, so choosing only 1 result which is at lower index pos
        opt=input['Team'].map(mapping)
        optindex=winput[winput.Opponent==opt.values[0]].index[0]
        inputindex=input.index[0]
        if optindex>inputindex:
            input=winput.loc[inputindex]
        else:
            input=winput.loc[optindex]
        minput=input[columns]
        minput=minput.to_numpy().reshape(1,-1)
        pred_prob=rfModel.predict_proba(minput)
        #Predictions based on probability
        print(pred_prob[0][1])
        if pred_prob[0][1]>=0.55:
            prediction=input.Team+' will WIN'
        elif pred_prob[0][1]<0.55 and pred_prob[0][1]>0.45:
            prediction='DRAW'
        elif pred_prob[0][1]<=0.45:
            prediction=input.Opponent+' will WIN'
        match=input.Team +' vs. '+input.Opponent

    return render_template('hometeam.html',teams=teams,week=week,prediction=prediction,match=match)

if __name__=="__main__":
    app.run(debug=True)


