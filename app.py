import dash
from dash import Dash, html, dcc


markdown_intro = """
# Red Wine quality

This is a dashboard visualising the red wine quality dataset from Kaggle (https://www.kaggle.com/datasets/uciml/red-wine-quality-cortez-et-al-2009).
"""

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets, use_pages=True)


app.layout = html.Div(children=[
    dcc.Markdown(
        children=[markdown_intro]
    ),
    dash.page_container
])


if __name__ == '__main__':
    app.run_server(debug=True)