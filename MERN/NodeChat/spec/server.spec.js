const request = require('request');

describe('get messages', () => {
	it('should return 200 OK', (done) => {
		request.get('http://127.0.0.1:777/messages', (err, res) => {
			expect(res.statusCode).toEqual(200);
			done();
		});
	});

	it('should return a list', (done) => {
		request.get('http://127.0.0.1:777/messages', (err, res) => {
			expect(JSON.parse(res.body).length).toBeGreaterThan(0);
			done();
		});
	});
});

describe('get messages from user', () => {
	it('should return 200 OK', (done) => {
		request.get('http://127.0.0.1:777/messages/Saurav', (err, res) => {
			expect(res.statusCode).toEqual(200);
			done();
		});
	});

	it('UserName should be Sachin', (done) => {
		request.get('http://127.0.0.1:777/messages/Sachin', (err, res) => {
			console.log(res.body);
			expect(JSON.parse(res.body)[0].name).toEqual('Sachin');
			done();
		});
	});
});
