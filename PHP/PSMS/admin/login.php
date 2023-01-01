<?php

ob_start();
session_start();
error_reporting(0);

include "includes/header.php";
$sql2 = "SELECT * FROM clg_details  WHERE id = 1";
$result2 = mysqli_query($conn,$sql2);
$row2 = mysqli_fetch_assoc($result2);

if(isset($_SESSION['login_user']))
{
    header("location:category");
}
else
{
	if($_SERVER["REQUEST_METHOD"] == "POST") 
	{
		$username=$_POST['username'];
        $password=$_POST['password'];
	   	$username=mysqli_real_escape_string($conn,$username);
		$password=mysqli_real_escape_string($conn,$password);
		$username=test_input($username);
		$password=test_input($password);

		$sql="select password from clg_details where username='$username'";
		$res=mysqli_query($conn,$sql);
		$row=mysqli_fetch_assoc($res);
		$pass=$row['password'];
		
		if(password_verify($password,$pass))
		{
			//session_register("username");
			$_SESSION['login_user'] = $username;
			header("location:category");
		}
		else 
		{
			$_SESSION['error'] = "Invalid Username or Password ! Try Again With Valid Credentials.";
		}
	}	
?>
	</head>
	<body>
	<br><br><br>
	<div class="container" style="width:40%;">
		<form action="" autocomplete="off" method="POST" enctype="multipart/form-data">
			<div class="text-center mb-4">
				<img class="mb-4" src="../register/images/<?php echo $row2['logo'];?>" alt="" width="120" height="120">
				<h1 class="h3 mb-3 font-weight-normal">PSMS</h1>
				<p><?php echo $row2['clg_name'];?>, <?php echo $row2['clg_add'];?></p>
			</div>
			<?php if(isset($_SESSION['error'])){ ?>
			<b><p align="center" class="alert alert-danger"><?php echo $_SESSION['error']; unset($_SESSION['error']);?></p></b>
			<?php } ?>
			<div class="form-label-group">
				<label for="username">Username</label>
					<input type="username" id="username" name="username" class="form-control" placeholder="Username" autofocus>
							</div>
			<div class="form-label-group">
			<label for="password">Password</label>
			<input type="password" id="password" name="password" class="form-control" placeholder="Password">
				</div>
			<br>
			<button class="btn btn-primary btn-md btn-block" type="submit">Sign In</button>
			<p class="mt-5 mb-3 text-muted text-center">&copy; 2020 - Developed By: Saurav iCafe</p>
		</form>
		</div>
	</body>
</html>
<?php } ?>