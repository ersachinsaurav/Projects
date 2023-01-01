<?php 
include "includes/session.php";
include "includes/header.php";
?>
	</head>
	<body class="d-flex flex-column h-100">
	<?php include "includes/navbar.php";?>
			<!-- Begin page content -->
		<main role="main" class="flex-shrink-0">
			<div class="container">
			<h1 class="mt-5">PSMS Category</h1>
			<br>
			<br>
			<?php if(isset($_SESSION['msg'])){ ?>
		<b>
			<p align="center" class="alert alert-success"><?php echo $_SESSION['msg']; unset($_SESSION['msg']);?></p>
		</b>
		<?php } ?>
		<?php if(isset($_SESSION['error'])){ ?>
		<b>
			<p align="center" class="alert alert-danger"><?php echo $_SESSION['error']; unset($_SESSION['error']);?></p>
		</b>
		<?php } ?>
			<div class="row">
				<div class="col-md-4">
					<h2>Teaching Staff</h2>
					<br>
					<a class="btn btn-secondary" href="teaching_staff" role="button">View details &raquo;</a>
				</div>
				<div class="col-md-4">
					<h2>Non Teaching Staff</h2>
					<br>
					<h3>III - Grade Staff</h3>
					<br>
					<a class="btn btn-secondary" href="third_staff" role="button">View details &raquo;</a>
					<br>
					<br>
					<br>
					<h3>IV - Grade Staff</h3>
					<br>
					<a class="btn btn-secondary" href="fourth_staff" role="button">View details &raquo;</a>
				
				</div>
				<div class="col-md-4">
					<h2>Altogether</h2>
					<br>
					<a class="btn btn-secondary" href="altogether" role="button">View details &raquo;</a>
				</div>
			</div>
		</main>
		<?php include "includes/footer.php";?>