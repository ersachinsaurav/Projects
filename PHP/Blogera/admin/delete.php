<?php
include "includes/header.php";
if(isset($_SESSION['username']))
{
	if(isset($_GET['id']))
	{
		$id=$_GET['id'];
		$id=mysqli_real_escape_string($conn,$id);
		$id=htmlentities($id);
		$sql="delete from posts where id=$id";
		$res=mysqli_query($conn,$sql);
		if($res)
		{
		  echo "<div class='chip green white-text'>Deleted Successfully.</div>";
		}
		else
		{
		  echo "<div class='chip red black-text'>Something Went Wrong.</div>";
		}
	}
	else
		{
			header("Location: dashboard.php");
		}
}
else
	{
		$_SESSION['message']="<div class='chip red white-text'>Please Login To Continue.</div>";
		header("Location: login.php");
	}
?>