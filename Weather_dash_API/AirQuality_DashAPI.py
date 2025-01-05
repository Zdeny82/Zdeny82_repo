"""
Tento soubor obsahuje aplikaci Dash pro vizualizaci znečištění ovzduší v České republice.
Obsahuje:
- Mapu znečištění s různými indikátory (PM2.5, PM10, CO, apod.).
- Dynamické sloupce zobrazené podle vybraných ukazatelů.
- Dynamické karty zobrazující informace o vybraných městech.

Závislosti:
- requests, pandas, plotly, dash, dash-bootstrap-components, gunicorn.
"""

# Základní knihovny
import requests
import pandas as pd
import datetime as dt
import base64

# Plotly knihovna
import plotly.express as px

# Dash framework a komponenty
import dash
from dash import html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable


# Lokality (hlavní města krajů ČR)
locations = {
    "Praha": {"latitude": 50.0755, "longitude": 14.4378},
    "Brno": {"latitude": 49.1951, "longitude": 16.6068},
    "Ostrava": {"latitude": 49.8209, "longitude": 18.2625},
    "Plzeň": {"latitude": 49.7384, "longitude": 13.3736},
    "České Budějovice": {"latitude": 48.9757, "longitude": 14.4800},
    "Hradec Králové": {"latitude": 50.2092, "longitude": 15.8328},
    "Olomouc": {"latitude": 49.5955, "longitude": 17.2518},
    "Ústí nad Labem": {"latitude": 50.6611, "longitude": 14.0505},
    "Liberec": {"latitude": 50.7671, "longitude": 15.0562},
    "Karlovy Vary": {"latitude": 50.2310, "longitude": 12.8717},
    "Zlín": {"latitude": 49.2222, "longitude": 17.6644},
    "Pardubice": {"latitude": 50.0370, "longitude": 15.7812},
}

town_list_data = []
for town in locations:
   
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = locations[town] | {"current": ["pm10", "pm2_5", "carbon_monoxide", "carbon_dioxide", "nitrogen_dioxide", "sulphur_dioxide"]}
    response = requests.get(url, params=params)
    

    if response.status_code == 200:
        data = response.json()
        df = pd.json_normalize({'town_name': town}|data) # vytvoří jednořádkový komplet df
        town_list_data.append(df)

    else:
        print(f"Chyba: {response.status_code}, {response.reason}")

# Spojení DataFrame pod sebe
combined_df = pd.concat(town_list_data, ignore_index=True)

combined_df
combined_df['current.time'] = combined_df['current.time'].astype('datetime64[ns]')
df_to_show = combined_df.copy()

# Úprava sloupců

df_to_show.rename(columns={"current.time": "time", 'current.interval': 'interval', 'current.pm10': 'pm10', 'current_units.pm10': 'pm10_u',
                    'current.pm2_5': 'pm2_5', 'current_units.pm2_5': 'pm2_5_u', 'current_units.interval': 'interval_u', 
                    'current.carbon_monoxide':'CO',
                    'current_units.carbon_monoxide': 'carbon_monoxide_u',
                     'current.carbon_dioxide': 'CO2',
                     'current_units.carbon_dioxide' : 'carbon_dioxide_u', 
                     'current.nitrogen_dioxide': 'NO2',
                     'current_units.nitrogen_dioxide' : 'nitrogen_dioxide_u', 
                     'current.sulphur_dioxide':'SO2',
                     'current_units.sulphur_dioxide' : 'sulphur_dioxide_u'
                   }, inplace=True)

df_to_show['date'] = df_to_show['time'].dt.strftime('%D')  # Den
df_to_show['time'] = df_to_show['time'].dt.strftime('%H:%M')  # Hodina:minuta

df_to_show['generationtime_ms'] = df_to_show['generationtime_ms'].round(4)

old_order = df_to_show.columns
new_order = ['town_name', 'latitude', 'longitude', 'elevation', 'date', 'timezone',
       'time', 
       'interval', 'interval_u',
       'pm10', 'pm10_u',
       'pm2_5', 'pm2_5_u',
       'CO','carbon_monoxide_u',
       'CO2','carbon_dioxide_u',
       'NO2','nitrogen_dioxide_u',
       'SO2', 'sulphur_dioxide_u', 
       'generationtime_ms']
