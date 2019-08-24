from .models import UserProfile, InformationHousehold
import pandas as pd
import numpy as np
import mysql.connector
import sqlalchemy
from datetime import datetime
import calendar


def load_df_from_mysql_3(table,  username='root', password='', host='localhost', dname='augdb'):
    database_username = username
    database_password = password
    database_ip = host
    database_name = dname
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                   format(database_username, database_password,
                                                          database_ip, database_name), pool_recycle=1,
                                                   pool_timeout=57600).connect()

    # df.to_sql(con=database_connection, name=name, if_exists='append', chunksize=100)
    df = pd.read_sql_table(table, database_connection)
    database_connection.close()
    return df


def get_meter_id(identifier):
    print(identifier)
    result_query = InformationHousehold.objects.filter(LCLid=identifier)
    print(result_query[0])
    if len(result_query) == 0:
        return False, None
    else:
        return True, result_query[0].file


def save_df_to_mysql(df, name, username='root', password='', host='localhost', dname='augdb'):
    database_username = username
    database_password = password
    database_ip = host
    database_name = dname
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                   format(database_username, database_password,
                                                          database_ip, database_name), pool_recycle=1,
                                                   pool_timeout=57600).connect()

    df.to_sql(con=database_connection, name=name, if_exists='append', chunksize=100)
    database_connection.close()


def load_df_from_mysql(table,  username='root', password='', host='localhost', dname='augdb'):
    database_username = username
    database_password = password
    database_ip = host
    database_name = dname
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                   format(database_username, database_password,
                                                          database_ip, database_name), pool_recycle=1,
                                                   pool_timeout=57600).connect()

    # df.to_sql(con=database_connection, name=name, if_exists='append', chunksize=100)
    df = pd.read_sql_table(table, database_connection)
    df.dropna(inplace=True)
    # df = df[df.col3 != 'Null']
    df.col3 = pd.to_numeric(df.col3)
    df.col2 = pd.to_datetime(df.col2)
    database_connection.close()
    return df



def load_df_from_mysql_2(table, identifier, username='root', password='', host='localhost', dname='augdb'):
    database_username = username
    database_password = password
    database_ip = host
    database_name = dname
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                   format(database_username, database_password,
                                                          database_ip, database_name), pool_recycle=1,
                                                   pool_timeout=57600).connect()

    # df.to_sql(con=database_connection, name=name, if_exists='append', chunksize=100)
    query = "select * from {} where col1='{}'".format(table, identifier)
    df = pd.read_sql_query(query, con=database_connection)
    df.dropna(inplace=True)
#     df = df[df.col3 != 'Null']
    df.col3 = pd.to_numeric(df.col3)
    df.col2 = pd.to_datetime(df.col2)
    database_connection.close()
    return df


def get_total_usage(identifier, block):
    # def idtotal(id, block):
    path = ''
    df = pd.read_csv(path, names=['col1', 'col2', 'col3'], skiprows=1)
    df = df[df.col1 == id]
    df = df[df.col3 != 'Null']
    df.col3 = pd.to_numeric(df.col3)
    tot_energy = np.sum(df.col3)
    #     for x in df['col1']:
    #         if(x == id):
    #             for val in df['col3']:
    #                 tot_energy += val
    return tot_energy


def get_energy_this_month(df):
    this_month = datetime.today().month
    df = df[df.col2.apply(lambda x: x.month == this_month)]
    return np.sum(df.col3)


def get_energy_last_months(df):
    this_month = datetime.today().month
    df['month'] = df.col2.apply(lambda x: x.month)
    df = df[df.month < this_month]
    return df.groupby(['month']).sum()['col3']


def get_energy_this_day(df):
    this_day = datetime.today().day
    df = df[df.col2.apply(lambda x: x.day == this_day)]
    return np.sum(df.col3)


def neighbourhood_average_this_month(df):
    this_month = datetime.today().month
    df = df[df.col2.apply(lambda x: x.month == this_month)]
    return np.mean(df.col3)

bank_holidays = load_df_from_mysql_3('bank_holidays')
bank_holidays['Bank holidays'] = pd.to_datetime(bank_holidays['Bank holidays'])
bank_holidays['day'] = bank_holidays['Bank holidays'].apply(lambda x:  str(x.day) + ',' + str(x.month))


def is_public_holiday(date):
    day = str(date.day) + ',' + str(date.month)
#     print(day)
    hai_kya = day in bank_holidays['day'].values
#     print(hai_kya)
    if hai_kya:
        return [1, 0]
    return [0, 1]

def findDay(date):
    date = date.split(" ")[0].replace("-", " ")
    day = datetime.strptime(date, '%Y %m %d').weekday()
    day = calendar.day_name[day]
    d = {
        'Sunday': 0, 'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0
    }
    d[day] = 1
    return list(d.values())


# print(findDay("2012-10-12 00:30:00.0000000"))


def predict_season(date):
    date = date.split(" ")[0].replace("-", " ")
    mon = datetime.strptime(date, '%Y %m %d').month
    day = datetime.strptime(date, '%Y %m %d').day
    if mon in ('January', 'February', 'March'):
        season = 'winter'
    elif mon in ('April', 'May', 'June'):
        season = 'spring'
    elif mon in ('July', 'August', 'September'):
        season = 'summer'
    else:
        season = 'autumn'
    if (mon == 'March') and (day > 19):
        season = 'spring'
    elif (mon == 'June') and (day > 20):
        season = 'summer'
    elif (mon == 'September') and (day > 21):
        season = 'autumn'
    elif (mon == 'December') and (day > 20):
        season = 'winter'

    d = {
        'winter': 0, 'summer': 0, 'autumn': 0, 'spring': 0
    }
    d[season] = 1
    return list(d.values())

def sasta_predict(values):
    vals = []


def price(pl, weth, totalusage, avgcurr, usgharka_usage):
    wethval = 0
    total_demand = 0
    ghar = 0
    dynamic_pricing = 0
    avgcurr = 3
    if weth > 30:
        wethval = 0.4
    elif weth < 10:
        wethval = 0.4
    else:
        wethval = 0.2
    if totalusage >= ((4 * 2.5 * avgcurr) - 6):
        total_demand = 0.6
    elif totalusage < ((4 * 2.5 * avgcurr) - 10) and totalusage > ((4 * 2.5 * avgcurr) - 15):
        total_demand = 0.3
    else:
        total_demand = 0.1
    if usgharka_usage < 10:  # usual value 50 assume kiya threshold
        ghar = 0.2
    elif usgharka_usage > 18:
        ghar = 0.5
    else:
        ghar = 0.3
    return ((wethval + total_demand + ghar) * 8)

