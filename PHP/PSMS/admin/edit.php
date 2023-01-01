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
	<br>
	<br>
	<div>
		<h3 align="center">Edit Employee</h3>
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
		<form action="edit_submit?id=<?php echo $row['id'];?>" method="POST" class="needs-validation" novalidate enctype="multipart/form-data" autocomplete="off">
			<div class="form-row">
				<div class="col-md-6">
					<label for="emp_name">Employee Name<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="emp_name" class="form-control" minlength="3" maxlength="150" id="emp_name" placeholder="Employee Name" required tabindex="1" value="<?php echo $row['emp_name'];?>">
					<div class="invalid-feedback">
						Enter Valid Employee Name.
					</div>
				</div>
				<div class="col-md-6">
					<label for="mname">Mother's Name<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="mname" class="form-control" id="mname" placeholder="Mother's Name" minlength="3" maxlength="150" required tabindex="2" value="<?php echo $row['mname'];?>">
					<div class="invalid-feedback">
						Enter Valid Mother's Name.
					</div>
				</div>
			</div>
			<div class="form-row">
				<div class="col-md-6">
					<label for="fname">Father's Name<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="fname" class="form-control" id="fname" placeholder="Father's Name" minlength="3" maxlength="150" required tabindex="3" value="<?php echo $row['fname'];?>">
					<div class="invalid-feedback">
						Enter Valid Father's Name.
					</div>
				</div>
				<div class="col-md-6">
					<label for="mname">Spouse's Name</label>
					<input type="text" name="sname" class="form-control" id="sname" placeholder="Spouse's Name" minlength="3" maxlength="150" tabindex="4" value="<?php echo $row['sname'];?>">
					<div class="invalid-feedback">
						Enter Valid Spouse's Name.
					</div>
				</div>
			</div>
			<div class="form-row">
				<div class="col-md-12">
					<label for="emp_add">Employee Address<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="emp_add" class="form-control" minlength="3" maxlength="200" id="emp_add" placeholder="Employee Address" required tabindex="5" value="<?php echo $row['emp_add'];?>">
					<div class="invalid-feedback">
						Enter Valid Employee Address.
					</div>
				</div>
			</div>
			<div class="form-row">
				<div class="col-md-6">
					<label for="dob">Date of Birth<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="dob" class="form-control" id="dob" pattern="(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[012])/\d{4}" placeholder="DD/MM/YYYY" minlength="10" maxlength="10" required tabindex="6" value="<?php echo $row['dob'];?>">
					<div class="invalid-feedback">
						Enter Valid Date of Birth [DD/MM/YYYY].
					</div>
				</div>
				<div class="col-md-6">
				<label for="gender">Gender<span style="color:red; font-weight:bold;">*</span></label>
					<select class="custom-select d-block w-100" name="gender" id="gender" required tabindex="7">
						<option value="">Choose...</option>
						<option value="Male" <?php if ($row['gender'] == 'Male') { echo 'selected'; } ?>>Male</option>
						<option value="Female" <?php if ($row['gender'] == 'Female') { echo 'selected'; } ?>>Female</option>
						<option value="Transgender" <?php if ($row['gender'] == 'Transgender') { echo 'selected'; } ?>>Transgender</option>
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
						<option value="General" <?php if ($row['category'] == 'General') { echo 'selected'; } ?>>General</option>
						<option value="EWS" <?php if ($row['category'] == 'EWS') { echo 'selected'; } ?>>EWS</option>
						<option value="EBC" <?php if ($row['category'] == 'EBC') { echo 'selected'; } ?>>EBC</option>
						<option value="BC" <?php if ($row['category'] == 'BC') { echo 'selected'; } ?>>BC</option>
						<option value="SC" <?php if ($row['category'] == 'SC') { echo 'selected'; } ?>>SC</option>
						<option value="ST" <?php if ($row['category'] == 'ST') { echo 'selected'; } ?>>ST</option>
					</select>
					<div class="invalid-feedback">
						Select Valid Category.
					</div>
				</div>
				<div class="col-md-6">
					<label for="marital_sts">Marital Status<span style="color:red; font-weight:bold;">*</span></label>
					<select class="custom-select d-block w-100" name="marital_sts" id="marital_sts" required tabindex="9">
						<option value="">Choose...</option>
						<option value="Unmarried" <?php if ($row['marital_sts'] == 'Unmarried') { echo 'selected'; } ?>>Unmarried</option>
						<option value="Married" <?php if ($row['marital_sts'] == 'Married') { echo 'selected'; } ?>>Married</option>
						<option value="Widow" <?php if ($row['marital_sts'] == 'Widow') { echo 'selected'; } ?>>Widow</option>
						<option value="Widower" <?php if ($row['marital_sts'] == 'Widower') { echo 'selected'; } ?>>Widower</option>
						<option value="Divorcee" <?php if ($row['marital_sts'] == 'Divorcee') { echo 'selected'; } ?>>Divorcee</option>
						<option value="Separated" <?php if ($row['marital_sts'] == 'Separated') { echo 'selected'; } ?>>Separated</option>
					</select>
					<div class="invalid-feedback">
						Select Valid Marital Status.
					</div>
				</div>
			</div>
			<div class="form-row">
				<div class="col-md-6">
				<label for="doa">Date of Appointment<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="doa" class="form-control" id="doa" pattern="(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[012])/\d{4}" placeholder="DD/MM/YYYY" minlength="10" maxlength="10" required tabindex="10" value="<?php echo $row['doa'];?>">
					<div class="invalid-feedback">
						Enter Valid Date of Appointment [DD/MM/YYYY].
					</div>
				</div>
				<div class="col-md-6">
					<label for="designation">Designation<span style="color:red; font-weight:bold;">*</span></label>
					<select class="custom-select d-block w-100" name="designation" id="designation" required tabindex="11">
						<option value="">Choose...</option>
						<option value="Principal" <?php if ($row['designation'] == 'Principal') { echo 'selected'; } ?>>Principal</option>
						<option value="Assistant_Professor" <?php if ($row['designation'] == 'Assistant_Professor') { echo 'selected'; } ?>>Assistant Professor</option>
						<option value="Associate_Professor" <?php if ($row['designation'] == 'Associate_Professor') { echo 'selected'; } ?>>Associate Professor</option>
						<option value="Store_Keeper_HA" <?php if ($row['designation'] == 'Store_Keeper_HA') { echo 'selected'; } ?>>Store Keeper/HA</option>
						<option value="Store_Keeper" <?php if ($row['designation'] == 'Store_Keeper') { echo 'selected'; } ?>>Store Keeper</option>
						<option value="Head_Assistant" <?php if ($row['designation'] == 'Head_Assistant') { echo 'selected'; } ?>>Head Assistant</option>
						<option value="UDC_Accountant" <?php if ($row['designation'] == 'UDC_Accountant') { echo 'selected'; } ?>>UDC/Accountant</option>
						<option value="Accountant" <?php if ($row['designation'] == 'Accountant') { echo 'selected'; } ?>>Accountant</option>
						<option value="UDC" <?php if ($row['designation'] == 'UDC') { echo 'selected'; } ?>>UDC</option>
						<option value="Routine_Clerk" <?php if ($row['designation'] == 'Routine_Clerk') { echo 'selected'; } ?>>Routine Clerk</option>
						<option value="Assistant" <?php if ($row['designation'] == 'Assistant') { echo 'selected'; } ?>>Assistant</option>
						<option value="Assistant_Librarian" <?php if ($row['designation'] == 'Assistant_Librarian') { echo 'selected'; } ?>>Assistant Librarian</option>
						<option value="Demonstrator" <?php if ($row['designation'] == 'Demonstrator') { echo 'selected'; } ?>>Demonstrator</option>
						<option value="Lab_Boy" <?php if ($row['designation'] == 'Lab_Boy') { echo 'selected'; } ?>>Lab Boy</option>
						<option value="Peon" <?php if ($row['designation'] == 'Peon') { echo 'selected'; } ?>>Peon</option>
						<option value="Sweeper" <?php if ($row['designation'] == 'Sweeper') { echo 'selected'; } ?>>Sweeper</option>
						<option value="Orderly" <?php if ($row['designation'] == 'Orderly') { echo 'selected'; } ?>>Orderly</option>
						<option value="LDC" <?php if ($row['designation'] == 'LDC') { echo 'selected'; } ?>>LDC</option>
						<option value="Night_Guard" <?php if ($row['designation'] == 'Night_Guard') { echo 'selected'; } ?>>Night Guard</option>
						<option value="Day_Guard" <?php if ($row['designation'] == 'Day_Guard') { echo 'selected'; } ?>>Day Guard</option>
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
						<option value="NA" <?php if ($row['department'] == 'NA') { echo 'selected'; } ?>>Not Applicable</option>
						<option value="Hindi" <?php if ($row['department'] == 'Hindi') { echo 'selected'; } ?>>Hindi</option>
						<option value="English" <?php if ($row['department'] == 'English') { echo 'selected'; } ?>>English</option>
						<option value="Bhojpuri" <?php if ($row['department'] == 'Bhojpuri') { echo 'selected'; } ?>>Bhojpuri</option>
						<option value="Sanskrit" <?php if ($row['department'] == 'Sanskrit') { echo 'selected'; } ?>>Sanskrit</option>
						<option value="Urdu" <?php if ($row['department'] == 'Urdu') { echo 'selected'; } ?>>Urdu</option>
						<option value="History" <?php if ($row['department'] == 'History') { echo 'selected'; } ?>>History</option>
						<option value="Economics" <?php if ($row['department'] == 'Economics') { echo 'selected'; } ?>>Economics</option>
						<option value="Philosophy" <?php if ($row['department'] == 'Philosophy') { echo 'selected'; } ?>>Philosophy</option>
						<option value="Psychology" <?php if ($row['department'] == 'Psychology') { echo 'selected'; } ?>>Psychology</option>
						<option value="Political_Science" <?php if ($row['department'] == 'Political_Science') { echo 'selected'; } ?>>Political Science</option>
						<option value="Physics" <?php if ($row['department'] == 'Physics') { echo 'selected'; } ?>>Physics</option>
						<option value="Mathematics" <?php if ($row['department'] == 'Mathematics') { echo 'selected'; } ?>>Mathematics</option>
						<option value="Chemistry" <?php if ($row['department'] == 'Chemistry') { echo 'selected'; } ?>>Chemistry</option>
						<option value="Botany" <?php if ($row['department'] == 'Botany') { echo 'selected'; } ?>>Botany</option>
						<option value="Zoology" <?php if ($row['department'] == 'Zoology') { echo 'selected'; } ?>>Zoology</option>
					</select>
					<div class="invalid-feedback">
						Select Valid Department.
					</div>	
				</div>
				<div class="col-md-6">
					<label for="grade">Grade<span style="color:red; font-weight:bold;">*</span></label>
					<select class="custom-select d-block w-100" name="grade" id="grade" required tabindex="13">
						<option value="">Choose...</option>
						<option value="NA" <?php if ($row['grade'] == 'NA') { echo 'selected'; } ?>>Not Applicable</option>
						<option value="Teaching_Staff" <?php if ($row['grade'] == 'Teaching_Staff') { echo 'selected'; } ?>>Teaching Staff</option>
						<option value="Third_Grade_Staff" <?php if ($row['grade'] == 'Third_Grade_Staff') { echo 'selected'; } ?>>Third Grade Staff</option>
						<option value="Fourth_Grade_Staff" <?php if ($row['grade'] == 'Fourth_Grade_Staff') { echo 'selected'; } ?>>Fourth Grade Staff</option>
						</select>
					<div class="invalid-feedback">
						Select Valid Grade.
					</div>
				</div>
			</div>
			<div class="form-row">
				<div class="col-md-6">
				<label for="salary">Basic Pay<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" placeholder="Basic Pay" name="salary" class="form-control" id="salary" minlength="3" maxlength="6" required tabindex="14" value="<?php echo $row['salary'];?>">
					<div class="invalid-feedback">
						Enter Valid Basic Pay.
					</div>
				</div>
				<div class="col-md-6">
				
				<label for="mob1">Mobile Number<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="mob1" class="form-control" id="mob1" pattern="[6-9]{1}[0-9]{9}" placeholder="Mobile Number" minlength="10" maxlength="10" required tabindex="15" value="<?php echo $row['mob1'];?>">
					<div class="invalid-feedback">
						Enter Valid Mobile Number.
					</div>
				</div>
			</div>
			<div class="form-row">
				<div class="col-md-6">
				<label for="mob2">Alternate Mobile Number</label>
					<input type="text" name="mob2" class="form-control" id="mob2" pattern="[6-9]{1}[0-9]{9}" placeholder="Alternate Mobile Number" minlength="10" maxlength="10" tabindex="16" value="<?php echo $row['mob2'];?>">
					<div class="invalid-feedback">
						Enter Valid Alternate Mobile Number.
					</div>
				</div>
				<div class="col-md-6">
				<label for="email">Email</label>
					<input type="email" placeholder="Email" name="email" class="form-control" id="email" minlength="6" maxlength="150" tabindex="17" value="<?php echo $row['email'];?>">
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
					Updating Employee Details.
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
				<button class="btn btn-primary btn-lg col-md-6" id="employee_edit" name="employee_edit" type="submit" tabindex="19" disabled>Save</button>
			</div>
			<br>
		</form>
	</div>
	<?php include "includes/footer.php";
	}
	else
		{
			header("Location:category");
		}?>
	
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
			document.getElementById("employee_edit").disabled = true;
			}
			else{ document.getElementById("employee_edit").disabled = false;}
			}
	</script>