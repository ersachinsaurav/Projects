require('dotenv').config();
const http = require('http');
const fs = require('fs');
const requests = require('requests');
const geoip = require('geoip-lite');

const replaceVal = (orgFile, apiVal) => {
	let tempFile = orgFile.replace('{%currentTemp%}', apiVal.main.temp);
	tempFile = tempFile.replace('{%minTemp%}', apiVal.main.temp_min);
	tempFile = tempFile.replace('{%maxTemp%}', apiVal.main.temp_max);
	tempFile = tempFile.replace('{%location%}', apiVal.name);
	tempFile = tempFile.replace('{%country%}', apiVal.sys.country);
	return tempFile;
};

var objData = null;

const server = http.createServer((request, response) => {
	const homeFile = fs.readFileSync('./index.html', 'utf-8');

	const requestIp = request.socket.remoteAddress;
	let city = 'Muzaffarpur';

	if ('127.0.0.1' !== requestIp) {
		let geo = geoip.lookup(requestIp);
		city = geo.city;
	}

	if ('/weatherapp' == request.url) {
		requests(
			`https://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&appid=${process.env.APIKEY}`
		)
			.on('data', (chunkData) => {
				objData = JSON.parse(chunkData);
				const realTimeData = [objData]
					.map((currentValue) => replaceVal(homeFile, currentValue))
					.join('');
				response.writeHead(200, { 'Content-Type': 'text/html' });
				response.write(realTimeData);
			})
			.on('end', (err) => {
				console.log(err ? err : "I'm good!");
				response.end();
			});
	} else if ('/style.css' == request.url) {
		const file = fs.readFileSync('./style.css', 'UTF-8');
		response.writeHead(200, { 'Content-Type': 'text/css' });
		response.write(file);
		response.end();
	} else if ('/script.js' == request.url) {
		const scriptFile = fs.readFileSync('./script.js', 'UTF-8');
		const realTimeData = [objData]
			.map((currentValue) =>
				scriptFile.replace('{%weatherType%}', currentValue.weather[0].main)
			)
			.join('');
		response.writeHead(200, { 'Content-Type': 'text/javascript' });
		response.write(realTimeData);
		response.end();
	} else {
		response.writeHead(404), { 'Content-type': 'text/html' };
		response.end('<h1>Not Found!</h1>');
	}
});

server.listen(process.env.PORT, process.env.SERVER_IP, () => {
	console.log(
		`Server running @ http://${process.env.SERVER_IP}:${process.env.PORT}/weatherapp`
	);
});
