import pandas as pd
import urlextract
from wordcloud import WordCloud
from collections import Counter
import emoji

def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df=df[df['users']==selected_user]

    total_messages=df.shape[0]

    words=[]
    for i in df['messages']:
        words.extend(i.split(' '))
    total_words=len(words)

    total_media=df[df['messages']=='<Media omitted>\n'].shape[0]

    extractor=urlextract.URLExtract()
    total_urls=[]
    for message in df['messages']:
        total_urls.extend(extractor.find_urls(message))
    total_urls=len(total_urls)

    return total_messages,total_words,total_media,total_urls

def fetch_most_active(df):
    top5_active_users = df['users'].value_counts().head()
    top5_percentage=round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'users': 'percentage'})
    return top5_active_users,top5_percentage

def fetch_wordcloud(selected_user,df):
    if selected_user!='Overall':
        df=df[df['users']==selected_user]

    wc=WordCloud(width=500,height=100,min_font_size=10,background_color='white')
    new_df=df[(df['messages']!='<Media omitted>\n') & (df['users']!='group_notification')]
    new_df['messages']=new_df['messages'].apply(remove_stop_words)
    wordcloud=wc.generate(new_df['messages'].str.cat(sep=" "))
    return wordcloud

def remove_stop_words(message):
    f = open('stopwords-hinglish.txt', 'r')
    stopwords = f.read()
    x = []
    for word in message.lower().split():
        if word not in stopwords:
            x.append(word)
    return " ".join(x)

def fetch_most_used_words(selected_user,df):
    if selected_user!='Overall':
        df=df[df['users']==selected_user]

    new_df = df[(df['messages'] != '<Media omitted>\n') & (df['users'] != 'group_notification')]
    f=open('stopwords-hinglish.txt','r')
    stopwords = f.read()
    most_words=[]
    for message in new_df['messages']:
        for word in message.lower().split():
            if word not in stopwords:
                most_words.append(word)

    most_words_df=pd.DataFrame(Counter(most_words).most_common(20)).rename(columns={0:'words',1:'count'})
    return most_words_df

def fetch_emoji_stats(selected_user,df):
    if selected_user!='Overall':
        df=df[df['users']==selected_user]

    emojis = []
    for message in df['messages']:
        for word in message.split():
            if emoji.is_emoji(word):
                emojis.extend(word)

    most_emojis_df = pd.DataFrame(Counter(emojis).most_common(5)).rename(columns={0: 'emojis', 1: 'count'})
    return most_emojis_df

def fetch_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['users']==selected_user]

    timeline = df.groupby(['year', 'month_val', 'month']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline

def fetch_weekly_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['users']==selected_user]

    timeline = df.groupby(['day_val']).count()['messages'].reset_index()
    return timeline

def fetch_monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['users']==selected_user]

    timeline = df.groupby(['month']).count()['messages'].reset_index()
    return timeline

def fetch_heatmap(selected_user,df):
    if selected_user!='Overall':
        df=df[df['users']==selected_user]

    activity_heatmap=df.pivot_table(index='day_val',columns='period',values='messages',aggfunc='count').fillna(0)
    return activity_heatmap