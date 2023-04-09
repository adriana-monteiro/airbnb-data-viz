
##### importing libraries #####

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from PIL import Image
from functions_pedro import app_objective, about_airbnb, scattermapbox_price, preattentive_dumbell, butterflyplot, grouped_attr_avg, boxplot, scatter_attr, scatter_res, get_highest_prices_map, min_clean, min_satis, max_satis, max_clean, max_airbnb, min_airbnb
import dash_bootstrap_components as dbc

## importing data ##
df_full = pd.read_csv('df_full.csv')

lista = [df_full]
for col in lista:
    # guest_satisfaction_overall
    col.loc[(col['guest_satisfaction_overall'] >=90.0),'overall_rating'] = 'Excellent'
    col.loc[ (col['guest_satisfaction_overall'] >= 70.0) & (col['guest_satisfaction_overall'] <= 89.0), 'overall_rating' ] = 'Very good'
    col.loc[(col['guest_satisfaction_overall'] <=69.0),'overall_rating'] = 'Reasonable'

df_full['realSum_log'] = df_full['realSum'].apply(lambda x: np.log10(x))

## fetching logo ##
pil_image = Image.open("logo3.png")

## citiy images
amsterdam_png = Image.open("amsterdam.png")
athens_png = Image.open("athens.png")
barcelona_png = Image.open("barcelona.png")
berlin_png = Image.open("berlin.png")
budapeste_png = Image.open("budapester.png")
london_png = Image.open("london.png")
paris_png = Image.open("paris.png")
rome_png = Image.open("rome.png")
vienna_png = Image.open("vienna.png ")
lisbon_png = Image.open("lisbon.png")


##airbnbs

a2_png = Image.open("img/2.png")
a3_png = Image.open("img/3.png")
a4_png = Image.open("img/4.png")
a7_png = Image.open("img/7.png")
a8_png = Image.open("img/8.png")
a9_png = Image.open("img/9.png")
a10_png = Image.open("img/10.png")
a12_png = Image.open("img/12.png")
a18_png = Image.open("img/18.png")
a19_png = Image.open("img/19.png")
a20_png = Image.open("img/20.png")
#a21_png = Image.open("img/21.png")




## sidebar image

plane_png = Image.open('plane.png')
house_png = Image.open('house.png')


######################### INTERACTIVE COMPONENTS ############################################

############ DROPDOWNS #######################

### main dropdown -> choose one city!
cities = df_full['city'].unique()
city_dropdown = dcc.Dropdown(
                        id="city-dropdown",
                        options=[{'label': city.title(), 'value': city} for city in cities],
                        value=None,
                        placeholder="Select a city",
                        clearable=True,
                        style = {'width': '200px', 'height': '50px','margin': '30px', 'text-align': 'center', 'justify-content': 'center', 'font-size': 16 }
                    )


############  RADIO ITEMS #####################


period_selector_2 = dcc.RadioItems(className='radio-container',
                        id = 'period-selector-2',
                        options = [
                                     {'label': 'Weekdays', 'value': 'weekdays'},
                                     {'label': 'Weekends', 'value': 'weekends'}
                                    ],
                        value='weekdays',

                        )

############ cards #################


card = dbc.Card([
    dbc.CardHeader(id='card-header', className='card-title'),
    dbc.CardBody(id='card-content', className='card-subtitle'),
    dbc.CardImg(id='card-image'),
], style={'height': '50%', 'width': '30%'})


kpis = html.Div([

html.Div([



dbc.Card([
    dbc.CardHeader('Lowest Average Guest Satisfaction', className='card-title'),
    dbc.CardBody(['City: '+ min_satis[0].title(),
                  html.Br(),
                  'Satisfaction: '+min_satis[1]], className='card-subtitle'),
], style={'height': '50%', 'width': '40%','borderColor': '#FF5C5C', 'marginRight':'6px'}),

 dbc.Card([

    dbc.CardHeader('Highest Average Guest Satisfaction', className='card-title'),
    dbc.CardBody(['City: '+ max_satis[0].title(),
                    html.Br(),
                  'Satisfaction: '+max_satis[1]], className='card-subtitle'),
], style={'height': '50%', 'width': '40%','borderColor': '#2F485'}),

], style= {'display':'flex'}),


html.Br(),

    html.Div([
dbc.Card([
    dbc.CardHeader('Lowest Average Clealiness Rating', className='card-title'),
    dbc.CardBody(['City: '+ min_clean[0].title(),
html.Br(),
                  'Satisfaction: '+min_clean[1]], className='card-subtitle')],
    style={'height': '50%', 'width': '40%','borderColor': '#FF5C5C', 'marginRight':'6px'}),

dbc.Card([
    dbc.CardHeader('Highest Average Clealiness Rating', className='card-title'),
    dbc.CardBody(['City: '+ max_clean[0].title(),
html.Br(),
                  'Satisfaction: '+max_clean[1]], className='card-subtitle'),
], style={'height': '50%', 'width': '40%','borderColor': '#2F485'},)
], style= {'display':'flex'}),
], style={'display': 'block'})





