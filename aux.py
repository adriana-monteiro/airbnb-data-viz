import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px


df_full = pd.read_csv('df_full.csv')

df_full['realSum_log'] = df_full['realSum'].apply(lambda x: np.log10(x))

for col in [df_full]:
    # cleanliness_rating
    col.loc[(col['cleanliness_rating'] >= 9.0), 'clean_rating'] = 'great'
    col.loc[(col['cleanliness_rating'] >= 7.0) & (col['cleanliness_rating'] <= 8.0), 'clean_rating'] = 'very good'
    col.loc[(col['cleanliness_rating'] <= 6.0), 'clean_rating'] = 'reasonable'

    # guest_satisfaction_overall
    col.loc[(col['guest_satisfaction_overall'] >= 90.0), 'overall_rating'] = 'Excellent'
    col.loc[(col['guest_satisfaction_overall'] >= 70.0) & (
                col['guest_satisfaction_overall'] <= 89.0), 'overall_rating'] = 'Very good'
    col.loc[(col['guest_satisfaction_overall'] <= 69.0), 'overall_rating'] = 'Reasonable'

def get_plotting_zoom_level_and_center_coordinates_from_lonlat_tuples(longitudes=None, latitudes=None):
    """Function documentation:\n
    Basic framework adopted from Krichardson under the following thread:
    https://community.plotly.com/t/dynamic-zoom-for-mapbox/32658/7

    # NOTE:
    # THIS IS A TEMPORARY SOLUTION UNTIL THE DASH TEAM IMPLEMENTS DYNAMIC ZOOM
    # in their plotly-functions associated with mapbox, such as go.Densitymapbox() etc.

    Returns the appropriate zoom-level for these plotly-mapbox-graphics along with
    the center coordinate tuple of all provided coordinate tuples.
    """

    # Check whether both latitudes and longitudes have been passed,
    # or if the list lenghts don't match
    if ((latitudes is None or longitudes is None)
            or (len(latitudes) != len(longitudes))):
        # Otherwise, return the default values of 0 zoom and the coordinate origin as center point
        return 0, (0, 0)

    # Get the boundary-box
    b_box = {}
    b_box['height'] = latitudes.max()-latitudes.min()
    b_box['width'] = longitudes.max()-longitudes.min()
    b_box['center']= (np.mean(longitudes), np.mean(latitudes))

    # get the area of the bounding box in order to calculate a zoom-level
    area = b_box['height'] * b_box['width']

    # * 1D-linear interpolation with numpy:
    # - Pass the area as the only x-value and not as a list, in order to return a scalar as well
    # - The x-points "xp" should be in parts in comparable order of magnitude of the given area
    # - The zpom-levels are adapted to the areas, i.e. start with the smallest area possible of 0
    # which leads to the highest possible zoom value 20, and so forth decreasing with increasing areas
    # as these variables are antiproportional
    zoom = np.interp(x=area,
                     xp=[0, 5**-10, 4**-10, 3**-10, 2**-10, 1**-10, 1**-5],
                     fp=[20, 15,    14,     13,     12,     7,      5])

    # Finally, return the zoom level and the associated boundary-box center coordinates
    return zoom, b_box['center']



about_airbnb = "Airbnb is an online marketplace founded in 2008 for people who want to rent their homes for a short period of time and for those " \
                "who are looking for accodations in a specific place." \
                'Europe, known for its restaurants, museums and architecture, has always been one the most sought-out destinations to visit. ' \
                'So, the two of them are a very good match for whomever is looking to have a nice vacation'



