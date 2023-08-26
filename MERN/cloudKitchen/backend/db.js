const mongoose = require('mongoose');

const mongoUsername = encodeURIComponent('ersachinsaurav');
var mongoPassword = encodeURIComponent('KoiCloud');

const mongoURI = `mongodb+srv://${mongoUsername}:${mongoPassword}@cloudkitchencluster.sx4ihot.mongodb.net/cloudKitchen?retryWrites=true&w=majority`;

const mongoDB = async () => {
    await mongoose.connect(mongoURI, { useNewUrlParser: true }).catch((error) => console.log(error));

    //setting the foodItems, foodCategories for global access
    global.foodItems = await getFoodItems();
    global.foodCategories = await getFoodCategories();
};

const getFoodItems = async () => {
    const foodItems = await mongoose.connection.db.collection('foodItems');

    try {
        return await foodItems.find({}).toArray();
    } catch (error) {
        console.log(error);
    }
};

const getFoodCategories = async () => {
    const foodCategories = await mongoose.connection.db.collection('foodCategories');

    try {
        return await foodCategories.find({}).toArray();
    } catch (error) {
        console.log(error);
    }
};

const renameCollection = async (oldCollectionName, newCollectionName) => {
    await mongoose.connection.db.collection(oldCollectionName).rename(newCollectionName);
    return 'Collection Renamed To: ' + newCollectionName;
};

module.exports = mongoDB;
