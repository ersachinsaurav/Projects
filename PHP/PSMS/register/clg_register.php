<?php include "includes/header.php";?>
<br>
<br>
<div>
	<h3 align="center">New College Registration</h3>
</div>
<br>
<br>
<div class="container">
	<?php if(isset($_SESSION['msg'])){ ?>
	<b>
	<p align="center" class="alert alert-danger"><?php echo $_SESSION['msg']; unset($_SESSION['msg']);?></p>
	</b>
	<?php } ?>
	<form action="clg_register_submit" method="POST" class="needs-validation" novalidate enctype="multipart/form-data" autocomplete="off">
		<div class="form-row">
			<div class="col-md-6">
				<label for="clg_name">College Name<span style="color:red; font-weight:bold;">*</span></label>
				<input type="text" name="clg_name" value="<?php echo $row['clg_name'];?>" class="form-control" minlength="3" maxlength="150" id="clg_name" placeholder="College Name" required tabindex="1">
				<div class="invalid-feedback">
					Enter Valid College Name.
				</div>
			</div>
			<div class="col-md-6">
				<label for="clg_add">College Address<span style="color:red; font-weight:bold;">*</span></label>
				<input type="text" name="clg_add" value="<?php echo $row['clg_add'];?>" class="form-control" minlength="3" maxlength="150" id="clg_add" placeholder="College Address" required tabindex="1">
				<div class="invalid-feedback">
					Enter Valid College Address.
				</div>
			</div>
		</div>
		<div class="form-row">
		<div class="col-md-6">
				<label for="principal">Principal Name</label>
				<input type="text" name="principal" class="form-control" value="<?php echo $row['principal'];?>" id="principal" minlength="3" maxlength="40" placeholder="Principal Name" tabindex="2">
				<div class="invalid-feedback">
					Enter Valid Principal Name.
				</div>
			</div>
			<div class="col-md-6">
				<label for="username">Admin Username<span style="color:red; font-weight:bold;">*</span></label>
				<div class="input-group">
					<div class="input-group-prepend">
						<span class="input-group-text" id="inputGroupPrepend">@</span>
					</div>
					<input type="text" class="form-control" name="username" value="<?php echo $row['username'];?>" id="username" placeholder="Admin Username" aria-describedby="inputGroupPrepend"  minlength="3" maxlength="40" required tabindex="3">
					<div class="invalid-feedback">
						Create Admin Username.
					</div>
				</div>
			</div>
		</div>
		<div class="form-row">
			<div class="col-md-6">
				<label for="password">Create Password<span style="color:red; font-weight:bold;">*</span></label>
				<input type="password" name="password" class="form-control" id="password" placeholder="Password" required  minlength="6" maxlength="30" tabindex="4">
				<div class="invalid-feedback">
					Create a password of minimum 6 characters.
				</div>
			</div>
			<div class="col-md-6">
				<label for="cpassword">Confirm Password<span style="color:red; font-weight:bold;">*</span></label>
				<input type="password" name="cpassword" class="form-control" id="cpassword" placeholder="Confirm Password" onkeyup="checkPass(); return false;" required  minlength="6" maxlength="30" tabindex="5">
				<span id="confirmMessage" class="confirmMessage"></span>
			</div>
		</div>
		<br>
		<br>
		<div class="form-group">
			<div class="form-check">
				<input class="form-check-input" type="checkbox" id="check" required tabindex="7">
				<label class="form-check-label" for="invalidCheck">
				Agree To Terms And Conditions Of Use
				</label>
				<div class="invalid-feedback">
					You Must Agree Before Submitting.
				</div>
			</div>
		</div>
		<hr class="mb-4">
		<div class="text-center alert alert-success font-weight-bold">Ensure All Field In Green Before Submitting The Form.</div>
		<div class="form-row">
			<button class="btn btn-danger btn-lg col-md-6" name="reset" type="reset" tabindex="0">Reset</button>
			<button class="btn btn-primary btn-lg col-md-6" id="step1_submit" name="step1_submit" type="submit" tabindex="8" disabled>Save</button>
		</div>
		<br>
	</form>
</div>

<?php include "includes/footer.php";?>

<script type="text/javascript">
//First Script
	function checkPass() {
	    var password = document.getElementById('password');
	    var cpassword = document.getElementById('cpassword');
	    var message = document.getElementById('confirmMessage');
	    if (password.value === cpassword.value) {
	        cpassword.style.borderColor = "#28A745";
			message.innerHTML=""
	    } else {
	        message.style.color = "#DC3545";
	        message.style.fontSize = "small";
			cpassword.style.borderColor = "#DC3545";
			message.innerHTML="Password And Confirm Password Must Be Same."
	    }
	}
	
//Second Script
	var val = document.getElementById("clg_name");
	var val2 = document.getElementById("principal");
	var val3 = document.getElementById("username");
	var val4 = document.getElementById("password");
	var val5 = document.getElementById("cpassword");
	var val6 = document.getElementById("check");
	var val7 = document.getElementById("clg_add");
		
	val.onchange=val2.onchange=val3.onchange=val4.onchange=val5.onchange=val6.onchange=val7.onchange = function () {
	if (val.value ==""||val2.value ==""||val3.value ==""||val4.value ==""||val5.value ==""||val7.value ==""||val6.checked == false||val4.value !== val5.value){
	document.getElementById("step1_submit").disabled = true;
	}
	else{ document.getElementById("step1_submit").disabled = false;}
	}
</script>

<script>
        //JavaScript for disabling form submissions if there are invalid fields
        (function() {
            'use strict';

            window.addEventListener('load', function() {
                // Fetch all the forms we want to apply custom Bootstrap validation styles to
                var forms = document.getElementsByClassName('needs-validation');

                // Loop over them and prevent submission
                var validation = Array.prototype.filter.call(forms, function(form) {
                    form.addEventListener('submit', function(event) {
                        if (form.checkValidity() === false) {
                            event.preventDefault();
                            event.stopPropagation();
                        }
                        form.classList.add('was-validated');
                    }, false);
                });
            }, false);
        })();
    </script>