const TorrentSearchApi = require('torrent-search-api');
const parseTorrent = require('parse-torrent');
var fs = require('fs');

// Enable public providers
TorrentSearchApi.enablePublicProviders();

const getParseTorrentInfo = ((magnetLink) => {
    const torrentDetails = parseTorrent(magnetLink);
        
    var torrentInfo = {
        infohash: torrentDetails.infoHash,
        name: torrentDetails.name,
        trackers: torrentDetails.tr
    };

    return torrentInfo
})

const getInfohashesForTop100 = (() => {
    var top100 = JSON.parse(fs.readFileSync('top100.json'));

    for(let movie of top100){
        const magnetLink = movie.magnet
        const torrentDetails = getParseTorrentInfo(magnetLink);

        movie.infohash = torrentDetails.infohash
        movie.name = torrentDetails.name
        movie.trackers = torrentDetails.trackers
    }
    
    fs.writeFile('top100wInfohash.json', JSON.stringify(top100), 'utf8', function (err, data) {
        if (!data) return;

        fs.writeFile('writeMe.txt', data, function (err, result) {
            if (err) console.log('error', err);
        });
    });
})

const getTorrentsForMoviesToTrack = (async () => {
    var moviesToTrack = JSON.parse(fs.readFileSync('moviesToTrack.json'));
    const result = []

    for(let movie of moviesToTrack){
        const torrents = await getTorrentsByTitle(movie.title);
        
        if(torrents == null)
            continue

        for(let torrent of torrents){
            movie.infohash = torrent.infohash
            movie.name = torrent.name
            movie.trackers = torrent.trackers
            movie.peers = torrent.peers,
            movie.seeds = torrent.seeds,
            movie.provider = torrent.provider

            result.push(movie)
        }
    }
    
    fs.writeFile('moviesToTrackTorrents.json', JSON.stringify(result), 'utf8', function (err, data) {
        if (!data) return;

        fs.writeFile('writeMe.txt', data, function (err, result) {
            if (err) console.log('error', err);
        });
    });
})

const getTorrentsByTitle = (async (title) => {
    const numberOfTorrentsByMovie = 1;
    return TorrentSearchApi.search(title, 'Movies', numberOfTorrentsByMovie)
        .then(async (torrents) => {
            if(torrents.length == 0){
                return null
            }

            let objs = [];

            for (let torrent of torrents) {
                let magnetLink = await TorrentSearchApi.getMagnet(torrent);
                let torrentDetails = getParseTorrentInfo(magnetLink);
                
                let torrentInfo = {
                    infohash: torrentDetails.infohash,
                    name: torrentDetails.name,
                    trackers: torrentDetails.trackers,
                    peers: torrent.peers,
                    seeds: torrent.seeds,
                    provider: torrent.provider
                };

                objs.push(torrentInfo);
            }

            return objs;
        })
        .catch((error) => {
            console.log(error)
        })
})


getInfohashesForTop100();
getTorrentsForMoviesToTrack();