
import streamlit as st
import pandas as pd
import altair as alt


#.......
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
st.title("Repeat Passenger Analysis by Trip Frequency")

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

#......................
#8. 
# Load data
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

# Streamlit layout
st.title("Repeat Passenger Rate Analysis")

# Display Top and Bottom Cities
st.subheader("Top 2 Cities with Highest Repeat Passenger Rate (RPR%)")
st.table(top_2_cities[['city_name', 'month', 'RPR%']])

st.subheader("Bottom 2 Cities with Lowest Repeat Passenger Rate (RPR%)")
st.table(bottom_2_cities[['city_name', 'month', 'RPR%']])

# Display Highest RPR Months
st.subheader("Months with Highest Repeat Passenger Rate (RPR%)")
st.table(highest_rpr_months[['month', 'RPR%']])

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
    x=alt.X('month:T', title='Month'),
    y=alt.Y('RPR%:Q', title='Repeat Passenger Rate (%)'),
    tooltip=['month', 'RPR%']
).properties(
    title="RPR% by Month",
    width=700,
    height=400
)

st.altair_chart(bar_chart, use_container_width=True)