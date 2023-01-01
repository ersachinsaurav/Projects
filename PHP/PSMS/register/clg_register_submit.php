<?php
include "includes/config.php";
ob_start();
session_start();

if(isset($_POST['step1_submit']))
{	
	$clg_name=$_POST['clg_name'];
	$clg_name=mysqli_real_escape_string($conn,$clg_name);
	$clg_name=test_input($clg_name);
	
	$clg_add=$_POST['clg_add'];
	$clg_add=mysqli_real_escape_string($conn,$clg_add);
	$clg_add=test_input($clg_add);

	$principal=$_POST['principal'];
	$principal=mysqli_real_escape_string($conn,$principal);
	$principal=test_input($principal);

	$username=$_POST['username'];
	$username=mysqli_real_escape_string($conn,$username);
	$username=test_input($username);

	$password=$_POST['password'];
	$password=mysqli_real_escape_string($conn,$password);
	$password=test_input($password);
	
	$cpassword=$_POST['cpassword'];
	$cpassword=mysqli_real_escape_string($conn,$cpassword);
	$cpassword=test_input($cpassword);
	
	$password2=test_input($password);
	$password=password_hash($password,PASSWORD_BCRYPT);

	$sql2="select * from clg_details where id=1";
	$res2=mysqli_query($conn,$sql2);
	
	if(($password2)===($cpassword))
	{
			if(mysqli_num_rows($res2)==1)
			{
				$sql4 = "UPDATE clg_details SET clg_name='$clg_name',clg_add='$clg_add',principal='$principal',username='$username',password='$password' WHERE id = 1";
				$res4=mysqli_query($conn, $sql4);
			}
			else
			{
				$sql = "INSERT INTO clg_details (clg_name, clg_add, principal, username, password) VALUES ('$clg_name', '$clg_add', '$principal', '$username', '$password')";
				$res=mysqli_query($conn, $sql);
			}

			if($res) 
			{
				$_SESSION['msg']="Registered Successfully! Now Update Respective Images.";
				header("Location:image_update");
			}
			else if($res4)
			{
				$_SESSION['msg']="Details Updated Successfully! Now Update Respective Images, If Needed.";
				header("Location:image_update");
			}
			else
			{
				$_SESSION['msg']="Something Went Wrong. Try Again!";
				header("Location:clg_register");
			}
	}
	else
	{
		$_SESSION['msg']="Password And Confirm Password Must Be Same.";
		header("Location:clg_register");
	}
}
else
{
	header("Location:$logout");
	die();	
}
mysqli_close($conn);
?>