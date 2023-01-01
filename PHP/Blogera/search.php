<?php
include "includes/header.php";
include "includes/navbar.php";
if(isset($_GET['search_submit']))
{
	$q=$_GET['search'];
	$q=mysqli_real_escape_string($conn,$q);
	$q=htmlentities($q);
	$sql="select * from posts where title like '$q' or content like '$q' or title like '%$q%' or content like '%$q%'";
	$res=mysqli_query($conn,$sql);
	if(mysqli_num_rows($res)>0)
	{
?>
		<div class="row">
		<!--This is main content area -->
		<div class="col l9 m9 s12">
		<?php
		while($row=mysqli_fetch_assoc($res))
		{
		?>
			<div class="col l3 m4 s6">
			<div class="card small">
			<div class="card-image">
			<img src="img/<?php echo $row['feature_image']?>" alt="">
			<span class="card-title black-text truncate"><?php echo $row['title']?></span>
			</div>
			<div class="card-content">
			<?php echo $row['content']?>
			</div>
			<div class="card-action teal center">
			<a href="post.php?id=<?php echo $row['id'];?>" class="white-text">Read More</a>
			</div>
			</div>
			</div>
		<?php
		}
		?>
		</div>
		<!--This is sidebar area -->
		<div class="col l3 m3 s12">
		<?php
		include "includes/sidebar.php"
		?>
		</div>
		</div>
	<?php
	}
	else
	{
		?>
		<div class="row">
		<!--This is main content area -->
		<div class="col l9 m9 s12">
		<h5 class="red-text">Sorry No Post Found By Entered Search Query, Try Again With Another Search Query.</h5>
		</div>
		<!--This is sidebar area -->
		<div class="col l3 m3 s12">
		<?php
		include "includes/sidebar.php"
		?>
		</div>
		</div>
	<?php
	}
}
else
{
	header("Location: index.php");
}
include "includes/footer.php";
?>