from dash import Dash, dcc, html, dash_table, Input, Output
import base64
import plotly.express as px
import pandas as pd 
 
df = pd.read_csv('All_F1_Races.csv')
df = df[['season','raceName','position','points','results.laps','Full Name','nationality.1']]

app = Dash(__name__)

# Přidání Flask serveru pro Gunicorn
server = app.server

# Načtení obrázku jako base64
def load_image(image_path):
    with open(image_path, "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode()
    return f"data:image/jpeg;base64,{encoded_image}"

image_path = 'foto.png'
encoded_image = load_image(image_path)

app.layout = html.Div(style={'border': '1px solid black', 'padding': '10px', 'width': '99%'}, 
                      children=[
    # titulek
    html.H1(
    "Zdeny's Racing Dashboard",
    style={
        'textAlign': 'center',
        'fontSize': '36px',  # Velikost písma
        'fontFamily': 'Arial, sans-serif',  # Moderní typ písma
        'fontWeight': 'bold',  # Tloušťka písma
        'color': 'grey',  # Barva textu
        'borderRadius': '8px',  # Zakulacené rohy
        'padding': '10px 20px',  # Vnitřní odsazení
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)',  # Stín
        'marginBottom': '20px',  # Odsazení dolů
        'width': '50%',  # Šířka
        'margin': '10px auto',  # Centrované na střed
    }
),

    html.Img(
                src=encoded_image,  # Cesta k souboru obrázku
                style={
                    'width': '200px',  # Šířka obrázku
                    'height': 'auto',  # Automatická výška pro zachování poměru stran
                    'border-radius': '10px',  # Zakulacené rohy
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
                    'display': 'block',
                    'margin': '10px auto'  # Posune obrázek na střed
            
    }
),

    # graf
    dcc.Graph(id='graph', 
            figure=px.bar(data_frame=df, x = 'Full Name', y = 'points')),
    # drop
    dcc.Dropdown(id='drop', 
                value= list(df[['points', 'position', 'results.laps']].columns)[0],
                options= list(df[['points', 'position', 'results.laps']].columns),
                placeholder='Select a category'

),                    

    # tabulka
    dash_table.DataTable(
        id='racing_table',
        columns=[{
            'name': '{}'.format(col),
            'id': '{}'.format(col),
            'deletable': True,
            'renamable': True,
            'hideable': True
        } for col in df.columns],
        data=df.to_dict('records'),
        editable=True,
        export_format='csv',
        export_headers='display',
        style_table={
        'width': '100%',  # Tabulka zabere 100% šířky hlavního divu
        'maxWidth': '100%',  # Omezíme maximální šířku
        'overflowX': 'auto',  # Posuvník, pokud je potřeba
        },
        style_cell={
        'textAlign': 'left',  # Zarovnání textu doleva
        'minWidth': '50px',  # Minimální šířka buňky
        'maxWidth': '100%',  # Maximální šířka buňky
        'whiteSpace': 'normal',  # Přizpůsobení obsahu buňky
    })
])


#callback
@app.callback(
        Output(component_id='graph', component_property='figure'),
        Input(component_id='drop', component_property= 'value')
            )

def update_function(dropd_value):
    
    # Debugging: Zobrazení vstupních hodnot
    # print(f"Slider Value: {slider_value}")
    # print(f"Dropdown Value: {dropd_value}")
            
    figure = px.bar(data_frame=df,
                    x = 'Full Name', 
                    y = dropd_value,
                    height=800)
    
    layout_updates = dict(
        xaxis=dict(
        tickangle=45,
        automargin=True,
        categoryorder='total descending'))
    
    figure.update_layout(**layout_updates)
    
    return figure

# pro lokální testování
# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port= 8050, debug=True)