kpis_price = html.Div([



dbc.Card([
    dbc.CardHeader('Highest Airbnb Price', className='card-title'),
    dbc.CardBody(['Price: ', round(max_airbnb['realSum'].values[0],2),'€',
                  html.Br(),

        'City: '+ max_airbnb['city'].values[0].title(),
                html.Br(),
                  'Time of the Week:', max_airbnb['period'].values[0],

                  html.Br(),
                  'Distance to the center:', str(round(max_airbnb['dist'].values[0],1))+' Km',
                  html.Br(),
                  'Guest Satisfaction: ', max_airbnb['guest_satisfaction_overall'].values[0],
                  html.Br(),
                  'Cleanliness Rating: ',max_airbnb['cleanliness_rating'].values[0],
                  html.Br(),
                  'Room Type: '+ max_airbnb['room_type'].values[0],
                  html.Br(),
                  'Person Capacity:', max_airbnb['person_capacity'].values[0],
                  html.Br(),
                  'Nr of Bedrooms: ', max_airbnb['bedrooms'].values[0]], className='card-subtitle'),
], style={'height': '50%', 'width': '40%','borderColor': '#FF5C5C', 'marginRight':'6px'}),

 dbc.Card([

     dbc.CardHeader('Lowest Airbnb Price', className='card-title'),
     dbc.CardBody(['Price: ', round(min_airbnb['realSum'].values[0],2),'€',
                   html.Br(),
                   'City: ' + min_airbnb['city'].values[0].title(),
                   html.Br(),
                   'Time of the Week, :' + min_airbnb['period'].values[0],
                   html.Br(),
                   'Distance to the center:', round(min_airbnb['dist'].values[0],1), 'Km',
                   html.Br(),
                   'Guest Satisfaction: ', min_airbnb['guest_satisfaction_overall'].values[0],
                   html.Br(),
                   'Cleanliness Rating: ', min_airbnb['cleanliness_rating'].values[0],
                   html.Br(),
                   'Room Type: '+ min_airbnb['room_type'].values[0],
                   html.Br(),
                   'Person Capacity:', min_airbnb['person_capacity'].values[0],
                   html.Br(),
                   'Nr of Bedrooms: ', min_airbnb['bedrooms'].values[0]], className='card-subtitle'),

], style={'height': '50%', 'width': '40%','borderColor': '#2F485'}),

], style= {'display':'flex'})


##################3 CAROUSSEL ##################


carousel = dbc.Carousel(
    items=[
     #   {"key": "1", "src": a1_png},
{"key": "2", "src": a2_png},
{"key": "3", "src": a3_png},
{"key": "4", "src": a4_png},
#{"key": "5", "src": a5_png},
#{"key": "6", "src": a6_png},
{"key": "7", "src": a7_png},
{"key": "8", "src": a8_png},
{"key": "9", "src": a9_png},
{"key": "10", "src": a10_png},
#{"key": "11", "src": a11_png},
{"key": "12", "src": a12_png},
#{"key": "13", "src": a13_png},
#{"key": "14", "src": a14_png},
#{"key": "15", "src": a15_png},
#{"key": "16", "src": a16_png},
#{"key": "17", "src": a17_png},
{"key": "18", "src": a18_png},
{"key": "19", "src": a19_png},
{"key": "20", "src": a20_png},
#{"key": "21", "src": a21_png},
    ],
    controls=True,
    indicators=False,
    interval=3700,
    ride="carousel",
    style={"width": "500px", "height": "200px"}
)


#################### TABS ################################

