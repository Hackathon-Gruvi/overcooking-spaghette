import pandas as pd

movie_summary_all = pd.read_csv('movie_summary.csv')
movie_summary = movie_summary_all[['movie_odid', 'display_name', 'genre', 'production_budget', 'international_box_office', 'worldwide_release_date']]

movie_ids = pd.read_csv('movie_identifiers.csv')
movie_ids = movie_ids[movie_ids['domain'] == 'IMDB']
torrent_data = pd.read_json('modifiedTPB.json')

movie_data = pd.merge(movie_summary, movie_ids, on='movie_odid' , how='inner')
crossed_data = pd.merge(movie_data, torrent_data, how='right', left_on='id', right_on='imdb')

crossed_data.sort_values(by='seeds')
print(crossed_data[['seeds', 'title', 'movie_odid']])
# relevant_info.to_csv('movie_sum_filtered.csv', index_label=False, index=False, header=False)