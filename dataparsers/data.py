import pandas as pd

opus_data = pd.read_csv('movie_summary.csv')

relevant_info = opus_data[['movie_odid', 'display_name', 'production_budget', 'international_box_office', 'worldwide_release_date']]

print(relevant_info)

relevant_info.to_csv('movie_sum_filtered.csv', index_label=False, index=False, header=False)