const mongoose = require('mongoose');
const mongoURI = 'mongodb://127.0.0.1:27017/cloudbook';

const connectToMongo = () => {
	mongoose.connect(mongoURI, () => {});
};

module.exports = connectToMongo;
