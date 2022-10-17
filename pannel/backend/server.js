var express = require("express")
var app = express()
var db = require("../datas/registered_data.json")
var bodyParser = require('body-parser');
var cors = require('cors')

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cors())


app.get("/", function(req, res) {
    res.send(db);
});

app.delete("/delete/:rna", function(req, res) {
    var rna = req.params.rna;
    for (const dept in db) {
        for (const obj_dev of db[dept]) {
            const obj = obj_dev.data;
            if(obj.rna == rna || obj.name == rna) {
                db[dept].splice(db[dept].indexOf(obj_dev), 1);
            }
        }
    }
    res.status(200).send("OK");
});

app.listen(3000, function() {
    console.log("Server running on port 3000");
});