import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

plt.close("all")

# Movie summary info
movie_summary_all = pd.read_csv('movie_summary.csv')
movie_summary_all['total_box_office'] = movie_summary_all['international_box_office'] + movie_summary_all['domestic_box_office']
movie_summary = movie_summary_all[['movie_odid', 'display_name', 'genre', 'total_box_office', 'production_budget', 'worldwide_release_date']]
# Movie identifiers (only IMDB)
movie_ids = pd.read_csv('movie_identifiers.csv')
movie_ids = movie_ids[movie_ids['domain'] == 'IMDB']
# Torrents
torrent_data_all = pd.read_json('modifiedTPB.json')
torrent_data = torrent_data_all.drop_duplicates(subset='imdb')
# Fix torrent dates
for ind, torrent in torrent_data.iterrows():
    torrent_data.at[ind, 'time'] = datetime.strptime(torrent['time'], '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d')
# Aggregate seeders for same movies
for ind1, torrent1 in torrent_data_all.iterrows():
    for ind2, torrent2 in torrent_data.iterrows():
        if ind1 != ind2 and torrent1['imdb'] == torrent2['imdb']:
            torrent_data.at[ind2, 'seeds'] = torrent_data.at[ind2, 'seeds'] + torrent1['seeds']
# Tickets price (2014)
tickets = pd.read_csv('international_prices.csv')
mean = tickets['Amount'].mean()
mean_ticket_price = round(mean, 2)
# Get losts from piracy
torrent_data['lost_revenue'] = torrent_data['seeds'] * mean_ticket_price

movie_data = pd.merge(movie_summary, movie_ids, on='movie_odid' , how='inner')
crossed_data = pd.merge(movie_data, torrent_data, how='inner', left_on='id', right_on='imdb').sort_values('seeds', ascending=False)
crossed_data['ratio'] = crossed_data['lost_revenue'] / crossed_data['total_box_office']

temp_crossed = crossed_data[['time', 'worldwide_release_date']]
for i, row in temp_crossed.iterrows():
    hacked = datetime.strptime(row['time'], '%Y-%m-%d')
    release = datetime.strptime(row['worldwide_release_date'], '%Y-%m-%d')
    if release.year == hacked.year:
        dif = (hacked - release).days
        crossed_data.at[i, 'time_to_hack'] = dif
    else:
        crossed_data.at[i, 'time_to_hack'] = None

crossed_data_prod_seeds = crossed_data[crossed_data['production_budget'] != 0]
crossed_data_prod_seeds.plot.scatter(x='production_budget', y='seeds')
plt.savefig("prod_seeds.png")

crossed_data_prod_seeds.plot.scatter(x='title', y='lost_revenue')
print('Mean lost revenue')
print(crossed_data_prod_seeds.lost_revenue.mean())
plt.savefig("lost_revs.png")

crossed_data.plot.scatter(x='genre', y='seeds')
plt.savefig("genre_seeds.png")

crossed_data_time = (crossed_data[['title', 'worldwide_release_date', 'time', 'time_to_hack']]).dropna()
print('Mean time to hack')
print(crossed_data_time.time_to_hack.mean())
crossed_data_time.plot.scatter(x='title', y='time_to_hack')
plt.savefig("hack_time.png")

