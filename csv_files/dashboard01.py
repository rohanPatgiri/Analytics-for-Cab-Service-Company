
# 1. Best and worst performing cities by total trips.

# A. Performing the relevant Calculations
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")

# Load data
dimCity = pd.read_csv("dim_city.csv")
dimDate = pd.read_csv("dim_date.csv")
passengerSummary = pd.read_csv('fact_passenger_summary.csv')
repeatTrip = pd.read_csv("dim_repeat_trip_distribution.csv")
factTrips = pd.read_csv("fact_trips.csv")


# Aggregating total trips by city
city_trip_summary = factTrips.groupby('city_id')['trip_id'].count().reset_index()
city_trip_summary.rename(columns={'trip_id': 'total_trips'}, inplace=True)

# Sorting cities by total trips
city_trip_summary_sorted = city_trip_summary.sort_values(by='total_trips', ascending=False)

# Top 3 and Bottom 3 performing cities
top_3_cities = city_trip_summary_sorted.head(3)
bottom_3_cities = city_trip_summary_sorted.tail(3)

# Merging with city names for better readability
top_3_cities = top_3_cities.merge(dimCity, on='city_id', how='left')
bottom_3_cities = bottom_3_cities.merge(dimCity, on='city_id', how='left')

#.....
#B. Display/ Visualize
# Streamlit App
st.title("Performance Metrics Dashboard")
st.subheader ("1. Cities with the highest and lowest trips")

# Visualizing Top and Bottom Cities
import plotly.express as px

# Display charts side-by-side
col011, col012 = st.columns(2)

with col011:
    fig_top = px.bar(top_3_cities, x='city_name', y='total_trips', title="Top 3 Cities by Total Trips", color='total_trips')
    st.plotly_chart(fig_top, use_container_width=True)

with col012:
    fig_bottom = px.bar(bottom_3_cities, x='city_name', y='total_trips', title="Bottom 3 Cities by Total Trips", color='total_trips')
    st.plotly_chart(fig_bottom, use_container_width=True)



#................................
#2. Average Fare Per Trip, Average Distance(in km) per trip and Fare per kilometer

# A. Calculations

# Load your data
dimCity = pd.read_csv("dim_city.csv")
factTrips = pd.read_csv("fact_trips.csv")

# Aggregate metrics for cities
city_fare_summary = factTrips.groupby('city_id').agg(
    total_distance=('distance_travelled(km)', 'sum'),
    total_fare=('fare_amount', 'sum'),
    total_trips=('trip_id', 'count')
).reset_index()

# Calculate additional metrics
city_fare_summary['avg_fare_per_trip'] = city_fare_summary['total_fare'] / city_fare_summary['total_trips']
city_fare_summary['avg_dist_per_trip'] = city_fare_summary['total_distance'] / city_fare_summary['total_trips']
city_fare_summary['fare_per_kilometer'] = city_fare_summary['avg_fare_per_trip'] / city_fare_summary['avg_dist_per_trip']

# Merge city names for readability
city_fare_summary = city_fare_summary.merge(dimCity, on='city_id', how='left')
# Remove duplicate rows, if any
city_fare_summary = city_fare_summary.drop_duplicates()

#.....
# B. Display in Dashboard

metrics = {
    'fare_per_kilometer': 'Fare per Kilometer',
    'avg_fare_per_trip': 'Average Fare per Trip',
    'avg_dist_per_trip': 'Average Distance per Trip'
}
st.subheader("2. Average Fare Per Trip, Average Distance(in km) per trip and Fare per kilometer")

selected_metric_key = st.selectbox("Select a Metric to Visualize", options=list(metrics.keys()), format_func=lambda x: metrics[x])

# Get the selected metric label
selected_metric_label = metrics[selected_metric_key]

# Filter data for top 5 and bottom 5
top_5 = city_fare_summary.nlargest(5, selected_metric_key)
bottom_5 = city_fare_summary.nsmallest(5, selected_metric_key)
# Visualizations


