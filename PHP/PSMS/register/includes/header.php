<?php 
include "config.php";
$sql = "SELECT * FROM clg_details  WHERE id = 1";
$result = mysqli_query($conn,$sql);
$row = mysqli_fetch_assoc($result);
?>
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="author" content="Saurav iCafe">
    <title>PSMS - College Registration</title>
    <link href="../css/bootstrap.min.css" rel="stylesheet">
	<script src="../js/jquery-3.4.1.slim.min.js"></script>
	<script src="../js/bootstrap.bundle.min.js"></script>
    <style>
    .imgsize{
    width:110px; 
    height:140px; 
    margin-bottom:20px;
  }

  .imgmargin{
    margin-left:50px;
  }
  </style>
</head>
<body class="bg-light">
<!-- Navbar -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark	">
		<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbar" aria-controls="navbar" aria-expanded="false" aria-label="Toggle navigation">
		<span class="navbar-toggler-icon"></span>
		</button>
		<div class="collapse navbar-collapse justify-content-md-center" id="navbar">
			<ul class="navbar-nav">
				<li class="nav-item">
					<a class="nav-link" href="clg_register">Register College</a>
				</li>
				<li class="nav-item">
					<a class="nav-link" href="image_update">Images Update</a>
				</li>
			</ul>
		</div>
	</nav>