import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
import datetime
import os
from dotenv import load_dotenv

# Load the path to the database.
load_dotenv()
DB_PATH = os.getenv("PATH_TO_DB")


def refresh_db():
    # Read the weight data. If no database is found, return a blank dataframe.
    try:
        db_table = "weights"
        with create_engine("sqlite:///" + DB_PATH).connect() as db_engine:
            df = pd.read_sql(db_table, con = db_engine)
            df.set_index("id", inplace = True)
    except:
        df = None
    
    return df


def build_layout():

    # Pull in the data.
    wt_data = refresh_db()
    
    if wt_data is not None:    
        # Generate the plot
        axis_labels = {"datetime" : "Date & Time Logged",
                   "weight" : "Weight (pounds)",
                   "person" : "Person"}
        plot = px.scatter(wt_data, x="datetime", y="weight", color="person",
                       labels = axis_labels)
        plot.update_traces(overwrite=True, mode="lines+markers")
        

        # Assemble the layout
        kids = []
        kids.append(html.H1(children='Chonky'))
        kids.append(
            html.Div(children="A simple weight-monitoring dashboard for hungry people.")
            )
        kids.append(
            dcc.Graph(
                id='weight-graph',
                figure=plot
                )
            )
        
        return html.Div(kids)
    
    else:
        return html.Div("No data in the database yet. Try logging some data in Discord.")



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = build_layout
app.title = "Chonky"

if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")