df_to_show = df_to_show[new_order]


# Vykreslení mapy
fig = px.scatter_mapbox(
    data_frame=df_to_show,
    
    lat="latitude",
    lon="longitude",
    size="pm2_5", 
    color="pm2_5",
    color_continuous_scale='bluered',  # Barevná škála od modré po červenou  
    hover_name='town_name',
    hover_data={"pm10": True, "pm2_5": True, "latitude": False, "longitude": False},
    title=f"Aktuální znečištění ovzduší v České republice",
    mapbox_style="outdoors",
    zoom=5.8,
    center={"lat": 49.8175, "lon": 15.4730}  # Střed České republiky
)

# Přidání Mapbox tokenu
fig.update_layout(mapbox_accesstoken="pk.eyJ1IjoiemRlbnk4MiIsImEiOiJjbTQyY3Rma2QyamZ0MmxxdG1ubTg4MGVqIn0.FcqTJTyPRFgbHzHNCwFOIQ",
                width=800,  # Šířka plátna
                height=600,  # Výška plátna
                title={"text": "Aktuální znečištění ovzduší v České republice", "x": 0.5}
                )

# Zobrazení mapy
# fig.show()

# Vykreslení barchartu
fig_2 = px.bar(
    data_frame=df_to_show,
    x = 'town_name',
    y = 'pm2_5',
    category_orders = df_to_show.sort_values(by="pm2_5", ascending=False),
    color_discrete_sequence=["#8C705F"],
    hover_name='town_name',
    title=f"Největší města dle znečištění",
    width=800,  # Šířka plátna
    height=550)

fig_2.update_layout(title={"text": "Aktuální znečištění ovzduší v České republice", "x": 0.5})
   
