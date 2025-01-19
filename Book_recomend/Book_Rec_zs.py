"""
--- Book Recommendation App ---

### Purpose:
This application provides users with book recommendations based on their favorite books using a machine learning algorithm

### Features:
1. Users input their favorite book, and the app recommends similar titles based on a recommendation algorithm
2. The algorithm:
   - Converts a DataFrame into a pivot table and then into a sparse matrix
   - Utilizes the 'Nearest Neighbors' model from the `sklearn.neighbors` library
3. Customizable parameter:
   - `number_of_neighbors`: Specifies the number of recommendations to generate
4. Data source:
   - The preprocessed DataFrame `df_raw` (from the file `Cleaned_Book_ETL.csv`) is used without additional filtering as in `testing_ML_Dash.ipynb`
   - Default filter NOT applied: Minimum of 10 ratings per user

### Workflow:
1. Load cleaned data from the CSV file
2. Convert data to appropriate `dtypes`
3. Initialize and configure the application background
4. Create a Flask server
5. Define the structure of the Dash application:
   - Main components
   - Callbacks for user interaction
   - Logic for filtering and selecting data from the DataFrame
   - Conditions, filters, and outputs
"""

# Import pandas
import pandas as pd

# Algorithm
from scipy.sparse import csr_matrix # sparse matrix
from sklearn.neighbors import NearestNeighbors # ML model

# Dash framework and components
import dash # app
from dash import html, dcc, Input, Output, State, dash_table # dash component
import dash_bootstrap_components as dbc # dbc formating
from dash.dash_table import DataTable # output table
import base64 # image coding
import re # string stuff

# Matching the finding titles
from rapidfuzz import fuzz, process

# Handle of missing html images
import dash.html as html

# Load cleaned data = dataset_lowercase
df_raw = pd.read_csv('Cleaned_Book_ETL.csv', encoding='UTF-8', sep=',')

# Convert data types

column_types = {
    'User-ID': 'int64',
    'ISBN': 'string',
    'Book-Rating': 'int64',
    'Book-Title': 'string',
    'Book-Author': 'string',
    'Year-Of-Publication': 'int64',  # nebo 'string', pokud jsou hodnoty smíšené
    'Publisher': 'string',
    'Image-URL-S': 'string',
    'Image-URL-M': 'string',
    'Image-URL-L': 'string'
}

# Data types conversion
for column, dtype in column_types.items():
    df_raw[column] = df_raw[column].astype(dtype)

