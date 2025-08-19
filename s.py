import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import db

# Page configuration
st.set_page_config(
    page_title="Crime Analysis Dashboard",
    page_icon="🚔",
    layout="wide"
)

# Sidebar Navigation
with st.sidebar:
    opt=option_menu("Navigation", ["Home", "Data Analysis", "Data Visualization", "Feedback"],
                    icons=["house", "bar-chart", "pie-chart", "chat-left-text"])

# Load dataset
df = pd.read_csv("Crime.csv")

# Initialize session state
if 'section' not in st.session_state:
    st.session_state.section = 'home'

# ---------------------- HOME SECTION ----------------------
if opt == 'Home':
    st.title("Crime Analysis Dashboard")
    st.subheader("🧩 Project Overview:")
    st.write("""
        The *Crime Analysis System* is a data-driven web application built using Python, Pandas, Streamlit, Matplotlib, Seaborn, and Plotly.  
        It analyzes Indian crime data across states, years, and crime types to extract meaningful insights.
    """)

    st.subheader("🎯 Objectives:")
    st.markdown("""
        - Analyze crime data across various states and years  
        - Visualize crime trends using interactive graphs  
        - Provide useful insights into crime patterns
    """)

    st.subheader("🔧 Technologies Used:")
    st.markdown("""
        - **Python** for processing  
        - **Pandas** for manipulation  
        - **Matplotlib**, **Seaborn**, **Plotly** for visualization  
        - **Streamlit** for UI
    """)

    st.subheader("📊 Features:")
    st.markdown("""
        - State-wise & Year-wise analysis  
        - Top crime types and affected areas  
        - Simple, clean user interface
    """)
# ---------------------- Regd. for get data ----------------------

# Check if the user is already logged in
if 'user' in st.session_state:
    st.session_state.section = 'Home'
    st.success(f"Welcome back, {st.session_state.user['Name']}!")
    st.write("You are already logged in.")
    st.stop()
# Sidebar for navigation
with st.sidebar:
    mode = option_menu("Menu", ["Registration", "Login"], icons=["person", "key"], default_index=0)

if mode=="Registration":
    with st.form("Reg"):
        Name = st.text_input("Enter your name")
        Phone = st.text_input("Enter your phone number")
        Email = st.text_input("Enter your email")
        Password = st.text_input("Enter your password", type="password")
        Why= st.text_area("Why you would want to use it?")
        bt = st.form_submit_button("Register")
    if bt:
        if Name=="" or Phone=="" or Email=="" or Password=="" or Why=="":
            st.error("Please fill all the fields")
            st.warning("Please fill all the fields")
        else:
            # st.success("You have submitted the form")
            # st.info("You have submitted the form")
            data=(Name,Phone,Email,Password,Why)
            res=db.reg(data)
            if res:
                st.success("Registration successful")
                # st.info("You have submitted the form")
            else    :
                st.error("Registration failed")

elif mode=="Login":
    with st.form("Login"):
        Email = st.text_input("Enter your email")
        Password = st.text_input("Enter your password", type="password")
        bt = st.form_submit_button("Login")
    if bt:
        if Email=="" or Password=="":
            st.error("Please fill all the fields")
            st.warning("Please fill all the fields")
        else:
            data=(Email,Password)
            res=db.login(data)
            if res:
                st.success("Login successful")
            else:
                st.error("invalid email or password")

# ---------------------- DATA ANALYSIS SECTION ----------------------
# if bt:
#     st.session_state.section = 'Data Analysis'

