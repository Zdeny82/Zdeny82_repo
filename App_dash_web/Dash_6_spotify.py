
import dash
import plotly.express as px
from dash import dcc 
from dash import html
from dash.dependencies import Output, Input, State
import pandas as pd    
 
 

spoty_df = pd.read_csv('App_dash_web\spotify_top100.csv')
spoty_df = spoty_df.dropna()

numeric_cols = spoty_df.select_dtypes(include=['float', 'int']).columns
spoty_df[numeric_cols] = spoty_df[numeric_cols].round(0).astype(int)
spoty_df[numeric_cols]

spoty_df_list = list(spoty_df['top year'].unique())
marks_labels = {int(x) : str(x) for x in spoty_df_list}
marks_labels
spoty_df_list

app = dash.Dash(__name__)

app.layout = html.Div(children=
                      [
                        html.H1(id='h1', children='Spotify top 100'),
                        dcc.Slider(id='slider',
                                     value=2010,
                                     step = 1,
                                     marks=marks_labels),
                                                
                        dcc.Graph(id='graph', 
                                  figure=px.bar(data_frame=spoty_df,
                                                x = list(spoty_df[['bpm', 'top year']].groupby('top year').agg('mean').index),
                                                y = list(spoty_df[['bpm', 'top year']].groupby('top year').agg('mean').values.squeeze()),
                                                labels=list(spoty_df[['bpm', 'top year']].groupby('top year').agg('mean').values.squeeze()))),

                        dcc.Dropdown(id='drop', 
                                     value= list(spoty_df[['nrgy', 'dB', 'live', 'val', 'dnce']].columns)[0],
                                     options= list(spoty_df[['nrgy', 'dB', 'live', 'val', 'dnce']].columns),
                                     placeholder='Select a category'

                                     )                    
                         
                      ])

@app.callback(
        Output(component_id='graph', component_property='figure'),
        Input(component_id='slider', component_property='value'),
        State(component_id='drop', component_property= 'value')
)

def update_function(slider_value, dropd_value):
    
    # Debugging: Zobrazení vstupních hodnot
    # print(f"Slider Value: {slider_value}")
    # print(f"Dropdown Value: {dropd_value}")
    
    numeric_columns = list(spoty_df[['nrgy', 'dB', 'live', 'val', 'dnce']].columns)

    
    filtered_df = spoty_df[spoty_df['top year'] == int(slider_value)]

    figure = px.bar(data_frame=filtered_df.head(15),
                    x = 'title', 
                    y = 'nrgy' if dropd_value == numeric_columns[0] else dropd_value,
                    height=800)
    
    layout_updates = dict(
        xaxis=dict(
        tickangle=45,
        automargin=True,
        categoryorder='total descending'))
    
    figure.update_layout(**layout_updates)
    
    return figure
    
if __name__ == '__main__':
    app.run(host='127.0.0.1', port= 3500, debug=True)





