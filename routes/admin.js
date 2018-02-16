let json = require('jsonify');
let request = require('request');

module.exports = function(app){
    app.get('/entity_recon_script', function(req, res){
        res.send('chegou get 1');
    });

    app.post('/', function(req, res){
        //res.send('chegou post 1');
        //console.log(req.body['content']);

        var json_text = {
            'data': [
                {
                    question: req.body['content']
                }
            ]
        };

        var json_object = json.parse(json.stringify(json_text));

        request({
            url: "http://127.0.0.1:4000/entity-recon",
            method: "POST",
            json: true,   // <--Very important!!!
            body: json_object
        }, function (error, response, body){
            //console.log(JSON.stringify(body.data[0]['answer']));
            var entities = [];

            for (i=0;i<body.data.length;i++){
                entities.push(body.data[i]['answer']);
            }
            //res.send([req.body['content'],entities]);
            text_global = req.body['content'];
            ent_global = entities;
            res.render('../views/pages/answer', {text: req.body['content'], ent: entities});
        });
    });
}