const express = require('express');
const app = express();
const port = 5111;

const mongoDB = require('./db');
mongoDB();

app.use((req, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Orgin, X-Requested-With, Content-Type, Accept');
    next();
});

app.use(express.json());

app.use('/api', require('./routes/User'));
app.use('/api', require('./routes/Food'));
app.use('/api', require('./routes/Order'));

app.listen(port, () => {
    console.clear();
    console.log(`Listening @ http://localhost:${port}`);
});
