
echo "Get torrents information"
node torrents/getTorrentInfo.js

echo "Get imdb codes for the top 100 movie torrents"
python3 imdbcodes/getImdbCodes.py

echo "Get peers information for top 100"
python3 peers/getPeers.py top100complete.json
echo "Get peers information for movies to track"
python3 peers/getPeers.py moviesToTrackTorrents.json