europe_tab = dbc.Tab(label='Europe', tab_id='europe',
                     children=[

                         html.Br(),
                         html.H4('How do Prices vary across Europe?', style = {'text-align':'left'}), html.Hr(),
                         html.Div([

                             html.Div([
                             html.Div(children = ['''One of the most important aspects of an airbnb listing
                                             is its price. In the map you can see how the prices are distributed across several cities in Europe
                                             colored according to how much two nights cost for two people. The marker's size is 
                                             proportional to the person capacity of all airbnb listings available in the city.
                                             ''',
                                                  html.Br(),
                                                kpis_price



                                                  ],
                                             style={'text-align': 'left', 'font-size':'17px', 'padding-left':'0%', 'padding-right':'1%', 'width': '700px'}),

                                 html.Div([
                                            dcc.Graph(
                                               id='europe-graph',
                                               figure=get_highest_prices_map()
                                           )],style={'padding-right': '20px'}),
                                 ], style = {'display':'flex'}),

                                 html.Br(),
                                html.Br(),

                                 html.Div([

                                          html.Div(children='''Prices can also change according to if the booking is done on the weekend or not. 
                                          Usually, it's more expensive on the weekends.
                                                                                        ''',style={'text-align': 'right', 'font-size': '17px',
                                                          'padding-left': '0%', 'padding-right': '0%'}),
                                                   html.Br(),

                                                dcc.Graph(id='dumbell', style = {'align-items':'right'}),

                                           ], style={'display': 'block','align-items':'right'})
                             ], style={'display': 'block',}, className='box'),

                             html.Br(),

                             html.Div([
                                    html.Div(children = '''Let's find out if guest satisfaction is related with how clean a
                                      listed apartment is!''',
                                style={'text-align': 'justify', 'font-size':'17px', 'padding-left':'3%', 'padding-right':'4%'}),
                                    html.Div([dcc.Graph(id='boxplot', figure = boxplot()),
                                              kpis], style={'display': 'flex','justify-content':'space-between'})

                             ], style={'display': 'block', 'width':'100%'}, className='box'),



                            html.Div([
                                 html.Div([html.Label(['Attraction and Restaurant Index'])]),
                                 html.Div([dcc.Graph(id='index-barchart')],
                                          style={'padding-right': '20px', 'height': '100%', 'width':'100%'})
                         ], style={'display': 'flex'}, className='box')
                     ], style = {'width':'100%'})



city_tab = dbc.Tab(label='City', tab_id='city',
                   children=[
                       html.Div([
                           html.Br(),
                           dbc.Alert("Don't forget to select a city before coming here!", color="danger", class_name='text-center', style = {'width': '100%', 'font-size':14}),
                           html.Br(),
                           html.Label('Select the time of the week:'),
                           period_selector_2,
                           html.Div([
                                     html.Br(),

                               html.Div([html.Label(['The size of the points represents the person capacity of the Airbnb']),
                                 dcc.Graph(id='scattermap')], style = {'padding-right':'0px', 'height':'100%'}),

                               card

                               ], style = {'display': 'flex'})
                           ],className='box'),


                        html.Div([
                           html.Br(),
                           html.Br(),
                           html.Div([
                               html.Div([html.Label(['Attractionskjfkdsjf']),
                                         html.Div([
                                             dcc.Graph(id='scatter_index_attr'),
                                             dcc.Graph(id='scatter_index_res')
                                         ]),
                                  ], style = {'padding-right':'20px', 'height':'100%', 'display':'flex'}),
                               ])
                           ], style={'display': 'flex'},className='box')


                       ], style = {'width': '100%'})





