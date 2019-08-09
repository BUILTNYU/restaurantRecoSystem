const express = require('express');
const app = express();
var mysql = require('mysql');

var con = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "root",
  port:8889,
  database:'UrbanConnector'
});

app.set('view engine', 'hbs');
const path = require('path');
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.urlencoded({ extended: false }));

con.connect(function(err) {
  if (err) throw err;
  console.log("Connected!");


  app.get("/",(req,res)=>{
    con.query("SELECT * FROM UserRating",function (error, results, fields){
      res.render("history",{records:results})
    })
    
  })

  app.listen(3000);

});


