from flask import Flask
from flask import Response
from flask_cors import CORS
import pandas as pd
import json
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)
CORS(app)

csv_files=dict()
data_frames=dict()
data = dict()
players = dict()

def setup():
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
                players[s]["Pos"]=row["Pos"]
            players[s]["end"]=i.split("-")[0]
            p = row["PPRFantasyPoints"]
            data[i][s]=p

    

@app.route("/get_players/", methods=['GET', 'POST'])
def get_players():#get the names of players and return a json file of their name...   
    json_object=json.dumps(players, indent=4)
    print(json_object)
    return json_object

@app.route('/testing/', methods=['GET', 'POST'])
def welcome():
    return pd.read_csv("./data/2019/week6.csv").to_json()
    
@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_graph():
    fig = Figure()

if __name__ == '__main__':
    setup()
    app.run(host='0.0.0.0', port=5555)
