<?php
include "includes/navbar.php";
if(isset($_SESSION['username']))
{
?>
	<?php
	if(isset($_GET['id']))
	{
		$id=$_GET['id'];
		$id=mysqli_real_escape_String($conn,$id);
		$id=htmlentities($id);
		$sql="select * from posts where id=$id";
		$res=mysqli_query($conn,$sql);
		if(mysqli_num_rows($res)>0)
		{   
			$row=mysqli_fetch_assoc($res);
	?>
			<div class="main">
			<form action="edit_check.php?id=<?php echo $id;?>" method="POST" enctype="multipart/form-data">
			<div class="card-panel">
			<?php
			if(isset($_SESSION['message']))
			{
				echo $_SESSION['message'];
				unset($_SESSION['message']);
			}
			?>
			<h5>Title For Post</h5>
			<textarea name="title" placeholder="Title Of Your For Post Here.." class="materialize-textarea" required><?php echo $row['title'];?>
			</textarea>
			<h5>Post Content</h5>
			<textarea name="ckeditor" id="ckeditor" cols="30" rows="10" class="materialize-textarea ckeditor" required><?php echo $row['content'];?></textarea>
			<br>
			<div class="center">
			<input type="submit" value="Update" name="update" class="btn white-text">
			</div>
			</div>
			</form>
			</div>

			<!--Import ckeditor materialize.js-->
			<script type="text/javascript" src="../js/ckeditor/ckeditor.js"></script>
	<?php    
		}
		else
		{
			header("Location: dashboard.php");
		}
	}
	else
		{
			header("Location: dashboard.php");
		}
	?>
<?php
}
else
	{
		$_SESSION['message']="<div class='chip red white-text'>Please Login To Continue.</div>";
		header("Location: login.php");
	}
include "includes/footer.php";
?>