# Loading a dash app background picture
def load_image(image_path):
    with open(image_path, "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode()
    return f"data:image/jpeg;base64,{encoded_image}"

image_path = 'StuttgartSelect.jpg' # from Kaggle

encoded_image = load_image(image_path)

# Running Dash server

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# add Flask server for Gunicorn
server = app.server

# APP Layout (dbc responsivity)
app.layout = dbc.Container(
    
    children=[  
     
        # 1 - App title + backround picture
        dbc.Row(
            dbc.Col([
                html.H1(
                    "Book recomendation",
                    
                    style={
                        'color': 'grey', # text color
                        "display": "flex",
                        "flex-wrap": "wrap",
                        "justify-content": "center",
                        "align-items": "center"
                            }
                ),
                html.Img(
                    src=encoded_image,
                    className="img-fluid",
                    style = {"objectFit": "cover"}
                )
            ]),
            style={
                    "display": "flex",
                    "flex-wrap": "wrap",
                    "justify-content": "center",
                    "align-items": "center",
                    "height": "80px"
            },
        ),

        # 2 -  Search for user input - title of the book
        dbc.Row(
            dbc.Col(
                dcc.Input(
                    id="search_box",
                    type="text",
                    placeholder="Enter your favorite book to recommendations for others you might like",
                    debounce=True,  # Callback requires pressing the Enter key
                    style={
                            "width" : "50%"
                    }
                ),
                style={
                        "display": "flex",
                        "flex-wrap": "wrap",
                        "justify-content": "center",
                        "align-items": "center",
                        "height": "50px"
                }
            ),
            style={
            }
        ),

        # 3 -  CheckChecklist filter (Can be extended with another option e.g.: a 'year of the book' option)
        dbc.Row(
            dbc.Col(
                dcc.Checklist(
                    id="author_filter",
                    options=[{"label": "Filter by same author", "value": "filter_author"}],
                    value=[],
                    style={
                        'color': 'black',
                        "font-weight": "normal",
                        'font-size': '16px',
                        "display": "flex",
                        "flex-wrap": "wrap",
                        "justify-content": "center",
                        "align-items": "center"
                    }
                )
            ),
            
            style={
                    },
        ),

        # 4 -  Slider for number of the result
        dbc.Row(
            dbc.Col(
                html.Div([
                    html.H6(
                        "Number of suggested books",
                        style={
                                'color': 'black',
                                "font-weight": "normal",
                                'font-size': '16px',
                                "display": "flex",
                                "flex-wrap": "wrap",
                                "justify-content": "center",
                                "align-items": "center"
                        }
                    ),
                    dcc.Slider(
                        id="slider",
                        value = 5,
                        step = 1,
                        marks={
                            i : {'label': str(i), 'style': {'color': 'black', 'font-size': '16px'}}
                            for i in range(2, 11)
                        },
                        tooltip={
                            "placement": "bottom", "always_visible": True,
                            "style": {
                                "color": "black", 
                                "backgroundColor": "#grey", 
                                'font-size': '18px'
                            }  # tooltipu style
                        },
                    )],
                    style={
                            "justify-content": "center", 
                            "align-items": "center",
                            "width" : "50%",
                            "color" : "black"
                    },
                ),
                style={
                        "display": "flex",
                        "flex-wrap": "wrap",
                        "justify-content": "center",
                        "align-items": "center"
                }
            ),
            style={
                    "height": "100px"
            },
        ),

        # 5 - Container for output table of recomendation books
        dbc.Row(    
            dbc.Col([
                html.Div(
                    id='output_table'
                )
            ]),
                style={
                    "display": "flex",
                    "flex-wrap": "wrap",
                    "justify-content": "center",
                    "align-items": "center"
                }
        ), 
            
        # 6 - Image Container for Book Recommendations
        dbc.Row(
            dbc.Col(
                html.Div(
                    id="image_container",
                    style={
                        "display": "flex",
                        "justify-content": "center",
                        "align-items": "center"
                    }
                )
            ),
            style={
                    "display": "flex",
                    "justify-content": "center",
                    "align-items": "center"
            }
        )
    ]
)

# Enter number of neighbors (to ML) to change the number of the recomendated titles
# number_of_neighbors = 10 # e.g.: n request = n - 1 result titles

# -------------------------- Table for book or error content --------------------------
def create_table(table_data, color_style, columns_style):
    
    return html.Div(dash_table.DataTable(
            data=table_data,
            columns=columns_style,
            style_table={"width": "50%"},
            style_cell={"textAlign": "left"},
            style_header={
                "textAlign": "center"
            }
                    ), 
        style={
            "display": "flex",
            "justify-content": "center",
            "align-items": "center",
            **color_style
        }
            )

# -------------------------- Book gallery content --------------------------

# Create the books images container
def create_image_container(image_urls):
    
    # Check the URL exists 
    if image_urls == []:
        return html.Div("No images available.", style={"textAlign": "center", "color": "red", "marginTop": "10px"})

    # Create a list of HTLM <img> tags for every image
    image_elements = [
        html.Img(src=url, style={"width": "100px", "height": "150px", "margin": "10px", "display": "inline-flex",
            "justify-content": "center", # jinak se nenačte stylování původního rozvrhu, které se hodí doleva
            "align-items": "center"}) for url in image_urls if url != ""
    ]

    return image_elements


# -------------------------- Callback (recomendation) --------------------------
@app.callback(
    [Output("output_table", "children"),  # output table
    Output("image_container", "children")],  # gallery
    [Input("search_box", "value"),  # Input book name
    Input("slider", "value"),
    Input("author_filter", "value")]  # check box 
)

def update_recommendations(chosen_book, slider_value, filter_author):
    
    slider_value = slider_value + 1

    # 1. check no input chosen_book
    if not chosen_book:

        return [None, None] # 1. initial non error message

    # Need a best match
    chosen_book = re.sub(r'\s+', ' ', chosen_book)
    name_of_the_book = df_raw.loc[df_raw['Book-Title'].str.contains(chosen_book, case=False, na=False, regex=False), 'Book-Title'] # Series
    list_of_names_of_the_book = list(name_of_the_book)
    best_match = process.extractOne(chosen_book, list_of_names_of_the_book) # tuple
    name_of_the_book = best_match[0] # str

    # 2. Tuple best_match emptiness check
    if best_match == ():
        
        table_data = [{"Suggested Books:":"Book name is not in database."}]
        color_style= {"color": "red"}
        columns_style = [{"name": "Suggested Books:", "id": "Suggested Books:"}]
        return [create_table(table_data, color_style, columns_style), None] # 2. error message
       
    # 3. a) Check if an author is selected 
    if filter_author:
        
        author_of_the_chosen_book = df_raw.loc[df_raw['Book-Title'] == name_of_the_book, 'Book-Author'].values[0] # author = author
        books_of_other_readers = df_raw.loc[df_raw['Book-Author'] == author_of_the_chosen_book] # df - all author books in df
    
    else: # b) The same author NOT selected 
        
        readers_of_the_book = df_raw.loc[df_raw['Book-Title'] == name_of_the_book, 'User-ID']
        books_of_other_readers = df_raw.loc[df_raw['User-ID'].isin(readers_of_the_book)] # df - Books by the selected author, as well as books by other authors from the filtered users

    # Pivot table
    book_pivot = books_of_other_readers.pivot_table(columns='User-ID', index='Book-Title', values='Book-Rating')
    book_pivot.fillna(0, inplace=True) # Memory-efficient

    if book_pivot.empty or len(book_pivot) < slider_value:  # If the pivot table is empty or contains fewer items than 'number_of_neighbors', no results can be generated
        table_data = [{"Suggested Books:":"Not enough data for model to suggest a book"}]
        color_style= {"color": "red"}
        columns_style = [{"name": "Suggested Books:", "id": "Suggested Books:"}]
        return [create_table(table_data, color_style, columns_style), None] # 3. error message

    # Sparse matrix
    book_sparse = csr_matrix(book_pivot)

    # Unsupervised learner for implementing neighbor searches
    model = NearestNeighbors(algorithm='brute')
    model.fit(book_sparse)

    # Suggestions indexes for book_pivot recomendation:
    distances, suggestions = model.kneighbors(book_pivot.loc[[name_of_the_book]].values, n_neighbors=slider_value) # n_neighbors=5, default

    # Making the list of suggested books
    list_of_suggested_books = []
    for i in range(len(suggestions)):
        recommended_books = book_pivot.index[suggestions[i]].tolist()  # need a list instead of stringarray
        for book in recommended_books:
            list_of_suggested_books.append({"Suggested Books:": book})

    # Pop the name_of_the_book from the list
    list_of_suggested_books = [book_dict for book_dict in list_of_suggested_books if book_dict["Suggested Books:"] != name_of_the_book] #Tento přístup projde každý slovník v seznamu list_of_suggested_books a ponechá jen ty, které nemají stejnou hodnotu
    
    # 4. Only one book result check
    if len(list_of_suggested_books) < 1:
        table_data = [{"Suggested Books:":f"Only avalaible result is the {name_of_the_book}"}]
        color_style= {"color": "red"}
        columns_style = [{"name": "Suggested Books:", "id": "Suggested Books:"}]
        
        image_urls_df_raw = df_raw.loc[df_raw['Book-Title'] == name_of_the_book, ['Book-Title', 'Image-URL-M']].groupby('Book-Title').max() # jedna knížka bude mít více hodnocení -> html odkazů
        image_urls_list = list(image_urls_df_raw['Image-URL-M'].values)

        return [create_table(table_data, color_style, columns_style), create_image_container(image_urls_list)] # 4. error message
    
    # Result table of suggested books
    table_data = list_of_suggested_books
    color_style = {"color": "black"}
    columns_style = [{"name": "Suggested Books:", "id": "Suggested Books:"}]
    list_of_titles = [x['Suggested Books:'] for x in list_of_suggested_books]
    image_urls_df_raw = df_raw.loc[df_raw['Book-Title'].isin(list_of_titles), ['Book-Title', 'Image-URL-M']].groupby('Book-Title').max()
    image_urls_list = list(image_urls_df_raw['Image-URL-M'].values)
    
    # debug prints
        
    return [create_table(table_data, color_style, columns_style), create_image_container(image_urls_list)]

# ----------------- Dash server ----------------- 

if __name__ == "__main__":
   app.run_server(host="127.0.0.1", port=8080, debug=True)