####################### APP LAYOUT #######################

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([       #dashboard

        #side bar
                html.Div([
                        html.Br(),
                        html.Div(

                            [html.Img(src=pil_image,style={'width':'100%'})],
                            style={'background-color': '#FF5C5C'}),

                        html.Br(),

                        html.Div([
                            html.Blockquote([about_airbnb], style =  {'color': 'white' }),
                        ], style={'text-align': 'justify', 'font-size':'17px', 'padding-left':'3%', 'padding-right':'4%', 'display':'flex'}),
                        html.Br(),
                        html.Div(

                            [html.Img(src=plane_png, style={'width':'50%','justify-content':'center', 'align-items':'center', 'margin-left':'50px' })],
                            style={'background-color': '#FF5C5C','justify-content':'center', 'align-items':'center'}),
                        html.Br(),
                        html.Div(

                            [html.Img(src=house_png, style={'width':'40%','justify-content':'center', 'align-items':'center', 'margin-left':'55px' })],
                            style={'background-color': '#FF5C5C','justify-content':'center', 'align-items':'center'})


        ], className='side_bar'),

    html.Div([

    html.Div([

        html.Div([

                html.H2(['Airbnb listings in European cities'], style ={'letter-spacing': '1.5px','font-weight': 'bold','text-transform': 'uppercase', 'align-text': 'center',
                                                                                         'display':'flex','height': '100%', 'color':'#FF5C5C', 'justify-content':'center'} ),
        ], style={'background-color': 'white', 'padding-top': '50px'}),

        html.Br(),

        html.Div([

                dbc.Card(dbc.CardBody([
                                 app_objective,
                html.Br(),
                html.Br(),
                '\nThe Tab "Europe" shows information about all of the cities. If you want to see some details about a specific city, you can select here a city. The details will be on the "City" tab.',
                html.Br(),
                    city_dropdown], style = {'justify-content':'center'}),
                                    style={'width': '450px', 'margin-right': '30px', 'height': '330px', 'justify-content':'center', 'font-size': 16}),

                            html.Div([carousel]),


      ],  style = {"display": "flex", 'height': '100%', 'width': '100%', 'justify-content':'center'}
),


   ], style={'display': 'block', 'width': '100%', 'padding-left': '0%'}),


       html.Div([

            html.Div([

                html.Br(),
                dbc.Tabs([europe_tab, city_tab])
            ])

           ])

        ],style={'height': '65%', 'width': '90%'}, className='main')
])


##################### CALLBACKS ###############################################

@app.callback(
    Output('scattermap', 'figure'),
    Input('city-dropdown', 'value'),
    Input('period-selector-2', 'value')
   # Input('scattermap-selector-2', 'value')
)


def update_scattermap(city, period):

    if city is None:

        city = cities[0]

        plot = scattermapbox_price(city, period)

        fig_scattermap = go.Figure(data=plot[0], layout=plot[1])
        #fig_scattermap.update_layout(coloraxis_colorbar_x=-0.15)


    else:

        plot = scattermapbox_price(city, period)

        fig_scattermap = go.Figure(data=plot[0], layout=plot[1])

    return fig_scattermap

    # fig = go.Figure(data=data, layout=layout)
    #
    # return fig


@app.callback(
    [Output('dumbell', 'figure'),
    Output('index-barchart', 'figure'),],
    [Input('city-dropdown', 'value')]
   # Input('scattermap-selector-2', 'value')
)

def update_dum_bar(city):
    if city is None:

        plot = preattentive_dumbell(city, False)

        barchart = butterflyplot(city, cities,False)


    else:
        plot = preattentive_dumbell(city, True)
        barchart = butterflyplot(city, grouped_attr_avg.index, True)

    return plot, barchart


@app.callback(
    [Output('scatter_index_attr', 'figure'),
    Output('scatter_index_res', 'figure')],
    Input('city-dropdown', 'value')
   # Input('index_selector', 'value')
)

def update_scatters (city):

    if city is None:
        city == 'amsterdam'

    plot_attr = scatter_attr(city)
    plot_res = scatter_res(city)

    return plot_attr, plot_res


@app.callback(
    Output('card-header', 'children'),
    Output('card-content', 'children'),
    Output('card-image', 'src'),
    Input('city-dropdown', 'value')
)

def update_card_header(city):


    if city is None or city == 'amsterdam':
        title = 'Amsterdam'
        image1 = amsterdam_png
        content = 'City of Netherlands'

    elif city == 'athens':
        title = 'Athens'
        image1 = athens_png
        content = 'City of Greece'

    elif city == 'berlin':
        title = 'Berlin'
        image1 = berlin_png
        content = 'City of Germany'

    elif city == 'budapest':

        title = 'Budapest'
        content = 'City of Hungary'
        image1 = budapeste_png

    elif city == 'london':

        title = 'Lonoon',
        content = 'City of United Kingdom'
        image1 = london_png

    elif city == 'paris':
        title = 'Paris'
        content = 'City of France'
        image1 = paris_png

    elif city == 'rome':
        title = 'Rome'
        content = 'City of Italy'
        image1 = rome_png

    elif city == 'vienna':
        title = 'Vienna'
        content = 'City of Austria'

    elif city == 'lisbon':
        title = 'Lisbon'
        content = 'City of Portugal'
        image1 = lisbon_png

    elif city == 'barcelona':
        title = 'Barcelona'
        content = 'City of Spain'
        image1 = barcelona_png

    return title, content, image1

if __name__ == '__main__':
    app.run_server(debug=True)