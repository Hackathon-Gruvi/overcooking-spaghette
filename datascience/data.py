import pandas as pd

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

# print(crossed_data[['title', 'genre', 'production_budget', 'total_box_office', 'lost_revenue', 'seeds', 'imdb']])

print(crossed_data.genre.mode())