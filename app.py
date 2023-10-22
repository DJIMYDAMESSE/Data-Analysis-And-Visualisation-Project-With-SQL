# import library
import streamlit as st
import pandas as pd 
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import mysql.connector
import time


# creat connection between the database and the app
connect = mysql.connector.connect(
    host = "localhost",
    passwd = "",
    db = "vizpro", 
    user = "root"
)
cursor = connect.cursor()

# define function to view all data
def view_all_data():
    cursor.execute("SELECT * FROM insurance ORDER BY id ASC")
    data = cursor.fetchall()
    return data


# config page
st.set_page_config(page_title="vizpro", page_icon="	:roller_coaster:", layout='wide')


# define the main function
def main():

    st.title("	:chart_with_upwards_trend: INSURANCE DESCRIPTIVE ANALYTICS  	:chart_with_upwards_trend:")

    st.subheader(":male-construction-worker: BY: JALIL KETOU (Data engineer)")
    
    st.markdown("# ")

    # show the database on the dashboard
    result = view_all_data()
    df = pd.DataFrame(result, columns=["Policy", "Expiry", "Location", "State", "Region", "Investment",
                                        "Construction", "BusinessType", "Earthquake", "Flood", "Rating", "id"])
    
    #transformer le type de la colonne Rating
    df['Rating'] = df['Rating'].apply(lambda x: str(x).replace(',', '.'))
    df["Rating"] = df['Rating'].apply(lambda x: float(x))
    

    # add and logo on the website in the sidebar
    st.sidebar.image("image/logo.png", caption="Online Analytics")


    # switcher menu

    st.sidebar.header("Please Filter")
    region = st.sidebar.multiselect(
        "Select region", 
        options=df['Region'].unique(),
        default=df['Region'].unique()
    )

    location = st.sidebar.multiselect(
        "Select Location",
        options=df['Location'].unique(),
        default=df['Location'].unique()
    )

    construction = st.sidebar.multiselect(
        "Select Construction",
        options=df['Construction'].unique(),
        default=df['Construction'].unique()
    )


    df_viewver = df.query(
        "Region==@region & Location==@location & Construction==@construction"
    )


    
   
    # definir une table

    def table():
        with st.expander("Tabular"):
            showdata = st.multiselect("Order by:", df_viewver.columns, default=[])
            st.write(df_viewver[showdata])

        # Compute top analytics
        total_investment = float(df_viewver["Investment"].sum())
        investment_mode = float(df_viewver["Investment"].mode().iloc[0])
        investment_mean = float(df_viewver["Investment"].mean())
        investment_median = float(df_viewver["Investment"].median())
        rating = df_viewver["Rating"].sum()

        total1, total2, total3, total4, total5 = st.columns(5)

        with total1:
            st.info("Total Investment", icon="📌")
            st.metric(label="sum TZS", value=numerize(total_investment))

        with total2:
            st.info("Most frequent", icon="📌")
            st.metric(label="mode TZS", value=numerize(investment_mode))

        with total3:
            st.info("Average investment", icon="📌")
            st.metric(label="average TZS", value=numerize(investment_mean))

        with total4:
            st.info("Central Earning", icon="📌")
            st.metric(label="median ZS", value=numerize(investment_median))

        with total5:
            st.info("Rating", icon="📌")
            st.metric(label="Rating", value=rating, help=f"Total rating: {rating}")

        st.markdown("---")


    # define de graph function

    def graph():
        total_investment = df_viewver['Investment'].sum()
        average_rating = round(df_viewver['Rating'].mean(), 2)

        # simple bar graph
        investment_by_business_type = (
            df_viewver.groupby(by=["BusinessType"]).count()[['Investment']].sort_values(by="Investment")
        )

        fig_investment = px.bar(
            investment_by_business_type,
            x="Investment",
            y=investment_by_business_type.index,
            orientation='h',
            title="<b>Investment by business type</b>",
            color=['#0083b8']*len(investment_by_business_type),
            template='plotly_white'
        )


        fig_investment.update_layout(
            plot_bgcolor = 'rgba(0, 0, 0, 0)',
            xaxis=(dict(showgrid=False))
        )


        # simple line graph
        investment_by_state = df_viewver.groupby(by=["State"]).count()[['Investment']]
        

        fig_state = px.line(
            investment_by_state,
            x=investment_by_state.index,
            y="Investment",
            orientation='v',
            title="<b>Investment by state</b>",
            color=['#0083b8']*len(investment_by_state),
            template='plotly_white'
        )

        fig_state.update_layout(
            xaxis=dict(tickmode='linear'),
            plot_bgcolor = 'rgba(0, 0, 0, 0)',
            yaxis=(dict(showgrid=False))
        )

        left, right = st.columns(2)

        left.plotly_chart(fig_investment, use_container_width=True)
        right.plotly_chart(fig_state, use_container_width=True)


    #create a progress bar
    def progress_bar():
        st.markdown("""<style>.stProgress > div > div > div > div {background-image: linear-gradient(to right, #99ff99, #FFFF00)}</style>""", unsafe_allow_html=True)
        target = 3000000000
        current = df_viewver["Investment"].sum()
        percent = round((current/target*100))
        mybar = st.progress(0)
        

        if percent>100:
            st.subheader("Target done !")
        else:
            st.write("you have ", percent, "% ", "of ", format(target, 'd'), 'TZS')
            for percent_complet in range(percent):
                time.sleep(0.1)
                mybar.progress(percent_complet+1, text="Target Percentage")

    # define de menu bar
    def sideBar():
        selected=option_menu(
                menu_title='Main Menu',
                options=['Home', 'Progress'],
                icons=['house', 'eye'],
                menu_icon='cast',
                default_index=0,
                orientation='horizontal'
                )
        if selected=='Home':
            st.subheader(f"Page: {selected}")
            table()
            graph()
        else :
            st.subheader(f"Page: {selected}")
            progress_bar()
            graph()

    sideBar()



    # theme
    hide_st_style = """

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

</style>
"""


if __name__=="__main__":
    main()