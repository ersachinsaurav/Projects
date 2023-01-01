<?php
include "includes/config.php";
include "includes/session.php";
if(isset($_SESSION['login_user']))
{
	if(isset($_GET['id']))
	{
		$id=$_GET['id'];
		$id=mysqli_real_escape_string($conn,$id);
		$id=test_input($id);
		$sql="delete from employee where id=$id";
		$res=mysqli_query($conn,$sql);
		if($res)
		{
		  echo "<b><p align='center' class='alert alert-success'>Employee Deleted Successfully.</p></b>";
		}
		else
		{
		  echo "<b><p align='center' class='alert alert-danger'>Something Went Wrong. Try Again!</p></b>";
		}
	}
	else
		{
			header("Location: category");
		}
}
else
	{
		header("Location: $logout");
	}
?>