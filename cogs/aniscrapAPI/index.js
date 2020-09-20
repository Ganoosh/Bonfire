const express = require('express')
var Anime = require('anime-scraper').Anime
const cheerio = require('cheerio');
const rp = require('request-promise');

const app = express()

app.get('/', function (req, res) {
  res.send("404 Not Found!")
})

app.get('/search', function(req, res) {

    let episode = req.query.episode
    let dub = req.query.dub
    let name;

    if(req.query.type === "dub") { name = req.query.query + '-dub'; } else { name = req.query.query }

    Anime.fromName(name).then(function (anime) {
        try {
            res.redirect(`/extract?url=${anime.episodes[episode].url}`)
        } catch {
            res.json({ 'error': 'invalid episode' })
        }
    })

    

})

app.get('/extract', function(req, res) {
    let url = req.query.url;
    let anime_source_url;
    
    async function callRp() {
        await rp({
            method: 'GET',
            url: url
        }, (err, res, body) => {

            if (err) return console.error(err);

            let $ = cheerio.load(body);

            let iframe_video = $('.active');

            data_url = $(iframe_video).attr('data-video');
            str_index = data_url.indexOf("id");
            
            var anime_id = data_url[str_index + 3] + data_url[str_index + 4] + data_url[str_index + 5] + data_url[str_index + 6] + data_url[str_index + 7] + data_url[str_index + 8] + data_url[str_index + 9]
            
            anime_source_url = `https://gogo-stream.com/download?id=${anime_id}`
        });
    }

    callRp().then(() => {
        
        res.redirect(`/gogostream?url=${anime_source_url}`)
        // res.json({'url':anime_source_url})
    })
})


app.get('/gogostream', function(req, res) {
    let url = req.query.url;
    let anime_source_url;
    let data_url;
    let api_url;
    
    async function callRp() {
        await rp({
            method: 'GET',
            url: url
        }, (err, res, body) => {

            if (err) return console.error(err);

            let $ = cheerio.load(body);

            let iframe_video = $('.dowload a');
            data_url = $(iframe_video).attr('href');            
        });
    }

    callRp().then(() => {
        res.redirect(`/mp4?url=${data_url}`)
        // res.json({'url':data_url})
    })
})

app.get('/mp4', function(req, res) {
    var request = require('request')

    var uri = req.query.url
    request(
      {
        uri: uri,
        followRedirect: false,
      },
      function(err, httpResponse) {
        if (err) {
          return console.error(err)
        }
        res.json({'url': httpResponse.headers.location || uri })
      }
    )
})


app.get('/create', function(req, res) {
	var options = {
	'method': 'POST',
	'url': 'https://w2g.tv/rooms/create.json',
	'headers': {
		'Content-Type': 'application/json',
	},
	body: JSON.stringify({"w2g_api_key":"my_api_key","share":req.query.url})

	};
	rp(options, function (error, response) {
	if (error) throw new Error(error);
	res.json(JSON.parse(response.body));
	});

})

app.listen(3000)