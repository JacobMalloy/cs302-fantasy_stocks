from flask import Flask
import pandas as pd

app = Flask(__name__)

@app.route('/testing/', methods=['GET', 'POST'])
def welcome():
    return pd.read_csv("./data/2019/week6.csv").to_json()
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)