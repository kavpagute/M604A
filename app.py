import psycopg2
import pandas as pd
import plotly.express as px
from flask import Flask, render_template, request, make_response

app = Flask(__name__)


def db_conn():
    try:
        conn = psycopg2.connect(database="toiletDB", host="localhost", user="postgres", password="Pass@word1",
                                port=5432)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None


def get_handicapped():
    con = db_conn()
    if con:
        try:
            cur = con.cursor()
            cur.execute(
                "select vh.location, vh.hc_true as no_of_toilet, tl.longitude, tl.latitude from vhandicapped as "
                "vh left join tbllocation as tl on vh.location=tl.location order by hc_true desc")
            data = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            cur.close()
            con.close()
            df_handicapped = pd.DataFrame(data, columns=column_names)
            return df_handicapped
        except psycopg2.Error as e:
            print(f"Error fetching data: {e}")
    return []


@app.route("/")
@app.route("/home")
def home_page():
    #toilet_data = get_data()
    return render_template("home.html")


@app.route("/handicapped")
def data_handicapped():
    df_handicapped = get_handicapped()
    location_list = df_handicapped['location'].tolist()
    ishandicapped_list = df_handicapped['no_of_toilet'].tolist()
    fig = px.scatter_mapbox(df_handicapped,
                            lat='latitude',
                            lon='longitude',
                            zoom=10,
                            width=1000,
                            height=500,
                            text='location',
                            color='location',
                            size='no_of_toilet',
                            center={'lat': 52.522, 'lon': 13.4004})
    fig.update_layout(mapbox_style='open-street-map', margin={"r": 0, "t": 0, "l": 0, "b": 0})
    div = fig.to_html(full_html=False)

    return render_template('handicapped_page.html', labels=location_list,
                           ishandicapped=ishandicapped_list, div_map=div)


def get_freetoilet():
    con = db_conn()
    if con:
        try:
            cur = con.cursor()
            cur.execute(
                "SELECT vf.location, vf.free_toilet, tl.longitude, tl.latitude FROM public.vfreetoilet as vf left join "
                "tbllocation as tl on vf.location=tl.location order by free_toilet desc, location asc")
            data = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            cur.close()
            con.close()
            df_freetoilet = pd.DataFrame(data, columns=column_names)
            return df_freetoilet
        except psycopg2.Error as e:
            print(f"Error fetching data: {e}")
    return []


@app.route("/freetoilet")
def data_freetoilet():
    data = get_freetoilet()
    location_list = data['location'].tolist()
    no_free_toilet = data['free_toilet'].tolist()

    fig = px.scatter_mapbox(data,
                            lat='latitude',
                            lon='longitude',
                            zoom=10,
                            width=1000,
                            height=500,
                            text='location',
                            color='location',
                            size='free_toilet',
                            center={'lat': 52.522, 'lon': 13.4004})
    fig.update_layout(mapbox_style='open-street-map', margin={"r": 0, "t": 0, "l": 0, "b": 0})
    div = fig.to_html(full_html=False)

    return render_template('free_toilet.html', labels=location_list, no_free_toilet=no_free_toilet, div_map=div)


def get_open24hours():
    con = db_conn()
    if con:
        try:
            cur = con.cursor()
            cur.execute(
                "SELECT tl.location, v.open24hours, tl.longitude, tl.latitude FROM public.visopen24hours as v "
                "left join tbllocation as tl on v.location=tl.location order by open24hours desc")
            data = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            cur.close()
            con.close()
            df_open24hours = pd.DataFrame(data, columns=column_names)
            return df_open24hours
        except psycopg2.Error as e:
            print(f"Error fetching data: {e}")
    return []


@app.route("/open24hours")
def data_open24hours():
    data = get_open24hours()
    location_list = data['location'].tolist()
    open24hours = data['open24hours'].tolist()
    fig = px.scatter_mapbox(data,
                            lat='latitude',
                            lon='longitude',
                            zoom=10,
                            width=1000,
                            height=500,
                            text='location',
                            color='location',
                            size='open24hours',
                            center={'lat': 52.522, 'lon': 13.4004})
    fig.update_layout(mapbox_style='open-street-map', margin={"r": 0, "t": 0, "l": 0, "b": 0})
    div = fig.to_html(full_html=False)
    return render_template('open24hours.html', labels=location_list, dataopen24hours=open24hours, div_map=div)


def getsummaryhandicapped():
    con = db_conn()
    if con:
        try:
            cur = con.cursor()
            cur.execute("SELECT * from vhandicappedtop10")
            data = cur.fetchall()
            return data
        except psycopg2.Error as e:
            print(f"Error fetching data: {e}")
    return []


def getsummaryfree():
    con = db_conn()
    if con:
        try:
            cur = con.cursor()
            cur.execute("SELECT * from vfreetop10")
            data = cur.fetchall()
            return data
        except psycopg2.Error as e:
            print(f"Error fetching data: {e}")
    return []

def getsummaryisopen():
    con = db_conn()
    if con:
        try:
            cur = con.cursor()
            cur.execute("SELECT * from visopentop10")
            data = cur.fetchall()
            return data
        except psycopg2.Error as e:
            print(f"Error fetching data: {e}")
    return []

def getsummaryhasurinal():
    con = db_conn()
    if con:
        try:
            cur = con.cursor()
            cur.execute("SELECT * from vhasurinaltop10")
            data = cur.fetchall()
            return data
        except psycopg2.Error as e:
            print(f"Error fetching data: {e}")
    return []

def getsummaryhaschangingtable():
    con = db_conn()
    if con:
        try:
            cur = con.cursor()
            cur.execute("SELECT * from vhaschangingtabletop10")
            data = cur.fetchall()
            return data
        except psycopg2.Error as e:
            print(f"Error fetching data: {e}")
    return []

@app.route("/summary", methods=["GET", "POST"])
def data_summary():
    if request.method == "GET":
        return render_template("summary.html")
    else:
        choice = request.form.get("choice")
        if choice == "Hand":
            data = getsummaryhandicapped()
            columnhead = "Handicapped Friendly"
        if choice == "Free":
            data = getsummaryfree()
            columnhead = "Free"
        if choice == "Open":
            data = getsummaryisopen()
            columnhead = "Open for 24 hours"
        if choice == "HasUrinal":
            data = getsummaryhasurinal()
            columnhead = "Has Urinal"
        if choice == "HasChangingTable":
            data = getsummaryhaschangingtable()
            columnhead = "Has Changing Table"

        return render_template('summary.html', data=data, columnhead=columnhead, ch=choice)


if __name__ == "__main__":
    app.run(debug=True)
