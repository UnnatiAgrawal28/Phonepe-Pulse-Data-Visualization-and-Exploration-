
#Import the required set of libraries



import pandas as pd
import streamlit as st
import pymongo

import sqlite3
import sqlalchemy
import json
import plotly.express as px

#--------------------------------------------------------------------------x----------------------------------------------------------------------#
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='PhonePe Pulse', page_icon=':bar_chart:', layout="wide")
st.markdown(f'<h1 style="text-align: center;">PhonePe Pulse Data Visualization \
            and Exploration</h1>', unsafe_allow_html=True)

def main():
    # Define sidebar options
    options = ["Home", "About", "Analysis", "Insights"]
    icons = ["🏠", "🧑‍💼", "📊", "🔍"]

    # Sidebar
    st.sidebar.title("phonepe Pulse Dashboard")
    selected_option = st.sidebar.selectbox("Navigate", options, format_func=lambda x: f"{icons[options.index(x)]} {x}")

    # Main content based on the selected option
    if selected_option == "Home":
        st.title("Welcome to the Home Page")
        st.write("This is the home page content.")

    elif selected_option == "About":
        st.title("About")
        st.write("This is the about page content.")

    elif selected_option == "Analysis":
        st.title("Analysis")
        # Sidebar options for type, year, and quarter
        Type = st.selectbox("Type", ("Transactions", "Users"))
        Year = st.selectbox("Year", list(range(2018, 2023)))
        Quarter = st.selectbox("Quarter", list(range(1, 5)))
        
        if st.button("Enter"):
            if Type == "Transactions":
            
                st.markdown("### :violet[State]")
                conn = sqlite3.connect('phonepe.db')
                cur = conn.cursor()
                cur.execute(f'''select state, sum(Transaction_count) as Total_Transactions_Count, 
                            sum(Transaction_amount) as Total from agg_transaction_data where year = {Year} 
                            and quarter = {Quarter} group by state order by Total desc limit 10''')
                df = pd.DataFrame(cur.fetchall(), columns=['State', 'Transactions_Count', 'Total_Amount'])
                fig = px.pie(df, values='Total_Amount',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count': 'Transactions_Count'})
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)

     
                st.markdown("### :violet[District]")
                conn = sqlite3.connect('phonepe.db')
                cur = conn.cursor()
                cur.execute(f'''select district , sum(Count) as Total_Count, 
                sum(Amount) as Total from map_transaction_data where year = {Year} and quarter = {Quarter} 
                group by district order by Total desc limit 10''')
                df = pd.DataFrame(cur.fetchall(), columns=['District', 'Transactions_Count', 'Total_Amount'])

                fig = px.pie(df, values='Total_Amount',
                                 names='District',
                                 title='Top 10',
                                 color_discrete_sequence=px.colors.sequential.Agsunset,
                                 hover_data=['Transactions_Count'],
                                 labels={'Transactions_Count': 'Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)

  
                st.markdown("### :violet[Pincode]")
                conn = sqlite3.connect('phonepe.db')
                cur = conn.cursor()
                cur.execute(f'''select pincode, sum(Transaction_count) as Total_Transactions_Count, 
                sum(Transaction_amount) as Total from top_transaction_data where year = {Year} 
                and quarter = {Quarter} group by pincode order by Total desc limit 10''')

                df = pd.DataFrame(cur.fetchall(), columns=['Pincode', 'Transactions_Count', 'Total_Amount'])
                fig = px.pie(df, values='Total_Amount',
                                 names='Pincode',
                                 title='Top 10',
                                 color_discrete_sequence=px.colors.sequential.Agsunset,
                                 hover_data=['Transactions_Count'],
                                 labels={'Transactions_Count': 'Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)

            if Type == "Users":            
                st.markdown("### :violet[Brands]")
                conn = sqlite3.connect('phonepe.db')
                cur = conn.cursor()
                cur.execute(f"select Brands, sum(Count) as Total_Count, avg(Percentage)*100 as Avg_Percentage from agg_user_data where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
                df = pd.DataFrame(cur.fetchall(), columns=['Brand', 'Total_Users', 'Avg_Percentage'])
                fig = px.bar(df,
                                 title='Top 10',
                                 x="Total_Users",
                                 y="Brand",
                                 orientation='h',
                                 color='Avg_Percentage',
                                 color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig, use_container_width=True)


                st.markdown("### :violet[District]")
                conn = sqlite3.connect('phonepe.db')
                cur = conn.cursor()
                cur.execute(f"select District, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user_data where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
                df = pd.DataFrame(cur.fetchall(), columns=['District', 'Total_Users', 'Total_Appopens'])
                df.Total_Users = df.Total_Users.astype(float)
                fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="District",
                             orientation='h',
                             color='Total_Users',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig, use_container_width=True)


                st.markdown("### :violet[Pincode]")
                conn = sqlite3.connect('phonepe.db')
                cur = conn.cursor()
                cur.execute(f"select Pincode, sum(RegisteredUsers) as Total_Users from top_user_data where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
                df = pd.DataFrame(cur.fetchall(), columns=['Pincode', 'Total_Users'])
                fig = px.pie(df,
                             values='Total_Users',
                             names='Pincode',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Users'])
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)


                st.markdown("### :violet[State]")
                conn = sqlite3.connect('phonepe.db')
                cur = conn.cursor()
                cur.execute(f"select state, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user_data where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
                df = pd.DataFrame(cur.fetchall(), columns=['State', 'Total_Users', 'Total_Appopens'])
                fig = px.pie(df, values='Total_Users',
                                 names='State',
                                 title='Top 10',
                                 color_discrete_sequence=px.colors.sequential.Agsunset,
                                 hover_data=['Total_Appopens'],
                                 labels={'Total_Appopens': 'Total_Appopens'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)

    elif selected_option == "Insights":
        st.title("Insights")
        Type = st.selectbox("Type", ("Transactions", "Users"))
        Year = st.selectbox("Year", list(range(2018, 2023)))
        Quarter = st.selectbox("Quarter", list(range(1, 5)))
        col1,col2 = st.columns(2)
        

        if Type == "Transactions":
            with col1:
                st.markdown("## :violet[Overall State Data - Transactions Amount]")
                conn = sqlite3.connect('phonepe.db')
                cur = conn.cursor()
                cur.execute(f"select State, sum(Count) as Total_Transactions, sum(Amount) as Total_amount from map_transaction_data where year = {Year} and quarter = {Quarter} group by state order by state")
                df1 = pd.DataFrame(cur.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])

                with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('Statenames.csv')
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_amount',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
                url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response= requests.get(url)
                data1= json.loads(response.content)
                states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
                states_name_tra.sort()
        
                fig_india_1= px.choropleth(df1, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                         color= "Total_Transactions", color_continuous_scale= "Sunsetdark",
                                         range_color= (df1["Total_Transactions"].min(),df1["Total_amount"].max()),
                                         hover_name= "States",title = f"{aiyq['Years'].min()} AND {quarter} TRANSACTION AMOUNT",
                                         fitbounds= "locations",width =600, height= 600)
                fig_india_1.update_geos(visible =False)
                
                st.plotly_chart(fig_india_1)

# Uncomment and adjust the indentation if you want to use the commented-out code blocks
#         # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
#         with col2:
#             st.markdown("## :violet[Overall State Data - Transactions Count]")
#             conn = sqlite3.connect('phonepe.db')
#             cur = conn.cursor()
#             cur.execute(f"select State, sum(Count) as Total_Transactions, sum(Amount) as Total_amount from map_transaction_data where year = {Year} and quarter = {Quarter} group by state order by state")
#             df1 = pd.DataFrame(cur.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
#             df1.Total_Transactions = df1.Total_Transactions.astype(int)

#             fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
#                       featureidkey='properties.ST_NM',
#                       locations='State',
#                       color='Total_Transactions',
#                       color_continuous_scale='sunset')

#             fig.update_geos(fitbounds="locations", visible=False)
#             st.plotly_chart(fig,use_container_width=True)

if __name__ == "__main__":
    main()

#         if Type == "Transactions":
            
#             # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
#             with col1:
#                 st.markdown("## :violet[Overall State Data - Transactions Amount]")
#                 conn = sqlite3.connect('phonepe.db')
#                 cur = conn.cursor()
#                 cur.execute(f"select State, sum(Count) as Total_Transactions, sum(Amount) as Total_amount from map_transaction_data where year = {Year} and quarter = {Quarter} group by state order by state")
#                 df1 = pd.DataFrame(cur.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
#                 #df2 = pd.read_csv('Statenames.csv')
#                 #df1.State = df2

#                 url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
#         response= requests.get(url)
#         data1= json.loads(response.content)
#         states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
#         states_name_tra.sort()

#         fig_india_1= px.choropleth(df1, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
#                                  color= "Total_Transactions", color_continuous_scale= "Sunsetdark",
#                                  range_color= (df1["Total_Transactions"].min(),df1["Total_amount"].max()),
#                                  hover_name= "States",title = f"{aiyq['Years'].min()} AND {quarter} TRANSACTION AMOUNT",
#                                  fitbounds= "locations",width =600, height= 600)
#         fig_india_1.update_geos(visible =False)
        
#         st.plotly_chart(fig_india_1)
    
#             #     fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
#             #               featureidkey='properties.ST_NM',
#             #               locations='State',
#             #               color='Total_amount',
#             #               color_continuous_scale='sunset')
    
#             #     fig.update_geos(fitbounds="locations", visible=False)
#             #     st.plotly_chart(fig,use_container_width=True)
                
#             # # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
#             # with col2:
                
#             #     st.markdown("## :violet[Overall State Data - Transactions Count]")
#             #     conn = sqlite3.connect('phonepe.db')
#             #     cur = conn.cursor()
#             #     cur.execute(f"select State, sum(Count) as Total_Transactions, sum(Amount) as Total_amount from map_transaction_data where year = {Year} and quarter = {Quarter} group by state order by state")
#             #     df1 = pd.DataFrame(cur.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
#             #     #df2 = pd.read_csv('Statenames.csv')
#             #     df1.Total_Transactions = df1.Total_Transactions.astype(int)
#             #     #df1.State = df2
    
#             #     fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
#             #               featureidkey='properties.ST_NM',
#             #               locations='State',
#             #               color='Total_Transactions',
#             #               color_continuous_scale='sunset')
    
#             #     fig.update_geos(fitbounds="locations", visible=False)
#             #     st.plotly_chart(fig,use_container_width=True)
                
                
            

# if __name__ == "__main__":
#     main()

# #-----------------------------------------------------------------------------------------------------------------------------------------------------

# st.set_page_config(page_title='PhonePe Pulse', page_icon=':bar_chart:', layout="wide")
# st.markdown(f'<h1 style="text-align: center;">PhonePe Pulse Data Visualization \
#             and Exploration</h1>', unsafe_allow_html=True)

# import streamlit as st

# def main():
#     # Define sidebar options
#     options = ["Home", "About", "Analysis", "Insights"]
#     icons = ["🏠", "🧑‍💼", "📊", "🔍"]

#     # Sidebar
#     st.sidebar.title("phonepe Pulse Dashboard")
#     selected_option = st.sidebar.selectbox("Navigate", options, format_func=lambda x: f"{icons[options.index(x)]} {x}")

#     # Main content based on selected option
#     if selected_option == "Home":
#         st.title("Welcome to the Home Page")
#         st.write("This is the home page content.")

#     elif selected_option == "About":
#         st.title("About")
#         st.write("This is the about page content.")

#     elif selected_option == "Analysis":
#         st.title("Analysis")
#     # Sidebar options for type, year, and quarter
#         Type = st.selectbox("Type", ("Transactions", "Users"))
#         Year = st.selectbox("Year", list(range(2018, 2023)))
#         Quarter = st.selectbox("Quarter", list(range(1, 5)))
        
#         if st.button("Enter"):
    
#             if Type == "Transactions":
#                 col1,col2,col3 = st.columns([1,1,1],gap="small")
            
#                 with col1:
#                     st.markdown("### :violet[State]")
#                     conn = sqlite3.connect('phonepe.db')
#                     cur = conn.cursor()
#                     cur.execute(f'''select state, sum(Transaction_count) as Total_Transactions_Count, 
#                                 sum(Transaction_amount) as Total from agg_transaction_data where year = {Year} 
#                                 and quarter = {Quarter} group by state order by Total desc limit 10''')
#                     df = pd.DataFrame(cur.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
#                     fig = px.pie(df, values='Total_Amount',
#                                  names='State',
#                                  title='Top 10',
#                                  color_discrete_sequence=px.colors.sequential.Agsunset,
#                                  hover_data=['Transactions_Count'],
#                                  labels={'Transactions_Count':'Transactions_Count'})
#                     fig.update_traces(textposition='inside', textinfo='percent+label')
#                     st.plotly_chart(fig,use_container_width=True)
#                     #st.write(f'''Maximum Total Amount: {agg_transaction_data['Total_Amount'].max()}, 
#                                #Minimum Total Amount: {agg_transaction_data['Total_Amount'].min()}''')
            
#                 with col2:
#                     st.markdown("### :violet[District]")
#                     conn = sqlite3.connect('phonepe.db')
#                     cur = conn.cursor()
#                     cur.execute(f'''select district , sum(Count) as Total_Count, 
#                     sum(Amount) as Total from map_transaction_data where year = {Year} and quarter = {Quarter} 
#                     group by district order by Total desc limit 10''')
#                     df = pd.DataFrame(cur.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])
        
#                     fig = px.pie(df, values='Total_Amount',
#                                      names='District',
#                                      title='Top 10',
#                                      color_discrete_sequence=px.colors.sequential.Agsunset,
#                                      hover_data=['Transactions_Count'],
#                                      labels={'Transactions_Count':'Transactions_Count'})
        
#                     fig.update_traces(textposition='inside', textinfo='percent+label')
#                     st.plotly_chart(fig,use_container_width=True)
#                     #st.write(f"Maximum Total Amount: {map_transaction_data['Total_Amount'].max()}, Minimum Total Amount: {map_transaction_data['Total_Amount'].min()}")
            
#                 with col3:
#                     st.markdown("### :violet[Pincode]")
#                     conn = sqlite3.connect('phonepe.db')
#                     cur = conn.cursor()
#                     cur.execute(f'''select pincode, sum(Transaction_count) as Total_Transactions_Count, 
#                     sum(Transaction_amount) as Total from top_transaction_data where year = {Year} 
#                     and quarter = {Quarter} group by pincode order by Total desc limit 10''')
                    
#                     df = pd.DataFrame(cur.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
#                     fig = px.pie(df, values='Total_Amount',
#                                      names='Pincode',
#                                      title='Top 10',
#                                      color_discrete_sequence=px.colors.sequential.Agsunset,
#                                      hover_data=['Transactions_Count'],
#                                      labels={'Transactions_Count':'Transactions_Count'})
        
#                     fig.update_traces(textposition='inside', textinfo='percent+label')
#                     st.plotly_chart(fig,use_container_width=True)
#                     #st.write(f"Maximum Total Amount: {top_transaction_data['Total_Amount'].max()}, Minimum Total Amount: {top_transaction_data['Total_Amount'].min()}")

#             if Type == "Users":
#                 col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
                    
#                 with col1:
#                     st.markdown("### :violet[Brands]")
#                     conn = sqlite3.connect('phonepe.db')
#                     cur = conn.cursor()
#                     cur.execute (f"select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user_data where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
#                     df = pd.DataFrame(cur.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
#                     fig = px.bar(df,
#                                      title='Top 10',
#                                      x="Total_Users",
#                                      y="Brand",
#                                      orientation='h',
#                                      color='Avg_Percentage',
#                                      color_continuous_scale=px.colors.sequential.Agsunset)
#                     st.plotly_chart(fig,use_container_width=True)   
            
#                 with col2:
#                     st.markdown("### :violet[District]")
#                     conn = sqlite3.connect('phonepe.db')
#                     cur = conn.cursor()
#                     cur.execute(f"select district, sum(Registered_User) as Total_Users, sum(app_opens) as Total_Appopens from map_user_data where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
#                     df = pd.DataFrame(cur.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
#                     df.Total_Users = df.Total_Users.astype(float)
#                     fig = px.bar(df,
#                                  title='Top 10',
#                                  x="Total_Users",
#                                  y="District",
#                                  orientation='h',
#                                  color='Total_Users',
#                                  color_continuous_scale=px.colors.sequential.Agsunset)
#                     st.plotly_chart(fig,use_container_width=True)
                      
#                 with col3:
#                     st.markdown("### :violet[Pincode]")
#                     conn = sqlite3.connect('phonepe.db')
#                     cur = conn.cursor()
#                     cur.execute(f"select Pincode, sum(Registered_Users) as Total_Users from top_user_data where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
#                     df = pd.DataFrame(cur.fetchall(), columns=['Pincode', 'Total_Users'])
#                     fig = px.pie(df,
#                                  values='Total_Users',
#                                  names='Pincode',
#                                  title='Top 10',
#                                  color_discrete_sequence=px.colors.sequential.Agsunset,
#                                  hover_data=['Total_Users'])
#                     fig.update_traces(textposition='inside', textinfo='percent+label')
#                     st.plotly_chart(fig,use_container_width=True)
                    
#                 with col4:
#                     st.markdown("### :violet[State]")
#                     conn = sqlite3.connect('phonepe.db')
#                     cur = conn.cursor()
#                     cur.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user_data where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
#                     df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
#                     fig = px.pie(df, values='Total_Users',
#                                      names='State',
#                                      title='Top 10',
#                                      color_discrete_sequence=px.colors.sequential.Agsunset,
#                                      hover_data=['Total_Appopens'],
#                                      labels={'Total_Appopens':'Total_Appopens'})
        
#                     fig.update_traces(textposition='inside', textinfo='percent+label')
#                     st.plotly_chart(fig,use_container_width=True)
                    

            

        # #st.write(""""#### From this menu we casn get insights like :
        #                 - Overall ranking on a particular Year and Quarter.
        #             - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
        #                 - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
        #         - Top 10 mobile brands and its percentage based on the how many people use phonepe.
        #             """,icon="🔍"")


    #    st.subheader('Analysis done on the basis of All India ,States and Top categories between 2018 and 2022')
    # # Sidebar options for type, year, and quarter
    #     Type = st.selectbox("Type", ("Transactions", "Users"))
    #     Year = st.selectbox("Year", list(range(2018, 2023)))
    #     Quarter = st.selectbox("Quarter", list(range(1, 5)))
    #     st.subheader('Analysis done on the basis of All India ,States and Top categories between 2018 and 2022')
    #     select = option_menu(None,
    #                      options=["INDIA", "STATES", "TOP CATEGORIES" ],
    #                      default_index=0,
    #                      orientation="horizontal",
    #                      styles={"container": {"width": "100%"},
    #                                "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px"},
    #                                "nav-link-selected": {"background-color": "#6F36AD"}})
    # if select == "INDIA":
    #     tab1, tab2 = st.tabs(["TRANSACTION","USER"])

    #     # TRANSACTION TAB
    #     with tab1:
    #         col1, col2, col3 = st.columns(3)
    #         with col1:
    #             in_tr_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='in_tr_yr')
    #         with col2:
    #             in_tr_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='in_tr_qtr')
    #         with col3:
    #             in_tr_tr_typ = st.selectbox('**Select Transaction type**',
    #                                         ('Recharge & bill payments', 'Peer-to-peer payments',
    #                                          'Merchant payments', 'Financial Services', 'Others'), key='in_tr_tr_typ')
    #         # SQL Query

    #         # Transaction Analysis bar chart query
    #         cursor.execute(
    #             f"SELECT State, Transaction_amount FROM aggregated_transaction WHERE Year = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
    #         in_tr_tab_qry_rslt = cursor.fetchall()
    #         df_in_tr_tab_qry_rslt = pd.DataFrame(np.array(in_tr_tab_qry_rslt), columns=['State', 'Transaction_amount'])
    #         df_in_tr_tab_qry_rslt1 = df_in_tr_tab_qry_rslt.set_index(pd.Index(range(1, len(df_in_tr_tab_qry_rslt) + 1)))

    #         # Transaction Analysis table query
    #         cursor.execute(
    #             f"SELECT State, Transaction_count, Transaction_amount FROM aggregated_transaction WHERE Year = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
    #         in_tr_anly_tab_qry_rslt = cursor.fetchall()
    #         df_in_tr_anly_tab_qry_rslt = pd.DataFrame(np.array(in_tr_anly_tab_qry_rslt),
    #                                                   columns=['State', 'Transaction_count', 'Transaction_amount'])
    #         df_in_tr_anly_tab_qry_rslt1 = df_in_tr_anly_tab_qry_rslt.set_index(
    #             pd.Index(range(1, len(df_in_tr_anly_tab_qry_rslt) + 1)))

    #         # Total Transaction Amount table query
    #         cursor.execute(
    #             f"SELECT SUM(Transaction_amount), AVG(Transaction_amount) FROM aggregated_transaction WHERE Year = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
    #         in_tr_am_qry_rslt = cursor.fetchall()
    #         df_in_tr_am_qry_rslt = pd.DataFrame(np.array(in_tr_am_qry_rslt), columns=['Total', 'Average'])
    #         df_in_tr_am_qry_rslt1 = df_in_tr_am_qry_rslt.set_index(['Average'])

    #         # Total Transaction Count table query
    #         cursor.execute(
    #             f"SELECT SUM(Transaction_count), AVG(Transaction_count) FROM aggregated_transaction WHERE Year = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
    #         in_tr_co_qry_rslt = cursor.fetchall()
    #         df_in_tr_co_qry_rslt = pd.DataFrame(np.array(in_tr_co_qry_rslt), columns=['Total', 'Average'])
    #         df_in_tr_co_qry_rslt1 = df_in_tr_co_qry_rslt.set_index(['Average'])

    #         # GEO VISUALISATION
    #         # Drop a State column from df_in_tr_tab_qry_rslt
    #         df_in_tr_tab_qry_rslt.drop(columns=['State'], inplace=True)
    #         # Clone the gio data
    #         url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    #         response = requests.get(url)
    #         data1 = json.loads(response.content)
    #         # Extract state names and sort them in alphabetical order
    #         state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
    #         state_names_tra.sort()
    #         # Create a DataFrame with the state names column
    #         df_state_names_tra = pd.DataFrame({'State': state_names_tra})
    #         # Combine the Gio State name with df_in_tr_tab_qry_rslt
    #         df_state_names_tra['Transaction_amount'] = df_in_tr_tab_qry_rslt
    #         # convert dataframe to csv file
    #         df_state_names_tra.to_csv('State_trans.csv', index=False)
    #         # Read csv
    #         df_tra = pd.read_csv('State_trans.csv')
    #         # Geo plot
    #         fig_tra = px.choropleth(
    #             df_tra,
    #             geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    #             featureidkey='properties.ST_NM', locations='State', color='Transaction_amount',
    #             color_continuous_scale='thermal', title='Transaction Analysis')
    #         fig_tra.update_geos(fitbounds="locations", visible=False)
    #         fig_tra.update_layout(title_font=dict(size=33), title_font_color='#AD71EF', height=800)
    #         st.plotly_chart(fig_tra, use_container_width=True)

    #         # ---------   /   All India Transaction Analysis Bar chart  /  ----- #
    #         df_in_tr_tab_qry_rslt1['State'] = df_in_tr_tab_qry_rslt1['State'].astype(str)
    #         df_in_tr_tab_qry_rslt1['Transaction_amount'] = df_in_tr_tab_qry_rslt1['Transaction_amount'].astype(float)
    #         df_in_tr_tab_qry_rslt1_fig = px.bar(df_in_tr_tab_qry_rslt1, x='State', y='Transaction_amount',
    #                                             color='Transaction_amount', color_continuous_scale='thermal',
    #                                             title='Transaction Analysis Chart', height=700, )
    #         df_in_tr_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
    #         st.plotly_chart(df_in_tr_tab_qry_rslt1_fig, use_container_width=True)

    #         # -------  /  All India Total Transaction calculation Table   /   ----  #
    #         st.header(':violet[Total calculation]')

    #         col4, col5 = st.columns(2)
    #         with col4:
    #             st.subheader(':violet[Transaction Analysis]')
    #             st.dataframe(df_in_tr_anly_tab_qry_rslt1)
    #         with col5:
    #             st.subheader(':violet[Transaction Amount]')
    #             st.dataframe(df_in_tr_am_qry_rslt1)
    #             st.subheader(':violet[Transaction Count]')
    #             st.dataframe(df_in_tr_co_qry_rslt1)

    #     # USER TAB
    #     with tab2:
    #         col1, col2 = st.columns(2)
    #         with col1:
    #             in_us_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='in_us_yr')
    #         with col2:
    #             in_us_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='in_us_qtr')

    #         # SQL Query

    #         # User Analysis Bar chart query
    #         cursor.execute(f"SELECT State, SUM(User_Count) FROM aggregated_user WHERE Year = '{in_us_yr}' AND Quarter = '{in_us_qtr}' GROUP BY State;")
    #         in_us_tab_qry_rslt = cursor.fetchall()
    #         df_in_us_tab_qry_rslt = pd.DataFrame(np.array(in_us_tab_qry_rslt), columns=['State', 'User Count'])
    #         df_in_us_tab_qry_rslt1 = df_in_us_tab_qry_rslt.set_index(pd.Index(range(1, len(df_in_us_tab_qry_rslt) + 1)))

    #         # Total User Count table query
    #         cursor.execute(f"SELECT SUM(User_Count), AVG(User_Count) FROM aggregated_user WHERE Year = '{in_us_yr}' AND Quarter = '{in_us_qtr}';")
    #         in_us_co_qry_rslt = cursor.fetchall()
    #         df_in_us_co_qry_rslt = pd.DataFrame(np.array(in_us_co_qry_rslt), columns=['Total', 'Average'])
    #         df_in_us_co_qry_rslt1 = df_in_us_co_qry_rslt.set_index(['Average'])



    #         # GEO VISUALIZATION FOR USER

    #         # Drop a State column from df_in_us_tab_qry_rslt
    #         df_in_us_tab_qry_rslt.drop(columns=['State'], inplace=True)
    #         # Clone the gio data
    #         url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    #         response = requests.get(url)
    #         data2 = json.loads(response.content)
    #         # Extract state names and sort them in alphabetical order
    #         state_names_use = [feature['properties']['ST_NM'] for feature in data2['features']]
    #         state_names_use.sort()
    #         # Create a DataFrame with the state names column
    #         df_state_names_use = pd.DataFrame({'State': state_names_use})
    #         # Combine the Gio State name with df_in_tr_tab_qry_rslt
    #         df_state_names_use['User Count'] = df_in_us_tab_qry_rslt
    #         # convert dataframe to csv file
    #         df_state_names_use.to_csv('State_user.csv', index=False)
    #         # Read csv
    #         df_use = pd.read_csv('State_user.csv')
    #         # Geo plot
    #         fig_use = px.choropleth(
    #             df_use,
    #             geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    #             featureidkey='properties.ST_NM', locations='State', color='User Count',
    #             color_continuous_scale='thermal', title='User Analysis')
    #         fig_use.update_geos(fitbounds="locations", visible=False)
    #         fig_use.update_layout(title_font=dict(size=33), title_font_color='#AD71EF', height=800)
    #         st.plotly_chart(fig_use, use_container_width=True)

    #         # ----   /   All India User Analysis Bar chart   /     -------- #
    #         df_in_us_tab_qry_rslt1['State'] = df_in_us_tab_qry_rslt1['State'].astype(str)
    #         df_in_us_tab_qry_rslt1['User Count'] = df_in_us_tab_qry_rslt1['User Count'].astype(int)
    #         df_in_us_tab_qry_rslt1_fig = px.bar(df_in_us_tab_qry_rslt1, x='State', y='User Count', color='User Count',
    #                                             color_continuous_scale='thermal', title='User Analysis Chart',
    #                                             height=700, )
    #         df_in_us_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
    #         st.plotly_chart(df_in_us_tab_qry_rslt1_fig, use_container_width=True)

    #         # -----   /   All India Total User calculation Table   /   ----- #
    #         st.header(':violet[Total calculation]')

    #         col3, col4 = st.columns(2)
    #         with col3:
    #             st.subheader(':violet[User Analysis]')
    #             st.dataframe(df_in_us_tab_qry_rslt1)
    #         with col4:
    #             st.subheader(':violet[User Count]')
    #             st.dataframe(df_in_us_co_qry_rslt1)

    # # STATE TAB
    # if select == "STATES":
    #     tab3 ,tab4 = st.tabs(["TRANSACTION","USER"])

    #     #TRANSACTION TAB FOR STATE
    #     with tab3:
    #         col1, col2, col3 = st.columns(3)
    #         with col1:
    #             st_tr_st = st.selectbox('**Select State**', (
    #             'andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar',
    #             'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
    #             'haryana', 'himachal-pradesh',
    #             'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
    #             'maharashtra', 'manipur',
    #             'meghalaya', 'mizoram', 'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
    #             'tamil-nadu', 'telangana',
    #             'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'), key='st_tr_st')
    #         with col2:
    #             st_tr_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='st_tr_yr')
    #         with col3:
    #             st_tr_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='st_tr_qtr')


    #         # SQL QUERY

    #         #Transaction Analysis bar chart query
    #         cursor.execute(f"SELECT Transaction_type, Transaction_amount FROM aggregated_transaction WHERE State = '{st_tr_st}' AND Year = '{st_tr_yr}' AND Quarter = '{st_tr_qtr}';")
    #         st_tr_tab_bar_qry_rslt = cursor.fetchall()
    #         df_st_tr_tab_bar_qry_rslt = pd.DataFrame(np.array(st_tr_tab_bar_qry_rslt),
    #                                                  columns=['Transaction_type', 'Transaction_amount'])
    #         df_st_tr_tab_bar_qry_rslt1 = df_st_tr_tab_bar_qry_rslt.set_index(
    #             pd.Index(range(1, len(df_st_tr_tab_bar_qry_rslt) + 1)))

    #         # Transaction Analysis table query
    #         cursor.execute(f"SELECT Transaction_type, Transaction_count, Transaction_amount FROM aggregated_transaction WHERE State = '{st_tr_st}' AND Year = '{st_tr_yr}' AND Quarter = '{st_tr_qtr}';")
    #         st_tr_anly_tab_qry_rslt = cursor.fetchall()
    #         df_st_tr_anly_tab_qry_rslt = pd.DataFrame(np.array(st_tr_anly_tab_qry_rslt),
    #                                                   columns=['Transaction_type', 'Transaction_count',
    #                                                            'Transaction_amount'])
    #         df_st_tr_anly_tab_qry_rslt1 = df_st_tr_anly_tab_qry_rslt.set_index(
    #             pd.Index(range(1, len(df_st_tr_anly_tab_qry_rslt) + 1)))

    #         # Total Transaction Amount table query
    #         cursor.execute(f"SELECT SUM(Transaction_amount), AVG(Transaction_amount) FROM aggregated_transaction WHERE State = '{st_tr_st}' AND Year = '{st_tr_yr}' AND Quarter = '{st_tr_qtr}';")
    #         st_tr_am_qry_rslt = cursor.fetchall()
    #         df_st_tr_am_qry_rslt = pd.DataFrame(np.array(st_tr_am_qry_rslt), columns=['Total', 'Average'])
    #         df_st_tr_am_qry_rslt1 = df_st_tr_am_qry_rslt.set_index(['Average'])

    #         # Total Transaction Count table query
    #         cursor.execute(f"SELECT SUM(Transaction_count), AVG(Transaction_count) FROM aggregated_transaction WHERE State = '{st_tr_st}' AND Year ='{st_tr_yr}' AND Quarter = '{st_tr_qtr}';")
    #         st_tr_co_qry_rslt = cursor.fetchall()
    #         df_st_tr_co_qry_rslt = pd.DataFrame(np.array(st_tr_co_qry_rslt), columns=['Total', 'Average'])
    #         df_st_tr_co_qry_rslt1 = df_st_tr_co_qry_rslt.set_index(['Average'])



    #         # -----    /   State wise Transaction Analysis bar chart   /   ------ #

    #         df_st_tr_tab_bar_qry_rslt1['Transaction_type'] = df_st_tr_tab_bar_qry_rslt1['Transaction_type'].astype(str)
    #         df_st_tr_tab_bar_qry_rslt1['Transaction_amount'] = df_st_tr_tab_bar_qry_rslt1['Transaction_amount'].astype(
    #             float)
    #         df_st_tr_tab_bar_qry_rslt1_fig = px.bar(df_st_tr_tab_bar_qry_rslt1, x='Transaction_type',
    #                                                 y='Transaction_amount', color='Transaction_amount',
    #                                                 color_continuous_scale='thermal',
    #                                                 title='Transaction Analysis Chart', height=500, )
    #         df_st_tr_tab_bar_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
    #         st.plotly_chart(df_st_tr_tab_bar_qry_rslt1_fig, use_container_width=True)

    #         # ------  /  State wise Total Transaction calculation Table  /  ---- #
    #         st.header(':violet[Total calculation]')

    #         col4, col5 = st.columns(2)
    #         with col4:
    #             st.subheader(':violet[Transaction Analysis]')
    #             st.dataframe(df_st_tr_anly_tab_qry_rslt1)
    #         with col5:
    #             st.subheader(':violet[Transaction Amount]')
    #             st.dataframe(df_st_tr_am_qry_rslt1)
    #             st.subheader(':violet[Transaction Count]')
    #             st.dataframe(df_st_tr_co_qry_rslt1)


    #     # USER TAB FOR STATE
    #     with tab4:
    #         col5, col6 = st.columns(2)
    #         with col5:
    #             st_us_st = st.selectbox('**Select State**', (
    #             'andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar',
    #             'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
    #             'haryana', 'himachal-pradesh',
    #             'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
    #             'maharashtra', 'manipur',
    #             'meghalaya', 'mizoram', 'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
    #             'tamil-nadu', 'telangana',
    #             'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'), key='st_us_st')
    #         with col6:
    #             st_us_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='st_us_yr')
    #         # SQL QUERY

    #         # User Analysis Bar chart query
    #         cursor.execute(f"SELECT Quarter, SUM(User_Count) FROM aggregated_user WHERE State = '{st_us_st}' AND Year = '{st_us_yr}' GROUP BY Quarter;")
    #         st_us_tab_qry_rslt = cursor.fetchall()
    #         df_st_us_tab_qry_rslt = pd.DataFrame(np.array(st_us_tab_qry_rslt), columns=['Quarter', 'User Count'])
    #         df_st_us_tab_qry_rslt1 = df_st_us_tab_qry_rslt.set_index(pd.Index(range(1, len(df_st_us_tab_qry_rslt) + 1)))

    #         # Total User Count table query
    #         cursor.execute(f"SELECT SUM(User_Count), AVG(User_Count) FROM aggregated_user WHERE State = '{st_us_st}' AND Year = '{st_us_yr}';")
    #         st_us_co_qry_rslt = cursor.fetchall()
    #         df_st_us_co_qry_rslt = pd.DataFrame(np.array(st_us_co_qry_rslt), columns=['Total', 'Average'])
    #         df_st_us_co_qry_rslt1 = df_st_us_co_qry_rslt.set_index(['Average'])


    #         # -----   /   All India User Analysis Bar chart   /   ----- #
    #         df_st_us_tab_qry_rslt1['Quarter'] = df_st_us_tab_qry_rslt1['Quarter'].astype(int)
    #         df_st_us_tab_qry_rslt1['User Count'] = df_st_us_tab_qry_rslt1['User Count'].astype(int)
    #         df_st_us_tab_qry_rslt1_fig = px.bar(df_st_us_tab_qry_rslt1, x='Quarter', y='User Count', color='User Count',
    #                                             color_continuous_scale='thermal', title='User Analysis Chart',
    #                                             height=500, )
    #         df_st_us_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
    #         st.plotly_chart(df_st_us_tab_qry_rslt1_fig, use_container_width=True)

    #         # ------    /   State wise User Total User calculation Table   /   -----#
    #         st.header(':violet[Total calculation]')

    #         col3, col4 = st.columns(2)
    #         with col3:
    #             st.subheader(':violet[User Analysis]')
    #             st.dataframe(df_st_us_tab_qry_rslt1)
    #         with col4:
    #             st.subheader(':violet[User Count]')
    #             st.dataframe(df_st_us_co_qry_rslt1)

    # # TOP CATEGORIES
    # if select == "TOP CATEGORIES":
    #     tab5, tab6 = st.tabs(["TRANSACTION", "USER"])

    #     # Overall top transaction
    #     #TRANSACTION TAB
    #     with tab5:
    #         top_tr_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='top_tr_yr')

    #         #SQL QUERY

    #         #Top Transaction Analysis bar chart query
    #         cursor.execute(
    #             f"SELECT State, SUM(Transaction_amount) As Transaction_amount FROM top_transaction WHERE Year = '{top_tr_yr}' GROUP BY State ORDER BY Transaction_amount DESC LIMIT 10;")
    #         top_tr_tab_qry_rslt = cursor.fetchall()
    #         df_top_tr_tab_qry_rslt = pd.DataFrame(np.array(top_tr_tab_qry_rslt),
    #                                               columns=['State', 'Top Transaction amount'])
    #         df_top_tr_tab_qry_rslt1 = df_top_tr_tab_qry_rslt.set_index(
    #             pd.Index(range(1, len(df_top_tr_tab_qry_rslt) + 1)))

    #         # Top Transaction Analysis table query
    #         cursor.execute(
    #             f"SELECT State, SUM(Transaction_amount) as Transaction_amount, SUM(Transaction_count) as Transaction_count FROM top_transaction WHERE Year = '{top_tr_yr}' GROUP BY State ORDER BY Transaction_amount DESC LIMIT 10;")
    #         top_tr_anly_tab_qry_rslt = cursor.fetchall()
    #         df_top_tr_anly_tab_qry_rslt = pd.DataFrame(np.array(top_tr_anly_tab_qry_rslt),
    #                                                    columns=['State', 'Top Transaction amount',
    #                                                             'Total Transaction count'])
    #         df_top_tr_anly_tab_qry_rslt1 = df_top_tr_anly_tab_qry_rslt.set_index(
    #             pd.Index(range(1, len(df_top_tr_anly_tab_qry_rslt) + 1)))



    #         # All India Transaction Analysis Bar chart
    #         df_top_tr_tab_qry_rslt1['State'] = df_top_tr_tab_qry_rslt1['State'].astype(str)
    #         df_top_tr_tab_qry_rslt1['Top Transaction amount'] = df_top_tr_tab_qry_rslt1[
    #             'Top Transaction amount'].astype(float)
    #         df_top_tr_tab_qry_rslt1_fig = px.bar(df_top_tr_tab_qry_rslt1, x='State', y='Top Transaction amount',
    #                                              color='Top Transaction amount', color_continuous_scale='thermal',
    #                                              title='Top Transaction Analysis Chart', height=600, )
    #         df_top_tr_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
    #         st.plotly_chart(df_top_tr_tab_qry_rslt1_fig, use_container_width=True)


    #         #All India Total Transaction calculation Table
    #         st.header(':violet[Total calculation]')
    #         st.subheader('Top Transaction Analysis')
    #         st.dataframe(df_top_tr_anly_tab_qry_rslt1)

    #     # OVERALL TOP USER DATA
    #     # USER TAB
    #     with tab6:
    #         top_us_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='top_us_yr')

    #         #SQL QUERY

    #         #Top User Analysis bar chart query
    #         cursor.execute(f"SELECT State, SUM(Registered_User) AS Top_user FROM top_user WHERE Year='{top_us_yr}' GROUP BY State ORDER BY Top_user DESC LIMIT 10;")
    #         top_us_tab_qry_rslt = cursor.fetchall()
    #         df_top_us_tab_qry_rslt = pd.DataFrame(np.array(top_us_tab_qry_rslt), columns=['State', 'Total User count'])
    #         df_top_us_tab_qry_rslt1 = df_top_us_tab_qry_rslt.set_index(
    #             pd.Index(range(1, len(df_top_us_tab_qry_rslt) + 1)))



    #         #All India User Analysis Bar chart
    #         df_top_us_tab_qry_rslt1['State'] = df_top_us_tab_qry_rslt1['State'].astype(str)
    #         df_top_us_tab_qry_rslt1['Total User count'] = df_top_us_tab_qry_rslt1['Total User count'].astype(float)
    #         df_top_us_tab_qry_rslt1_fig = px.bar(df_top_us_tab_qry_rslt1, x='State', y='Total User count',
    #                                              color='Total User count', color_continuous_scale='thermal',
    #                                              title='Top User Analysis Chart', height=600, )
    #         df_top_us_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
    #         st.plotly_chart(df_top_us_tab_qry_rslt1_fig, use_container_width=True)

    #         #All India Total Transaction calculation Table
    #         st.header(':violet[Total calculation]')
    #         st.subheader('violet[Total User Analysis]')
    #         st.dataframe(df_top_us_tab_qry_rslt1)

#     elif selected_option == "Insights":
#         st.title("Insights")
#         st.write("This is the insights page content.")
        

# if __name__ == "__main__":
#     main()






