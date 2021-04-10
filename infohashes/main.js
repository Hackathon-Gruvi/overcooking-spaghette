const TorrentSearchApi = require('torrent-search-api');
const parseTorrent = require('parse-torrent');
var fs = require('fs');

// Get providers
const providers = TorrentSearchApi.getProviders();
 
// Get active providers
const activeProviders = TorrentSearchApi.getActiveProviders();
 
// Enable public providers
TorrentSearchApi.enablePublicProviders();

const getTorrents = (async ()=>{
    return TorrentSearchApi.search('Endgame', 'Movies', 20)
        .then((torrents) => {
            console.log(torrents[0])
            return torrents[0]
        })
        .then(async (torrent) => {
            const magnetLink = torrent.magnet;
            const torrentDetails = parseTorrent(magnetLink);

            var torrents = {
                infohash: torrentDetails.infoHash,
                name: torrentDetails.name,
                trackers: torrentDetails.tr
            };

            // obj.table.push({id: 1, square:2});

            var json = JSON.stringify(torrents);

            fs.writeFile('torrents.json', json, 'utf8', function (err, data) {
                fs.writeFile('writeMe.txt', data, function(err, result) {
                   if(err) console.log('error', err);
                });
            });
        })
        .catch((error)=>{
            console.log(error)
        })
})

getTorrents();