from dash import html
from pathlib import Path

import plotly.express as px
import pandas as pd


def load_data():
    pathname = Path("data")
    filename = "winequality-red.csv"
    df = pd.read_csv(pathname / filename)
    return df


def generate_table(df, max_rows=10):
    cols = df.columns
    return html.Table(
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


def render_quality_piechart(df):
    fig = px.pie(df, names='quality')
    return fig


def get_quality_codes(df):
    return df['quality'].unique()