fig_top = px.bar(
    top_5,
    x='city_name',
    y=selected_metric_key,
    title=f"Top 5 Cities with the highest {selected_metric_label}",
    color=selected_metric_key,
    text=selected_metric_key
)
fig_top.update_layout(height=400, width=500, margin=dict(l=20, r=20, t=50, b=50))
fig_top.update_traces(texttemplate='%{text:.2f}', textposition='outside')

fig_bottom = px.bar(
    bottom_5,
    x='city_name',
    y=selected_metric_key,
    title=f"Top 5 Cities with the lowest {selected_metric_label}",
    color=selected_metric_key,
    text=selected_metric_key
)
fig_bottom.update_layout(height=400, width=500, margin=dict(l=20, r=20, t=50, b=50))
fig_bottom.update_traces(texttemplate='%{text:.2f}', textposition='outside')

# Display charts side-by-side
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_top)
with col2:
    st.plotly_chart(fig_bottom)

#....................
#3. Passenger and Driver Ratings

import streamlit as st
import pandas as pd

# Load the datasets
dimCity = pd.read_csv("dim_city.csv")
factTrips = pd.read_csv("fact_trips.csv")

# Calculate the ratings summary
ratingsSummary = factTrips.groupby(['city_id', 'passenger_type']).agg(
    avg_passenger_rating=("passenger_rating", 'mean'),
    avg_driver_rating=("driver_rating", 'mean')
).reset_index()

# Merge with city names
ratingsSummary = ratingsSummary.merge(dimCity, on='city_id', how='left')

# Streamlit app
st.subheader("3. Passenger and Driver Ratings")

# Sidebar filters
#st.sidebar.header("Filters")
#selected_city = st.sidebar.selectbox("Select City", options=ratingsSummary['city_name'].unique(), index=0)
#selected_passenger_type = st.sidebar.selectbox("Select Passenger Type", options=ratingsSummary['passenger_type'].unique(), index=0)

# Filters on the main page
col1, col2 = st.columns(2)

with col1:
    selected_city = st.selectbox("Select City", options=ratingsSummary['city_name'].unique(), index=0)

with col2:
    selected_passenger_type = st.selectbox("Select Passenger Type", options=ratingsSummary['passenger_type'].unique(), index=0)


# Apply filters
filtered_data = ratingsSummary[
    (ratingsSummary['city_name'] == selected_city) &
    (ratingsSummary['passenger_type'] == selected_passenger_type)
]

# Display the filtered data
st.write(f"#### Filtered Data for {selected_city} and {selected_passenger_type} passengers")
st.dataframe(filtered_data)

# Summary insights
# Find top 5 and bottom 5 cities for passenger and driver ratings
top_5_passenger = ratingsSummary.nlargest(5, 'avg_passenger_rating')
bottom_5_passenger = ratingsSummary.nsmallest(5, 'avg_passenger_rating')
top_5_driver = ratingsSummary.nlargest(5, 'avg_driver_rating')
bottom_5_driver = ratingsSummary.nsmallest(5, 'avg_driver_rating')

# Create charts
top_passenger_chart = alt.Chart(top_5_passenger).mark_bar().encode(
    x=alt.X('avg_passenger_rating:Q', title='Avg Passenger Rating'),
    y=alt.Y('city_name:N', sort='-x', title='City'),
    color=alt.value('blue'),
    tooltip=['city_name', 'avg_passenger_rating']
).properties(
    title='Top 5 Avg Passenger Ratings',
    width=300,
    height=300
)

bottom_passenger_chart = alt.Chart(bottom_5_passenger).mark_bar().encode(
    x=alt.X('avg_passenger_rating:Q', title='Avg Passenger Rating'),
    y=alt.Y('city_name:N', sort='x', title='City'),
    color=alt.value('red'),
    tooltip=['city_name', 'avg_passenger_rating']
).properties(
    title='Bottom 5 Avg Passenger Ratings',
    width=300,
    height=300
)

top_driver_chart = alt.Chart(top_5_driver).mark_bar().encode(
    x=alt.X('avg_driver_rating:Q', title='Avg Driver Rating'),
    y=alt.Y('city_name:N', sort='-x', title='City'),
    color=alt.value('green'),
    tooltip=['city_name', 'avg_driver_rating']
).properties(
    title='Top 5 Avg Driver Ratings',
    width=300,
    height=300
)

