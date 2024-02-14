


##importing libraries


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from PIL import Image
from aux import about_airbnb, scattermapbox_price, preattentive_dumbell, butterflyplot, grouped_attr_avg, boxplot, scatter_attr, scatter_res, get_highest_prices_map, min_clean, min_satis, max_satis, max_clean, max_airbnb, min_airbnb, attr_avg_plot, rest_avg_plot
import dash_bootstrap_components as dbc


############################### IMPORTING THE DATA ##########################################################

df_full = pd.read_csv('df_full.csv')

########################### CREATING NECESSARY COLUMNS ######################################################3

# creating a categorical column for guest satisfaction
for col in [df_full]:
    # guest_satisfaction_overall
    col.loc[(col['guest_satisfaction_overall'] >=90.0),'overall_rating'] = 'Excellent'
    col.loc[ (col['guest_satisfaction_overall'] >= 70.0) & (col['guest_satisfaction_overall'] <= 89.0), 'overall_rating' ] = 'Very good'
    col.loc[(col['guest_satisfaction_overall'] <=69.0),'overall_rating'] = 'Reasonable'

df_full['realSum_log'] = df_full['realSum'].apply(lambda x: np.log10(x))


################################## FETCHING IMAGES #########################################

# logo
pil_image = Image.open("img/logo3.png")

# cities
amsterdam_png = Image.open("img/amsterdam.png")
athens_png = Image.open("img/athens.png")
barcelona_png = Image.open("img/barcelona.png")
berlin_png = Image.open("img/berlin.png")
budapest_png = Image.open("img/budapest.png")
london_png = Image.open("img/london.png")
paris_png = Image.open("img/paris.png")
rome_png = Image.open("img/rome.png")
vienna_png = Image.open("img/vienna.png")
lisbon_png = Image.open("img/lisbon.png")

# airbnbs
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

# plane and house of sidebar
plane_png = Image.open('img/plane.png')




#################################################################### DROPDOWNS #####################################################################################################################

## city dropdown
cities = df_full['city'].unique() # getting a list of all cities
city_dropdown = dcc.Dropdown(
                        id="city-dropdown",
                        options=[{'label': city.title(), 'value': city} for city in cities],
                        value=None,
                        optionHeight=35,
                        placeholder="Select a city",
                        clearable=True,
                        searchable= True,
                        style = {'width': '100%','height':'20%', 'font-size': 16 }
                    )


############################################################### RADIO ITEMS #########################################################################################################################


# selecting the time of the week
period_selector_2 = dcc.RadioItems(className='radio-container',
                        id = 'period-selector-2',
                        options = [
                                     {'label': 'Weekdays', 'value': 'weekdays'},
                                     {'label': 'Weekends', 'value': 'weekends'}
                                    ],
                        value='weekdays',

                        )


###################################################################### CARDS ####################################################################################################################

# card of the city with picture

city_card = dbc.Card([
    dbc.CardHeader(id='card-header', className='card-title',style={'font-size': 15, 'font-weight': 'bold'}),
    dbc.CardBody(id='card-content', className='card-subtitle'),
    dbc.CardImg(id='card-image'),
    html.Br()
])



#satisfaction and rating kpi

