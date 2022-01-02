## import libraries
import streamlit as st
from code_base import *
from search_history import *
import sqlite3




## saves results from the create_dateframe function

## saves dataframe table as search_df
#search_df = save_search()


st.set_page_config(
     page_title="EBS App",
     page_icon="🧊",
     layout="wide"
      )

st.title(
  'An Electronic Event Based Surveillance System'
)

st.markdown(
  'This project is aimed at demonstrating how health surveillance officers at different levels can monitor online news or events to anticipate a potential health threat'
  )

col1, col2 = st.columns([1, 3])

with col1:
  form = st.form(key='search_disease')
  search_term = form.text_input(label='Enter disease search term')
  search_button = form.form_submit_button(label='Search')

  form = st.form(key = 'search_history')
  history_term = form.text_input (label = 'Insert disease or time search term')
  history_button = form.form_submit_button(label='Search History')


eb = event_based()
eb.change_params(search_term)
result = eb.search_google()
ds = eb.create_dateframe(result)
search_plot=eb.save_search(ds)
plot = eb.plot_searches(search_plot)
plot


if search_button:
  with col2:
    st.dataframe(ds)
  
elif history_button:
  connection = sqlite3.connect('search_database.db') 
  cursor = connection.cursor()
  table = cursor.execute('SELECT * FROM search_history WHERE snippet LIKE ? OR date LIKE ?', (f'%{history_term}%', f'%{history_term}%'))
  cols = ['index', 'position', 'date', 'title', 'source', 'link', 'snippet']
  table_results = pd.DataFrame(table, columns= cols)
  with col2:
    table_results

  st.write("Results not found")
else:
  pass
