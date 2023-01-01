<?php include "includes/header.php";?>
<br>
<br>
<div>
	<h3 align="center">Image Update</h3>
</div>
<br>
<br>
<div class="container">
    <?php if(isset($_SESSION['error'])){ ?>
	<b>
	<p align="center" class="alert alert-danger"><?php echo $_SESSION['error']; unset($_SESSION['error']);?></p>
	</b>
	<?php } ?>
	<?php if(isset($_SESSION['msg'])){ ?>
	<b>
	<p align="center" class="alert alert-success"><?php echo $_SESSION['msg']; unset($_SESSION['msg']);?></p>
	</b>
	<?php } ?>
<div class="form-row">
			<!--Logo-->
<div class="col divmargin lg-6 md-6 sm-12">
<form action="uploads/logo" method="POST" enctype="multipart/form-data">
<h4>Institution's Logo</h4>
<img src="images/<?php echo $row['logo'];?>" class="img-responsive imgsize" id="logo" />
<input class="btn btn-warning imgmargin " type="submit" name="logo_upload" value="Upload">
<br><br>
<input type="file" accept="image/*" name="logo" onchange="preview_logo(event)">
</form>
</div>

			<!--Principal's Photo-->
            <div class="col divmargin lg-6 md-6 sm-12">
<form action="uploads/principal_photo" method="POST" enctype="multipart/form-data">
<h4>Principal's Photo</h4>
<img src="images/<?php echo $row['principal_photo'];?>" class="img-responsive imgsize" id="principal_photo" />
<input class="btn btn-warning imgmargin " type="submit" name="principal_photo_upload" value="Upload">
<br><br>
<input type="file" accept="image/*" name="principal_photo" onchange="principal_preview_photo(event)">
</form>
</div>
</div>
</div>
<?php include "includes/footer.php";?>

<script type='text/javascript'>
    function preview_logo(event) {
        var reader = new FileReader();
        reader.onload = function() {
            var output = document.getElementById('logo');
            output.src = reader.result;
        }
        reader.readAsDataURL(event.target.files[0]);
    }

    function principal_preview_photo(event) {
        var reader = new FileReader();
        reader.onload = function() {
            var output = document.getElementById('principal_photo');
            output.src = reader.result;
        }
        reader.readAsDataURL(event.target.files[0]);
    }
</script>