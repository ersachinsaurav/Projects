const patchHTML = (weatherData) => {
	document.getElementsByClassName(
		'temp'
	)[0].innerHTML = `${weatherData.main.temp}&deg;C`;
	document.getElementsByClassName(
		'tempMinMax'
	)[0].innerHTML = `<b>Min</b> ${weatherData.main.temp_min}&deg;C | <b>Max</b> ${weatherData.main.temp_max}&deg;C`;
	document.getElementsByClassName(
		'locationInfo'
	)[0].innerHTML = `${weatherData.name}, ${weatherData.sys.country}`;

	const weatherType = weatherData.weather[0].main;

	const wc = document.getElementsByClassName('weathercon')[0];

	if (weatherType == 'Clear') {
		wc.innerHTML = "<i class='fa-solid fa-sun' style='color: #eccc68;'></i>";
	} else if (weatherType == 'Clouds') {
		wc.innerHTML = "<i class='fa-solid fa-cloud' style='color: #f1f2f6;'></i>";
	} else if (weatherType == 'Rain') {
		wc.innerHTML =
			"<i class='fa-solid fa-cloud-rain' style='color: #f1f2f6;'></i>";
	} else if (weatherType == 'Thunderstorm') {
		wc.innerHTML =
			"<i class='fa-solid fa-cloud-bolt' style='color: #47475c;'></i>";
	} else if (weatherType == 'Drizzle') {
		wc.innerHTML =
			"<i class='fa-solid fa-cloud-sun-rain' style='color: #FFFFF;'></i>";
	} else if (weatherType == 'Snow') {
		wc.innerHTML =
			"<i class='fa-solid fa-snowman' style='color: #f1f7ed;'></i>";
	} else {
		wc.innerHTML = "<i class='fa-solid fa-smog' style='color:#090975;'></i>";
	}
};

const getCurrentDay = () => {
	let weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thurs', 'Fri', 'Sat'];
	let currentDateTime = new Date();
	let day = weekdays[currentDateTime.getDay()];
	return day;
};

const getCurrentDateTime = () => {
	let months = [
		'Jan',
		'Feb',
		'Mar',
		'Apr',
		'May',
		'Jun',
		'Jul',
		'Aug',
		'Sep',
		'Oct',
		'Nov',
		'Dec',
	];

	let currentDateTime = new Date();
	let month = months[currentDateTime.getMonth()];
	let date = currentDateTime.getDate();
	let hours = currentDateTime.getHours();
	let mins = currentDateTime.getMinutes();

	let meridiem = 'AM';
	if (hours > 11) {
		meridiem = 'PM';
		if (hours > 12) hours -= 12;
	}
	if (mins < 10) {
		mins = '0' + mins;
	}

	return `${month} ${date} | ${hours}:${mins}${meridiem}`;
};

const patchDateTime = () => {
	document.getElementsByClassName('dateTimeInfo')[0].innerHTML =
		innerHTML = `${getCurrentDay()} | ${getCurrentDateTime()}`;
};

(function () {
	setInterval(patchDateTime, 1000);
})();
