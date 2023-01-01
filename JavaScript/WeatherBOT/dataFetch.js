const options = {
  enableHighAccuracy: true,
  timeout: 5000,
  maximumAge: 0,
};

// API keys needs to added here
const appID = "appID";
const apiKey = "apiKey";
var coords = {};

const valGeoData = () => {
  if (
    typeof coords.latitude !== "undefined" &&
    coords.latitude !== "undefined" &&
    typeof coords.longitude !== "undefined" &&
    coords.longitude !== "undefined"
  ) {
    return true;
  }
  return false;
};

const getGeoByIP = async () => {
  showAlert();
  const ipResponse = await fetch("https://api64.ipify.org?format=json");
  const ipResponseData = await ipResponse.json();

  const geoLocationResponse = await fetch(
    `https://geo.ipify.org/api/v2/country,city?apiKey=${apiKey}&ipAddress=${ipResponseData.ip}`
  );
  const geoLocationResponseData = await geoLocationResponse.json();
  coords.latitude = geoLocationResponseData.location.lat;
  coords.longitude = geoLocationResponseData.location.lng;
  getWeatherInfo();
};

const getWeatherInfo = async () => {
  if (true === valGeoData()) {
    const lat = coords.latitude;
    const lon = coords.longitude;
    const cityAPI = `https://api.openweathermap.org/geo/1.0/reverse?lat=${lat}&lon=${lon}&limit=1&appid=${appID}`;
    const responseCity = await fetch(cityAPI);
    const locationData = await responseCity.json();
    const city = locationData[0].name;
    const state = locationData[0].state;

    let weatherAPI = `https://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&appid=${appID}`;
    let responseWeather = await fetch(weatherAPI);
    if (404 === responseWeather.status) {
      weatherAPI = `https://api.openweathermap.org/data/2.5/weather?q=${state}&units=metric&appid=${appID}`;
      responseWeather = await fetch(weatherAPI);
    }
    const weatherData = await responseWeather.json();
    patchHTML(weatherData);
  } else {
    getGeoByIP();
  }
};

const getCoords = async (pos) => {
  coords = pos.coords;
  getWeatherInfo();
};

const error = (err) => {
  console.warn(`ERROR(${err.code}): ${err.message}`);
};

const getLocation = () => {
  navigator.geolocation.getCurrentPosition(getCoords, error, options);
};

(function () {
  if (false === valGeoData()) {
    getLocation();
  }
  getWeatherInfo();
})();
