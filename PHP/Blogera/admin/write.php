<?php
include "includes/navbar.php";
if(isset($_SESSION['username']))
	{
?>
	<div class="main">
	<form action="write_check.php" method="POST" enctype="multipart/form-data">
	<div class="card-panel">
	<?php
	if(isset($_SESSION['message']))
	{
		echo $_SESSION['message'];
		unset($_SESSION['message']);
	}
	?>
	<h5 class="center">Write New Post</h5>
	
	<h5>Title For Post</h5>
	<textarea name="title" placeholder="Title Of Your For Post Here.." class="materialize-textarea" required></textarea>
	
	<h5>Featured Image</h5>
	<div class="input-field file-field">
	<div class="btn">
	Upload file
	<input type="file" name="image" required>
	</div>
	<div class="file-path-wrapper">
	<input type="text" class="file-path">
	</div>
	</div>

	<h5>Post Content</h5>
	<textarea name="ckeditor" id="ckeditor" cols="30" rows="10" class="materialize-textarea ckeditor" required></textarea>
	<br>
  <div class="center">
	<input type="submit" value="Publish" name="publish" class="btn white-text">
	</div>
	</div>
	</form>
	</div>

	<!--Import ckeditor materialize.js-->
	  <script type="text/javascript" src="../js/ckeditor/ckeditor.js"></script>
<?php
	include "includes/footer.php";
}
else
	{
		$_SESSION['message']="<div class='chip red white-text'>Please Login To Continue.</div>";
		header("Location: login.php");
	}
?>