kpis_satisrate = dbc.Col([
html.Br(),
                    dbc.Row([html.H5('Guest Satisfaction', style={'font-size':15,'letter-spacing': '1.2px','text-transform': 'uppercase','align-text': 'center', 'justify-content':'center'}),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader('Lowest Average ', className='card-title', style={'font-size':15,'font-weight': 'bold', 'color':'#FF5C5C'}),
                            dbc.CardBody(['City: '+min_satis[0].title(),
                            html.Br(),
                             'Satisfaction: '+min_satis[1]], className='card-subtitle',style={'font-size':14}),
                            ], style={'borderColor': '#FF5C5C'}),
                            ], width=6),

                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader('Highest Average', className='card-title',style={'font-size':15,'font-weight': 'bold', 'color':'#2F4858'}),
                                dbc.CardBody(['City: '+ max_satis[0].title(),
                                html.Br(),
                                'Satisfaction: '+max_satis[1]], className='card-subtitle',style={'font-size':14}),
                                ], style={'borderColor': '#2F4858'}),

                    ], width=6),
            ], align='center', justify='center'),

    html.Br(),

    dbc.Row([html.Br()]),
                dbc.Row([  html.H5('Cleanliness Rating', style={'font-size':15,'letter-spacing': '1.2px','text-transform': 'uppercase','align-text': 'center', 'justify-content':'center'}),

                    dbc.Col([
                    dbc.Card([
                        dbc.CardHeader('Lowest Average', className='card-title', style={'font-size':15,'font-weight': 'bold', 'color':'#FF5C5C'}),
                        dbc.CardBody(['City: '+ min_clean[0].title(),
                        html.Br(),
                        'Rating: '+min_clean[1]], className='card-subtitle',style={'font-size':14})
                    ], style={'borderColor': '#FF5C5C'}),
]),
                    dbc.Col([

                        dbc.Card([
                            dbc.CardHeader('Highest Average', className='card-title',style={'font-size':15,'font-weight': 'bold', 'color':'#2F4858'}),
                            dbc.CardBody(['City: ' + max_clean[0].title(),
                                          html.Br(),
                                          'Rating: ' + max_clean[1]], className='card-subtitle',style={'font-size':14}),
                        ], style={'borderColor': '#2F4858'}, )

                    ])
            ])
])



kpis_price = dbc.Row([

dbc.Col([
    #################################### LOWEST PRICE ##############################################3
    dbc.Card([dbc.CardHeader('Lowest Airbnb Price', className='card-title',
                             style={'font-size': 15, 'font-weight': 'bold', 'color': '#FF5C5C'}), dbc.CardBody(
        [html.Div(['Price: ', html.Span(str(round(min_airbnb['realSum'].values[0], 2))+' €', style={'margin-left': '5px'}),
                   ], style={'margin-bottom': '5px'}),
         html.Div(['City: ' + min_airbnb['city'].values[0].title(),
                   ], style={'margin-bottom': '5px'}),
         html.Div(['Distance to the center: ',
                   html.Span(str(round(min_airbnb['dist'].values[0],1))+' Km', style={'margin-left': '5px'}),
                   ], style={'margin-bottom': '5px'}),
         html.Div(['Guest Satisfaction: ',
                   html.Span(str(round(min_airbnb['guest_satisfaction_overall'].values[0])) + '/100',
                             style={'margin-left': '5px'}),
                   ], style={'margin-bottom': '5px'}),
         html.Div(['Room Type: ' + min_airbnb['room_type'].values[0],
                   ], style={'margin-bottom': '0px'}),
         ], className='card-subtitle', style={'font-size': 14, 'padding-top': '15px'}),
              ], style={'borderColor': '#FF5C5C'}),
            ]),

    dbc.Col([
        dbc.Card([dbc.CardHeader('Highest Airbnb Price', className='card-title',
                                 style={'font-size': 15, 'font-weight': 'bold', 'color': '#2F4858'}), dbc.CardBody(
            [html.Div(['Price: ',
                       html.Span(str(round(max_airbnb['realSum'].values[0], 2)) + ' €', style={'margin-left': '5px'}),
                       ], style={'margin-bottom': '5px'}),
             html.Div(['City: ' + max_airbnb['city'].values[0].title(),
                       ], style={'margin-bottom': '5px'}),
             html.Div(['Distance to the center: ',
                       html.Span(str(round(max_airbnb['dist'].values[0], 1)) + ' Km', style={'margin-left': '5px'}),
                       ], style={'margin-bottom': '5px'}),
             html.Div(['Guest Satisfaction: ',
                       html.Span(str(round(max_airbnb['guest_satisfaction_overall'].values[0])) + '/100',
                                 style={'margin-left': '5px'}),
                       ], style={'margin-bottom': '5px'}),
             html.Div(['Room Type: ' + max_airbnb['room_type'].values[0],
                       ], style={'margin-bottom': '0px'}),
             ], className='card-subtitle', style={'font-size': 14, 'padding-top': '15px'}),
                  ], style={'borderColor': '#2F4858'}),
        ])
])

