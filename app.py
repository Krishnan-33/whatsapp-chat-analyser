import streamlit as st
import pandas as pd
import preprocess
import helper
import matplotlib.pyplot as plt
import seaborn as sns

# with open('style.css','r') as f:
#     st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

st.sidebar.title('Whatsapp Chat Analyser')


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode(encoding='utf-8')

    df=preprocess.preprocess(data)

    users_list=df['users'].unique().tolist()
    users_list.remove('group_notification')
    users_list.sort()
    users_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Select option to do analysis",users_list)

    if st.sidebar.button("Show Analysis"):
        total_messages,total_words,total_media,total_urls=helper.fetch_stats(selected_user,df)

        st.title("Total Statistics")

        col1, col2, col3, col4=st.columns(4,gap='large')
        with col1:
            st.subheader("Total Messages")
            st.title(total_messages)
        with col2:
            st.subheader("Total Words")
            st.title(total_words)
        with col3:
            st.subheader("Media Shared")
            st.title(total_media)
        with col4:
            st.subheader("Links Shared")
            st.title(total_urls)


        if(selected_user=='Overall'):
            st.title("Most active users")
            x,y=helper.fetch_most_active(df)

            col1, col2=st.columns(2,gap='large')

            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index,x.values,color='#790252',edgecolor='black')
                plt.xticks(rotation=90)
                plt.xlabel("Users",fontweight='bold')
                plt.ylabel("Count of Messages",fontweight='bold')
                st.pyplot(fig)

            with col2:
                st.dataframe(y)

        st.title("Daily Timeline")
        timeline = helper.fetch_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'], color='red')
        plt.xticks(rotation=90)
        plt.xlabel("Timeline",fontweight="bold")
        plt.ylabel("Count of messages",fontweight="bold")
        st.pyplot(fig)

        st.title("Activity Map")
        col1, col2 = st.columns(2)
        with col1:
            st.title("Most Busy Day")
            weekly_timeline = helper.fetch_weekly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(weekly_timeline['day_val'], weekly_timeline['messages'], color='blue')
            plt.xticks(rotation=90)
            plt.xlabel("Days", fontweight="bold")
            plt.ylabel("Count of messages", fontweight="bold")
            st.pyplot(fig)

        with col2:
            st.title("Most Busy Month")
            monthly_timeline = helper.fetch_monthly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(monthly_timeline['month'], monthly_timeline['messages'], color='orange')
            plt.xticks(rotation=90)
            plt.xlabel("Months", fontweight="bold")
            plt.ylabel("Count of messages", fontweight="bold")
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap=helper.fetch_heatmap(selected_user,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        plt.xlabel("Time period", fontweight="bold")
        plt.ylabel("Days", fontweight="bold")
        st.pyplot(fig)

        st.title("Wordcloud")
        df_wc = helper.fetch_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.title("Most used words")
        most_used_words = helper.fetch_most_used_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_used_words['words'], most_used_words['count'], color='#A3C7D6')
        plt.xticks(rotation=90)
        plt.xlabel("Count of words", fontweight="bold")
        plt.ylabel("Words", fontweight="bold")
        st.pyplot(fig)

        most_used_emojis = helper.fetch_emoji_stats(selected_user, df)
        if (most_used_emojis.shape[0] >= 1):
            st.title("Most used emojis")
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(most_used_emojis)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(most_used_emojis['count'],labels=most_used_emojis['emojis'],autopct='%0.2f')
                st.pyplot(fig)