# function for scattermaps
def scattermapbox_price(city_, period_):
    values = df_full[(df_full['city'] == city_) & (df_full['period'] == period_)]['realSum_log'].values

    # print(values)

    num_ticks = 6
    tick_values = np.linspace(min(values), max(values), num=num_ticks)

    nonlog_tick_values = np.power(10, tick_values)


    # defining zoom and center
    zoom, center = get_plotting_zoom_level_and_center_coordinates_from_lonlat_tuples(
        df_full[(df_full['city'] == city_) & (df_full['period'] == period_)]['lat'],
        df_full[(df_full['city'] == city_) & (df_full['period'] == period_)]['lng']
    )

    # Define the scattermapbox trace and layout
    scattermap = dict(
        type='scattermapbox',
        lat=df_full[(df_full['city'] == city_) & (df_full['period'] == period_)]['lat'],
        lon=df_full[(df_full['city'] == city_) & (df_full['period'] == period_)]['lng'],
        hovertext=df_full[(df_full['city'] == city_) & (df_full['period'] == period_)].apply(
            lambda
                row: f"Price: {row['realSum']:.2f} €<br>Person Capacity: {row['person_capacity']}",
            axis=1),
        mode='markers',
        name='Airbnb properties',
        marker=dict(
            color=df_full[(df_full['city'] == city_) & (df_full['period'] == period_)]['realSum_log'],
            colorscale=['#FF5A5F', '#DC5086', '#A65699', '#6B5A94', '#3E547B', '#484848'],
            colorbar=dict(title=dict(text='Price <br>&nbsp;'),
                          xanchor = 'left',
                          orientation = 'v',
                          tickvals=tick_values,
                          tickmode='array',
                          tickfont=dict(size=12),
                          ticktext=[str(round(i)) + ' €' for i in nonlog_tick_values]),
            size=df_full[(df_full['city'] == city_) & (df_full['period'] == period_)]['person_capacity'],
            sizemode='diameter',
            sizeref=0.4,
            sizemin=1
        ),
        hovertemplate='%{hovertext}',
    )

    layout_scattermap = dict(
        mapbox=dict(
            style='carto-positron',
            center=dict(lat=center[0], lon=center[1]),
            zoom=zoom,
        ),
      #  title=dict(text=f'Logarithm of Airbnb Prices in {city_.title()} during the {period_}', x=.5),
        width=600,
        height=400,
        margin={'l': 1, 'r': 1, 't': 1, 'b': 1},
    )

    return scattermap, layout_scattermap


def scattermapbox_rating(city_, period_):
    #     Define the color mapping dictionary
    color_map = {
        'Very good': '#E0FF4F',
        'Excellent': '#5F8D4E',
        'Reasonable': '#F0544F'
    }

    colors_ = list(color_map.values())
    labels_ = list(color_map.keys())
    # # Map the color for each row
    colors = [color_map[rating] for rating in df_full['overall_rating']]

    # zoom and center

    zoom, center = get_plotting_zoom_level_and_center_coordinates_from_lonlat_tuples(
        df_full[(df_full['city'] == city_) & (df_full['period'] == period_)]['lat'],
        df_full[(df_full['city'] == city_) & (df_full['period'] == period_)]['lng']
    )

    # scatter

    scattermap_review = dict(
        type='scattermapbox',
        lat=df_full[(df_full['city'] == city_) & (df_full['period'] == period_)]['lat'],
        lon=df_full[(df_full['city'] == city_) & (df_full['period'] == period_)]['lng'],
        hovertext=df_full[(df_full['city'] == city_) & (df_full['period'] == period_)].apply(
            lambda
                row: f"Rating: {row['overall_rating']}<br>Room Type: {row['room_type']}<br>Bedrooms: {row['bedrooms']}",
            axis=1),
        mode='markers',
        name='Airbnb properties',
        marker=dict(
            color=colors,

        ),

        hovertemplate='%{hovertext}',
    )

    layout_scattermap_review = dict(
        mapbox=dict(
            style='carto-positron',
            center=dict(lat=center[0], lon=center[1]),
            zoom=zoom,
        ),
        title=dict(text=f'Airbnb overall ratings in {city_.title()} during the {period_}', x=.5),
        width=1000,
        height=800)

    return scattermap_review, layout_scattermap_review


def which_color(city, cities):
    city_id = np.where(cities == city)[0][0]
    #  print(city_id)

    colors_red = []
    colors_blue = []
    colors_line = []

    for index in range(len(cities)):
        if index == city_id:
            colors_red.append('#FF5C5C')
            colors_blue.append('#2F4858')
            colors_line.append('black')
        else:
            colors_red.append('grey')
            colors_blue.append('grey')
            colors_line.append('grey')

    return colors_red, colors_blue, colors_line


def which_size(city, cities):
    city_id = np.where(cities == city)[0][0]
    # print(city_id)

    sizes = []
    # sizes_blue  =[]
    # sizes_line = []

    for index in range(len(cities)):
        if index == city_id:
            sizes.append(12)
        else:
            sizes.append(10)
            # sizes_blue.append('#d3d3d3')
        #  sizes_line.append('#d3d3d3')

    return sizes




