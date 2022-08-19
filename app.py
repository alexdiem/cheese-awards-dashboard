from dash import Dash, html, dcc
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


df = load_data()
df = etl(df)

data = df.query("category_code == '5001'")

company_histogram = px.histogram(data, x='company')
company_histogram.update_layout(
    plot_bgcolor=colours['background'],
    paper_bgcolor=colours['background'],
    font_color=colours['text']
)

country_histogram = px.histogram(data, x='country')
country_histogram.update_layout(
    plot_bgcolor=colours['background'],
    paper_bgcolor=colours['background'],
    font_color=colours['text']
)

sunburst = px.sunburst(data, path=["country", "company", "product_name"], values='rating')
sunburst.update_layout(
    plot_bgcolor=colours['background'],
    paper_bgcolor=colours['background'],
    font_color=colours['text']
)

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
                html.H4(
                    children="Table: World Cheese Awards 2021",
                    style={
                        'textAlign': 'center',
                        'color': colours['text']
                    }
                ),
                generate_table(df)
            ]
        ),

        dcc.Graph(
            id="company_histogram",
            figure=company_histogram
        ),

        dcc.Graph(
            id="country_histogram",
            figure=country_histogram
        ),

        dcc.Graph(
            id="sunburst",
            figure=sunburst
        )
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)