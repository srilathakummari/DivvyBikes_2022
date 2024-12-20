import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image
import os

########################### Initial settings for the dashboard ####################################################


st.set_page_config(page_title = 'Divvy Bikes Strategy Dashboard', layout='wide')
st.title("Divvy Bikes Strategy Dashboard")

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page","Weather component and bike usage",
   "Most popular stations",
    "Interactive map with aggregated bike trips", "Recommendations"])

########################## Import data ###########################################################################################

df = pd.read_csv('Data/reduced_data_to_plot_7.csv', index_col = 1)
top20 = pd.read_csv('Data/top20.csv', index_col = 2)

######################################### DEFINE THE PAGES #####################################################################


### Intro page

if page == "Intro page":
    st.markdown("#### This dashboard aims at providing helpful insights on the expansion problems Divvy Bikes currently faces.")
    st.markdown("Right now, Divvy bikes runs into a situation where customers complain about bikes not being available at certain times. This analysis will look at the potential reasons behind this. The dashboard is separated into 4 sections:")
    st.markdown("- Most popular stations")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")

    image_path = os.path.join(os.getcwd(), "img", "Intropageimage.jpg")
    
    myImage = Image.open(image_path) 
    st.image(myImage)



    ### Create the dual axis line chart page ###
    
elif page == 'Weather component and bike usage':

    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])
    fig_2.add_trace(
    go.Scatter(x = df['date'], y = df['bike_rides_daily_x'], name = 'Daily bike rides', marker={'color': df['bike_rides_daily_x'],'color': 'blue'}),
        secondary_y = False
        )
    
    fig_2.add_trace(go.Scatter(x=df['date'], y = df['avgTemp'], name = 'Daily temperature', marker={'color': df['avgTemp'],'color': 'red'}),
        secondary_y=True
        )
    fig_2.update_layout(
        title = 'Daily bike trips and temperatures in 2022',
        height = 400
        )
    
    st.plotly_chart(fig_2, use_container_width=True)
    st.markdown("There is an obvious correlation between the rise and drop of temperatures and their relationship with the frequency of bike trips taken daily. As temperatures plunge, so does bike usage. This insight indicates that the shortage problem may be prevalent merely in the warmer months, approximately from May to October.")

### Most popular stations page

    # Create the season variable

elif page == 'Most popular stations':
    
    # Create the filter on the side bar
    
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season', options=df['season'].unique(),
    default=df['season'].unique())
    
    df1 = df.query('season == @season_filter')
    
    # Define the total rides
    total_rides = float(df1['bike_rides_daily_x'].count())    
    st.metric(label = 'Total Bike Rides', value= numerize(total_rides))
    
    # Bar chart
    df1['value'] = 1
    df_groupby_bar = df1.groupby('start_station_name', as_index = False).agg({'value': 'sum'}) 
    top20 = df_groupby_bar.nlargest(20, 'value')
    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color':top20['value'], 'colorscale': 'Blues'}))
    fig.update_layout(
    title = 'Top 20 most popular bike stations in New York',
    xaxis_title = 'Start station',
    yaxis_title = 'Sum of trips',
    width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width=True)
    # df1['value'] = 1 
    # df_groupby_bar = df1.groupby('start_station_name', as_index = False).agg({'value': 'sum'})
    # top20 = df_groupby_bar.nlargest(20, 'value')
    # fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value']))
    # fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker = {'color':top20['value'],'colorscale': 'Blues'}))
    # fig.update_layout(
    # title = 'Top 20 most popular bike stations in New York',
    # xaxis_title = 'Start stations',
    # yaxis_title ='Sum of trips',
    # width = 900, height = 600sxs
    # )
    # st.plotly_chart(fig, use_container_width=True)
    st.markdown("From the bar chart it is clear that there are some start stations that are more popular than others - in the top 3 we can see start_station_name Grove St PATH, South Waterfront Walkway - Sinatra Dr & 1 St as well as Hoboken Terminal - Hudson St & Hudson Pl. There is a big jump between the highest and lowest bars of the plot indicating some clear preferences for the leading stations. This is a finding that we could cross reference with the interactive map that you can access through the side bar select box.")

# elif page =='Interactive map with aggregated bike trips': 

#     ### Create the map ###

#     st.write("Interactive map showing aggregated bike trips over New York")

#     path_to_html = "kepler_map.html" 

#     # Read file and keep in variable
#     with open(path_to_html,'r') as f: 
#         html_data = f.read()

#     ## Show in webpage
#     st.header("Aggregated Bike Trips in New York")
#     st.components.v1.html(html_data,height=1000)
#     st.markdown("#### Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips.")
#     st.markdown("The most popular start stations are:")
#     st.markdown("Grove St PATH, South Waterfront Walkway - Sinatra Dr & 1 St as well as Hoboken Terminal - Hudson St & Hudson Pl.")
#     st.markdown("The most common routes (>2,000) are between Washington St, Sip Ave, Madison St & 1 St, Marin Light Rail, Newport Pkwy, which are predominantly located along the water.")

else:

    image_path = os.path.join(os.getcwd(), "img", "recommendation.png")
    st.header("Conclusions and recommendations")
    bikes = Image.open(image_path)  #source: Midjourney
    st.image(bikes)
    st.markdown("### Our analysis has shown that Divvy Bikes should focus on the following objectives moving forward:")
    st.markdown("- Add more stations to the locations around the water line, such as Washington St, Sip Ave, Madison St & 1 St, Marin Light Rail, Newport Pkwy")
    st.markdown("- Ensure that bikes are fully stocked in all these stations during the warmer months in order to meet the higher demand, but provide a lower supply in winter and late autumn to reduce logistics costs")