bottom_driver_chart = alt.Chart(bottom_5_driver).mark_bar().encode(
    x=alt.X('avg_driver_rating:Q', title='Avg Driver Rating'),
    y=alt.Y('city_name:N', sort='x', title='City'),
    color=alt.value('orange'),
    tooltip=['city_name', 'avg_driver_rating']
).properties(
    title='Bottom 5 Avg Driver Ratings',
    width=300,
    height=300
)

# Display charts side by side
st.title("Top and Bottom Ratings for Cities")

col1, col2 = st.columns(2)
with col1:
    st.altair_chart(top_passenger_chart, use_container_width=True)
    st.altair_chart(top_driver_chart, use_container_width=True)

with col2:
    st.altair_chart(bottom_passenger_chart, use_container_width=True)
    st.altair_chart(bottom_driver_chart, use_container_width=True)


#---------------------
#4.

import streamlit as st
import pandas as pd
import altair as alt

# Load the datasets
dimCity = pd.read_csv("dim_city.csv")
passengerSummary = pd.read_csv("fact_passenger_summary.csv")

# Merge passenger summary with city names for better readability
passengerSummary = passengerSummary.merge(dimCity, on='city_id', how='left')

# Streamlit app
st.subheader("4. Peak and low demand months")

# User selection for city
selected_city_name = st.selectbox("Select City Name", options=passengerSummary['city_name'].unique())

# Filter data for the selected city
city_data = passengerSummary[passengerSummary['city_name'] == selected_city_name]

# Create the line chart
chart = alt.Chart(city_data).mark_line(point=True).encode(
    x=alt.X('month:O', title='Month'),
    y=alt.Y('total_passengers:Q', title='Total Passengers'),
    tooltip=['month', 'total_passengers']
).properties(
    title=f"Total Passengers for Each Month in {selected_city_name}",
    width=700,
    height=400
)

# Display the chart
st.altair_chart(chart)
# Distribution of the Peak demand month and low demand month.

# Identify peak demand and low demand months for each city
peak_demand = passengerSummary.loc[
    passengerSummary.groupby('city_id')['total_passengers'].idxmax()
]
low_demand = passengerSummary.loc[
    passengerSummary.groupby('city_id')['total_passengers'].idxmin()
]

# Merge with city names for better readability
peak_demand = peak_demand.merge(dimCity, on='city_id', how='left')
low_demand = low_demand.merge(dimCity, on='city_id', how='left')

# Streamlit app
st.subheader("Distribution of Peak and Low Demand Months")

# Distribution of Peak Demand Months
# Distribution of Peak Demand Months
peak_month_distribution = peak_demand['month'].value_counts().reset_index()
peak_month_distribution.columns = ['month', 'count']

peak_chart = alt.Chart(peak_month_distribution).mark_bar().encode(
    x=alt.X('month:O', title='Month'),
    y=alt.Y('count:Q', title='Number of Cities'),
    tooltip=['month', 'count']
).properties(
    title="Peak Demand Month Distribution",
    width=300,
    height=400
)

# Distribution of Low Demand Months
low_month_distribution = low_demand['month'].value_counts().reset_index()
low_month_distribution.columns = ['month', 'count']

low_chart = alt.Chart(low_month_distribution).mark_bar().encode(
    x=alt.X('month:O', title='Month'),
    y=alt.Y('count:Q', title='Number of Cities'),
    tooltip=['month', 'count']
).properties(
    title="Low Demand Month Distribution",
    width=300,
    height=400
)

# Display charts side by side


col1, col2 = st.columns(2)

with col1:
    st.altair_chart(peak_chart, use_container_width=True)

with col2:
    st.altair_chart(low_chart, use_container_width=True)

# Insights
st.write("### Insights")
st.write("These charts show the distribution of months when cities experienced their peak and low demands.")


#.....
# 5. 

# First, Ensure both datasets have a common column for merging
dimDate['date'] = pd.to_datetime(dimDate['date'])
factTrips['date'] = pd.to_datetime(factTrips['date'])