########################################################################## AIRBNB IMAGES CAROUSEL #################################################################################################


carousel = dbc.Carousel(
                    items=[
                        {"key": "2", "src": a2_png},
                        {"key": "3", "src": a3_png},
                        {"key": "4", "src": a4_png},
                        {"key": "7", "src": a7_png},
                        {"key": "8", "src": a8_png},
                        {"key": "9", "src": a9_png},
                        {"key": "10", "src": a10_png},
                        {"key": "12", "src": a12_png},
                        {"key": "18", "src": a18_png},
                        {"key": "19", "src": a19_png},
                        {"key": "20", "src": a20_png},
                        ],
                    controls=True,
                    indicators=False,
                    interval=3700,
                    ride="carousel",
                    style={"width": "500px", "height": "200px"}
                )



############################################################################### TABS #################################################################################################################



############################################################################ EUROPE ##############################################################################################################
europe_tab = dbc.Tab(label='Europe', tab_id='europe',
                     children=[
                        #### start! #############
                         dbc.Container([

                            html.Br(),
                             dbc.Row([
        ############################################################################# #1 ######################################################################################################
                                html.H5('How do Prices vary across Europe?', style={'text-align': 'left','letter-spacing': '1.5px','text-transform': 'uppercase'}), html.Hr(),
                                    ]),
############################################################################# #2 ######################################################################################################
                             dbc.Row([
                                 dbc.Col([
                                     dbc.Row(children=['''One of the most important aspects of an airbnb listing
                        is its price. In the map you can see how the prices are distributed across several cities in Europe
                        colored according to how much two nights cost for two people. The marker's size is 
                        proportional to the person capacity of all airbnb listings available in the city.
                        ''',html.Br() ,html.Br() ],style={'text-align': 'left', 'font-size': 14,'text-align': 'justify'}),

                                    dbc.Row([

                                        dbc.Col([kpis_price]),
                                       # dbc.Col([kpis_rating])
                                    ],justify='center'),
                                ], width=7),

                                dbc.Col([
                                    dcc.Graph(
                                        id='europe-graph',
                                        figure=get_highest_prices_map()
                                    )], width=4, style= {'pading':'1%'}),

                                dbc.Col([''], width=1)
                    ], className='g-5'),

############################################################################# #3 ######################################################################################################

                            dbc.Row([html.Br(),html.Br(),]),
                            dbc.Row([
                                html.Br(),
                                html.H5('Weekdays vs Weekends'),
                                            html.Br(),

                            ],style={'letter-spacing': '1 px','text-align': 'left'}),


############################################################################# #4 ######################################################################################################
                             dbc.Row(['Prices may differ if the listing is for two weekdays or a weekend.',html.Br(),html.Br()],
                                     style={'text-align': 'left', 'font-size': 14,}
                                     ),
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(id='dumbell')
                                        ], align='center')
                                    ]),


############################################################################# #5 ######################################################################################################
dbc.Row([html.Br(), html.Br(), html.Br()]),
                                dbc.Row([
                                html.Br(),

                                html.H5('How does Cleanliness Rating affects Guest Satisfaction?', style={'text-align': 'left','letter-spacing': '1.5px','text-transform': 'uppercase'}), html.Hr(),
                                    ]),


    ############################################################################# #6 ######################################################################################################

                                dbc.Row([
                                    dbc.Col([
                                    dcc.Graph(id='boxplot', figure=boxplot())
                                            ], width=7),

                                    dbc.Col([kpis_satisrate
                                            ], width=5)

                                        ], className="g-0"),

    ############################################################################# #7 ######################################################################################################