# Načtení obrázku jako base64
def load_image(image_path):
    with open(image_path, "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode()
    return f"data:image/jpeg;base64,{encoded_image}"

image_path = 'foto.png'
encoded_image = load_image(image_path)

# DataFrame ze slovníku

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Přidání Flask serveru pro Gunicorn
server = app.server

# Layout aplikace
app.layout = dbc.Container(
    [   
        # titulek
        dbc.Row(
            dbc.Col([
                html.H1(
                "Zdeny's Dashboard",
                className="mb-4",
                style={
                    'textAlign': 'center',
                    "display": "inline-block",  # Umožňuje inline zarovnání
                    'color': 'grey',  # Barva textu
                    'borderRadius': '8px',  # Zakulacené rohy
                    'padding': '10px 20px',  # Vnitřní odsazení
                    'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)',  # Stín
                    'marginBottom': '20px'  # Odsazení dolů
                    
                    
                }
            ),

            html.Img(
                            src=encoded_image,  # Cesta k souboru obrázku
                            style={
                                'width': '100px',  # Šířka obrázku
                                'height': 'auto',  # Automatická výška pro zachování poměru stran
                                'border-radius': '10px',  # Zakulacené rohy
                                'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
                                'display': 'block'
                                
                            }
            )], 
            
            )
        ),


        # Nadpis
        dbc.Row(
            dbc.Col(html.H1("Aktuální znečištění ovzduší v ČR"), 
                    style={
                        "display": "flex",
                        "justify-content": "center",
                        "align-items": "center"}
                        ),
            className="mb-4",
            style={
                        "display": "flex",
                        "justify-content": "center",
                        "align-items": "center",
                        "height": "100px"  # Nastavení pevné výšky
                    }
        ),
        
        # Hlavní karty
        dbc.Row(
            [
                # Karta Praha
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(f"Praha {df_to_show.loc[df_to_show['town_name'] == 'Praha', 'time'].values.squeeze()}"),
                            dbc.CardBody(
                                [
                                    html.H5(f"PM2.5: {df_to_show.loc[df_to_show['town_name'] == 'Praha', 'pm2_5'].iloc[0]} µg/m³", className="card-title"),
                                    html.P(f"PM10: {df_to_show.loc[df_to_show['town_name'] == 'Praha', 'pm10'].iloc[0]} µg/m³?", className="card-text"),
                                ]
                            ),
                        ],
                        color="#1F0318", inverse=True, style={"height": "100%"}
                    ),
                    width=3,
                ),
                # Karta Brno
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(f"Brno {df_to_show.loc[df_to_show['town_name'] == 'Brno', 'time'].values.squeeze()}"),
                            dbc.CardBody(
                                [
                                    html.H5(f"PM2.5: {df_to_show.loc[df_to_show['town_name'] == 'Brno', 'pm2_5'].iloc[0]} µg/m³", className="card-title"),
                                    html.P(f"PM10: {df_to_show.loc[df_to_show['town_name'] == 'Brno', 'pm10'].iloc[0]} µg/m³", className="card-text"),
                                ]
                            ),
                        ],
                        color="#8C705F", inverse=True, style={"height": "100%"}
                    ),
                    width=3,
                ),
                # Dynamická karta (město z dropdownu)
                dbc.Col(
                    dbc.Card(
                        id="dynamic-card",
                        color="#7F534B", inverse=True, style={"height": "100%"}
                    ),
                    width=3,
                ),
            ],
            style={
                        "display": "flex",
                        "justify-content": "center",
                        "align-items": "center"},
            className="mb-4",
        ),

        # Dropdown pro výběr města
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id="city-dropdown",
                    options=[{"label": city, "value": city} for city in df_to_show['town_name'].values],
                    value="Ostrava",  # Defaultní město
                    placeholder="Vyber třetí město"
                ),
                width=3,
            ),
            style={
                        "display": "flex",
                        "justify-content": "center",
                        "align-items": "center",
                        "height": "100px"  # Nastavení pevné výšky
                    },
            className="mb-4",
        ),

        # Row kontejner pro graf i graf 2
        dbc.Row(
            [
                # Sloupec pro graf
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id="my-graph",
                            figure=fig,
                            responsive=True  # Povolit responzivní přizpůsobení
                        )
                    ),
                    width=6,  # Šířka sloupce pro graf (z celkových 12)
                ),
            
            # Sloupec pro graf II
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id="my-graph_2",
                            figure=fig_2,
                            responsive=True  # Povolit responzivní přizpůsobení
                        )
                    ),
                    style={
                        "display": "flex",
                        "justify-content": "center",
                        "align-items": "center"},
                    width=6, # Šířka sloupce pro graf (z celkových 12)
                ),
            ],
            style={
                        "display": "flex",
                        "justify-content": "center",
                        "align-items": "center"},
            className="mb-4"  # Odsazení mezi řádky
        ),

        # Sloupec pro dropdown
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id="indicator-dropdown",
                    options=[
                        {"label": "PM2.5", "value": "pm2_5"},
                        {"label": "PM10", "value": "pm10"},
                        {"label": "CO", "value": "CO"},
                        {"label": "CO2", "value": "CO2"},
                        {"label": "NO2", "value": "NO2"},
                        {"label": "SO2", "value": "SO2"}
                    ],
                    value="pm2_5",  # Výchozí hodnota
                    placeholder="Vyber ukazatel",
                    style={"align-items": "center"}
                ),
                width=3,  # Šířka sloupce pro dropdown (z celkových 12)
            ),
            style={
                    "display": "flex",
                    "justify-content": "center",
                    "align-items": "center",
                    "height": "100px"  # Nastavení pevné výšky
                },
            className="mb-4",  # Odsazení mezi řádky
        ),

        # Tabulka
        dbc.Row(
            dbc.Col(
                dash_table.DataTable(
                    id="city-table",
                    columns=[{"name": col, "id": col} for col in df_to_show.columns],
                    data=[],
                    
                    style_cell={"textAlign": "left"}  # Zarovnání textu doleva
                ),
                style={
                        "display": "flex",
                        
                        "justify-content": "center",  # Zarovnání obsahu na střed
                    },
                width=12,
            )
        )
    
    ],
    fluid=True,
)

# slovníky pro mapování barev ve callbacks

color_scale = {
            "pm2_5" : "ind_1",
            "pm10" : "ind_2",
            "CO" : "ind_3",
            "CO2" : "ind_4",
            "NO2" : "ind_5",
            "SO2" : "ind_6"
                }

