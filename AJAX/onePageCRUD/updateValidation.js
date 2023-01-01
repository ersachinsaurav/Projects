var nameError = "",
	emailError = "",
	mobileError = "",
	dobError = "",
	genderError = "",
	countryError = "",
	stateError = "",
	cityError = "";

var id = $('#id').val();

$(document).ready(function () {
	$('#country').on('change', function () {
		var country = this.value;
		$.ajax({
			url: "states.php",
			type: "POST",
			data: {
				country: country
			},
			cache: false,
			success: function (result) {
				$("#state").html(result);
				$('#city').html('<option value="">Select State First</option>');
			}
		});
	});

	$('#state').on('change', function () {
		var state = this.value;
		$.ajax({
			url: "cities.php",
			type: "POST",
			data: {
				state: state
			},
			cache: false,
			success: function (result) {
				$("#city").html(result);
			}
		});
	});
});

$('#email').on('blur', function (e) {
	var email = $('#email').val();
	if (email == '') {
		$(".error-email").text("E-Mail Can't Empty !");
		emailError = "error";
		return false;
	} else {
		$(".error-email").text("");
		emailError = "";
	}
	$.ajax({
		url: 'email-check.php',
		type: 'post',
		data: {
			'update_email_check': 1,
			'email': email,
			'id': id,
		},
		success: function (response) {
			if (response != 'true') {
				$(".error-email").text(response);
				emailError = "error";
			} else {
				$(".error-email").text("");
				emailError = "";
			}
		}
	});
});

$('#mobile').on('blur', function (e) {
	var mobile = $('#mobile').val();
	if (mobile == "") {
		$('.error-mobile').text('Enter Your Mobile Number');
		mobileError = "error";
		return false;
	} else if (mobile.length != 10) {
		$('.error-mobile').text('Enter Valid Mobile Number');
		mobileError = "error";
		return false;
	} else {
		$('.error-mobile').text('');
		mobileError = "";
	}

	$.ajax({
		url: 'mobile-check.php',
		type: 'post',
		data: {
			'update_mobile_check': 1,
			'mobile': mobile,
			'id': id,
		},
		success: function (response) {
			if (response != 'true') {
				$(".error-mobile").text(response);
				mobileError = "error";
			} else {
				$(".error-mobile").text("");
				mobileError = "";
			}
		}
	});
});


$('#update').click(function (e) {
	var name = $('#name').val();
	var nwc = $('#name').val().split(' ');
	if (name == "") {
		$('.error-name').text('Enter Your Name');
		nameError = "error";
	} else if (nwc.length < 2 || nwc.length > 5) {
		$('.error-name').text('Name Must Be Between Two To Five Words');
		nameError = "error";
	} else {
		$('.error-name').text('');
		nameError = "";
	}

	var mobile = $('#mobile').val();
	if (mobile == "") {
		$('.error-mobile').text('Enter Mobile Number');
		mobileError = "error";
	}

	var gender = $('#gender').val();
	if (gender == "") {
		$('.error-gender').text('Select Gender');
		genderError = "error";
	} else {
		$('.error-gender').text('');
		genderError = "";
	}

	var dob = $('#dob').val();
	if (dob == "") {
		$('.error-dob').text('Select Valid Date  of Birth');
		dobError = "error";
	} else {
		newDob = new Date(dob);
		var today = new Date();
		var age = Math.floor((today - newDob) / (365.25 * 24 * 60 * 60 * 1000));
		if (age < 18) {
			$('.error-dob').text('Age Must Be Above 18');
			dobError = "error";
		} else {
			$('.error-dob').text('');
			dobError = "";
		}
	}

	var email = $('#email').val();
	if (email == "") {
		$('.error-email').text('Enter Email Address');
		emailError = "error";
	}

	var country = $('#country').val();
	if (country == "") {
		$('.error-country').text('Select Country');
		countryError = "error";
	} else {
		$('.error-country').text('');
		countryError = "";
	}

	var state = $('#state').val();
	if (state == "") {
		$('.error-state').text('Select State');
		stateError = "error";
	} else {
		$('.error-state').text('');
		stateError = "";
	}

	var city = $('#city').val();
	if (city == "") {
		$('.error-city').text('Select City');
		cityError = "error";
	} else {
		$('.error-city').text('');
		cityError = "";
	}

	if (nameError == "" && mobileError == "" && emailError == "" && dobError == "" && genderError == "" && countryError == "" && stateError == "" && cityError == "") {
		$.ajax({
			url: 'update.php',
			type: 'post',
			data: {
				'user': 1,
				'id': id,
				'name': name,
				'mobile': mobile,
				'gender': gender,
				'dob': dob,
				'email': email,
				'country': country,
				'state': state,
				'city': city,
			},
			success: function (response) {
				if (response == 'true') {
					$('.error-msg').text('');
					$('.error').text('');
					alert('Updated Successfully!');
					$("#form").load("formRegister.php");
					$("#data").load("data.php");
				} else {
					$('.error').text(response);
				}
			}
		});
	} else {
		return false;
	}
});