dbc.Row([html.Br(), html.Br(), html.Br()]),
dbc.Row([
                                html.Br(),

                                html.H5('How do the average attraction and restaurant indexes change across Europe?', style={'text-align': 'left','letter-spacing': '1.5px','text-transform': 'uppercase'}), html.Hr(),
                                    ]),
                             dbc.Row(['Attraction and Restaurant indexes are metrics to measure how well surrounded by attractions and restaurant the airbnb listings are, according to reviews of these places and distance to a certain airbnb.', html.Br(),
                                      html.Br()],
                                     style={'text-align': 'left', 'font-size': 14, 'text-align': 'justify'}
                                     ),

                                dbc.Row([
                                    dcc.Graph(id='index-barchart'
                                              )
                                ])
                             ])
                         ])




######################################################################### CITY #################################################################################################33


city_tab = dbc.Tab(label='City', tab_id='city',
                   children=[
                       dbc.Container([
############################################################################## #1 #########################################################################################################
                           dbc.Row([ html.Br(),]),


                           dbc.Row([
                            dbc.Alert("Don't forget to select a city before coming here!", color="danger", class_name='text-center', style = {'width': '100%', 'font-size':16}),
                           ]),
                           dbc.Row([
                                html.Br(),

                                html.H5(['How are prices distributed across ',
                                         html.Span('Amsterdam', id='city-title'),'?'], style={'text-align': 'left','letter-spacing': '1.5px','text-transform': 'uppercase'}), html.Hr(),
                                    ]),

############################################################################## #2 #########################################################################################################
                           dbc.Row([html.Label('You can select the time of the week here:'),
                                    period_selector_2, ]),

############################################################################## #3 #########################################################################################################
                           dbc.Row([
                               dbc.Col([
                                   dbc.Row([
                                       dcc.Graph(id='scattermap')
                                   ])
                               ], width=7),

                               dbc.Col([''], width=1),

                               dbc.Col([

dbc.Row(['The map on the left has each airbnb location as marker colored by price and with size proportional to its person capacity. You might need to click on the zoom buttons to show the entire map.', html.Br(),
                                      html.Br()],
                                     style={'text-align': 'left', 'font-size': 14,'text-align': 'justify' }
                                     ),

                                       dbc.Row([city_card])

                                   ])

                         ]),

############################################################################## #4 #########################################################################################################
                            dbc.Row([html.Br()]),
dbc.Row([
                                html.Br(),
    dbc.Row([html.Br()]),

                                html.H5(['How do the Attraction and Restaurant Indexes of ',
                                            html.Span('Amsterdam', id='city-title2'),' change with distance to its center?'], style={'text-align': 'left','letter-spacing': '1.5px','text-transform': 'uppercase'}), html.Hr(),
                                    ]),

dbc.Row(['Attraction and Restaurant indexes are metrics to measure how well surrounded by attractions and restaurant the airbnb listings are, according to reviews of these places and distance to a certain airbnb.', html.Br(),
                                      html.Br()],
                                     style={'text-align': 'left', 'font-size': 14, 'text-align': 'justify'}
                                     ),

                            dbc.Row([

                               dbc.Col([
                                   dbc.Row([
                                       html.Br(),
                                       html.H5('Attraction Index'),
                                       html.Br(),

                                   ], style={'letter-spacing': '1 px', 'text-align': 'left'}),

                                   dcc.Graph(id='scatter_index_attr')], width=8),

                                dbc.Col([dcc.Graph(id='attr_avg')], width=4,
                                        style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                                        )

                           ]),
############################################################################## #5 #########################################################################################################
                           dbc.Row([html.Br()]),

                           dbc.Row([

                               dbc.Col([dbc.Row([
                                       html.Br(),
                                       html.H5('Restaurant Index'),
                                       html.Br(),

                                   ], style={'letter-spacing': '1 px', 'text-align': 'left'}),


                                   dcc.Graph(id='scatter_index_res')], width=8),

                               dbc.Col([dcc.Graph(id='rest_avg')], width=4,
                                      style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                                       )

                           ])
############################################################################## #6 #########################################################################################################
                           ])
                       ])















################################################################################### APP #######################################################################################################################################################

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}],
                )

server =app.server
######################################################################### APP LAYOUT ################################################################################################################################