# Merge the 'day_type' column from dimDate to factTrips based on the 'date' column
factTrips2 = factTrips.merge(dimDate[['date', 'day_type']], on='date', how='left')

wdayVsWend = factTrips2.groupby(['city_id','day_type'])['trip_id'].count().reset_index()
wdayVsWend_df = pd.DataFrame(wdayVsWend, columns = ['city_id','day_type', 'trip_id'])
wdayVsWend_df= wdayVsWend_df.rename(columns= {'trip_id': 'total_trips'})

wdayVsWend_df = wdayVsWend_df.merge(dimCity[['city_name', 'city_id']], on='city_id', how='left')
wdayVsWend_df = wdayVsWend_df[['city_id','city_name','day_type','total_trips']]

# Streamlit app
st.subheader("5. City-wise Trip Analysis: Weekday vs Weekend")

# City selection
city_list = wdayVsWend_df['city_name'].unique()
selected_city = st.selectbox("Select a City:", city_list)

# Filter data for the selected city
city_data = wdayVsWend_df[wdayVsWend_df['city_name'] == selected_city]

# Bar chart
chart = alt.Chart(city_data).mark_bar().encode(
    x=alt.X('day_type:N', title='Day Type'),
    y=alt.Y('total_trips:Q', title='Total Trips'),
    color=alt.Color('day_type:N', legend=None),
    tooltip=['day_type', 'total_trips']
).properties(
    title=f"Total Trips for {selected_city}: Weekday vs Weekend",
    width=600,
    height=400
)

st.altair_chart(chart, use_container_width=True)

#....
# 5 more


# Load datasets
dimCity = pd.read_csv("dim_city.csv")
factTrips = pd.read_csv("fact_trips.csv")
dimDate = pd.read_csv("dim_date.csv")

# Merge the factTrips and dimDate datasets to get day type
factTrips = factTrips.merge(dimDate[['date', 'day_type']], on='date', how='left')

# Aggregate data by city and day_type
weekday_weekend_summary = factTrips.groupby(['city_id', 'day_type']).agg(
    total_trips=('trip_id', 'count')
).reset_index()

# Pivot to create separate columns for weekday and weekend trips
weekday_weekend_pivot = weekday_weekend_summary.pivot(
    index='city_id', columns='day_type', values='total_trips'
).reset_index()

# Rename columns for clarity
weekday_weekend_pivot.columns = ['city_id', 'Weekend_Trips', 'Weekday_Trips']

# Calculate the difference (Weekday Trips - Weekend Trips)
weekday_weekend_pivot['Weekday_vs_Weekend_Difference'] = (
    weekday_weekend_pivot['Weekday_Trips'] - weekday_weekend_pivot['Weekend_Trips']
)

# Merge with city names for better readability
weekday_weekend_pivot = weekday_weekend_pivot.merge(dimCity, on='city_id', how='left')

# Streamlit app
st.subheader("Weekday vs Weekend Trips by City")

# Chart explanation
st.markdown("""
##### Chart Explanation:
- **Negative Y-Axis**: Weekday trips were **more** than Weekend trips.
- **Positive Y-Axis**: Weekend trips were **more** than Weekday trips.
""")

# Create the bar chart
fig = px.bar(
    weekday_weekend_pivot,
    x='city_name',
    y='Weekday_vs_Weekend_Difference',
    title="Weekday vs Weekend Trips: City-Wise Analysis",
    labels={
        'Weekday_vs_Weekend_Difference': 'Difference (Weekday - Weekend Trips)',
        'city_name': 'City'
    },
    text='Weekday_vs_Weekend_Difference',
    color='Weekday_vs_Weekend_Difference',
    color_continuous_scale='Tealrose',
)

# Update chart layout
fig.update_layout(
    xaxis_title="City",
    yaxis_title="Difference (Weekday Trips - Weekend Trips)",
    coloraxis_showscale=False,
    template='plotly_white',
    title_x=0.5  # Center the title
)

# Add a horizontal line at y=0 for reference
fig.add_hline(y=0, line_dash="dash", line_color="gray")