color_scale_dictionary_bar = {
    "ind_1" : "#083D77", 
    "ind_2" : "#713F6F", 
    "ind_3" : "#DA4167", 
    "ind_4" : "#E78A63", 
    "ind_5" : "#F4D35E", 
    "ind_6" : "#F78764" 
                        }

color_scale_dictionary_scatter = {
    "ind_1" : "Turbo",  # Modrá až červená
    "ind_2" : "Turbo", # Fialová až žlutá
    "ind_3" : "Turbo", # Fialová až oranžová
    "ind_4" : "Turbo", # Modrá až žlutá
    "ind_5" : "Turbo", # Fialová až žlutá
    "ind_6" : "Turbo" # Modrá až červená
                        }

# Callback pro barchart
@app.callback(
    Output("my-graph_2", "figure"),
    Input("indicator-dropdown", "value"),
)
def update_map(selected_indicator_bar):
    
    # Dynamická tvorba mapy na základě vybraného ukazatele
    
    fig_2 = px.bar(
    data_frame=df_to_show,
    x = 'town_name',
    y = selected_indicator_bar,
    category_orders = df_to_show.sort_values(by=selected_indicator_bar, ascending=False),
    color_discrete_sequence=[color_scale_dictionary_bar[color_scale[selected_indicator_bar]]],
    hover_name='town_name',
    title=f"Největší města dle znečištění")
    
    fig_2.update_layout(title={"text": "Největší města dle znečištění", "x": 0.5})

    return fig_2

# Callback pro aktualizaci mapy
@app.callback(
    Output("my-graph", "figure"),
    Input("indicator-dropdown", "value"),
)
def update_map(selected_indicator):

    fig = px.scatter_mapbox(
        data_frame=df_to_show,
        
        lat="latitude",
        lon="longitude",
        size=selected_indicator, 
        color=selected_indicator,
        color_continuous_scale= color_scale_dictionary_scatter[color_scale[selected_indicator]],  # Barevná škála od modré po červenou  
        hover_name='town_name',
        hover_data={"pm10": True, "pm2_5": True, "latitude": False, "longitude": False},
        title=f"Aktuální znečištění ovzduší v České republice",
        mapbox_style="outdoors",
        zoom=5.8,
        center={"lat": 49.8175, "lon": 15.4730}  # Střed České republiky
    )
    fig.update_layout(title={"text": "Aktuální znečištění ovzduší v České republice", "x": 0.5})


    # Přidání Mapbox tokenu
    fig.update_layout(mapbox_accesstoken="pk.eyJ1IjoiemRlbnk4MiIsImEiOiJjbTQyY3Rma2QyamZ0MmxxdG1ubTg4MGVqIn0.FcqTJTyPRFgbHzHNCwFOIQ",
                width=800,  # Šířka plátna
                height=500  # Výška plátna
                )
    
    return fig


# Callback pro změnu dynamické karty
@app.callback(
    Output("dynamic-card", "children"),
    Input("city-dropdown", "value")
)
def update_dynamic_card(selected_city):
    
    return [
        dbc.CardHeader(f"{selected_city} {df_to_show.loc[df_to_show['town_name'] == 'Brno', 'time'].values.squeeze()}"),
        dbc.CardBody(
            [
                html.H5(f"PM2.5: {df_to_show.loc[df_to_show['town_name'] == selected_city, 'pm2_5'].iloc[0]} µg/m³", className="card-title"),
                html.P(f"PM10: {df_to_show.loc[df_to_show['town_name'] == selected_city, 'pm10'].iloc[0]} µg/m³", className="card-text"),
            ]
        ),
    ]

# Callback pro aktualizaci tabulky
@app.callback(
    Output("city-table", "data"),
    Input("city-dropdown", "value")
)
def update_table(selected_city):
    # Filtrovat DataFrame podle vybraného města
    filtered_df = df_to_show[df_to_show['town_name'] == selected_city]
    return filtered_df.to_dict("records")

# if __name__ == "__main__":
#   app.run_server(host="127.0.0.1", port=8050, debug=True)
