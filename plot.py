import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash()

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
    'gdp-life-exp-2007.csv')


def generate_table(dataframe, max_rows=10):
    print (dataframe.head())
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app.layout = html.Div([
    html.H4(children='GDP Per Capita'),
    generate_table(df),
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure = {
            'data': [
                go.Scatter(
                    x = df[df['continent'] == i]['gdp per capita'],
                    y = df[df['continent'] == i]['life expectancy'],
                    text = df[df['continent'] == i]['country'],
                    mode = 'markers',
                    opacity = 0.7,
                    marker={
                        'size': 15,
                        'line' : {'width': 0.5, 'color': 'white'}
                    },
                    name = i
                ) for i in df.continent.unique()
            ],

            'layout': go.Layout(
                xaxis = {'type': 'log', 'title': 'GDP per Capita'},
                yaxis = {'title': 'Life Expectany'},
                margin = {'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend = {'x': 0, 'y': 1},
                hovermode = 'closest'
            )
        }
    )
])


if __name__ == '__main__':
    app.run_server()
