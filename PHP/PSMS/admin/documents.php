<?php 
include "includes/session.php";
include "includes/header.php";
if(isset($_GET['id']))
	{
	$id=$_GET['id'];
	$id=mysqli_real_escape_string($conn,$id);
	$id=test_input($id);
	$sql = "SELECT * FROM employee WHERE id = $id";
	$result = mysqli_query($conn,$sql);
	$row = mysqli_fetch_assoc($result);
?>
	</head>
	<body class="d-flex flex-column h-100">
	<?php include "includes/navbar.php";?>
			<!-- Begin page content -->
		<main role="main" class="flex-shrink-0">
			<div class="container">
			<h1 class="mt-5">Photo & Documents</h1>
			<br>
			<br>


<?php if(isset($_SESSION['msg'])){ ?>
<b><p align="center" class="alert alert-success"><?php echo $_SESSION['msg']; unset($_SESSION['msg']);?></p></b>
<?php } ?>

<?php if(isset($_SESSION['error'])){ ?>
<b><p align="center" class="alert alert-danger"><?php echo $_SESSION['error']; unset($_SESSION['error']);?></p></b>
<?php } ?>



<div align="center" class="alert alert-warning">
<strong>Note: </strong>Upload All Available Documents <strong>(JPG/JPEG/PNG Format, Max 1MB Each File)</strong>; Don't Leave It Blank Unless You're Unable To Do So!
</div>
<br>

<!--Start Upload Section-->
<div class="row">

<!--Photo-->
<div class="col divmargin lg-4 md-6 sm-12">
<form action="uploads/emp_photo?id=<?php echo $row['id'];?>" method="POST" enctype="multipart/form-data">
<h4>Employee Photo</h4>
<img src="images/<?php echo $row['id'];?>/<?php echo $row['emp_photo'];?>" class="img-responsive imgsize" id="emp_photo" />
<input class="btn btn-warning imgmargin" type="submit" name="emp_photo_upload" value="Upload">
<br><br>
<input type="file" accept="image/*" value="<?php $row['emp_photo'];?>" name="emp_photo" onchange="preview_emp_photo(event)">
</form>
</div>

<!--Doc1-->
<div class="col divmargin lg-4 md-6 sm-12">
<form action="uploads/doc1?id=<?php echo $row['id'];?>" method="POST" enctype="multipart/form-data">
<h4>Doc1</h4>
<img src="images/<?php echo $row['id'];?>/<?php echo $row['doc1'];?>" class="img-responsive imgsize" id="doc1" />
<input class="btn btn-warning imgmargin" type="submit" name="doc1_upload" value="Upload">
<br><br>
<input type="file" accept="image/*" value="<?php $row['doc1'];?>" name="doc1" onchange="preview_doc1(event)">
</form>
</div>

<!--Doc2-->
<div class="col divmargin lg-4 md-6 sm-12">
<form action="uploads/doc2?id=<?php echo $row['id'];?>" method="POST" enctype="multipart/form-data">
<h4>Doc2</h4>
<img src="images/<?php echo $row['id'];?>/<?php echo $row['doc2'];?>" class="img-responsive imgsize" id="doc2" />
<input class="btn btn-warning imgmargin" type="submit" name="doc2_upload" value="Upload">
<br><br>
<input type="file" accept="image/*" value="<?php $row['doc2'];?>" name="doc2" onchange="preview_doc2(event)">
</form>
</div>

</div>
<!--End Upload Section-->
<br>
<br>
</main>
<?php 
include "includes/footer.php";
include "includes/upload.js";

}
else
    {
        header("Location: category");
    }
?>