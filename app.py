from dash import Dash, html, dcc
from winequality.winequality import *


markdown_intro = """
# Red Wine quality

This is a dashboard visualising the red wine quality dataset from Kaggle (https://www.kaggle.com/datasets/uciml/red-wine-quality-cortez-et-al-2009).
"""


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

df = load_data()
quality_codes = get_quality_codes(df)


app.layout = html.Div(
    children = [
        dcc.Markdown(children=markdown_intro),

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
                        dcc.Graph(
                            id="quality_piechart",
                            figure=render_quality_piechart(df)
                        )
                    ],
                    style={
                        'width': '30%',
                        'display': 'inline-block',
                        'vertical-align': 'top'
                    }
                ),

                html.Div(
                    children=[
                        generate_table(df)
                    ],
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
                    quality_codes, 5, id='quality_dropdown',
                    style={
                        'width': '20%', 
                        'display': 'inline-block',
                        'vertical-align': 'top'
                    }
                )
            ],
            
        )
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)