elif opt== 'Data Analysis':
    st.title("🧠 Crime Data Analysis (India)")
    st.markdown("---")

    st.header("📌 Basic Information")
    st.write("*Total Rows:*", len(df))
    st.write("*Year Range:*", df['YEAR'].min(), "to", df['YEAR'].max())
    st.write("*Unique States/UTs:*", df['STATE/UT'].nunique())
    st.write("*Unique Districts:*", df['DISTRICT'].nunique())

    total_cases = df["TOTAL IPC CRIMES"].sum()
    st.metric("📦 Total IPC Crime Cases in India", f"{total_cases:,}")

    st.header("📆 Crimes Per Year")
    yearly_crime = df.groupby("YEAR")["TOTAL IPC CRIMES"].sum().reset_index()
    st.dataframe(yearly_crime)

    st.header("📍 Total Crimes by State/UT")
    state_crime = df.groupby("STATE/UT")["TOTAL IPC CRIMES"].sum().sort_values(ascending=False).reset_index()
    st.dataframe(state_crime.head(10))

    st.header("🏙 Top Districts with Most Crime")
    district_crime = df.groupby("DISTRICT")["TOTAL IPC CRIMES"].sum().sort_values(ascending=False).reset_index()
    st.dataframe(district_crime.head(10))

    st.header("🚨 Most Reported Crime Types")
    crime_cols = df.columns[3:-1]  # Skipping Year, State/UT, District
    crime_type_sum = df[crime_cols].sum().sort_values(ascending=False).reset_index()
    crime_type_sum.columns = ["Crime Type", "Total Cases"]
    st.dataframe(crime_type_sum.head(10))

    st.header("📊 Peak Crime Year in Each State/UT")
    idx = df.groupby("STATE/UT")["TOTAL IPC CRIMES"].idxmax()
    peak_crime_years = df.loc[idx, ["STATE/UT", "YEAR", "TOTAL IPC CRIMES"]].reset_index(drop=True)
    st.dataframe(peak_crime_years)

    st.header("📈 Crime Trend for a Selected State/UT")
    selected_state = st.selectbox("Select State/UT", sorted(df["STATE/UT"].unique()))
    state_trend = df[df["STATE/UT"] == selected_state].groupby("YEAR")["TOTAL IPC CRIMES"].sum().reset_index()
    st.dataframe(state_trend)

    st.header("📌 State-wise Contribution to Total Crime (%)")
    state_contrib = (state_crime.set_index("STATE/UT")["TOTAL IPC CRIMES"] / total_cases * 100).round(2).reset_index()
    state_contrib.columns = ["State/UT", "Contribution (%)"]
    st.dataframe(state_contrib.head(10))
    
    st.subheader("🔍 Crime Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    st.subheader("📌 Summary Statistics")
    st.write(df.describe())

    years = sorted(df["YEAR"].unique())
    states = sorted(df["STATE/UT"].unique())
   
    st.subheader("🎚 Filter Options")
    col1, col2,col3 = st.columns(3)
    with col1:
        selected_year = st.selectbox("Select Year", ["All"] + years)
    with col2:
        selected_state = st.selectbox("Select State/UT", ["All"] + states)

    # Filtered data
    filtered_df = df.copy()
    if selected_year != "All":
        filtered_df = filtered_df[filtered_df["YEAR"] == selected_year]
    if selected_state != "All":
        filtered_df = filtered_df[filtered_df["STATE/UT"] == selected_state]

    st.subheader("📋 Filtered Data")
    st.dataframe(filtered_df, use_container_width=True)


# ---------------------- DATA VISUALIZATION SECTION ----------------------
elif opt == 'Data Visualization':
    
    st.title("📊 Data Visualization")

#Q1 Which states had the highest number of total IPC crimes year-wise?
    
    st.subheader("IPC Crimes by State (Year-wise)")

    years = sorted(df["YEAR"].unique())
    selected_year = st.selectbox("Select Year", years)
    
    data = df[df["YEAR"] == selected_year]
    grouped = data.groupby("STATE/UT")["TOTAL IPC CRIMES"].sum()
    grouped = grouped[grouped > 0]
    grouped_df = grouped.reset_index()

    fig = px.bar(grouped_df,
        x="STATE/UT",
        y="TOTAL IPC CRIMES",
        title=f"Total IPC Crimes by State in {selected_year}",
        color="TOTAL IPC CRIMES")
    st.plotly_chart(fig)

# Q2. How has the number of all cases as per select by user changed in India from 2001 to 2013? 

    non_crime_cols = ['YEAR', 'STATE/UT', 'DISTRICT']
    crime_columns = [col for col in df.columns if col not in non_crime_cols and df[col].dtype in ['int64', 'float64']]

    st.subheader("📈 Crime Trend in India (2001–2013)")
    # Select crime type
    selected_crime = st.selectbox("Select Crime Type", crime_columns)
    # Filter for year range
    filtered_df = df[(df["YEAR"] >= 2001) & (df["YEAR"] <= 2013)]
    # Group and prepare data
    trend_data = filtered_df.groupby("YEAR")[selected_crime].sum().reset_index()

    # Plot
    fig = px.line(trend_data, x="YEAR", y=selected_crime, markers=True,
                title=f"{selected_crime} Cases in India (2001–2013)")

    st.plotly_chart(fig)
    
# Q3. What percentage of different crimes were reported in different States/UT in differnt year?

    non_crime_cols = ['YEAR', 'STATE/UT', 'DISTRICT']
    crime_columns = [col for col in df.columns if col not in non_crime_cols and df[col].dtype in ['int64', 'float64']]

    st.subheader("📊 Crime Type Percentage in State/UT (Year-wise)")

    # Filter widgets
    col1, col2 = st.columns(2)
    with col1:
        years = sorted(df["YEAR"].unique())
        selected_year = st.selectbox("Select Year", years, key="year_selectbox_1")

    with col2:
        states = sorted(df["STATE/UT"].unique())
        selected_state = st.selectbox("Select State/UT", states, key="state_selectbox_1")

    # Filtered Data
    filtered_df = df[(df["YEAR"] == selected_year) & (df["STATE/UT"] == selected_state)]

    # Sum all crimes for that State-Year
    crime_counts = filtered_df[crime_columns].sum().reset_index()
    crime_counts.columns = ['Crime_Type', 'Count']

    # Remove 0 values
    crime_counts = crime_counts[crime_counts['Count'] > 0]

    # Pie Chart
    fig = px.pie(crime_counts,
                names='Crime_Type',
                values='Count',
                title=f"Crime Distribution in {selected_state} - {selected_year}"
    )
    st.plotly_chart(fig)

# Q4. Which are the top 10 states with the most selected cases in selected years?

    st.subheader("Top 10 States with Most Cases (Selected Years)")
    col1, col2 = st.columns(2)

    with col1:
        years = sorted(df["YEAR"].unique())
        selected_year_1 = st.selectbox("Select Year", years, key="year_selected_1")
        
    with col2:
        crime_columns = [col for col in df.columns if col not in ['YEAR', 'STATE/UT', 'DISTRICT'] and df[col].dtype in ['int64', 'float64']]
        selected_crime = st.selectbox("Select Crime Type", crime_columns, key="crime_selected_1")
    # Filter data for selected year
    if selected_year_1 != "All":
        filtered_df = df[df["YEAR"] == selected_year_1]
    else:
        filtered_df = df.copy()
    # Group by state and sum the selected crime type
    state_crime = filtered_df.groupby("STATE/UT")[selected_crime].sum().sort_values(ascending=False).reset_index()
    # Get top 10 states
    top_states = state_crime.head(10)
    # Plot
    fig = px.bar(top_states,
        x="STATE/UT",
        y=selected_crime,
        title=f"Top 10 States with Most {selected_crime} Cases in {selected_year}",
        color=selected_crime)
    st.plotly_chart(fig)
    
#Q5. Which states report the most crimes against women (rape, dowry deaths, cruelty by husband)?


    st.subheader("Top 10 States with crimes against women")

    crimes_women = ["RAPE", "DOWRY DEATHS", "CRUELTY BY HUSBAND OR HIS RELATIVES"]

    # Group and sort by total crimes
    df_grouped = df.groupby("STATE/UT")[crimes_women].sum().reset_index()
    df_grouped["TOTAL"] = df_grouped[crimes_women].sum(axis=1)
    df_grouped = df_grouped.sort_values("TOTAL", ascending=False)

    # Get top 10 states
    top_states = df_grouped.head(10)

    # Convert to long format for px
    df_long = top_states.melt(id_vars=["STATE/UT"], value_vars=crimes_women,
                            var_name="Crime Type", value_name="Cases")

    # Plot horizontal grouped bar
    fig_q5 = px.bar(
        df_long,
        x="STATE/UT",
        y="Cases",
        color="Crime Type",
        barmode="group",
        title="Top 10 States - Crimes Against Women"
    )

    fig_q5.update_layout(height=500)
    st.plotly_chart(fig_q5, use_container_width=True)


# ---------------------- FEEDBACK SECTION ----------------------
elif opt == 'Feedback':
    st.title("📝 Feedback")
    st.write("We value your feedback! Please share your thoughts below.")

    with st.form("fed"):
            Name=st.text_input("Enter your name")
            Email=st.text_input("Enter your email")
            Feedback=st.text_area("Enter your feedback")
            bt=st.form_submit_button("Submit")
    if bt:
         if Name=="" or Email=="" or Feedback=="":
                st.error("Please fill all the fields")
                st.warning("Please fill all the fields")
         else:
                # st.success("You have submitted the form")
                # st.info("You have submitted the form")
                data=(Name,Email,Feedback)
                res=db.fed(data)
                if res:
                   st.success("Thank you for your feedback!")
                    # st.info("You have submitted the form")
                else:
                    st.error("Feedback submission failed. Please try again later.")
        
    
# ---------------------- FOOTER ----------------------

st.markdown(
    """
    <hr style="margin-top: 50px;"/>
    <div style='text-align: center; font-size: 14px; color: gray;'>
        Developed by: <b>Mayank</b> | Contact: <a href='mailto:mayank221605@gmail.com'>mayank221605@gmail.com</a>
    </div>
    """,
    unsafe_allow_html=True
)        

# ---------------------- END OF CODE ----------------------
