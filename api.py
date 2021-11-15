from flask import Flask
import pandas as pd
import json

app = Flask(__name__)

csv_files=dict()
data_frames=dict()
data = dict()
players = dict()

class player_data:
    def __init__(self, name, start):
        self.name = name
        self.start = start#starting and ending years
        self.end=start

def setup():
    #gets all of the csv files.
    for year in range(1999,2021):
        for week in range(1,18):
            csv_files[f"{year}-{week:02}"]=(f"./data/{year}/week{week}.csv")
    #declare the dataframes pulling the data from the csv files
    for i in csv_files:
        data_frames[i]=(pd.read_csv(csv_files[i])[["Player","PPRFantasyPoints","Pos"]])

    #setup data and player data structure
    for i in data_frames:
        data[i]=dict()
        for index, row in data_frames[i].iterrows():
            s = row["Player"]
            if s not in players:
                players[s] = dict()
                players[s]["start"]=i.split("-")[0]
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
    

if __name__ == '__main__':
    setup()
    app.run(host='0.0.0.0', port=5555)
