<?php
include "includes/navbar.php";
if(isset($_SESSION['username']))
{
	if(isset($_POST['publish']))
	{
		$username=$_SESSION['username'];

		$data=$_POST['ckeditor'];
		$data=mysqli_real_escape_string($conn,$data);

		$title=$_POST['title'];
		$title=mysqli_real_escape_string($conn,$title);
		$title=htmlentities($title);

		$image=$_FILES['image'];
        $img_size=$_FILES['image']['size'];
		$tmp_dir=$_FILES['image']['tmp_name'];
        $type=$_FILES['image']['type'];
        $img_name=mt_rand().'.'.jpg;

		if($type=="image/jpeg" || $type=="image/jpg" || $type=="image/png")
		{
			if($img_size<=1048576)
			{   move_uploaded_file($tmp_dir,"../img/".$img_name);
				$sql="insert into posts (title,content,feature_image,author) values('$title', '$data', '$img_name','$username')";
				$res=mysqli_query($conn,$sql);
				
				if($res)
				{
					$_SESSION['message']="<div class='chip green white-text'>Post Published.</div>";
					header("Location: write.php");
				}
				else
				{
					$_SESSION['message']="<div class='chip red white-text'>Something Went Wrong.</div>";
					header("Location: write.php");
				}
            }
            else
            {
                $_SESSION['message']="<div class='chip red white-text'>Image Size Exceded 1 MB.</div>";
                header("Location: write.php");
            }
        }
        else
        {
            $_SESSION['message']="<div class='chip red white-text'>Image Format Not Supported.</div>";
            header("Location: write.php");
        }
	}
}
else
	{
		$_SESSION['message']="<div class='chip red white-text'>Please Login To Continue.</div>";
		header("Location: login.php");
	}
?>