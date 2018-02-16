let json = require('jsonify');
let request = require('request');

module.exports = function(app){

    app.post('/send', function(req, res){
        console.log(ent_global);
        console.log();
        var data_format = {
            "data" :[
                text_global, 
                {"entities":ent_global}
             ]};
     
        var json_object = json.parse(json.stringify(data_format));
        //console.log(json_object['data'][1].entities);
        console.log(json_object);
    });
}