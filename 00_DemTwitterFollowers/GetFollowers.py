from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
import os

# Official twitter accounts for major Dem candidates
dems = ['@BernieSanders', '@ewarren', '@TomSteyer', '@amyklobuchar', '@AndrewYang', '@PeteButtigieg', '@JoeBiden', '@MikeBloomberg']
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
columns = ['Date', 'SANDERS', 'WARREN', 'STEYER', 'KLOBUCHAR', 'YANG', 'BUTTIGIEG', 'BIDEN', 'BLOOMBERG']

# Grab today's date + add it to list of headers
today = (datetime.datetime.now()).strftime("%x")
followers.insert(0, today)

# Make dictionary out of column headers / follower data
dem_dict = {}

for i in range(len(columns)):

    dem_dict[columns[i]] = followers[i]

demData = pd.DataFrame(dem_dict, index = [0])

# Current working directory
here = os.getcwd()

# Format filename
filename = (datetime.datetime.now()).strftime('%m%d') + '.csv'

# Save CSV to a new directory
# If directory doesn't exist, make one!
try:
    demData.to_csv(os.path.join(here + "/Candidates on Twitter/" + filename))

except:
    os.mkdir("Candidates on Twitter")
    print("\nCreating new directory ... \n")
    demData.to_csv(os.path.join(here + "/Candidates on Twitter/" + filename))

print("\nTwitter information logged!\n")
