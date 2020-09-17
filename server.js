var express = require('express');
var mysql = require('mysql');
var fs = require('fs');

var connection = mysql.createConnection({
	host : 'localhost',
	user : 'pi',
	password : '',
	database : 'mysql',
	port: '3306',
	insecurreAuth : true
})
connection.connect();

var app = express();
app.use(express.static(__dirname + '/public'));

app.get("/", function(request, response){
	connection.query('SELECT * from temp', function(error, results, fields)
	{
		if(error) {
			console.log(error);
		}
		else{
			console.log(results);
			response.send(results);
		}
	})
})

app.listen(8080);