# Display the chart
st.plotly_chart(fig)

#.......................................................
# 06.  Repeat Passenger Analysis by Trip Frequency

# Load data
dimCity = pd.read_csv("dim_city.csv")
dimDate = pd.read_csv("dim_date.csv")
passengerSummary = pd.read_csv('fact_passenger_summary.csv')
repeatTrip = pd.read_csv("dim_repeat_trip_distribution.csv")
factTrips = pd.read_csv("fact_trips.csv")

targetRating = pd.read_csv("city_target_passenger_rating.csv")
targetNewPassengers= pd.read_csv("monthly_target_new_passengers.csv")
targetTrips = pd.read_csv("monthly_target_trips.csv")

# Group and calculate totals
city_total_repeat_passengers = repeatTrip.groupby('city_id')['repeat_passenger_count'].sum().reset_index()
city_total_repeat_passengers.rename(columns={'repeat_passenger_count': 'total_repeat_passengers'}, inplace=True)

# Merge totals back into the repeatTrip dataset
repeatTrip_with_totals = repeatTrip.merge(city_total_repeat_passengers, on='city_id', how='left')

# Calculate percentages
repeatTrip_with_totals['percentage'] = (
    repeatTrip_with_totals['repeat_passenger_count'] / repeatTrip_with_totals['total_repeat_passengers'] * 100
)

# Merge city names for better readability
repeatTrip_with_totals = repeatTrip_with_totals.merge(dimCity, on='city_id', how='left')

# Streamlit app
st.subheader("6. Repeat Passenger Analysis by Trip Frequency")

# City selection
city_list = repeatTrip_with_totals['city_name'].unique()
selected_city = st.selectbox("Select a City:", city_list, key = 'trip_frequency')

# Filter data for the selected city
city_data = repeatTrip_with_totals[repeatTrip_with_totals['city_name'] == selected_city]

# Bar chart
chart = alt.Chart(city_data).mark_bar().encode(
    x=alt.X('trip_count:O', title='Trip Count'),
    y=alt.Y('percentage:Q', title='Percentage of Repeat Passengers'),
    color=alt.Color('trip_count:N', legend=None),
    tooltip=['trip_count', 'percentage']
).properties(
    title=f"Percentage of Repeat Passengers by Trip Frequency for {selected_city}",
    width=600,
    height=400
)

st.altair_chart(chart, use_container_width=True)


#.............
# 7. Monthly Target Achievement Analysis for Key Metrics
#7.1 Re
import pandas as pd
import streamlit as st

# Load the datasets
dimCity = pd.read_csv("dim_city.csv")
factPassengerSummary = pd.read_csv("fact_passenger_summary.csv")
targetPassengers = pd.read_csv("monthly_target_new_passengers.csv")

# Merge actual passenger data with target passenger data on city_id and month
monthly_passenger_comparison = factPassengerSummary.merge(
    targetPassengers, on=['city_id', 'month'], how='inner'
)

# Merge with city names for better readability
monthly_passenger_comparison = monthly_passenger_comparison.merge(dimCity, on='city_id', how='left')

# Calculate the difference between actual and target passengers
monthly_passenger_comparison['passenger_difference'] = (
    monthly_passenger_comparison['total_passengers'] - monthly_passenger_comparison['target_new_passengers']
)

# Streamlit App
st.subheader("7.1 Monthly Target vs Actual Passengers Dashboard")

# Dropdown for selecting a city
city_option = st.selectbox(
    "Select a City to View Monthly Target vs Actual Passenger Data:",
    monthly_passenger_comparison['city_name'].unique()
)

# Filter the data for the selected city
filtered_data = monthly_passenger_comparison[monthly_passenger_comparison['city_name'] == city_option]

# Display the table
st.subheader(f"Monthly Target vs Actual Passenger Data for {city_option}")
st.dataframe(filtered_data[['month', 'total_passengers', 'target_new_passengers', 'passenger_difference']])

# Optional: Add chart visualization
st.subheader(f"Passenger Difference Trend for {city_option}")
st.line_chart(
    filtered_data.set_index('month')['passenger_difference']
)




