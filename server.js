// server.js
// load the things we need
var express = require('express');
var request = require('request');
var consign = require('consign');
var bodyParser = require('body-parser');
var app = express();

// set the view engine to ejs
//app.set('view engine', 'html');
app.set('view engine', 'ejs');

// use res.render to load up an ejs view file

// index page 
app.get('/', function(req, res) {
    res.render('pages/index');
});

app.use(bodyParser.urlencoded({extended: true}));
app.use(express.static(__dirname + '/public'));

consign()
    .include('/routes')
    .into(app);


app.listen(8080);
console.log('8080 is the magic port');