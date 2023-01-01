<?php
include "includes/header.php";
if(isset($_SESSION['username']))
{
	if(isset($_POST['update']))
	{
		$id=$_GET['id'];
		$id=mysqli_real_escape_string($conn,$id);
		$id=htmlentities($id);

		$data=$_POST['ckeditor'];
		$data=mysqli_real_escape_string($conn,$data);
		$data=htmlentities($data);

		$title=$_POST['title'];
		$title=mysqli_real_escape_string($conn,$title);
		$title=htmlentities($title);

		$sql="update posts set title='$title',content='$data' where id=$id";
		$res=mysqli_query($conn,$sql);

		if($res)
		{
			$_SESSION['message']="<div class='chip green white-text'>Post Updated.</div>";
			header("Location: edit.php?id=".$id);
		}
		else
		{
			$_SESSION['message']="<div class='chip red white-text'>Something Went Wrong.</div>";
			header("Location: edit.php?id=".$id);
		}
	}
	else
		{
			header("Location: edit.php?id=".$id);
		}
}
else
	{
		$_SESSION['message']="<div class='chip red white-text'>Please Login To Continue.</div>";
		header("Location: login.php");
	}
?>