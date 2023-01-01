<?php 
	include "includes/session.php";
	include "includes/header.php";
	?>
</head>
<body class="d-flex flex-column h-100">
	<?php include "includes/navbar.php";?>
	<br>
	<br>
	<div>
		<h3 align="center">Add Employee</h3>
	</div>
	<br>
	<br>
	<div class="container" style="width:80%;">
		<?php if(isset($_SESSION['msg'])){ ?>
		<b>
			<p align="center" class="alert alert-success"><?php echo $_SESSION['msg']; unset($_SESSION['msg']);?></p>
		</b>
		<?php } ?>
		<?php if(isset($_SESSION['error'])){ ?>
		<b>
			<p align="center" class="alert alert-danger"><?php echo $_SESSION['error']; unset($_SESSION['error']);?></p>
		</b>
		<?php } ?>
		<form action="add_employee_submit" method="POST" class="needs-validation" novalidate enctype="multipart/form-data" autocomplete="off">
			<div class="form-row">
				<div class="col-md-6">
					<label for="emp_name">Employee Name<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="emp_name" class="form-control" minlength="3" maxlength="150" id="emp_name" placeholder="Employee Name" required tabindex="1">
					<div class="invalid-feedback">
						Enter Valid Employee Name.
					</div>
				</div>
				<div class="col-md-6">
					<label for="mname">Mother's Name<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="mname" class="form-control" id="mname" placeholder="Mother's Name" minlength="3" maxlength="150" required tabindex="2">
					<div class="invalid-feedback">
						Enter Valid Mother's Name.
					</div>
				</div>
			</div>
			<div class="form-row">
				<div class="col-md-6">
					<label for="fname">Father's Name<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="fname" class="form-control" id="fname" placeholder="Father's Name" minlength="3" maxlength="150" required tabindex="3">
					<div class="invalid-feedback">
						Enter Valid Father's Name.
					</div>
				</div>
				<div class="col-md-6">
					<label for="mname">Spouse's Name</label>
					<input type="text" name="sname" class="form-control" id="sname" placeholder="Spouse's Name" minlength="3" maxlength="150" tabindex="4">
					<div class="invalid-feedback">
						Enter Valid Spouse's Name.
					</div>
				</div>
			</div>
			<div class="form-row">
				<div class="col-md-12">
					<label for="emp_add">Employee Address<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="emp_add" class="form-control" minlength="3" maxlength="200" id="emp_add" placeholder="Employee Address" required tabindex="5">
					<div class="invalid-feedback">
						Enter Valid Employee Address.
					</div>
				</div>
			</div>
			<div class="form-row">
				<div class="col-md-6">
					<label for="dob">Date of Birth<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="dob" class="form-control" id="dob" pattern="(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[012])/\d{4}" placeholder="DD/MM/YYYY" minlength="10" maxlength="10" required tabindex="6">
					<div class="invalid-feedback">
						Enter Valid Date of Birth [DD/MM/YYYY].
					</div>
				</div>
				<div class="col-md-6">
				<label for="gender">Gender<span style="color:red; font-weight:bold;">*</span></label>
					<select class="custom-select d-block w-100" name="gender" id="gender" required tabindex="7">
						<option value="">Choose...</option>
						<option value="Male">Male</option>
						<option value="Female">Female</option>
						<option value="Transgender">Transgender</option>
					</select>
					<div class="invalid-feedback">
						Select Valid Gender.
					</div>
				</div>
			</div>
			<div class="form-row">
				<div class="col-md-6">
					<label for="category">Category<span style="color:red; font-weight:bold;">*</span></label>
					<select class="custom-select d-block w-100" id="category" name="category" required tabindex="8">
						<option value="">Choose...</option>
						<option value="General">General</option>
						<option value="EWS">EWS</option>
						<option value="EBC">EBC</option>
						<option value="BC">BC</option>
						<option value="SC">SC</option>
						<option value="ST">ST</option>
					</select>
					<div class="invalid-feedback">
						Select Valid Category.
					</div>
				</div>
				<div class="col-md-6">
					<label for="marital_sts">Marital Status<span style="color:red; font-weight:bold;">*</span></label>
					<select class="custom-select d-block w-100" name="marital_sts" id="marital_sts" required tabindex="9">
						<option value="">Choose...</option>
						<option value="Unmarried">Unmarried</option>
						<option value="Married">Married</option>
						<option value="Widow">Widow</option>
						<option value="Widower">Widower</option>
						<option value="Divorcee">Divorcee</option>
						<option value="Separated">Separated</option>
					</select>
					<div class="invalid-feedback">
						Select Valid Marital Status.
					</div>
				</div>
			</div>
			<div class="form-row">
				<div class="col-md-6">
				<label for="doa">Date of Appointment<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="doa" class="form-control" id="doa" pattern="(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[012])/\d{4}" placeholder="DD/MM/YYYY" minlength="10" maxlength="10" required tabindex="10">
					<div class="invalid-feedback">
						Enter Valid Date of Appointment [DD/MM/YYYY].
					</div>
				</div>
				<div class="col-md-6">
					<label for="designation">Designation<span style="color:red; font-weight:bold;">*</span></label>
					<select class="custom-select d-block w-100" name="designation" id="designation" required tabindex="11">
						<option value="">Choose...</option>
						<option value="Principal">Principal</option>
						<option value="Assistant_Professor">Assistant Professor</option>
						<option value="Associate_Professor">Associate Professor</option>
						<option value="Store_Keeper_HA">Store Keeper/HA</option>
						<option value="Store_Keeper">Store Keeper</option>
						<option value="Head_Assistant">Head Assistant</option>
						<option value="UDC_Accountant">UDC/Accountant</option>
						<option value="Accountant">Accountant</option>
						<option value="UDC">UDC</option>
						<option value="Routine_Clerk">Routine Clerk</option>
						<option value="Assistant">Assistant</option>
						<option value="Assistant_Librarian">Assistant Librarian</option>
						<option value="Demonstrator">Demonstrator</option>
						<option value="Lab_Boy">Lab Boy</option>
						<option value="Peon">Peon</option>
						<option value="Sweeper">Sweeper</option>
						<option value="Orderly">Orderly</option>
						<option value="LDC">LDC</option>
						<option value="Night_Guard">Night Guard</option>
						<option value="Day_Guard">Day Guard</option>
						</select>
					<div class="invalid-feedback">
						Select Valid Designation.
					</div>
				</div>
			</div>
			<div class="form-row">
				<div class="col-md-6">
				<label for="department">Department<span style="color:red; font-weight:bold;">*</span></label>
					<select class="custom-select d-block w-100" name="department" id="department" required tabindex="12">
						<option value="">Choose...</option>
						<option value="NA">Not Applicable</option>
						<option value="Hindi">Hindi</option>
						<option value="English">English</option>
						<option value="Bhojpuri">Bhojpuri</option>
						<option value="Sanskrit">Sanskrit</option>
						<option value="Urdu">Urdu</option>
						<option value="History">History</option>
						<option value="Economics">Economics</option>
						<option value="Philosophy">Philosophy</option>
						<option value="Psychology">Psychology</option>
						<option value="Political_Science">Political Science</option>
						<option value="Physics">Physics</option>
						<option value="Mathematics">Mathematics</option>
						<option value="Chemistry">Chemistry</option>
						<option value="Botany">Botany</option>
						<option value="Zoology">Zoology</option>
					</select>
					<div class="invalid-feedback">
						Select Valid Department.
					</div>	
				</div>
				<div class="col-md-6">
					<label for="grade">Grade<span style="color:red; font-weight:bold;">*</span></label>
					<select class="custom-select d-block w-100" name="grade" id="grade" required tabindex="13">
						<option value="">Choose...</option>
						<option value="NA">Not Applicable</option>
						<option value="Teaching_Staff">Teaching Staff</option>
						<option value="Third_Grade_Staff">Third Grade Staff</option>
						<option value="Fourth_Grade_Staff">Fourth Grade Staff</option>
						</select>
					<div class="invalid-feedback">
						Select Valid Grade.
					</div>
				</div>
			</div>
			<div class="form-row">
				<div class="col-md-6">
				<label for="salary">Basic Pay<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" placeholder="Basic Pay" name="salary" class="form-control" id="salary" minlength="3" maxlength="6" required tabindex="14">
					<div class="invalid-feedback">
						Enter Valid Basic Pay.
					</div>
				</div>
				<div class="col-md-6">
				
				<label for="mob1">Mobile Number<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="mob1" class="form-control" id="mob1" pattern="[6-9]{1}[0-9]{9}" placeholder="Mobile Number" minlength="10" maxlength="10" required tabindex="15">
					<div class="invalid-feedback">
						Enter Valid Mobile Number.
					</div>
				</div>
			</div>
			<div class="form-row">
				<div class="col-md-6">
				<label for="mob2">Alternate Mobile Number</label>
					<input type="text" name="mob2" class="form-control" id="mob2" pattern="[6-9]{1}[0-9]{9}" placeholder="Alternate Mobile Number" minlength="10" maxlength="10" tabindex="16">
					<div class="invalid-feedback">
						Enter Valid Alternate Mobile Number.
					</div>
				</div>
				<div class="col-md-6">
				<label for="email">Email</label>
					<input type="email" placeholder="Email" name="email" class="form-control" id="email" minlength="6" maxlength="150" tabindex="17">
					<div class="invalid-feedback">
						Enter Valid Email Address.
					</div>
				</div>
			</div>
			<br>
			<div class="form-group">
				<div class="form-check">
					<input class="form-check-input" type="checkbox" id="check" required tabindex="18">
					<label class="form-check-label" for="invalidCheck">
					Registering As New Employee.
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
				<button class="btn btn-primary btn-lg col-md-6" id="employee_add" name="employee_add" type="submit" tabindex="19" disabled>Save</button>
			</div>
			<br>
		</form>
	</div>
	<?php include "includes/footer.php";?>
	<script type="text/javascript">
		//First Script
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
		
		//Second Script
			var val = document.getElementById("emp_name");
			var val2 = document.getElementById("mname");
			var val3 = document.getElementById("fname");
			var val4 = document.getElementById("doa");
			var val5 = document.getElementById("dob");
			var val6 = document.getElementById("emp_add");
			var val7 = document.getElementById("designation");
			var val8 = document.getElementById("category");
			var val9 = document.getElementById("marital_sts");
			var val10 = document.getElementById("mob1");
			var val11 = document.getElementById("salary");
			var val12 = document.getElementById("check");
			var val13 = document.getElementById("gender");
			var val14 = document.getElementById("grade");
			var val15 = document.getElementById("department");
				
			val.onchange=val2.onchange=val3.onchange=val4.onchange=val5.onchange=val6.onchange=val7.onchange=val8.onchange=val9.onchange=val10.onchange=val11.onchange=val12.onchange=val13.onchange=val14.onchange=val5.onchange = function () {
			if (val.value ==""||val2.value ==""||val3.value ==""||val4.value ==""||val5.value ==""||val6.value ==""||val7.value ==""||val8.value ==""||val9.value ==""||val10.value ==""||val11.value ==""||val12.checked ==false||val13.value ==""||val14.value ==""||val5.value ==""){
			document.getElementById("employee_add").disabled = true;
			}
			else{ document.getElementById("employee_add").disabled = false;}
			}
	</script>