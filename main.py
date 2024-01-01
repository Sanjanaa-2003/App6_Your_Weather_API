from flask import Flask, render_template
import pandas as pd


app=Flask(__name__)

stations= pd.read_csv("data_small/stations.txt",skiprows=17)
stations = stations[["STAID","STANAME                                 "]]
@app.route("/")         #calls the home function
def home():
    return render_template("home.html",data=stations.to_html())     #when home is called returns content of tutoial.html

@app.route("/api/v1/<station>/<date>")
def about(station,date):
    filename = "data_small/TG_STAID"+str(station).zfill(6)+".txt"
    df = pd.read_csv(filename,skiprows=20, parse_dates=['    DATE'])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() /10
    return {"station":station,
            "date":date,
            "temperature":temperature}

@app.route("/api/v1/<station>")

def all_data(station):
    filename="data_small/TG_STAID"+str(station).zfill(6)+".txt"
    df=pd.read_csv(filename,skiprows=20,parse_dates=['    DATE'])
    result = df.to_dict(orient="records")
    return result

@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station,year):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    df['    DATE'] = df['    DATE'].astype(str)
    result = df[df['    DATE'].str.startswith(str(year))].to_dict(orient="records")
    return result
if __name__ == "__main__":      #runs this file only when it is executed directly and not when it is imported
    app.run(debug=True)

#
# http://127.0.0.1:5000/api/v1/yearly/10/1988     ==  Paste this in the window that opens to see everything in that particular year
#Run this file and a link will be in console --  it'll open in jupyter notebook  --  paste the example url
# from that page in search bar and a dictionary will be printed out
















# TYPE: http://127.0.0.1:5000/about/ in edge browser so that file opens
# http://127.0.0.1:5000/home