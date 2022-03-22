## import libraries
import streamlit as st
from code_base import *
import sqlite3





st.set_page_config(
     page_title="EBS App",
     page_icon="🧊",
     layout="wide"
      )

st.title(
  'An Electronic Event Based Surveillance System (eEBS)'
)

st.markdown(
  'This project is aimed at demonstrating how health surveillance officers at different levels can monitor online news or events to anticipate a potential health threat.')
  
st.markdown(
  'According to the World Health Organization (WHO), Event-based surveillance is the organized colection, monitoring, assessment and interpretation of unstructured ad hoc information regard health events or risk,which may represent an acute risk to health.'
)
    
st.markdown(
  'popular examples of a electronic event based surveillance system are [HealthMap](https://healthmap.org/) and Tatafo (used by Nigeria Centre for Disease Control (NCDC)).'
)

st.markdown(
  'This is a prototype emualating some core features of an electronic event based surveillance system.'
)

  
## divides the display area into two
col1, col2 = st.columns([1, 3])


## creates search boxes
with col1:
  form = st.form(key='search_disease')
  search_term = form.text_input(label='Enter disease search term')
  search_button = form.form_submit_button(label='Search')

  form = st.form(key = 'search_history')
  history_term = form.text_input (label = 'Insert disease or time search term')
  history_button = form.form_submit_button(label='Search History')




try:
  ## initializes the class
  eb = event_based() 

  ## replaces search query
  eb.change_params(search_term)
     
  ## searches for the term and saves the dictionary input
  result = eb.search_google()

  ## converts the 'news result' dictionary into 
  ds = eb.create_dateframe(result['news_results'])
  #saves search details and plots a line chart of the details
  search_plot=eb.save_search(ds)
  
  connection = sqlite3.connect('plot.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
  searches_df = pd.read_sql_query("SELECT * FROM plot_table", connection)
     
  gp_chart = alt.Chart(searches_df).mark_line().encode(
       alt.X('time', title = 'Date'),
       alt.Y('count:Q', title = 'News alert count'), 
       alt.Color('disease:N')).properties(width=1200,height=500, title = 'A plot showing daily alerts')
  
   gp_chart
     
  ## if search button is clicked it displays search dataframe'''
  if search_button:
    with col2:
      #result['news_results']
      st.dataframe(ds)

  ## if the history button is clicked it displays data from available database
  elif history_button:
      connection = sqlite3.connect('search_database.db') 
      cursor = connection.cursor()
      table = cursor.execute('SELECT * FROM search_history WHERE snippet LIKE ? OR date LIKE ?', (f'%{history_term}%', f'%{history_term}%'))
      cols = ['index', 'position', 'date', 'title', 'source', 'link', 'snippet']
      table_results = pd.DataFrame(table, columns= cols)
      with col2:
        table_results

  else:
    pass
except AttributeError:
     print('Results unavailabe')
except KeyError:
     pass
except UnboundLocalError:
     print('Results unavailabe')
     pass



