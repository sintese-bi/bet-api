from urllib.parse import quote_plus
import datetime
from flask import Flask, json, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import psycopg2 as pg
import pandas as pd
from flask import Flask
from flask_caching import Cache
import re
from datetime import datetime, timedelta

db_password = pwrd_env
db_ip = db_env
db_password_encoded = quote_plus(db_password)


# Atualize a string de conexão com o banco de dados substituindo a senha codificada
#DB_CONFIG = string env
#DB_CONFIG = f"postgresql://postgres:{db_password_encoded}@134.209.223.235/comercial_BI"

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.config["DEBUG"] = True
app.config['ENV'] = 'production'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG
app.config['SQLALCHEMY_POOL_SIZE'] = 200
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 10
app.config['TIMEOUT'] = 300
db = SQLAlchemy(app)
CORS(app)

VERSION = "v2"





def get_games(liga):
    connection =connectionDataBase()
    cursor=connection.cursor()
    GAMES_Q = f'''select distinct game from {liga}_games_result'''
    query = cursor.execute(GAMES_Q)
    GAMES = cursor.fetchall()
    lista = [value[0] for value in GAMES]
    return lista

def create_data(liga,game):
    connection =connectionDataBase()
    cursor=connection.cursor()
    dfQ = f'''select distinct * from {liga}_games_result where game='{game}' '''
    query = cursor.execute(dfQ)
    GAMES = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    df_data=pd.DataFrame(GAMES,columns=column_names)
    try:
        under25=round(df_data['r_odd_less25'].value_counts()[1]*100/df_data['r_odd_less25'].value_counts().sum(),2)
    except:
        under25=0
    try:
        over25=round(df_data['r_odd_over25'].value_counts()[1]*100/df_data['r_odd_over25'].value_counts().sum(),2)
    except:
        over25=0
    try:
        over35=round(df_data['r_odd_over35'].value_counts()[1]*100/df_data['r_odd_over35'].value_counts().sum(),2)
    except:
        over35=0
    try:
        home=round(df_data['r_odd_home'].value_counts()[1]*100/df_data['r_odd_home'].value_counts().sum(),2)
    except:
        home=0
    try:
        vis=round(df_data['r_odd_vis'].value_counts()[1]*100/df_data['r_odd_vis'].value_counts().sum(),2)
    except:
        vis=0
    return df_data,under25,over25,over35,home,vis


def create_LIGA(liga):
    connection =connectionDataBase()
    cursor=connection.cursor()
    dfQ = f'''select distinct * from {liga}_games_result'''
    query = cursor.execute(dfQ)
    GAMES = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    df_data=pd.DataFrame(GAMES,columns=column_names)
    try:
        under25=round(df_data['r_odd_less25'].value_counts()[1]*100/df_data['r_odd_less25'].value_counts().sum(),2)
    except:
        under25=0
    try:
        over25=round(df_data['r_odd_over25'].value_counts()[1]*100/df_data['r_odd_over25'].value_counts().sum(),2)
    except:
        over25=0
    try:
        over35=round(df_data['r_odd_over35'].value_counts()[1]*100/df_data['r_odd_over35'].value_counts().sum(),2)
    except:
        over35=0
    try:
        home=round(df_data['r_odd_home'].value_counts()[1]*100/df_data['r_odd_home'].value_counts().sum(),2)
    except:
        home=0
    try:
        vis=round(df_data['r_odd_vis'].value_counts()[1]*100/df_data['r_odd_vis'].value_counts().sum(),2)
    except:
        vis=0
    return under25,over25,over35,home,vis





@app.route(f'/{VERSION}/league', methods=['GET'])
def league():
    league_ = request.args.get('league')

    list_games = get_games(league_)


    json_data = {"games":list_games}


    return json.dumps(json_data,indent=4)





@app.route(f'/{VERSION}/infogames', methods=['POST'])
def infogames():
    data = request.get_json() 
   
    response = json.loads(request.data)
    league= response.get("liga")
    game = response.get("game")

    df,under25,over25,over35,home,vis=create_data(league,game)

    final_dict = {
        'tableData':df.to_dict(orient='records'),
        'under25':str(under25),
        'over25':str(over25),
        'over35':str(over35),
        'home':str(home),
        'vis':str(vis)
    }
    return json.dumps(final_dict,indent=4)
    


@app.route(f'/{VERSION}/infoleague', methods=['GET'])
def infoleague():
    league_ = request.args.get('infoleague')
   

    under25,over25,over35,home,vis=create_LIGA(league_)

    final_dict = {
        'under25':str(under25),
        'over25':str(over25),
        'over35':str(over35),
        'home':str(home),
        'vis':str(vis)
    }
    

    return json.dumps(final_dict,indent=4)
    

#Roda o projeto
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True, processes=1)
    # app.run(host="104.131.163.240", port=8080)
