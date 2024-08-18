# Youtube-data-Harvesting-and-warehousing
YouTube Data Harvesting & Warehousing using SQL
Domain : Social Media
Overview :
Build a simple dashboard or UI using Streamlit and retrieve YouTube channel data with the help of the YouTube API. Stored the data in an SQL database(warehousing), enabling querying of the data using SQL.Visualize the data within the Streamlit app to uncover insights, trends with the YouTube channel data

Video:[Uploading streamlit.webm...]()

Skill Take Away :
Python scripting,Data Collection,API integration,Data Management using SQL,Streamlit

About :
Hello! I'm Vinoothna, a Mechanical Engineering graduate with a deep passion for AI, ML, and robotics. I'm currently embarking on an exciting journey into data science, with my first project titled YouTube Data Harvesting and Warehousing Using SQL. In this project, I delved into the vast expanse of YouTube data to extract meaningful insights. This experience ignited my enthusiasm for data-driven decision-making and significantly enhanced my skills in data extraction techniques and database management.

Problem Statement:
The problem statement is to create a Streamlit application that allows users to access and analyze data from multiple YouTube channels.
The application should have the following features:
  Ability to input a YouTube channel ID and retrieve all the relevant data (Channel name, subscribers, total video count, playlist ID, video ID, likes, dislikes, comments of each video) using Google API.
 Ability to collect data for up to 10 different YouTube channels and store them in the data lake by clicking a button.
 Option to store the data in a MYSQL or PostgreSQL.
Ability to search and retrieve data from the SQL database using different search options, including joining tables to get channel details.

Approach:
Set up a Streamlit app: Streamlit is a great choice for building data visualization and analysis tools quickly and easily. You can use Streamlit to create a simple UI where users can enter a YouTube channel ID, view the channel details, and select channels to migrate to the data warehouse.
Connect to the YouTube API: You'll need to use the YouTube API to retrieve channel and video data. You can use the Google API client library for Python to make requests to the API.
Store and Clean data : Once you retrieve the data from the YouTube API, store it in a suitable format for temporary storage before migrating to the data warehouse. You can use pandas DataFrames or other in-memory data structures.
Migrate data to a SQL data warehouse: After you've collected data for multiple channels, you can migrate it to a SQL data warehouse. You can use a SQL database such as MySQL or PostgreSQL for this.
Query the SQL data warehouse: You can use SQL queries to join the tables in the SQL data warehouse and retrieve data for specific channels based on user input. You can use a Python SQL library such as SQLAlchemy to interact with the SQL database.
Display data in the Streamlit app: Finally, you can display the retrieved data in the Streamlit app. You can use Streamlit's data visualization features to create charts and graphs to help users analyze the data.
Overall, this approach involves building a simple UI with Streamlit, retrieving data from the YouTube API, storing the data SQL as a warehouse, querying the data warehouse with SQL, and displaying the data in the Streamlit app.

SQL Query Output is displayed as table in Streamlit Application:
1.What are the names of all the videos and their corresponding channels?


2.Which channels have the most number of videos, and how many videos do
 they have?

 
3.What are the top 10 most viewed videos and their respective channels?


4.How many comments were made on each video, and what are their
 corresponding video names?

 
5.Which videos have the highest number of likes, and what are their 
corresponding channel names?


6.What is the total number of likes and dislikes for each video, and what are 
their corresponding video names?


7.What is the total number of views for each channel, and what are their 
corresponding channel names?


8.What are the names of all the channels that have published videos in the year
 2022?

 
9.What is the average duration of all videos in each channel, and what are their 
corresponding channel names?


10.Which videos have the highest number of comments, and what are their 
corresponding channel names?
