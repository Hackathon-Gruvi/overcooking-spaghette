
echo "Get torrents information"
node torrents/getTorrentInfo.js

echo "Get imdb codes for the top 100 movie torrents"
python3 imdbcodes/getImdbCodes.py


echo "Get peers information for movies to track"
python3 peers/getPeers.py moviesToTrackTorrents.json

# Note that for a 100 torrents this operation takes a long time.
# To just test that it's working you can stop the process mid-run, it won't have have every possible result, but it gives an idea of how it works.
echo "Get peers information for top 100"
python3 peers/getPeers.py top100complete.json