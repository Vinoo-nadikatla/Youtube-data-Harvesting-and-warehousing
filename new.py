import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import plotly.express as px
import re
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from datetime import datetime
import mysql.connector
from sqlalchemy import create_engine

#API key connection to interact with youtube API
api_service_name = "youtube"
api_version = "v3"
api_Key="YOUTUBE API KEY"
youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=api_Key
            )
 
#engine and mycurser created to intreact with MYSQL Database
engine = create_engine("mysql+mysqlconnector://USERNAME:PASSWORD@HOST/DATABASE")
mydb = mysql.connector.connect(host="HOST",user="USERNAME",password="PASSWORD")   
mycursor = mydb.cursor(buffered=True)
 
#to create and use the database in MYSQL database 
mycursor.execute('create database if not exists youtube_1')
mycursor.execute('use youtube_1')

#setting up streamlit page and adding name to it
icon=Image.open(r"C:\Users\rames\Downloads\Youtube_logo.png")
st.set_page_config(page_title='YouTube Data Harvesting and Warehousing',
                    page_icon=icon,
                    layout='wide',
                    initial_sidebar_state='expanded',
                    menu_items={'About': '''This streamlit application was developed by Vinoothna.N.
                                Contact_e-mail:nadikatlavinoothna46@gmail.com'''})

import streamlit as st
from streamlit_option_menu import option_menu

