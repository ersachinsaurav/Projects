<?php
error_reporting(0);
	include "includes/navbar.php";
	if(isset($_SESSION['username']))
	{
		$username=$_SESSION['username'];
	?>
		<!---Main Content-->
		<div class="main">
		<div class="row">
		<div class="col l6 m6 s12">
		<ul class="collection with-header">
		<li class="collection-header teal">
		<h5 class="white-text">Recent Posts</h5>
		<span id="message"></span>
		</li>
		<?php
		$sql="select * from posts where author='$username' order by id desc limit 7";
		$res=mysqli_query($conn,$sql);
		if(mysqli_num_rows($res)>0)
		{
			while($row=mysqli_fetch_assoc($res))
			{
			?>
			<li class="collection-item">
			<a href=""><?php echo $row['title']?></a>
			<br>
			<span><a href="edit.php?id=<?php echo $row['id']; ?>"><i class="material-icons tiny">edit</i> Edit</a> | <a href="" id="<?php echo $row['id']; ?>" class="delete"><i class="material-icons tiny red-text">clear</i> Delete</a> | <a href=""><i class="material-icons tiny green-text">share</i> Share</a></span>
			</li>
		<?php
			}
			?>
			<br>
			<a href="post.php" class="right">View All</a>
			<?php
		}
		else
		{
		  echo "<div class='chip red white-text'>No Post in Database , write a New One by clicking circular button Below</div>";
		}
		?>
		</ul>
		</div>
		
		<div class="col l6 m6 s12">
		<ul class="collection with-header">
		<li class="collection-header teal">
		<h5 class="white-text">Recent Comments</h5>
		<span id="message2"></span>
		</li>
	
		<?php
$sql5="select * from comment where author='$username' order by id desc limit 7";
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
<br>
		<span><a href="" class="approve" id="<?php echo $row5['id'];?>"><i class="material-icons tiny green-text">done</i> Approve</a> | <a href="" class="remove" id="<?php echo $row5['id'];?>"><i class="material-icons red-text tiny">clear</i> Remove</a></span>
</li>
<?php
	}
}
?>
		</li>
		<br>
			<a href="comment.php" class="right">View All</a>
		
		</ul>
		</div>
		</div>
		</div>
		



		<div class="fixed-action-btn">
		<a href="write.php" class="btn-floating btn btn-large white-text pulse"><i class="material-icons">edit</i></a>
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
	<!---JS For Post Deletion-->
	<script>
	const del=document.querySelectorAll(".delete");
	del.forEach(function(item,index)
	{
		item.addEventListener("click",deleteNow)
	})
	
	function deleteNow(e)
	{
		e.preventDefault();
		if(confirm("Do you really Want to Delete"))
		{
			const xhr=new XMLHttpRequest();
			xhr.open("GET","delete.php?id="+Number(e.target.id),true)
			xhr.onload=function()
			{
			  const messg=xhr.responseText;
			  const message=document.getElementById("message")
			  message.innerHTML=messg;
			}
			xhr.send()
		}
	}
	</script>

	<!---JS For Comment Approval-->
<script>
	const aprv=document.querySelectorAll(".approve");
	aprv.forEach(function(item,index)
	{
		item.addEventListener("click",approveNow)
	})
	
	function approveNow(e)
	{
		e.preventDefault();
		if(confirm("Do You Really Want To Approve"))
		{
			const xhr=new XMLHttpRequest();
			xhr.open("GET","approve.php?id="+Number(e.target.id),true)
			xhr.onload=function()
			{
			  const messg=xhr.responseText;
			  const message=document.getElementById("message2")
			  message.innerHTML=messg;
			}
			xhr.send()
		}
	}
	</script>

	<!---JS For Comment Removal-->
<script>
	const rmv=document.querySelectorAll(".remove");
	rmv.forEach(function(item,index)
	{
		item.addEventListener("click",removeNow)
	})
	
	function removeNow(e)
	{
		e.preventDefault();
		if(confirm("Do You Really Want To Remove"))
		{
			const xhr=new XMLHttpRequest();
			xhr.open("GET","remove.php?id="+Number(e.target.id),true)
			xhr.onload=function()
			{
			  const messg=xhr.responseText;
			  const message=document.getElementById("message2")
			  message.innerHTML=messg;
			}
			xhr.send()
		}
	}
	</script>