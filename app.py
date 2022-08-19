from dash import Dash, html, dcc, Input, Output
from pathlib import Path

import plotly.express as px
import pandas as pd


app = Dash(__name__)

colours = {
    'background': '#111111',
    'text': '#7FDBFF'
}

markdown_intro = """
# World Cheese Awards

This is a dashboard visualising the World Cheese Awards dataset from Kaggle (https://www.kaggle.com/datasets/ericsims/world-cheese-awards-worlds-cheesiest-dataset?resource=download).
"""


def load_data():
    pathname = Path("data")
    filename = "world_cheese_awards_2021.csv"
    df = pd.read_csv(pathname / filename, index_col=0)
    return df


def etl(df):
    df['category'] = df['category'].str.replace("–", "-")
    df[['category_code', 'category', 'subcategory']] = df['category'].str.split(" - ", expand=True)
    rating_dict = {"SUPER GOLD": 0, "GOLD": 1, "SILVER": 2, "BRONZE": 3}
    df = df.replace({"rating": rating_dict})
    return df


def generate_table(df, max_rows=10):
    cols = df.columns
    return html.Table(
        style={'color': colours['text']},
        children=[
            html.Thead(
                html.Tr(
                    [html.Th(col) for col in cols]
                )
            ),
            html.Tbody(
                [
                    html.Tr(
                        [html.Td(df.iloc[i][col]) for col in cols]
                    ) for i in range(min(len(df), max_rows))
                ]
            )
        ]
    )


def query_category_code(df, category_code):
    return df.query("category_code == '{}'".format(category_code))


@app.callback(
    Output('company_histogram_graph', 'figure'),
    Input('cat_code_dropdown', 'value')
)
def render_company_histogram(cat_code):
    data = query_category_code(df, cat_code)

    fig = px.histogram(data, x='company')
    fig.update_layout(
        plot_bgcolor=colours['background'],
        paper_bgcolor=colours['background'],
        font_color=colours['text']
    )
    return fig


@app.callback(
    Output('country_histogram_graph', 'figure'),
    Input('cat_code_dropdown', 'value')
)
def render_country_histogram(cat_code):
    data = query_category_code(df, cat_code)

    fig = px.histogram(data, x='country')
    fig.update_layout(
        plot_bgcolor=colours['background'],
        paper_bgcolor=colours['background'],
        font_color=colours['text']
    )
    return fig


@app.callback(
    Output('sunburst_graph', 'figure'),
    Input('cat_code_dropdown', 'value')
)
def render_sunburst(cat_code):
    data = query_category_code(df, cat_code)

    fig = px.sunburst(data, path=["country", "company", "product_name"], values='rating')
    fig.update_layout(
        plot_bgcolor=colours['background'],
        paper_bgcolor=colours['background'],
        font_color=colours['text']
    )
    return fig


df = load_data()
df = etl(df)

cat_codes = df['category_code'].unique()

app.layout = html.Div(
    style={'backgroundColor': colours['background']},
    children = [
        html.Div(
            children=dcc.Markdown(children=markdown_intro),
            style={
                'textAlign': 'center',
                'color': colours['text']
            }
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            children=[
                                html.Label('Dropdown'),
                                dcc.Dropdown(
                                    cat_codes, 
                                    '5001',
                                    id='cat_code_dropdown'
                                )
                            ]
                        )
                    ], style={'padding': 10, 'flex': 1}
                ),

                html.Div(
                    [
                        html.H4(
                            children="Table: World Cheese Awards 2021",
                            style={
                                'textAlign': 'center',
                                'color': colours['text']
                            }
                        ),
                        generate_table(df)
                    ]
                )
            ], style={'display': 'flex', 'flex-direction': 'row'}
        ),

        dcc.Graph(id="company_histogram_graph"),

        dcc.Graph(id="country_histogram_graph"),

        dcc.Graph(id="sunburst_graph")
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)