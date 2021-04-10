const TorrentSearchApi = require('torrent-search-api');
const parseTorrent = require('parse-torrent');
var fs = require('fs');

// Get providers
const providers = TorrentSearchApi.getProviders();

// Get active providers
const activeProviders = TorrentSearchApi.getActiveProviders();

// Enable public providers
TorrentSearchApi.enablePublicProviders();

const getTorrents = (async () => {
    return TorrentSearchApi.search('Titanic', 'Movies', 20)
        .then((torrents) => {
            return torrents;
        })
        .then(async (torrentObj) => {
            let objs = [];

            for (const torrent of torrentObj) {
                const magnetLink = await TorrentSearchApi.getMagnet(torrent);

                const peers = torrent.peers;
                const seeds = torrent.seeds;
                const torrentDetails = parseTorrent(magnetLink);

                var torrentObj = {
                    infohash: torrentDetails.infoHash,
                    name: torrentDetails.name,
                    trackers: torrentDetails.tr,
                    peers: peers,
                    seeds: seeds,
                    provider: torrent.provider
                };

                objs.push(torrentObj);
            }

            fs.writeFile('torrents.json', JSON.stringify(objs), 'utf8', function (err, data) {
                if (!data) return;

                fs.writeFile('writeMe.txt', data, function (err, result) {
                    if (err) console.log('error', err);
                });
            });
        })
        .catch((error) => {
            console.log(error)
        })
})

getTorrents();