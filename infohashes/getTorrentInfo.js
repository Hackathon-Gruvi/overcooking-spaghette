const express = require('express')
const cors = require('cors')
const app = express()
const port = 5001
const TorrentSearchApi = require('torrent-search-api');
const parseTorrent = require('parse-torrent');
var fs = require('fs');

// app.get('/', cors(), (req, res) => {
//     const title = req.query.title;
//     console.log("Request received; Title = " + title);
//     getTorrentInfo(title).then((torrentsArray) => {
//         res.send(torrentsArray);
//     })
// })

// app.listen(port, () => {
//     console.log(`Running at http://localhost:${port}`)
// })

// Enable public providers
TorrentSearchApi.enablePublicProviders();

const getTorrentInfo = (async (title) => {
    return TorrentSearchApi.search(title, 'Movies', 20)
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

            return objs;
        })
        .catch((error) => {
            console.log(error)
        })
})