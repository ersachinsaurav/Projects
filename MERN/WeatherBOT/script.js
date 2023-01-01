const currentDate = document.getElementsByClassName('date')[0];
const wc = document.getElementsByClassName('weathercon')[0];
const weatherType = '{%weatherType%}';

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

// Immediately Invoked Function Expressions (IIFE) -> Self executing function
(function () {
	currentDate.innerHTML = getCurrentDay() + ' | ' + getCurrentDateTime();

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
})();
