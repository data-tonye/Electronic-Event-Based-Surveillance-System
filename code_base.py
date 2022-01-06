from serpapi import GoogleSearch
import pandas as pd
import more_itertools as mt
from datetime import datetime
import sqlite3
import dateparser
import urllib

import altair as alt



class event_based:
  def __init__(self):
    ## Retreives the date for today and previous day
    now = datetime.now()

    ## retreives month, day and year
    month = now.month
    from_day = now.day
    to_day = now.day
    year = now.year
    params = {
          "q": None,
          "tbm": "nws",
          "tbs": f"cdr:1,cd_min:{month}/{from_day}/{year},cd_max:{month}/{to_day}/{year}",
          "num": 1000,
          "location": "Nigeria",
          "api_key": "abb004e760c772655be12e1183199ecd8fe41ec4b62112be17772fb1be6c8598"
          }
    
    self.params = params
    
    
    
  def change_params(self, term):
    self.params.update(q = term)


  def search_google(self):
    '''
    initiates the google api call with
    the search parameters

    INPUT: None
    
    OUTPUT: returns a block of dictionaries with the google news results
    '''
    parameters = self.params  ## using the dictionary params in this function

    ## searches with the given parameters
    search = GoogleSearch(parameters) 

    ## get the results in dictionary form
    results = search.get_dict()

    ## streamlines the results to news results only
    #news_results = results['news_results'] 

    return results
    pass


  def create_dateframe(self, results):

    '''
    takes the results from the google search function,
    cleans it and creates a dataframe.

    INPUT: dictionary key names picked to create the
    desired columns and values for the dataframe table

    OUTPUT:
    - saved table in an sqlite database to store historic data
    - returns a cleaned dataframe
    '''
    ## saves results from the google search function
    

    ## iterates through the results dictionary and saves each
    ## value in a list under a key name variable
    ## globals() changes the key name into a variable to save the results
    ## of the desired key

    for index in range(len(results)):
      for key in results[index]:
        position = [d['position'] for d in mt.collapse(results, base_type=dict)]
        date = [d['date'] for d in mt.collapse(results, base_type=dict)]
        title = [d['title'] for d in mt.collapse(results, base_type=dict)]
        source = [d['source'] for d in mt.collapse(results, base_type=dict)]
        link = [d['link'] for d in mt.collapse(results, base_type=dict)]
        snippet = [d['snippet'] for d in mt.collapse(results, base_type=dict)]

        ## each key name becomes a column with values from the above variables
        d = {'position' : position, 'date' : date, 'title' : title, 'source' : source, 'link' : link, 'snippet' : snippet}
    ## creates a data frame from the data
    df = pd.DataFrame(data = d)

    ## sets parameters for the dataframe when displayed
    pd.set_option("display.max_rows", None, "display.max_columns", None, "max_colwidth", None)

    ## changes 'x ago' values to standard time values
    df['date'] = df['date'].apply(lambda x :dateparser.parse(x).strftime("%d %B %Y"))

    def make_clickable(val):
      '''
      INPUT: values from column
      OUTPUT: values with clickable links
      '''
      # target _blank to open new window
      return '<a target="_blank" href="{}">{}</a>'.format(val,val)

    df.style.format({'link': make_clickable})
    

    ## saves a copy of the dataframe values and saves it in a databases
    ## and appends with dataframes from new searches
    df_historic = df

    connection = sqlite3.connect('search_database.db',
                              detect_types=sqlite3.PARSE_DECLTYPES |
                              sqlite3.PARSE_COLNAMES)

    df_historic.to_sql(name='search_history', con=connection, if_exists = 'append')
    connection.commit()
    connection.close()

    return df
    pass


  def save_search(self, df):
    '''
    saves the search term, the number of results and date
    of the search in a database

    INPUT: none

    OUTPUT: dataframe with searche results, number of searches
    date of search
    '''
    

    ## initializing a dictionary
    dict_list = ['disease', 'count', 'time']
    plot_dict = dict.fromkeys(dict_list)

    ## updates the value for the 'disease' key
    plot_dict.update(disease = self.params['q'])

    ## gets result count and updates the value 
    ## of the 'çount' key
    result_count = df.position.count()
    plot_dict.update(count = result_count)

    ## gets the current date and updates the value 
    ## of the 'time' key
    now = datetime.now()
    day_time = now.strftime("%d %B %Y")
    plot_dict.update(time = day_time)

    ## saves values in a database
    connection = sqlite3.connect('plot.db',
                              detect_types=sqlite3.PARSE_DECLTYPES |
                              sqlite3.PARSE_COLNAMES)
    cursor = connection.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS plot_table (
      disease TEXT, 
      count TEXT,
      time TEXT)'''
      )
    
    columns = ', '.join("`" + str(x).replace('/', '_') + "`"
    for x in plot_dict.keys())
    values = ', '.join("'" + str(x).replace('/', '_') + "'"
    for x in plot_dict.values())

    sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('plot_table', columns, values)
    cursor.execute(sql)
    search_table = pd.read_sql('select * from plot_table', connection)
    connection.commit()
    connection.close()

    return search_table
    pass

  def plot_searches(self, search_df):
    '''
    plots the search results over time

    INPUT: search data

    OUTPUT: plots a line chart of count of
            disease search results over time
    '''

    ## converts the time column into datetime format

    ## saves the search dataframe and plots a line chart


    gp_chart = alt.Chart(search_df).mark_line().encode(
      alt.X('time', title = 'Date'),
      alt.Y('count:Q', title = 'Disease count'), 
      alt.Color('disease:N')).properties(width=1200,height=500, title = 'A plot showing daily alerts')
  
    
    return gp_chart
    pass