# Apply the overall background color
st.markdown(
    """
    <style>
    /* Set the background color for the whole page */
    .css-18e3th9, .css-1d391kg, .css-1outpf7, .block-container, .css-fg4pbf {
        background-color: #201e43 !important;
    }

    /* Set text color and font */
    .css-10trblm, .css-1cpxqw2, .css-1d391kg, .css-1outpf7 {
        color: #0a0a0a;
        font-family: 'serif', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create a top navigation bar
selected = option_menu(
    menu_title=None,  # No title for the menu
    options=["Home", "Data collection and upload", "MYSQL Database", "Analysis using SQL"],
    icons=["house", "cloud-upload", "database", "filetype-sql"],
    menu_icon="menu-up",
    default_index=0,  # Set the default index (optional)
    orientation="horizontal",  # Horizontal menu
    styles={
        "container": {"padding": "0!important", "background-color": "#201e43"},  # Main content background color
        "icon": {"color": "#989da4", "font-size": "20px"},  # Icon color and size
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "margin": "0px",
            "color": "#0a0a0a",  # Text color
            "background-color": "#F0F2F6"  # Background color for links
        },
        "nav-link-selected": {
            "background-color": "#134b70",  # Selected tab background
            "color": "#FFFFFF",  # Selected tab text color
        },
    }
)

# Page content based on the selected option
if selected == "Home":
    st.title("Home")
    st.write("Welcome to the Home Page!")
elif selected == "Data collection and upload":
    st.title("Data Collection and Upload")
    st.write("Here you can collect and upload your data.")
elif selected == "MYSQL Database":
    st.title("MYSQL Database")
    st.write("Manage your MySQL Database here.")
elif selected == "Analysis using SQL":
    st.title("Analysis using SQL")
    st.write("Perform SQL analysis here.")

# Setting up the option "Home" in streamlit page
if selected == "Home":
    st.title(':red[You]Tube :blue[Data Harvesting & Warehousing using SQL]')
    st.subheader(':blue[Domain :] Social Media')
    st.subheader(':blue[Overview :]')
    st.markdown('''Build a simple dashboard or UI using Streamlit and 
                retrieve YouTube channel data with the help of the YouTube API.
                Stored the data in an SQL database(warehousing),
                enabling querying of the data using SQL.Visualize the data within the Streamlit app to uncover insights,
                trends with the YouTube channel data''')
    st.subheader(':blue[Skill Take Away :]')
    st.markdown(''' Python scripting,Data Collection,API integration,Data Management using SQL,Streamlit''')
    st.subheader(':blue[About :]')
    st.markdown('''Hello! I'm Vinoothna, a Mechanical Engineering graduate with a deep passion for AI, ML, and robotics.
                 I'm currently embarking on an exciting journey into data science, 
                with my first project titled YouTube Data Harvesting and Warehousing Using SQL.
                 In this project, I delved into the vast expanse of YouTube data to extract meaningful insights. 
                This experience ignited my enthusiasm for data-driven decision-making and significantly enhanced my skills in data extraction techniques and database management.''')
    st.subheader(':blue[Contact:]')
    st.markdown('#### linkedin: www.linkedin.com/in/vinoothna-nadikatla-557354283/')
    st.markdown('#### Email : nadikatlavinoothna46@gmail.com')

# Function to Retrieve channel information from Youtube
def channel_information(channel_id):
    request = youtube.channels().list(
    part="snippet,contentDetails,statistics",
    id=channel_id)
    response = request.execute()

    for i in response['items']:
        channel_data= dict(
            channel_name=i['snippet']['title'],
            Channel_id=i["id"],
            channel_Description=i['snippet']['description'],
            channel_Thumbnail=i['snippet']['thumbnails']['default']['url'],
            channel_playlist_id=i['contentDetails']['relatedPlaylists']['uploads'],
            channel_subscribers=i['statistics']['subscriberCount'],
            channel_video_count=i['statistics']['videoCount'],
            channel_views=i['statistics']['viewCount'],
            channel_publishedat=convert_published_at(i['snippet']['publishedAt']))
    return (channel_data)


# Function to Retrieve playlist information of channel from Youtube
def playlist_information(channel_id):
    playlist_info=[]
    nextPageToken=None #pagination
    try:
        while True:
            request = youtube.playlists().list(
                        part="snippet,contentDetails",
                        channelId=channel_id,
                        maxResults=100,
                        pageToken=nextPageToken
                    )
            response = request.execute()
        
            for i in response['items']:
                data=dict(
                    playlist_id=i['id'],
                    playlist_name=i['snippet']['title'],
                    publishedat=convert_published_at(i['snippet']['publishedAt']),
                    channel_ID=i['snippet']['channelId'],
                    channel_name=i['snippet']['channelTitle'],
                    videoscount=i['contentDetails']['itemCount'])
                playlist_info.append(data)
                nextPageToken=response.get('nextPageToken')
            if nextPageToken is None:
                break
    except HttpError as e:
        error_message = f"Error retrieving playlists: {e}"   # Handle specific YouTube API errors
        st.error(error_message)
    return (playlist_info)

#Function to Retrieve video ids of a channel from Youtube
def get_video_ids(channel_id):
    response= youtube.channels().list( part="contentDetails",
                                        id=channel_id).execute()
    playlist_videos=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    next_page_token=None
    
    videos_ids=[]

    while True:
        response1=youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_videos,
            maxResults=100,
            pageToken=next_page_token).execute()
        
        for i in range (len(response1['items'])):
            videos_ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])
            next_page_token=response1.get('nextPageToken')
        
        if next_page_token is None:
            break
    return (videos_ids)

#Function to convert Duration from ISO 8601 format to HH:MM:SS format
def convert_duration(duration): 
        regex = r'PT(\d+H)?(\d+M)?(\d+S)?'
        match = re.match(regex, duration)
        if not match:
                return '00:00:00'
        hours, minutes, seconds = match.groups()
        hours = int(hours[:-1]) if hours else 0
        minutes = int(minutes[:-1]) if minutes else 0
        seconds = int(seconds[:-1]) if seconds else 0
        total_seconds = hours * 3600 + minutes * 60 + seconds
        return '{:02d}:{:02d}:{:02d}'.format(int(total_seconds / 3600), int((total_seconds % 3600) / 60), int(total_seconds % 60))

# Function to handle publishedAt
def convert_published_at(publishedAt):
    try:
        # Try to parse with microseconds
        return datetime.strptime(publishedAt, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        # Fallback to parsing without microseconds
        return datetime.strptime(publishedAt, '%Y-%m-%dT%H:%M:%SZ')

#Function to Retrieve video information of all video IDS from Youtube
def video_information(video_IDS):
    video_info=[]
    for video_id in video_IDS:
        response= youtube.videos().list(
                        part="snippet,contentDetails,statistics",
                        id=video_id).execute()
        
        for i in response['items']:
                data=dict(
                        channel_id=i['snippet']['channelId'],
                        video_id=i['id'],
                        video_name=i['snippet']['title'],
                        video_Description=i['snippet']['description'],
                        Thumbnail=i['snippet']['thumbnails']['default']['url'],
                        Tags=i['snippet'].get('tags'),
                        publishedAt=convert_published_at(i['snippet']['publishedAt']),
                        Duration=convert_duration(i['contentDetails']['duration']),
                        View_Count=i['statistics']['viewCount'],
                        Like_Count=i['statistics'].get('likeCount'),
                        Dislike_Count=i['statistics'].get('dislikeCount'),
                        Favorite_Count=i['statistics'].get('favoriteCount'),
                        Comment_Count=i['statistics'].get('commentCount'),
                        Caption_Status=i['contentDetails']['caption'] 
                        )
                video_info.append(data)
    return(video_info)

#Function to Retrieve comments information of all video IDS from Youtube
def comments_information(video_IDS):
    comments_info=[]
    try:
        for video_id in video_IDS:
            request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=200)
            response = request.execute()

            for i in response.get('items',[]):
                data=dict(
                            video_id=i['snippet']['videoId'],
                            comment_id=i['snippet']['topLevelComment']['id'],
                            comment_text=i['snippet']['topLevelComment']['snippet']['textDisplay'],
                            comment_author=i['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                            comment_publishedat=convert_published_at(i['snippet']['topLevelComment']['snippet']['publishedAt']))
                comments_info.append(data)
                # Pagination for comments
            nextPageToken = response.get('nextPageToken')
            while nextPageToken:
                request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=100,
                    pageToken=nextPageToken
                )
                response = request.execute()
                for i in response.get('items', []):
                    data = dict(
                        video_id=video_id,
                        comment_id=i['id'],
                        comment_text=i['snippet']['topLevelComment']['snippet']['textDisplay'],
                        comment_author=i['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        comment_publishedat=convert_published_at(i['snippet']['topLevelComment']['snippet']['publishedAt'])
                    )
                    comments_info.append(data)
                nextPageToken = response.get('nextPageToken')

    except HttpError as e:
        error_details = str(e)
        if 'commentsDisabled' in error_details:
            st.warning(f"Comments are disabled for video ID: {video_id}. Skipping this video.")
        elif 'quotaExceeded' in error_details:
            st.error("API Quota exceeded. Please try again later.")
            
        else:
                st.error(f"An error occurred: {e}")

    return comments_info

#setting up the option "Data collection and upload" in streamlit page
if selected == "Data collection and upload":
    st.subheader(':blue[Data collection and upload]')
    st.markdown('''
                - Provide channel ID in the input field.
                - Clicking the 'View Details' button will display an overview of youtube channel.
                - Clicking 'Upload to MYSQL database' will store the extracted channel information,
                Playlists,Videos,Comments in MYSQL Database''')
    st.markdown('''
                :red[note:] ***you can get the channel ID :***
                open youtube - go to any channel - go to about - share cahnnel - copy the channel ID''')
    
    channel_ID = st.text_input("**Enter the channel ID in the below box :**")
    
    if st.button("View details"): # Shows the channel information from Youtube
        with st.spinner('Extraction in progress...'):
            try:
                extracted_details = channel_information(channel_id=channel_ID)
                st.write('**:blue[Channel Thumbnail]** :')
                st.image(extracted_details.get('channel_Thumbnail'))
                st.write('**:blue[Channel Name]** :', extracted_details['channel_name'])
                st.write('**:blue[Description]** :', extracted_details['channel_Description'])
                st.write('**:blue[Total_Videos]** :', extracted_details['channel_video_count'])
                st.write('**:blue[Subscriber Count]** :', extracted_details['channel_subscribers'])
                st.write('**:blue[Total Views]** :', extracted_details['channel_views'])
            except HttpError as e:
                if e.resp.status == 403 and e.error_details[0]["reason"] == 'quotaExceeded':
                    st.error(" API Quota exceeded. Please try again later.")
            except:
                st.error("Please ensure to give valid channel ID")
   
# upload the youtube retrieved data into MYSQL database
    if st.button("Upload to MYSQL database"): 

        with st.spinner('Upload in progress...'):
            try:
                #to create a channel table in sql database
                mycursor.execute('''create table if not exists channel( channel_name VARCHAR(100) ,
                                channel_id VARCHAR(50) PRIMARY KEY,channel_Description VARCHAR(1000),channel_Thumbnail VARCHAR(100),
                                channel_playlist_id VARCHAR(50),channel_subscribers BIGINT,channel_video_count BIGINT,
                                channel_views BIGINT,channel_publishedat DATETIME)''')
                
                #to create a playlist table in sql database
                mycursor.execute('''create table if not exists playlist(playlist_id VARCHAR(50) PRIMARY KEY,playlist_name VARCHAR(100),
                                publishedat DATETIME,channel_id VARCHAR(50),channel_name VARCHAR(100),videoscount BIGINT)''')
                
                #to create videos table in sql database
                mycursor.execute('''create table if not exists videos(channel_id VARCHAR(50),video_id VARCHAR(50)primary key,
                                video_name VARCHAR(100),video_Description VARCHAR(500),Thumbnail VARCHAR(100),Tags VARCHAR(250),
                                publishedAt DATETIME,Duration VARCHAR(10),View_Count BIGINT,Like_Count BIGINT,Favorite_Count BIGINT,
                                Comment_Count BIGINT,Caption_Status VARCHAR(10),
                                FOREIGN KEY (channel_id) REFERENCES channel(channel_id))''')
                
                #to create comments table in sql database
                mycursor.execute('''create table if not exists comments(video_id VARCHAR(50),comment_id VARCHAR(50),comment_text TEXT,
                                comment_author VARCHAR(50),comment_publishedat DATETIME,FOREIGN KEY (video_id) REFERENCES videos(video_id))''')
                
                
                #Transform corresponding data's into pandas dataframe
                df_channel=pd.DataFrame(channel_information(channel_id=channel_ID),index=[0])
                df_playlist=pd.DataFrame(playlist_information(channel_id=channel_ID))
                df_videos=pd.DataFrame(video_information(video_IDS= get_video_ids(channel_id=channel_ID)))
                df_comments=pd.DataFrame(comments_information(video_IDS=get_video_ids(channel_id=channel_ID)))
                
                #load the dataframe into tabel in SQL Database
                df_channel.to_sql('channel',engine,if_exists='append',index=False)
                df_playlist.to_sql('playlist',engine,if_exists='append',index=False)
                df_videos['Tags'] = df_videos['Tags'].apply(lambda x: ', '.join(x) if isinstance(x, list) else '')
                df_videos.to_sql('videos',engine,if_exists='append',index=False)
                df_comments.to_sql('comments',engine,if_exists='append',index=False)
                mydb.commit()
                st.success('Uploaded successfully')
            except :
                st.error('channel already uploaded or exist in MYSQL Database')


# Function to retrieve channel names from SQL DB
def fetch_channel_names(): 
    mycursor.execute("SELECT channel_name FROM channel")
    channel_names = [row[0] for row in mycursor.fetchall()]
    st.write("Channel names retrieved:", channel_names)
    return channel_names


# Function to Fetch all the related data from SQL DB
def load_channel_data(channel_name):
    # Fetch channel data
    mycursor.execute("SELECT * FROM channel WHERE channel_name = %s", (channel_name,))
    channel_df = pd.DataFrame(mycursor.fetchall(), columns=[i[0] for i in mycursor.description])

    # Fetch playlists data
    mycursor.execute("SELECT * FROM playlist WHERE channel_id = %s", (channel_df['channel_id'].iloc[0],))
    playlists_df = pd.DataFrame(mycursor.fetchall(), columns=[i[0] for i in mycursor.description])

    # Fetch videos data
    mycursor.execute("SELECT * FROM videos WHERE channel_id = %s", (channel_df['channel_id'].iloc[0],))
    videos_df = pd.DataFrame(mycursor.fetchall(), columns=[i[0] for i in mycursor.description])

    # Fetch comments data
    mycursor.execute("SELECT * FROM comments WHERE video_id IN (SELECT video_id FROM videos WHERE channel_id = %s)",
                    (channel_df['channel_id'].iloc[0],))
    comments_df = pd.DataFrame(mycursor.fetchall(), columns=[i[0] for i in mycursor.description])

    return channel_df,playlists_df,videos_df,comments_df

# Setting up the option "MYSQL Database" in streamlit page 
if selected =="MYSQL Database":
    st.subheader(':blue[MYSQL Database]')
    st.markdown('''__You can view the channel details along with the playlist,videos,comments in table format 
                    which is stored in MYSQL database__''')
    try:
        channel_names = fetch_channel_names()
        if not channel_names:
            st.warning("No channels found in the database")
        else:
            selected_channel = st.selectbox(':red[Select Channel]', channel_names) 
    
            if selected_channel:
                channel_info,playlist_info,videos_info,comments_info = load_channel_data(selected_channel)

            st.subheader(':blue[Channel Table]')
            st.write(channel_info)
            st.subheader(':blue[Playlists Table]')
            st.write(playlist_info)
            st.subheader(':blue[Videos Table]')
            st.write(videos_info)
            st.subheader(':blue[Comments Table]')
            st.write(comments_info)
            

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Function to excute Query of 1st Question 
def sql_question_1():
    mycursor.execute('''SELECT channel.channel_name,videos.video_name
                        FROM videos 
                        JOIN channel ON channel.Channel_id = videos.Channel_id
                        ORDER BY channel_name''')
    out=mycursor.fetchall()
    Q1= pd.DataFrame(out, columns=['Channel Name','Videos Name']).reset_index(drop=True)
    Q1.index +=1
    st.dataframe(Q1)

    
# Function to excute Query of 2nd Question 
def sql_question_2():
    mycursor.execute('''SELECT DISTINCT channel_name,COUNT(videos.video_id) as Total_Videos 
                        FROM channel 
                        JOIN videos on Channel.channel_id = videos.channel_id
                        GROUP BY channel_name 
                        ORDER BY Total_videos DESC''')
    out=mycursor.fetchall()
    Q2= pd.DataFrame(out, columns=['Channel Name','Total Videos']).reset_index(drop=True)
    Q2.index +=1
    st.dataframe(Q2)
    st.write("### :green[Number of videos in each channel :]")
    #st.bar_chart(Q2,x= mycursor.column_names[0],y= mycursor.column_names[1])
    fig = px.bar(Q2,
                     x='Channel Name',
                     y='Total Videos',
                     orientation='v',
                     color='Channel Name'
                    )
    st.plotly_chart(fig,use_container_width=True)


# Function to excute Query of 3rd Question 
def sql_question_3():
    mycursor.execute('''
        SELECT channel.Channel_name, videos.Video_name, videos.View_Count as Total_Views
        FROM videos
        JOIN channel ON channel.Channel_id = videos.Channel_id
        WHERE videos.View_Count IS NOT NULL  #Ensure only valid view counts are considered
        ORDER BY videos.View_Count DESC  #Correct ordering by the actual column name
        LIMIT 10;
    ''')
    out = mycursor.fetchall()
    Q3 = pd.DataFrame(out, columns=['Channel Name', 'Videos Name', 'Total Views']).reset_index(drop=True)
    Q3.index += 1
    st.dataframe(Q3)
    st.write("### :green[Top 10 most viewed videos :]")
    fig = px.bar(Q3,
                     x='Total Views',
                     y='Videos Name',
                     orientation='h',
                     color='Channel Name'
                    )
    st.plotly_chart(fig,use_container_width=True)
   
    
    
# Function to excute Query of  4th Question 
def sql_question_4():
    mycursor.execute('''SELECT videos.video_name,videos.comment_count as Total_Comments
                    FROM videos
                    ORDER BY videos.comment_count DESC''')
    out=mycursor.fetchall()
    Q4= pd.DataFrame(out, columns=['Videos Name','Total Comments']).reset_index(drop=True)
    Q4.index +=1
    st.dataframe(Q4)

# Function to excute Query of 5th Question 
def sql_question_5():
    mycursor.execute('''
        SELECT channel.channel_name, videos.video_name, videos.like_count AS Likes
        FROM videos
        JOIN channel ON videos.channel_id = channel.channel_id
        ORDER BY videos.like_count DESC
        LIMIT 10;''')
    out = mycursor.fetchall()
    Q5 = pd.DataFrame(out, columns=['Channel Name', 'Video Name', 'Likes']).reset_index(drop=True)
    Q5.index += 1
    st.dataframe(Q5)

    st.write("### :green[The top liked videos :]")
    fig = px.bar(Q5,
                     x='Video Name',
                     y='Likes',
                     orientation='v',
                     color='Channel Name'
                    )
    st.plotly_chart(fig,use_container_width=True)
    
# Function to execute query for total likes and dislikes
def sql_question_6():
    mycursor.execute('''SELECT video_name, 
                    SUM(like_count) AS total_likes, 
                    SUM(dislike_count) AS total_dislikes
                    FROM videos
                    GROUP BY video_name
                    ORDER BY total_likes + total_dislikes DESC;
                ''')
    out = mycursor.fetchall()
    Q6 = pd.DataFrame(out, columns=['Video Name', 'Total Likes', 'Total Dislikes']).reset_index(drop=True)
    Q6.index += 1
    st.dataframe(Q6)

# Function to excute Query of 7th Question 
def sql_question_7():
    mycursor.execute('''SELECT channel.channel_name, SUM(videos.View_Count) as Total_Views 
                        FROM videos 
                        JOIN channel ON channel.Channel_id = videos.Channel_id
                        GROUP BY channel.channel_name
                        ORDER BY Total_Views DESC''')
    out = mycursor.fetchall()
    Q7 = pd.DataFrame(out, columns=['Channel Name', 'Total Views']).reset_index(drop=True)
    Q7.index += 1
    st.dataframe(Q7)
    st.write("### :green[The total number of views for each channel :]")
    fig = px.bar(Q7,
                     x='Channel Name',
                     y='Total Views',
                     orientation='v',
                     color='Channel Name'
                    )
    st.plotly_chart(fig,use_container_width=True)
    
# Function to excute Query of 8th Question 
def sql_question_8():
    mycursor.execute('''SELECT DISTINCT channel.channel_name
                    FROM channel
                    JOIN videos ON  videos.channel_id=channel.channel_id
                    WHERE YEAR(videos.PublishedAt) = 2022 ''')
    out=mycursor.fetchall()
    Q8= pd.DataFrame(out, columns=['Channel Name']).reset_index(drop=True)
    Q8.index +=1
    st.dataframe(Q8)

# Function to excute Query of 9th  Question 
def sql_question_9():
    mycursor.execute('''SELECT channel.channel_name,
                    TIME_FORMAT(SEC_TO_TIME(AVG(TIME_TO_SEC(TIME(videos.Duration)))), "%H:%i:%s") AS Duration
                    FROM videos
                    JOIN channel ON videos.channel_id=channel.channel_id
                    GROUP BY channel.channel_name
                    ORDER BY AVG(TIME_TO_SEC(videos.Duration))   ''')
    out=mycursor.fetchall()
    Q9= pd.DataFrame(out, columns=['Chanel Name','Duration']).reset_index(drop=True)
    Q9.index +=1
    st.dataframe(Q9)
    st.write("### :green[The Average Duration of all videos in each channel :]")
    fig = px.bar(Q9,
                     x='Chanel Name',
                     y='Duration',
                     orientation='v',
                     color='Chanel Name'
                    )
    st.plotly_chart(fig,use_container_width=True)

# Function to excute Query of 10th Question 
def sql_question_10():
    mycursor.execute('''SELECT channel.channel_name, videos.video_name, videos.comment_count
                    FROM videos
                    JOIN channel ON videos.channel_id = channel.channel_id
                    ORDER BY videos.comment_count DESC
                    LIMIT 10; ''')

    out = mycursor.fetchall()
    Q10 = pd.DataFrame(out, columns=['Channel Name', 'Video Name', 'Comments']).reset_index(drop=True)
    Q10.index += 1
    st.dataframe(Q10)
    st.write("### :green[Top 10 Videos with Most Comments:]")
    fig = px.bar(Q10,
                 x='Video Name',
                 y='Comments',
                 orientation='v',
                 color='Channel Name',
                 title='Top 10 Videos with Most Comments'
                )
    st.plotly_chart(fig, use_container_width=True)


    
    
# Setting up the option "Analysis using SQL" in streamlit page 
if selected == 'Analysis using SQL':
    st.subheader(':blue[Analysis using SQL]')
    st.markdown('''__Select any question to run the SQL query and analyze the data stored in the MySQL database.__''')
    Questions = ['Select your Question',
        '1.What are the names of all the videos and their corresponding channels?',
        '2.Which channels have the most number of videos, and how many videos do they have?',
        '3.What are the top 10 most viewed videos and their respective channels?',
        '4.How many comments were made on each video, and what are their corresponding video names?',
        '5.Which videos have the highest number of likes, and what are their corresponding channel names?',
        '6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
        '7.What is the total number of views for each channel, and what are their corresponding channel names?',
        '8.What are the names of all the channels that have published videos in the year 2022?',
        '9.What is the average duration of all videos in each channel, and what are their corresponding channel names?',
        '10.Which videos have the highest number of comments, and what are their corresponding channel names?' ]
    
    Selected_Question = st.selectbox(' ',options=Questions)
    if Selected_Question =='1.What are the names of all the videos and their corresponding channels?':
        sql_question_1()
    if Selected_Question =='2.Which channels have the most number of videos, and how many videos do they have?':
        sql_question_2()
    if Selected_Question =='3.What are the top 10 most viewed videos and their respective channels?': 
        sql_question_3()
    if Selected_Question =='4.How many comments were made on each video, and what are their corresponding video names?':
        sql_question_4()  
    if Selected_Question =='5.Which videos have the highest number of likes, and what are their corresponding channel names?':
        sql_question_5() 
    if Selected_Question =='6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
        st.write('**:red[Note]:- Dislike property was made private as of December 13, 2021.**')
        sql_question_6()   
    if Selected_Question =='7.What is the total number of views for each channel, and what are their corresponding channel names?':
        sql_question_7()
    if Selected_Question =='8.What are the names of all the channels that have published videos in the year 2022?':
        sql_question_8()
    if Selected_Question =='9.What is the average duration of all videos in each channel, and what are their corresponding channel names?':
        sql_question_9()
    if Selected_Question =='10.Which videos have the highest number of comments, and what are their corresponding channel names?':
        sql_question_10()



