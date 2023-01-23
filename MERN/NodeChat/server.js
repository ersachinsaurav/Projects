const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const mongoose = require('mongoose');

console.clear();

app.use(express.static(__dirname));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

mongoose.Promise = Promise;

const dbURI = 'mongodb://127.0.0.1:27017/';

const userMessages = mongoose.model('userMessages', {
	name: String,
	msg: String,
});

app.get('/messages', (req, res) => {
	userMessages.find({}, (err, objMessages) => {
		res.send(objMessages);
	});
});

app.get('/messages/:user', (req, res) => {
	const userName = req.params.user;
	userMessages.find({ name: userName }, (err, objMessages) => {
		res.send(objMessages);
	});
});

app.post('/messages', async (req, res) => {
	const userMsg = new userMessages(req.body);

	const savedMsg = await userMsg.save();

	const objCensored = await userMessages.findOneAndDelete({
		msg: { $regex: 'test|demo|sample', $options: 'i' },
	});
	if (objCensored) {
		console.log('Censored word(s) found and message deleted!');
	} else {
		console.log('Saved!');
		io.emit('newMsg', req.body);
	}
	res.sendStatus(200);
});

io.on('connection', (socket) => {
	console.log('A user connected');
});

mongoose.set('strictQuery', false);

mongoose.connect(dbURI, (err) => {
	console.log(err ? err.message : 'Connected to DB!');
});

const server = http.listen(777, () => {
	console.log('App URL: http://127.0.0.1:' + server.address().port);
});
