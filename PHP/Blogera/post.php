<?php
include "includes/header.php"
?>
<?php
include "includes/navbar.php"
?>

<div class="row">
<!--This is main post area -->
<div class="col l9 m9 s12">

<?php
if(isset($_GET['id']))
{
$id=$_GET['id'];
$id=mysqli_real_escape_string($conn,$id);
$id=htmlentities($id);
$sql="select * from posts where id=$id";
$res=mysqli_query($conn,$sql);
if(mysqli_num_rows($res)>0)
{
$sql2="select views from posts where id=$id";
$res2=mysqli_query($conn,$sql2);
$row2=mysqli_fetch_assoc($res2);
$views=$row2['views'];
$views=$views+1;
$sql3="update posts set views=$views where id=$id";
mysqli_query($conn,$sql3);
$row=mysqli_fetch_assoc($res);
$title=$row['title'];
$content=$row['content'];

?>
<div class="card-panel">
<h5 class="center"><?php echo ucwords ($title);?></h5>
<div class="card-image center">
	<img src="img/<?php echo $row['feature_image']?>" alt=""class="responsive-img">
	</div>
<p class="flow-text"><?php echo ucwords ($content);?></p>
<div class="divider"></div>
<br>
<div class="card-panel">
<h5>Post Your Comment</h5>
<?php
if(isset($_SESSION['message']))
{
  echo $_SESSION['message'];
  unset($_SESSION['message']);
}
?>
<div class="row">
<div class="col 18 offset-12 m10 offset-m1 s12">
<form action="post.php?id=<?php echo $id;?>" method="POST">
<div class="input-field">
<input type="email" name="email" id="email" placeholder="Enter Yout Email" class="validate">
<label for="email" data-error="Invalid Email Format"></label>
</div>
<div class="input-field">
<textarea name="comment" id="comment" class="materialize-textarea" placeholder="Enter Your Comment Here.."></textarea>
</div>
<div class="center">
<input type="submit" value="Comment" name="comment_submit" class="btn">
</div>
</form>
<h5>Comments</h5>
<ul class="collection">
<?php
$sql5="select * from comment where post_id=$id and status=1 order by id desc";
$res5=mysqli_query($conn,$sql5);
if(mysqli_num_rows($res5)>0)
{
	while($row5=mysqli_fetch_assoc($res5))
	{
	?>
<li class="collection-item">
<?php echo $row5['comment_text']; ?>
<span class="secondary-content">
<?php echo $row5['email']; ?>
</span>
</li>
<?php
	}
}
?>
</ul>
</div>
</div>
</div>

<div class="divider"></div>
<h5>Related Post</h5>
<div class="row">
<?php
$sql="select * from posts order by rand() limit 4";
$res=mysqli_query($conn,$sql);
if(mysqli_num_rows($res)>0)
{
while($row=mysqli_fetch_assoc($res))
{
?>

<div class="col l3 m3 s6">
<div class="card small">
<div class="card-image">
	<img src="img/<?php echo $row['feature_image']?>" alt="">
	<span class="card-title black-text truncate"><?php echo $row['title']?></span>
</div>
<div class="card-content truncate">
<?php echo $row['content']?>
</div>
<div class="card-action teal center">
	<a href="post.php?id=<?php echo $row['id'];?>" class="white-text">Read More</a>
</div>
</div>
</div>

<?php
}
}
?>
</div>
</div>


<?php
}
else
{
header("Location: index.php");
}
}
else
{
header("Location: index.php");
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
include "includes/footer.php"
?>

<?php
if(isset($_POST['comment_submit']))
{
	$email=$_POST['email'];
	$email=mysqli_real_escape_string($conn,$email);
	$email=htmlentities($email);

	$comment=$_POST['comment'];
	$comment=mysqli_real_escape_string($conn,$comment);
	$comment=htmlentities($comment);

	$id1=$_GET['id'];
	$id1=mysqli_real_escape_string($conn,$id1);
	$id1=htmlentities($id1);

	$sql4="insert into comment (email, comment_text,post_id) values('$email','$comment',$id1)";
	$sql6="UPDATE comment SET author=(SELECT author FROM posts WHERE comment.post_id = posts.id);";
	$res4=mysqli_query($conn,$sql4);
	mysqli_query($conn,$sql6);

	if($res4)
	{
		$_SESSION['message']="<div class='chip green white-text'>Comment Posted Successfully.</div>";
		header("Location: post.php?id=$id");	
	}
	else
	{
		$_SESSION['message']="<div class='chip red white-text'>Something Went Wrong, Try Again.</div>";
		header("Location: post.php?id=$id");
	}
}

?>