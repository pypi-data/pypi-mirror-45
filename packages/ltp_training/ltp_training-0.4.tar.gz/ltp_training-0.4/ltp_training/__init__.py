import pandas as pd
from sqlalchemy import *
import os

def getResultsPY(team_name, username, password):
    query='''
    SELECT * FROM PUBLIC.TITANIC_SUBMISSIONS
    '''
    print(f'Querying results for team name : {team_name}')
    print(os.getcwd())

    real=pd.read_csv('titanic_testkey.csv')

    predictions = queryRedshiftToPandas(query) #see the function definition at the end of the code
    predictions=predictions.merge(real, how='inner', on='passengerid') #get the real results
    predictions['error'] = 1-abs(predictions.survived_x - predictions.survived_y) #calculate accuracy
    
    predictions=predictions[['teamid', 'error']] #drop unimportant columns
    predictions=predictions.groupby(['teamid']).mean().reset_index() #group by to get the average accuracy per team

    team_prediction=predictions[predictions.teamid==team_name] #select the specific team's result
    accuracy = '{:.1%}'.format(team_prediction.error.iloc[0]) #display the accuracy
    print(f'Your team accuracy was {accuracy}') #print the output
    return True

    

def get_engine_redshift(username, password):
    url = 'ltp-redshift.cv6audww0okc.eu-west-1.redshift.amazonaws.com'
    db = 'training'
    return create_engine( 'postgresql://{0}:{1}@{2}:5439/{3}'.format(username, password, url, db))



def queryRedshiftToPandas(query):
    """Function to run querys on redhsift and return the result as a pandas dataframe.

    Args:
        query (str): The query to be run in redshift.

    Returns:
        pandas dataframe: result of the query run.
    """
        
    engine = get_engine_redshift() 
 
    with engine.connect() as conn, conn.begin():
        df = pd.read_sql(query, conn)
    
    return df

