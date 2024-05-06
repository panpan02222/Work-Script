const mysql = require('mysql');  
  
const pool  = mysql.createPool({  
  connectionLimit : 10,  
  host            : 'localhost',  
  user            : 'root',  
  password        : 'dyy*1234',  
  database        : 'world'  
});


const express = require('express');  
const app = express();  
const port = 3000; // 你可以选择一个未被占用的端口号  
  
app.get('/', (req, res) => {  
  res.send('Hello World!');  
});  
  
app.listen(port, () => {  
  console.log(`Server is running on port ${port}`);  
});