#...........
#7.2 Target vs Actual Ratings



# Load the datasets
dimCity = pd.read_csv("dim_city.csv")
factTrips = pd.read_csv("fact_trips.csv")
targetRating = pd.read_csv("city_target_passenger_rating.csv")

# Step 1: Calculate the actual average passenger ratings for each city
city_actual_ratings = factTrips.groupby('city_id').agg(
    actual_avg_passenger_rating=('passenger_rating', 'mean')
).reset_index()

# Step 2: Merge actual ratings with target ratings
ratings_comparison = city_actual_ratings.merge(targetRating, on='city_id', how='inner')

# Step 3: Merge with city names for better readability
ratings_comparison = ratings_comparison.merge(dimCity, on='city_id', how='left')

# Step 4: Calculate Target vs Actual comparison
ratings_comparison['rating_difference'] = ratings_comparison['actual_avg_passenger_rating'] - ratings_comparison['target_avg_passenger_rating']
ratings_comparison['target_status'] = ratings_comparison['rating_difference'].apply(
    lambda x: 'Met or Exceeded Target' if x >= 0 else 'Missed Target'
)

# Streamlit App
st.sidebar.header("Settings")

# Display the DataFrame as a table
st.subheader("7.2 Target vs Actual Passenger Ratings Data")
st.dataframe(ratings_comparison[['city_name', 'actual_avg_passenger_rating', 'target_avg_passenger_rating', 'rating_difference', 'target_status']])

# Add a selector for visualization
metric_option = st.sidebar.selectbox("Select a Metric to Visualize:", ["Rating Difference", "Target Status"])

# Plot for Rating Difference
if metric_option == "Rating Difference":
    
    fig_diff = px.bar(ratings_comparison, x='city_name', y='rating_difference', color='rating_difference',
                      title="Difference Between Actual and Target Passenger Ratings",
                      labels={'rating_difference': 'Difference'})
    st.plotly_chart(fig_diff)

# Plot for Target Status
elif metric_option == "Target Status":
    st.subheader("Target Status by City")
    fig_status = px.bar(ratings_comparison, x='city_name', color='target_status', 
                        title="Target Status (Met/Exceeded vs Missed)",
                        barmode='group', labels={'target_status': 'Status'})
    st.plotly_chart(fig_status)
#...........
#7.3 Target vs Actual Total trips
import pandas as pd
import streamlit as st
import plotly.express as px

# Load the datasets
dimCity = pd.read_csv("dim_city.csv")
factTrips = pd.read_csv("fact_trips.csv")
targetTrips = pd.read_csv("monthly_target_trips.csv")

# Step 1: Calculate the actual total trips for each city
city_actual_trips = factTrips.groupby('city_id').agg(
    actual_total_trips=('trip_id', 'count')
).reset_index()

# Step 2: Aggregate the total target trips for each city
city_target_trips = targetTrips.groupby('city_id').agg(
    total_target_trips=('total_target_trips', 'sum')
).reset_index()

# Step 3: Merge actual trips with target trips
trips_comparison = city_actual_trips.merge(city_target_trips, on='city_id', how='inner')

# Step 4: Merge with city names for better readability
trips_comparison = trips_comparison.merge(dimCity, on='city_id', how='left')

# Step 5: Calculate Target vs Actual comparison
trips_comparison['trip_difference'] = trips_comparison['actual_total_trips'] - trips_comparison['total_target_trips']
trips_comparison['target_status'] = trips_comparison['trip_difference'].apply(
    lambda x: 'Met or Exceeded Target' if x >= 0 else 'Missed Target'
)

# Streamlit App
st.subheader("7.3 Target vs Actual Total Trips Dashboard")
st.sidebar.header("Settings")

# Display the DataFrame as a table
st.subheader("Target vs Actual Total Trips Data")
st.dataframe(trips_comparison[['city_name', 'actual_total_trips', 'total_target_trips', 'trip_difference', 'target_status']])

# Add a selector for visualization
metric_option = st.sidebar.selectbox("Select a Metric to Visualize:", ["Trip Difference", "Target Status"])