def preattentive_dumbell(city_, preattentive):
    if preattentive and city_ is not None:
        cities = df_full['city'].unique()

        data = {"line_x": [], "line_y": [], "weekdays": [], "weekends": []}

        for city in cities:
            data["weekdays"].extend(
                [df_full.loc[(df_full.period == 'weekdays') & (df_full.city == city)]["realSum"].mean()])
            data["weekends"].extend(
                [df_full.loc[(df_full.period == "weekends") & (df_full.city == city)]["realSum"].mean()])
            data["line_x"].extend(
                [
                    df_full.loc[(df_full.period == 'weekdays') & (df_full.city == city)]["realSum"].mean(),
                    df_full.loc[(df_full.period == "weekends") & (df_full.city == city)]["realSum"].mean(),
                    None,
                ]
            )
            data["line_y"].extend([city, city, None]),

        fig = go.Figure(
            data=[
                go.Scatter(
                    x=data["line_x"],
                    y=data["line_y"],
                    mode="lines",
                    name='City',
                    showlegend=False,
                    marker=dict(
                        color='grey',
                    ),
                    hovertemplate=''

                ),
                go.Scatter(
                    x=data["weekdays"],
                    y=cities,
                    mode="markers",
                    name="Weekdays",
                    showlegend=False,
                    marker=dict(
                        color=which_color(city_, cities)[0],
                        size=which_size(city_, cities),
                        opacity=1
                    ),
                    hovertemplate='%{x:.0f}€'

                ),
                go.Scatter(
                    x=data["weekends"],
                    y=cities,
                    mode="markers",
                    name="Weekends",
                    showlegend=False,
                    marker=dict(
                        color=which_color(city_, cities)[1],
                        size=which_size(city_, cities),
                        opacity=1
                    ),
                    hovertemplate='%{x:.0f}€'

                ),

                go.Scatter(x=[None], y=[None], mode='markers',
                           marker=dict(size=10, color='#FF5C5C'),
                           legendgroup='Buy', showlegend=True, name='Weekdays'),

                go.Scatter(x=[None], y=[None], mode='markers',
                           marker=dict(size=10, color='#2F4858'),
                           legendgroup='Buy', showlegend=True, name='Weekends')
            ]
        )

        fig.update_layout(
            # title="Difference of Average Prices between",
            height=540,
            width=1000,
            legend_itemclick=False,
            yaxis=dict(categoryorder='total descending', title =dict(font=dict(size=12)),tickfont = dict(size=14)),
           template='simple_white',
            xaxis=dict(title=dict(text = 'Price (€)', font = dict(size=12)),tickfont = dict(size=14)),
            hovermode="x unified",
            hoverlabel = dict(align="left", namelength=-1, font=dict(size=12)),
            margin={'t': 1, 'b': 1},
            font=dict(family='sans-serif semibold'),
            legend=dict(
                font=dict(size=14),
                yanchor="top",
                y=0.8,
                xanchor="right",
                x=0.92,
                itemclick=False,
                itemdoubleclick=False
            )
        )

        fig.update_yaxes(ticktext=[city.title() for city in cities], tickvals=cities)



    else:
        cities = df_full['city'].unique()

        data = {"line_x": [], "line_y": [], "weekdays": [], "weekends": []}

        for city in cities:
            data["weekdays"].extend(
                [df_full.loc[(df_full.period == 'weekdays') & (df_full.city == city)]["realSum"].mean()])
            data["weekends"].extend(
                [df_full.loc[(df_full.period == "weekends") & (df_full.city == city)]["realSum"].mean()])
            data["line_x"].extend(
                [
                    df_full.loc[(df_full.period == 'weekdays') & (df_full.city == city)]["realSum"].mean(),
                    df_full.loc[(df_full.period == "weekends") & (df_full.city == city)]["realSum"].mean(),
                    None,
                ]
            )
            data["line_y"].extend([city, city, None]),

        fig = go.Figure(
            data=[
                go.Scatter(
                    x=data["line_x"],
                    y=data["line_y"],
                    mode="lines",
                    name='City',
                    showlegend=False,
                    marker=dict(
                        color="grey"
                    ),
                    hovertemplate=''

                ),
                go.Scatter(
                    x=data["weekdays"],
                    y=cities,
                    text='wow',
                    mode="markers",
                    name="Weekdays",
                    marker=dict(
                        color="#FF5C5C",
                        size=10
                    ),
                    hovertemplate='%{x:.0f}€'

                ),
                go.Scatter(
                    x=data["weekends"],
                    y=cities,
                    mode="markers",
                    name="Weekends",
                    marker=dict(
                        color="#2F4858",
                        size=10
                    ),
                    hovertemplate='%{x:.0f}€'

                ),
            ]
        )

        fig.update_layout(
            height=540,
            width=1000,
            legend_itemclick=False,
            yaxis=dict(categoryorder='total descending', title =dict(font=dict(size=12)), tickfont = dict(size=14)),
           template='simple_white',
            xaxis=dict(title=dict(text = 'Price (€)', font = dict(size=14)),tickfont = dict(size=14)),
            hoverlabel=dict(align="left", namelength=-1,font=dict(size=12)),
            margin={'t': 1, 'b': 1},
            hovermode="x unified",
            font=dict(family='sans-serif semibold'),
            legend=dict(
                font=dict(size=14),
                yanchor="top",
                y=0.8,
                xanchor="right",
                x=0.92,
                itemclick=False,
                itemdoubleclick=False))

        fig.update_yaxes(ticktext=[city.title() for city in cities], tickvals=cities)
        # fig.update_layout(hovermode="x unified")

    return fig



