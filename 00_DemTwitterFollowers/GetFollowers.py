from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime

# Official twitter accounts for major Dem candidates ... sorry Mayor Bloomberg
dems = ['@BernieSanders', '@ewarren', '@TomSteyer', '@amyklobuchar', '@AndrewYang', '@PeteButtigieg']
followers = []

# Scrape followers, add to empty list
for candidate in dems:

    temp = requests.get('https://twitter.com/' + candidate)
    soup = BeautifulSoup(temp.text, 'lxml')

    try:
        follow_box = soup.find('li',{'class':'ProfileNav-item ProfileNav-item--followers'})
        total = follow_box.find('a').find('span',{'class':'ProfileNav-value'})
        clean_total = total.get('data-count')
        followers.append(clean_total)

    except:
        print("Whoops! Account " + candidate + " not found...")

# Column headers for data frame
columns = ['Date', 'SANDERS', 'WARREN', 'STEYER', 'KLOBUCHAR', 'YANG', 'BUTTIGIEG']

# Grab today's date + add it to list of headers
today = (datetime.datetime.now()).strftime("%x")
followers.insert(0, today)

# Make dictionary out of column headers / follower data
dem_dict = {}

for i in range(len(columns)):

    dem_dict[columns[i]] = followers[i]

demData = pd.DataFrame(dem_dict, index = [0])

# Save dataframe to CSV file with today's date
filename = (datetime.datetime.now()).strftime('%m%d') + '.csv'
demData.to_csv(filename)
