<!doctype html>
<html lang="en">
	<head>
		<title>CRUD</title>
		<link href="bootstrap.min.css" rel="stylesheet">
		<script type="text/javascript" src="jquery.min.js"></script>
		<style>
		.error-msg, .error {
			color: red;
			font-weight: 400;
			font-size: 14px;
			padding-left: 10px;
		}
		.error {
			font-size: 18px;
			font-weight: 500;
			text-align: center;
			padding: 10px;
		}
		</style>
	</head>
	<body class="bg-light">
		<div class="container" id="form">
			<?php 
			include("formRegister.php");
			?>

		</div>
		<div class="container">
			<div class="pb-4">
				<div class="py-5 text-center ">
						<h2>Registered Users</h2>
				</div>
				
				<div class="row pt-3 font-weight-bold border-bottom">
					<div class="col-1">SN#</div>
					<div class="col-3">Name</div>
					<div class="col-4">Email</div>
					<div class="col-2">Mobile</div>
					<div class="col-1">Edit</div>
					<div class="col-1">Delete</div>
				</div>
				<div class="row">
					<div class="col-12" id="data">

					</div>

				</div>


			</div>

		</div>

		<script type="text/javascript" src="validation.js"></script>
		<script type="text/javascript" src="manipulators.js"></script>
	</body>
</html>