grouped_res_avg = df_full.groupby('city')['rest_index_norm'].mean()
grouped_res_avg.sort_index(inplace =True, ascending=False)
grouped_attr_avg = df_full.groupby('city')['attr_index_norm'].mean()
grouped_attr_avg.sort_index(inplace =True, ascending=False)


def butterflyplot(city, cities, preattentive=False):

    if preattentive:

        fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=False,
                            shared_yaxes=True, horizontal_spacing=0,
                            vertical_spacing=0)  # Set the height of the second row to 1/5 of the height of the first row

        fig.append_trace(go.Bar(x=grouped_attr_avg.values,
                                y=[i.title() for i in grouped_attr_avg.index],
                                text=grouped_attr_avg.values,
                                # Display the numbers with thousands separators in hover-over tooltip
                                textposition='outside',
                                hovertext=[i.title() for i in grouped_attr_avg.index],
                                orientation='h',
                                width=0.7,
                                name="Attraction Index    ",
                                texttemplate='%{text:.2f}%  ',
                                textfont=dict(size=14),
                                showlegend=True,
                                marker=dict(color=which_color(city, cities)[0],
                                            line=dict(
                                                color='#FF5A5F',
                                                width=2)
                                            )
                                ),
                         1, 1)  # 1,1 represents row 1 column 1 in the plot grid

        fig.append_trace(go.Bar(x=grouped_res_avg.values,
                                y=[i.title() for i in grouped_attr_avg.index],
                                text=grouped_res_avg.values,
                                textposition='outside',
                                orientation='h',
                                width=0.7,
                                hovertext=[i.title() for i in grouped_attr_avg.index],
                                name="Restaurant Index      ",
                                showlegend=True,
                                texttemplate='  %{text:.2f}%',
                                textfont=dict(size=14),
                                marker=dict(color=which_color(city, cities)[1],
                                            line=dict(
                                                color='#2F4858',
                                                width=2)
                                            ),
                                ),
                         1, 2)  # 1,2 represents row 1 column 2 in the plot grid

        fig.update_xaxes(showticklabels=False, row=1, col=1, range=[50, 0])
        fig.update_xaxes(showticklabels=False, row=1, col=2, range=[0, 50])

        fig.update_layout(
                          margin=dict(l=10, r=0, t=15, b=5),
                          width=900,
                          height=500,
                          title_x=0.5,
                          title_y=0.94,
                          font=dict(family='sans-serif semibold', size=16),
                          paper_bgcolor='rgb(255, 255, 255)',
                          plot_bgcolor='rgb(255, 255, 255)',
            template='simple_white',
                          legend=dict(font=dict(
                              size=14),
                              yanchor="top",
                              # orientation='h',
                              y=1,
                              xanchor="left",
                              x=0.9
                          )
                          )

    else:

        fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=False,
                            shared_yaxes=True, horizontal_spacing=0,
                            vertical_spacing=0)  # Set the height of the second row to 1/5 of the height of the first row

        fig.append_trace(go.Bar(x=grouped_attr_avg.values,
                                y=[i.title() for i in grouped_attr_avg.index],
                                text=grouped_attr_avg.values,
                                # Display the numbers with thousands separators in hover-over tooltip
                                textposition='outside',
                                hovertext=[i.title() for i in grouped_attr_avg.index],
                                orientation='h',
                                width=0.7,
                                name="Attraction Index    ",
                                texttemplate='%{text:.2f}%  ',
                                textfont=dict(size=14),
                                showlegend=True,
                                marker=dict(color='#FF5A5F',
                                            line=dict(
                                                color='#FF5A5F',
                                                width=1)
                                            )
                                ),
                         1, 1)  # 1,1 represents row 1 column 1 in the plot grid

        fig.append_trace(go.Bar(x=grouped_res_avg.values,
                                y=[i.title() for i in grouped_attr_avg.index],
                                text=grouped_res_avg.values,
                                textposition='outside',
                                orientation='h',
                                width=0.7,
                                hovertext=[i.title() for i in grouped_attr_avg.index],
                                name="Restaurant Index       ",
                                showlegend=True,
                                texttemplate='  %{text:.2f}%',
                                textfont=dict(size=14),
                                marker=dict(color='#2F4858',
                                            line=dict(
                                                color='#2F4858',
                                                width=1)
                                            ),
                                ),
                         1, 2)  # 1,2 represents row 1 column 2 in the plot grid

        fig.update_xaxes(showticklabels=False, row=1, col=1, range=[50, 0])
        fig.update_xaxes(showticklabels=False, row=1, col=2, range=[0, 50])

        fig.update_layout(
                          margin=dict(l=5, r=0, t=15, b=5),
                          width=900,
                          height=500,
                          title_x=0.5,
                          title_y=0.94,
                          font=dict(family='sans-serif semibold', size=14),
                          paper_bgcolor='rgb(255, 255, 255)',
                          plot_bgcolor='rgb(255, 255, 255)',
            template='simple_white',
                          legend=dict(font=dict(
                              size=14),
                              yanchor="top",
                              # orientation='h',
                              y=1,
                              xanchor="left",
                              x=0.9
                          )
                          )
    return fig


