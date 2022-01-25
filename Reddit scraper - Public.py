# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 15:45:11 2021
@author: Solayrro

When executed correctly, this script will allow you to scrape the top 1000 posts of all time in the r/researchchemicals subreddit.
Instead of the top 1000 posts of all time, the 1000 most recent posts can also be scraped by changing the time filter.
In another script called "Reddit Monthly Scraper - Public" I have done this, with the goal to back up all monthly post (since there are less than 1000 per month).

As we are using the official Reddit API, called PRAW, we have some limitations. The main one being that PRAW only allows scraping 1000 posts.
Therefore, this script (sadly) only stores the 1000 highest voted posts.
I intend on developing a method for scraping more than 1000 posts, possibly all. But in the mean time, a montly scrape of 1000 posts will be the best we can do.
"""
# This section imports and activates the Reddit API. For this it is required to make a client ID and obtain the required login information.
# I recommend reading the following article for clear instructions on this process:
# https://towardsdatascience.com/scraping-reddit-data-1c0af3040768

import praw

my_secret = 
my_client_id = 
my_user_agent = 



reddit = praw.Reddit(client_id= my_client_id, client_secret= my_secret, user_agent= my_user_agent)

#%% This section is just to check whether the login was succesfull

rc = reddit.subreddit('researchchemicals')
top_rc = rc.top(time_filter = 'all', limit=3)
for post in top_rc:
    print(post.selftext)
    
#%% This section scrapes the top 1000 posts of all time, together with the number of comments, post title & text, date of creation, url, score
# after scraping, the data is converted into a pandas dataframe

import pandas as pd
top_posts = []
rc_subreddit = reddit.subreddit('researchchemicals')

for post in rc_subreddit.top(time_filter = 'all', limit=1000):
    top_posts.append([post.title, post.score, post.url, post.num_comments, post.selftext, post.created])

top_posts = pd.DataFrame(top_posts,columns=['title', 'score', 'url', 'num_comments', 'text', 'created'])
#print(top_posts)

#%% This section adds a column for year, month, and day of creation of the post for further archiving and indexing.

import datetime

top_posts["created"] = pd.to_datetime(top_posts["created"], unit='s')
top_posts["year"] = top_posts["created"].dt.year
top_posts["month"] = top_posts["created"].dt.month
top_posts["day"] = top_posts["created"].dt.day

#%% This section converts the pandas dataframe into an Excel file, and stores it in the given file location


path = # here you post the correct string of the path where you want the file to be stored. For example: 'C:/Users/Solayrro/Documents/
top_posts.to_csv(path+'top_rc_1000.csv')
