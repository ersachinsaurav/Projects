const Pool = require('pg').Pool;

const pool = new Pool({
	user: 'postgres',
	password: 'postgres',
	host: '127.0.0.1',
	port: 7432,
	database: 'pern',
});

module.exports = pool;