def boxplot():
    y = df_full['guest_satisfaction_overall']
    x = df_full['cleanliness_rating']

    data = dict(type='box',
                x=x,
                y=y,
                name='Rating vs cleanliness boxplot',
                marker_color='#6B5A94',
                opacity=1
                )

    layout = dict(
                  xaxis=dict(title='Cleanliness Rating',tickmode='linear'),
                  yaxis=dict(title='Guest Satisfaction'),
                  font=dict(family='sans-serif semibold', size=14),
                  paper_bgcolor='rgb(255, 255, 255)',
                  plot_bgcolor='rgb(255, 255, 255)',
                  margin={'l': 5, 'r':5, 't': 5, 'b': 5},
                  height = 400,
                  width = 550,
        template='simple_white'
                  )

    fig = go.Figure(data=data, layout=layout)

    return fig


def scatter_res(city):

    trace = dict(type='scatter',
                 x=df_full[df_full.city == city]['dist'],
                 y=df_full[df_full.city == city]['rest_index_norm'],
                 name='Attraction Index',
                 mode='markers',
                 opacity=0.8,
                 marker=dict(color='#6B5A94')
                 )

    layout = dict( margin={"t": 5},
                xaxis = dict(title='Distance to center', autorange = 'reversed'),
                yaxis = dict(title='Index'),
                  font=dict(family='sans-serif semibold', size=14),
                  paper_bgcolor='rgb(255, 255, 255)',
                  plot_bgcolor='rgb(255, 255, 255)',
    template = 'simple_white',
    width = 600,
    height = 400
    )


    fig = go.Figure(data=trace, layout=layout)

    return fig

def scatter_attr(city):
    trace = dict(type='scatter',
                 x=df_full[df_full.city == city]['dist'],
                 y=df_full[df_full.city == city]['attr_index_norm'],
                 name='Attraction Index',
                 mode='markers',
                 opacity=0.8,
                 marker=dict(color='#6B5A94')
                 )

    layout = dict( margin={"t": 5},
                xaxis = dict(title='Distance to center',autorange = 'reversed'),
                yaxis = dict(title='Index'),
                  font=dict(family='sans-serif semibold', size=14),
                  paper_bgcolor='rgb(255, 255, 255)',
                  plot_bgcolor='rgb(255, 255, 255)',
                  template='simple_white',
                height = 400,
                width = 600
    )


    fig = go.Figure(data=trace, layout=layout)

    return fig



