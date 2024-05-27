import pandas as pd
import re
def preprocess(data):
    pattern1 = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'  #24hr format
    pattern2 = '\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{1,2}\s[A-Z]{2}\s-\s' #12hr format
    pattern3 = '\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{1,2}\s[A-Za-z]{2}\s-\s' #12hr formart with small am,pm

    messages=[]
    mess1 = re.split(pattern1, data)[1:]
    mess2 = re.split(pattern2, data)[1:]
    mess3 = re.split(pattern3, data)[1:]
    maxlen = max(len(mess1),len(mess2),len(mess3))
    if len(mess1) == maxlen:
        messages = mess1
    elif len(mess2) == maxlen:
        messages = mess2
    else:
        messages = mess3

    dates=[]
    dates1 = re.findall(pattern1, data)
    dates2 = re.findall(pattern2, data)
    dates3 = re.findall(pattern3, data)
    maxdatelen = max(len(dates1),len(dates2),len(dates3))
    if len(dates1) == maxdatelen:
        dates = dates1
    elif len(dates2) == maxdatelen:
        dates = dates2
    else:
        dates = dates3

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    if len(dates1) == maxdatelen:
        df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M - ')
    elif len(dates2) == maxdatelen:
        df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p - ')
    else:
        df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_val'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_val'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_val', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + '00')
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))
    df['period'] = period

    return df