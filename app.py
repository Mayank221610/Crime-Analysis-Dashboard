import streamlit as st
from streamlit.components.v1 import html
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import db



# ---------------------- PAGE CONFIGURATION ----------------------
st.set_page_config(
    page_title="Crime Analysis Dashboard",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ----------------- SESSION STATE -----------------
# ----------------- SESSION STATE -----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False   # Default: Not logged in
if "show_logout_popup" not in st.session_state:
    st.session_state.show_logout_popup = False

# ----------------- TOP-RIGHT LOGOUT BUTTON -----------------
if st.session_state.logged_in:
    topbar = st.container()
    with topbar:
        col1, col2 = st.columns([8, 1])  # Right align
        with col2:
            if st.button("Logout"):
                st.session_state.show_logout_popup = True

# ----------------- POPUP (Dialog) -----------------
if st.session_state.show_logout_popup:

    @st.dialog("Confirm Logout")
    def logout_confirm():
        st.write("Do you want to log out?")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Yes, Logout"):
                st.session_state.logged_in = False
                st.session_state.show_logout_popup = False
                st.success("You have been logged out!")
                st.rerun()

        with col2:
            if st.button("Cancel"):
                st.session_state.show_logout_popup = False
                st.rerun()

    logout_confirm()

# ---------------------- LOAD DATA ----------------------
df = pd.read_csv("Crime.csv")

# ---------------------- SIDEBAR NAVIGATION ----------------------
with st.sidebar:
    if not st.session_state.logged_in:
        # Default menu (jab app open ho)
        opt = option_menu(
            "Navigation",
            ["Home", "Registration", "Login", "Forget Password"],
            icons=["house", "person", "key", "lock"]
        )
    else:
        # Agar login ho gaya ho to dusra menu
        opt = option_menu(
            "Navigation",
            ["Home", "Data Analysis", "Data Visualization", "Feedback"],
            icons=["house", "bar-chart", "pie-chart", "chat-left-text"]
        )
# ---------------------- HOME ----------------------
if opt == "Home":
    st.title("🚔 Crime Analysis Dashboard")
    st.write("Welcome to the Crime Analysis System.")
    st.markdown("---")
    st.title("Introduction")

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

# ---------------------- REGISTRATION ----------------------
if opt == "Registration" and not st.session_state.get("logged_in", False):
    st.title("📝 Registration")

    with st.form("Reg"):
        Name = st.text_input("Enter your name")
        Phone = st.text_input("Enter your phone number")
        Email = st.text_input("Enter your email")
        Password = st.text_input("Enter your password", type="password")
        Why = st.text_area("Why you would want to use it?")
        bt = st.form_submit_button("Register")

    if bt:
        # Check empty fields
        if not all([Name, Phone, Email, Password, Why]):
            st.warning("Please fill all the fields")
        # Phone validation
        elif not (Phone.isdigit() and len(Phone) == 10):
            st.error("Please enter a valid 10-digit phone number")
        # Basic email validation
        elif " " in Email or Email.count("@") != 1:
            st.error("Please enter a valid email with exactly one '@' and no spaces")
        else:
            username, domain = Email.split("@")
            ext = domain.split(".")[-1] if "." in domain else ""
            if (
                len(username) < 3
                or not username[0].isalpha()
                or ".." in username
                or username.startswith(".")
                or username.endswith(".")
                or "." not in domain
                or domain.startswith(".")
                or domain.endswith(".")
                or ".." in domain
                or len(ext) < 2
                or not ext.isalpha()
            ):
                st.error("Invalid email format")
            else:
                # Save data in DB
                res = db.reg((Name, Phone, Email, Password, Why))
                if res is True:
                    st.success("Registration successful")
                elif "Email" in str(res):
                    st.error("Email already exists. Please use another email.")
                elif "Phone" in str(res):
                    st.error("Phone number already exists. Please use another number.")
                else:
                    st.error("Registration failed")

# ---------------------- FORGET PASSWORD ----------------------
elif opt == "Forget Password" and not st.session_state.logged_in:
    st.title("🔐 Forgot Password")

    with st.form("forget_form"):
        email = st.text_input("Enter your registered email")
        new_password = st.text_input("Enter new password", type="password")
        confirm_password = st.text_input("Confirm new password", type="password")
        btn = st.form_submit_button("Reset Password")

    if btn:
        if not email or not new_password or not confirm_password:
            st.warning("Please fill all fields")
        elif new_password != confirm_password:
            st.error("Passwords do not match")
        else:
            result = db.reset_password(email, new_password)
            if result:
                st.success("Password updated successfully!")
                st.toast("Your password has been changed")
            else:
                st.error("Email not found in our database")


# ---------------------- LOGIN ----------------------
elif opt == "Login" and not st.session_state.logged_in:
    st.title("🔐 Login")
    with st.form("Login"):
        Email = st.text_input("Enter your email")
        Password = st.text_input("Enter your password", type="password")
        bt = st.form_submit_button("Login")

    if bt:
        if not Email or not Password:
            st.warning(" Please fill all the fields")
        else:
            res = db.login((Email, Password))
            if res:
                st.session_state.logged_in = True
                st.session_state.user = Email
                st.success(" Login successful")
                st.rerun()
            else:
                st.error("Invalid email or password")

# ---------------------- DATA ANALYSIS ----------------------
elif opt == "Data Analysis" and st.session_state.logged_in:
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
    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox("Select Year", ["All"] + years)
    with col2:
        selected_state = st.selectbox("Select State/UT", ["All"] + states)

    filtered_df = df.copy()
    if selected_year != "All":
        filtered_df = filtered_df[filtered_df["YEAR"] == selected_year]
    if selected_state != "All":
        filtered_df = filtered_df[filtered_df["STATE/UT"] == selected_state]

    st.subheader("📋 Filtered Data")
    st.dataframe(filtered_df, use_container_width=True)

# ---------------------- DATA VISUALIZATION ----------------------
elif opt == 'Data Visualization' and st.session_state.logged_in:
    st.title("📊 Data Visualization")

    # Q1 IPC Crimes by State Year-wise
    st.subheader("IPC Crimes by State (Year-wise)")
    years = sorted(df["YEAR"].unique())
    selected_year = st.selectbox("Select Year", years)
    data = df[df["YEAR"] == selected_year]
    grouped_df = data.groupby("STATE/UT")["TOTAL IPC CRIMES"].sum().reset_index()
    fig = px.bar(grouped_df, x="STATE/UT", y="TOTAL IPC CRIMES",
                 title=f"Total IPC Crimes by State in {selected_year}",
                 color="TOTAL IPC CRIMES")
    st.plotly_chart(fig)

    # Q2 Crime Trend India
    crime_columns = [col for col in df.columns if col not in ['YEAR', 'STATE/UT', 'DISTRICT']]
    st.subheader("📈 Crime Trend in India (2001–2013)")
    selected_crime = st.selectbox("Select Crime Type", crime_columns)
    filtered_df = df[(df["YEAR"] >= 2001) & (df["YEAR"] <= 2013)]
    trend_data = filtered_df.groupby("YEAR")[selected_crime].sum().reset_index()
    fig = px.line(trend_data, x="YEAR", y=selected_crime, markers=True,
                  title=f"{selected_crime} Cases in India (2001–2013)")
    st.plotly_chart(fig)

    # Q3 Crime Percentage Pie
    st.subheader("📊 Crime Type Percentage in State/UT (Year-wise)")
    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox("Select Year", years, key="year_selectbox_1")
    with col2:
        selected_state = st.selectbox("Select State/UT", sorted(df["STATE/UT"].unique()), key="state_selectbox_1")
    filtered_df = df[(df["YEAR"] == selected_year) & (df["STATE/UT"] == selected_state)]
    crime_counts = filtered_df[crime_columns].sum().reset_index()
    crime_counts.columns = ['Crime_Type', 'Count']
    crime_counts = crime_counts[crime_counts['Count'] > 0]
    fig = px.pie(crime_counts, names='Crime_Type', values='Count',
                 title=f"Crime Distribution in {selected_state} - {selected_year}")
    st.plotly_chart(fig)

    # Q4 Top 10 States
    st.subheader("Top 10 States with Most Cases (Selected Years)")
    col1, col2 = st.columns(2)
    with col1:
        selected_year_1 = st.selectbox("Select Year", years, key="year_selected_1")
    with col2:
        selected_crime = st.selectbox("Select Crime Type", crime_columns, key="crime_selected_1")
    filtered_df = df[df["YEAR"] == selected_year_1]
    state_crime = filtered_df.groupby("STATE/UT")[selected_crime].sum().sort_values(ascending=False).reset_index()
    top_states = state_crime.head(10)
    fig = px.bar(top_states, x="STATE/UT", y=selected_crime,
                 title=f"Top 10 States with Most {selected_crime} Cases in {selected_year_1}",
                 color=selected_crime)
    st.plotly_chart(fig)

    # Q5 Crimes Against Women
    st.subheader("Top 10 States with crimes against women")
    crimes_women = ["RAPE", "DOWRY DEATHS", "CRUELTY BY HUSBAND OR HIS RELATIVES"]
    df_grouped = df.groupby("STATE/UT")[crimes_women].sum().reset_index()
    df_grouped["TOTAL"] = df_grouped[crimes_women].sum(axis=1)
    df_grouped = df_grouped.sort_values("TOTAL", ascending=False).head(10)
    df_long = df_grouped.melt(id_vars=["STATE/UT"], value_vars=crimes_women,
                              var_name="Crime Type", value_name="Cases")
    fig_q5 = px.bar(df_long, x="STATE/UT", y="Cases", color="Crime Type",
                    barmode="group")
    st.plotly_chart(fig_q5, use_container_width=True)

# q6 Which years saw the biggest rise in murder cases?

    st.subheader("Yearly Murder Cases in India")
    murder_per_year = df.groupby("YEAR")["MURDER"].sum().reset_index()
   
    fig = px.line(
        murder_per_year,
        x="YEAR",
        y="MURDER",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)
    
# q7 Which state had the most district-wise reports in selected year?

# ---------------------- FEEDBACK ----------------------
elif opt == "Feedback" and st.session_state.logged_in:
    st.title("📝 Feedback")
    with st.form("fed"):

        Feedback = st.text_area("Enter your feedback")
        bt = st.form_submit_button("Submit")

    if bt:
        if not Feedback:
            st.warning(" Please fill all the fields")
        else:
            res = db.fed((Feedback,))  # comma is important
            if res:
                st.success("Thank you for your feedback!")
            else:
                st.error("Feedback submission failed.")

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