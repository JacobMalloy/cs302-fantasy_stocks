#Jacob Malloy and Taegun Harshbarger
#api.py
#implement a flask api in python to be the backend for the project


#lots of dependencies in the normal style of python
from flask.wrappers import Request
import matplotlib.pyplot as plt
import numpy as np
import io
import random
from flask import Flask
import flask
from flask import Response
from flask_cors import CORS
import pandas as pd
import json
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


app = Flask(__name__)#create a flask app for the program
CORS(app)#make the app cross origin compatible

data = dict()#declare data to be used
players = dict()#declare the player list

def setup():
    global players#these are two variables that are global
    global data

    csv_files=dict()#local variable for the names of csv files that are not needed outside the setup
    data_frames=dict()#dataframes used to extract data

    #gets all of the csv files.
    for year in range(1999,2021):
        for week in range(1,18):
            csv_files[f"{year}-{week:02}"]=(f"./data/{year}/week{week}.csv")
    #declare the dataframes pulling the data from the csv files
    for i in csv_files:
        data_frames[i]=(pd.read_csv(csv_files[i])[["Player","PPRFantasyPoints","Pos","Tm"]])

    #setup data and player data structure
    #get player position and team into the players object
    for i in data_frames:
        data[i]=dict()
        for index, row in data_frames[i].iterrows():
            s = row["Player"]
            if s not in players:
                players[s] = dict()
                players[s]["start"]=i.split("-")[0]
                players[s]["pos"]=str(row["Pos"])
            players[s]["end"]=i.split("-")[0]
            p = row["PPRFantasyPoints"]
            data[i][s]=p
    players={key: value for key, value in sorted(players.items(), key=lambda item: item[0])}#sort the players before returning them



@app.route("/get_players/", methods=['GET', 'POST'])
def get_players():#get the names of players and return a json file of their name...
    json_object=json.dumps(players, indent=4)
    print(json_object)
    return json_object

@app.route('/testing/', methods=['GET', 'POST'])
def welcome():
    return pd.read_csv("./data/2019/week6.csv").to_json()

@app.route('/plot.png/')
def plot_png():
    fig = create_figure(flask.request.args.get("player").replace("%20"," "))#get the value from the get request and change %20 to spaces
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    plt.close(fig)#cleanup memory in a garbage collected language?
    return Response(output.getvalue(), mimetype='image/png')#output the images

def create_figure(player):

    playerData=dict()
    score =0.0
    upto="2020-17"#this is the latest data we have
    for i in data:
        if i==upto:
            break
        score*=.8
        if player in data[i]:
            score += data[i][player]
        if score<0:
            score =0
        playerData[i]=score
    lists = sorted(playerData.items()) # sorted by key, return a list of tuples


    fig = plt.figure(figsize=(12, 6))

    ax = fig.add_subplot(111)


    x, y = zip(*lists) # unpack a list of pairs into two tuples
    x = list(x)
    x = [val.split("-")[0] if val.split("-")[1]=="01" else val for val in x]#change the first weeks to not have the `-week`part
    plt.plot(x, y)
    plt.ylim(0,None);

    ax.plot(x,y)

    fig.canvas.draw()
    ax.set_xticks(np.arange(0, len(x)+1, 17))
    #ax.set_xticklabels([x.get_text().split("-")[0] for x in ax.get_xticklabels()] )
    plt.xticks(rotation = 45) # Rotates X-Axis Ticks by 45-degrees

    return fig


if __name__ == '__main__':
    setup()#run the setup
    app.run(host='0.0.0.0', port=5555)#run on 5555 becuase it is an open port that can be easily used