# Plot for Trip Difference
if metric_option == "Trip Difference":
    st.subheader("Trip Difference by City")
    fig_diff = px.bar(trips_comparison, x='city_name', y='trip_difference', color='trip_difference',
                      title="Difference Between Actual and Target Total Trips",
                      labels={'trip_difference': 'Difference'})
    st.plotly_chart(fig_diff)

# Plot for Target Status
elif metric_option == "Target Status":
    st.subheader("Target Status by City")
    fig_status = px.bar(trips_comparison, x='city_name', color='target_status', 
                        title="Target Status (Met/Exceeded vs Missed)",
                        barmode='group', labels={'target_status': 'Status'})
    st.plotly_chart(fig_status)

#.......

#......................


#8.0
st.subheader("8. Repeat Passenger Rate Analysis")
# Load the dataset
dimCity = pd.read_csv("dim_city.csv")
passengerSummary = pd.read_csv('fact_passenger_summary.csv')

# Calculate RPR% for each city and month
passengerSummary['RPR%'] = (passengerSummary['repeat_passengers'] / passengerSummary['total_passengers']) * 100

# Calculate the average RPR% for each city
city_rpr_summary = passengerSummary.groupby('city_id').agg(
    avg_rpr=('RPR%', 'mean')
).reset_index()

# Merge with city names for readability
city_rpr_summary = city_rpr_summary.merge(dimCity, on='city_id', how='left')

# Sort cities by average RPR% in descending order
city_rpr_summary = city_rpr_summary.sort_values(by='avg_rpr', ascending=False)

# Streamlit app to display the table
st.subheader("Average Repeat Passenger Rate (RPR%) by City")
st.table(city_rpr_summary[['city_name', 'avg_rpr']])








#............

#8. Highest and Lowest Repeat Passenger Rate (RPR%) by City and Month

fact_passenger_summary = pd.read_csv('fact_passenger_summary.csv')
dim_city = pd.read_csv('dim_city.csv')
# Calculate Repeat Passenger Rate (RPR%)
fact_passenger_summary['RPR%'] = (
    fact_passenger_summary['repeat_passengers'] / fact_passenger_summary['total_passengers'] * 100
)

# Merge city names for better readability
fact_passenger_summary = fact_passenger_summary.merge(dim_city, on='city_id', how='left')

# Identify the top 2 and bottom 2 cities based on RPR%
top_2_cities = fact_passenger_summary.nlargest(2, 'RPR%')
bottom_2_cities = fact_passenger_summary.nsmallest(2, 'RPR%')

# Identify the months with the highest RPR% across all cities
month_rpr = fact_passenger_summary.groupby('month')['repeat_passengers', 'total_passengers'].sum().reset_index()
month_rpr['RPR%'] = (month_rpr['repeat_passengers'] / month_rpr['total_passengers']) * 100
highest_rpr_months = month_rpr.nlargest(2, 'RPR%')


# Visualization
st.subheader("RPR% by City and Month")

# Interactive selection
selected_city03 = st.selectbox("Select a City:", fact_passenger_summary['city_name'].unique(), key = 'rpr_analysis')
city_data03 = fact_passenger_summary[fact_passenger_summary['city_name'] == selected_city03]

chart = alt.Chart(city_data03).mark_line(point=True).encode(
    x=alt.X('month:T', title='Month'),
    y=alt.Y('RPR%:Q', title='Repeat Passenger Rate (%)'),
    color=alt.Color('city_name:N', legend=None),
    tooltip=['month', 'RPR%']
).properties(
    title=f"Repeat Passenger Rate (%) for {selected_city03}",
    width=700,
    height=400
)

st.altair_chart(chart, use_container_width=True)

# Bar chart for month-level RPR%
st.subheader("Repeat Passenger Rate by Month Across All Cities")
bar_chart = alt.Chart(month_rpr).mark_bar().encode(
    x=alt.X('month:O', title='Month', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('RPR%:Q', title='Repeat Passenger Rate (%)'),
    tooltip=['month', 'RPR%']
).properties(
    title="RPR% by Month",
    width=700,
    height=400
)

st.altair_chart(bar_chart, use_container_width=True)
