<?php
ob_start();
session_start();
include "dbh.php";
?>

<!DOCTYPE html>
<html>

<head>
	<!--Import Google Icon Font-->
	<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

	<!--Import Font Awesome Icon Font-->
	<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">

	<!--Import materialize.css-->
	<link type="text/css" rel="stylesheet" href="../css/materialize.min.css" media="screen,projection" />

	<!--Let browser know website is optimized for mobile-->
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<title>Blogera</title>

	<style>
		::placeholder {
			/* Chrome, Firefox, Opera, Safari 10.1+ */
			color: blue;
			opacity: 1;
			/* Firefox */
		}
		
		:-ms-input-placeholder {
			/* Internet Explorer 10-11 */
			color: blue;
		}
		
		::-ms-input-placeholder {
			/* Microsoft Edge */
			color: blue;
		}
		
		footer,
		header,
		.main {
			padding-left: 310px;
		}
		
		@media(max-width:992px) {
			footer,
			header,
			.main {
				padding-left: 0px;
			}
		}
	</style>

</head>

<body>