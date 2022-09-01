import dash
from dash import callback, dcc, html, Input, Output
from pathlib import Path

import plotly.express as px
import pandas as pd


dash.register_page(__name__, path="/")


def load_data():
    pathname = Path("data")
    filename = "winequality-red.csv"
    df = pd.read_csv(pathname / filename)
    return df


def get_attributes(df):
    return df.columns


def generate_table(max_rows=10):
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


def render_quality_piechart():
    fig = px.pie(df, names='quality')
    return fig


@callback(
    Output('attribute_histogram', 'figure'),
    Input('attribute_dropdown', 'value')
)
def render_attribute_histogram(attribute):
    fig = px.histogram(df, x=attribute, color='quality')
    return fig


@callback(
    Output('attribute_boxplot', 'figure'),
    Input('attribute_dropdown', 'value')
)
def render_attribute_boxplot(attribute):
    fig = px.box(df, x='quality', y=attribute, points="all")
    return fig


df = load_data()
attributes = get_attributes(df)


layout = html.Div(
    children = [
        html.Div(
            children=[
                html.Div(
                    [
                        html.H4(
                            children="Quality distribution",
                            style={
                                'textAlign': 'center'
                            }
                        ),
                        dcc.Graph(figure=render_quality_piechart())
                    ],
                    style={
                        'width': '30%',
                        'display': 'inline-block',
                        'vertical-align': 'top'
                    }
                ),

                html.Div(
                    children=[generate_table()],
                    style={
                        'width': '65%', 
                        'display': 'inline-block',
                        'vertical-align': 'top'
                    }
                )
            ]
        ),

        html.Div(
            children=[
                html.P(
                    children=["Choose quality"],
                    style={
                        'width': '10%', 
                        'display': 'inline-block',
                        'vertical-align': 'top'
                    }
                ),
                dcc.Dropdown(
                    attributes, 'fixed acidity', id='attribute_dropdown',
                    style={
                        'width': '30%', 
                        'display': 'inline-block',
                        'vertical-align': 'top'
                    }
                )
            ]
        ),

        html.Div(
            children=[
                dcc.Graph(id="attribute_histogram"),
                dcc.Graph(id="attribute_boxplot")
            ]
        )
    ]
)