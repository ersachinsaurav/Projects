<?php
include "includes/navbar.php";
if(isset($_SESSION['username']))
{
	$dir="../img/";
	$files=scandir($dir);
	if($files)
	{
?>
		<div class="main">
		<div class="row">
		<?php
		foreach($files as $file)
		{
			if(strlen($file)>2)
			{
		?>
			<div class="col l2 m3 s4">
			<div class="card">
			<div class="card-image">
			<img src="../img/<?php echo $file;?>" alt="" style="height:100px; width:150px;">
			<span class="card-title truncate"><?php echo $file;?></span>
			</div>
			</div>
			</div>
		<?php
			}
		}
	}
		?>
		</div>
		</div>
<?php
}
else
	{
		$_SESSION['message']="<div class='chip red white-text'>Please Login To Continue.</div>";
		header("Location: login.php");
	}
include "includes/footer.php";
?>