def get_highest_prices_map():

    ticks = [200,250,300,350,400,450,500,550]

    colorscale = ['#FF5A5F', '#DC5086', '#A65699', '#6B5A94', '#3E547B', '#484848']
    # Calculate the highest prices and person capacity per city
    highest_price = df_full.groupby('city').mean().reset_index()
    highest_price["person_capacity_sum"] = df_full.groupby('city')["person_capacity"].sum().values
    #highest_price['city'] = highest_price.index
    # # Map the cities to countries
    # highest_price['country'] = highest_price['city'].map(city_to_country)


    #num_ticks = 6
    #tick_values = np.linspace(min(values), max(values), num=num_ticks)

    #nonlog_tick_values = np.power(10, tick_values)

    fig = px.scatter_mapbox(highest_price, lat="lat", lon="lng", hover_data=["city","person_capacity_sum", "realSum"],
                            color="realSum", zoom=2.5, size="person_capacity_sum", size_max=30, width=900,
                            color_continuous_scale=colorscale)

    fig.update_traces(hovertemplate='<b>City: %{customdata[0]}</b><br>Price: %{customdata[2]:.2f} €\
                      <br>Person Capacity: %{customdata[1]}<br>')

    fig.update_layout(mapbox_style="carto-positron",
                      margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      height=300,
                      width=415,
                      coloraxis_colorbar= dict(
                          title = 'Average</b><br>Price',
                            tickmode = 'array',
                                   tickvals = ticks,
                                   ticktext = [str(i)+'€' for i in ticks])
                      )



    return fig




grouped_satisfaction = df_full.groupby('city')['guest_satisfaction_overall'].mean().sort_values()

min_satis = (grouped_satisfaction.index[0], str(round(grouped_satisfaction[0]))+'/100')

max_satis = (grouped_satisfaction.index[-1], str(round(grouped_satisfaction[-1]))+'/100')


grouped_clean = df_full.groupby('city')['cleanliness_rating'].mean().sort_values()

min_clean = (grouped_clean.index[0], str(round(grouped_clean[0],2))+'/10')

max_clean = (grouped_clean.index[-1], str(round(grouped_clean[-1],2))+'/10')



max_airbnb = df_full[(df_full['realSum'] == df_full['realSum'].max())]

min_airbnb = df_full[(df_full['realSum'] == df_full['realSum'].min())]


def attr_avg_plot(city):
    if city is not None:


        avg_att = df_full['attr_index_norm'].mean()
        avg_cities = df_full.groupby('city')['attr_index_norm'].mean()

        trace_att_city = go.Scatter(
            x=[avg_cities[city]],
            y=[0],
            name=str(city).title()+" Average Attraction Index",
            mode='markers',
            marker=dict(size=20, color='#FF5A5F')
        )
        trace_att_avg = go.Scatter(
            x=[avg_att],
            y=[0],
            name="Europe Average Attraction Index",
            mode='markers',
            marker=dict(size=20, color='#484848')
        )


        fig = go.Figure(data=[trace_att_city, trace_att_avg])
        #fig.add_trace(trace_att)
        fig.update_xaxes(showgrid=False, range=[avg_att - 9, avg_att + 9])
        fig.update_yaxes(showgrid=False,
                         zeroline=True, zerolinecolor='grey', zerolinewidth=4,
                         showticklabels=False)
        fig.update_layout(
            height=200, width=600, plot_bgcolor='white', legend=dict(
            orientation='h',
            yanchor='bottom',
            y=3,
            xanchor='right',
            x=0.5,
            font=dict(size=12)))

        return fig


def rest_avg_plot(city):

    if city == 'paris':
        print('got it')

        print(df_full.groupby('city')['rest_index_norm'].mean())


    if city is not None:

        avg_rest = df_full['rest_index_norm'].mean()
        avg_cities_rest = df_full.groupby('city')['rest_index_norm'].mean()

        trace_att_city = go.Scatter(
                x=[avg_cities_rest[city]],
            y=[0],
            name=str(city).title()+" Average Restaurant Index",
            mode='markers',
            marker=dict(size=20, color='#FF5A5F')
        )
        trace_att_avg = go.Scatter(
            x=[avg_rest],
            y=[0],
            name = "Europe Average Restaurant Index",
            mode='markers',
            marker=dict(size=20, color='#484848')
        )

        fig = go.Figure(data=[trace_att_city, trace_att_avg])
       # fig.add_trace(trace_att)
        fig.update_xaxes(showgrid=False, range=[avg_rest - 21, avg_rest + 21])
        fig.update_yaxes(showgrid=False,
                         zeroline=True, zerolinecolor='grey', zerolinewidth=4,
                         showticklabels=False)
        fig.update_layout(height=200, width=600, plot_bgcolor='white',legend=dict(
                          orientation='h',
                          yanchor='bottom',
                          y=3,
                          xanchor='right',
                          x=0.5,
                          font=dict(size=12)))

    return fig