app.layout = html.Div([
    dbc.Container([

######################################### SIDE BAR ###############################################################################################################################################################3

                dbc.Col([
                            html.Div(
                                [html.Img(src=pil_image,style={'width':'100%'})],
                            style={'background-color': '#FF5C5C'}),
                            html.Div([
                            html.Blockquote([about_airbnb], style =  {'color': 'white' }),
                            ], style={'text-align': 'justify', 'font-size':'14px', 'padding-left':'3%', 'padding-right':'4%', 'display':'flex'}),
                            html.Div(
                                [html.Img(src=plane_png, style={'width':'60%','justify-content':'center', 'align-items':'center' })],
                            style={'background-color': '#FF5C5C','justify-content':'center', 'align-items':'center','margin-left':'50px'}),

                ], align = 'center',
                    style= {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#FF5C5C"
,
}    ),


###########################################################################      MAIN     ################################################################################################33

                dbc.Col([
                    dbc.Row([
                        html.H2(['Airbnb listings in European cities'], style ={'letter-spacing': '1.5px','font-weight': 'bold','text-transform': 'uppercase', 'align-text': 'center',
                                                                                         'display':'flex','height': '100%', 'color':'#FF5C5C', 'justify-content':'center'} ),
                            ], style={'background-color': 'white', 'padding-top': '2.5rem'}),

                    html.Br(),
                    html.Br(),

                    dbc.Row([

                        dbc.Col([
                            dbc.Card(dbc.CardBody([
                                        "This dashboard explores some characteristics of Aribnb listings in 10 european cities. Here you'll be able to find information about prices, locations and more.",
                                        html.Br(),
                                        html.Br(),
                                        "\nThe Tab 'Europe' shows information about all of the cities. If you want to see some details about a specific city, you can select a city in the dropdown below.\n As soon as you do that, some graphs in the 'Europe' Tab will change, and you'll be able to know more details if you click on the 'City' tab.",
                                        html.Br(),
                                        html.Br(),
                                        city_dropdown,
                                        html.Br(),

                            ], style = {'justify-content':'center','align-items':'center','text-align': 'justify'}),
                                        style={'width': '100%', 'height':'100%', 'font-size': 15}
                                    )], width = 5, style= {'align-items':'center', 'justify-content':'center'}),


                        dbc.Col([
                            html.Div([carousel])], width = 6 )
                                ],   justify = 'center',
                            ),
                    dbc.Row([html.Br(), html.Br()]),

                    dbc.Row([


                    dbc.Tabs([europe_tab,city_tab])

                    ]),
dbc.Row([html.Br(), html.Br(), html.Br(),html.Br(), html.Br(), html.Br()]),
    dbc.Row([
        html.Label('Data Visualization Project - 2023'),
        html.Br(),
        html.Label('Authors:\n'
                   'Adriana Monteiro - 20220604,\n'
                   'Eduardo Palma - 20221022,\n'
                   'José Ramirez Fernandes - 20220641,\n'
                   'Pedro Nuno Ferreira - 20220589\n')
    ], style={'font-size':12})
 ], style={
    'width':'64rem',
    "margin-left": "15rem",
    "margin-right": "8rem",
    "padding": "2rem 1rem",
}),


]),



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
    Output('scatter_index_res', 'figure'),],
    Input('city-dropdown', 'value')
)

def update_scatters(city):
    if city is None:
        city = 'amsterdam'

    plot_attr = scatter_attr(city)
    plot_res = scatter_res(city)


    return plot_attr, plot_res


@app.callback(
    [Output('attr_avg', 'figure'),
    Output('rest_avg', 'figure')],
    Input('city-dropdown', 'value')
)

def update_avgs(city):

    if city is None:
        city = 'amsterdam'


    plot_attr_avg = attr_avg_plot(city)
    plot_rest_avg = rest_avg_plot(city)

    return plot_attr_avg, plot_rest_avg

@app.callback(
    Output('city-title', 'children'),
Output('city-title2', 'children'),
    [Input('city-dropdown', 'value')])

def update_text(city):
    if city is None:
        city = 'amsterdam'
    return city.title(),city.title()




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
        image1 = budapest_png

    elif city == 'london':

        title = 'London',
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
        image1 = vienna_png

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
