from pyYify import yify

movies_list  = yify.get_top_seeded_torrents()
movies_info = {}

for movie in movies_list:
	movies_info = movie.getinfo()
	trimmed_info = [movie.imdb_code, movie.torrents.peers, movie.torrents.seeders, movie.torrents.quality]
	movies_info[movie.title] = trimmed_info

print(movies_info)
