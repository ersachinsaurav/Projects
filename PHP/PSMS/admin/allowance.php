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

	$sql2 = "SELECT * FROM allowance WHERE eid = $id";
	$result2 = mysqli_query($conn,$sql2);
	$row2 = mysqli_fetch_assoc($result2);
?>
</head>
<body class="d-flex flex-column h-100">
	<?php include "includes/navbar.php";?>
	<br>
	<br>
	<div>
		<h3 align="center">Manage Allowance</h3>
	</div>
	<br>
	<br>
	<div class="container" style="width:80%;">
	<b>
			<p align="center" class="alert alert-info">Enter 0 (Zero) In The Respective Field Where Value Is Not Applicable.</p>
		</b>
		<br>
		
		<form action="allowance_submit?id=<?php echo $row[id];?>" method="POST" class="needs-validation" novalidate enctype="multipart/form-data" autocomplete="off">
		<div class="form-row">
				<div class="col-md-3">
				<label for="emp_name">Employee Name<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="emp_name" class="form-control" minlength="3" maxlength="150" id="emp_name" placeholder="Employee Name" tabindex="0" value="<?php echo $row['emp_name'];?>" readonly>
				</div>
				<div class="col-md-3">
				<label for="grade">Grade<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" placeholder="Grade" name="grade" class="form-control" id="grade" minlength="3" maxlength="6" tabindex="0" value="<?php echo $row['grade'];?>" readonly>
				</div>
				<div class="col-md-3">
				<label for="designation">Designation<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" placeholder="Designation" name="designation" class="form-control" id="designation" minlength="3" maxlength="6" tabindex="0" value="<?php echo $row['designation'];?>" readonly>
				</div>
				<div class="col-md-3">
				<label for="salary">Basic Pay<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" placeholder="Basic Pay" name="salary" class="form-control" id="salary" minlength="3" maxlength="6" tabindex="0" value="<?php echo $row['salary'];?>" readonly>
				</div>
			</div>
		<div class="form-row">
			<div class="col-md-3">
			<label for="smonth">Month<span style="color:red; font-weight:bold;">*</span></label>
					<select class="custom-select d-block w-100" name="smonth" id="smonth" required tabindex="1" autofocus>
						<option value="">Choose...</option>
						<option value="January">January</option>
						<option value="February">February</option>
						<option value="March">March</option>
						<option value="April">April</option>
						<option value="May">May</option>
						<option value="June">June</option>
						<option value="July">July</option>
						<option value="August">August</option>
						<option value="September">September</option>
						<option value="October">October</option>
						<option value="November">November</option>
						<option value="December">December</option>
					</select>
					<div class="invalid-feedback">
						Select Valid Month Of Salary.
					</div>				
			</div>
				<div class="col-md-3">
					<label for="fyear">Financial Year<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="fyear" class="form-control" id="fyear" placeholder="Financial Year" minlength="4" maxlength="4" required tabindex="2">
					<div class="invalid-feedback">
						Enter Valid Value For Year.
					</div>
				</div>
				<div class="col-md-3">
					<label for="da">DA (%)<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="da" class="form-control" minlength="1" maxlength="6" id="da" placeholder="Dearness Allowance" required tabindex="3" value="<?php echo $row2['da'];?>" autofocus>
					<div class="invalid-feedback">
						Enter Valid Value For DA (%).
					</div>
				</div>
				<div class="col-md-3">
					<label for="hra">HRA (%)<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="hra" class="form-control" id="hra" placeholder="House Rent Allowance" minlength="1" maxlength="6" required tabindex="4" value="<?php echo $row2['hra'];?>">
					<div class="invalid-feedback">
						Enter Valid Value For HRA (%).
					</div>
				</div>
			</div>
			<div class="form-row">
				<div class="col-md-3">
					<label for="agp">AGP<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="agp" class="form-control" minlength="1" maxlength="6" id="agp" placeholder="Academic Grade Pay" required tabindex="5" value="<?php echo $row2['agp'];?>">
					<div class="invalid-feedback">
						Enter Valid Value For AGP.
					</div>
				</div>
				<div class="col-md-3">
					<label for="med">Medical Allowance<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="med" class="form-control" id="med" placeholder="Medical Allowance" minlength="1" maxlength="6" required tabindex="6" value="<?php echo $row2['med'];?>">
					<div class="invalid-feedback">
						Enter Valid Value For Medical Allowance.
					</div>
				</div>
				<div class="col-md-3">
					<label for="other1">Other #1 (Added With Salary)<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="other1" class="form-control" id="other1" placeholder="Any Other Allowance" minlength="1" maxlength="6" required tabindex="7" value="<?php echo $row2['other1'];?>">
					<div class="invalid-feedback">
						Enter Valid Value For Other #1 Allowance.
					</div>
				</div>
				<div class="col-md-3">
					<label for="wf">Welfare Allowance<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="wf" class="form-control" id="wf" placeholder="Welfare Allowance" minlength="1" maxlength="6" required tabindex="8" value="<?php echo $row2['wf'];?>">
					<div class="invalid-feedback">
						Enter Valid Value For WF.
					</div>
				</div>
			</div>
			<div class="form-row">
				<div class="col-md-3">
				<label for="pf">PF (%)<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="pf" class="form-control" id="pf" placeholder="Provident Fund" minlength="1" maxlength="6" required tabindex="9" value="<?php echo $row2['pf'];?>">
					<div class="invalid-feedback">
						Enter Valid Value For PF (%).
					</div>
				</div>
				<div class="col-md-3">
				<label for="pfadv">PF Advance<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="pfadv" class="form-control" minlength="1" maxlength="6" id="pfadv" placeholder="PF Advance" required tabindex="9" value="<?php echo $row2['pfadv'];?>">
					<div class="invalid-feedback">
						Enter Valid Value For PF Advance.
					</div>
				</div>
				<div class="col-md-3">
					<label for="it">Income Tax<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="it" class="form-control" id="it" placeholder="Income Tax" minlength="1" maxlength="6" required tabindex="10" value="<?php echo $row2['it'];?>">
					<div class="invalid-feedback">
						Enter Valid Value For Income Tax.
					</div>
				</div>
				<div class="col-md-3">
				<label for="lic">LIC<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="lic" class="form-control" id="lic" placeholder="LIC" minlength="1" maxlength="6" required tabindex="11" value="<?php echo $row2['lic'];?>">
					<div class="invalid-feedback">
						Enter Valid Value For LIC.
					</div>
				</div>
			</div>
			<div class="form-row">
				<div class="col-md-3">
					<label for="wa">Washing Allowance<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="wa" class="form-control" minlength="1" maxlength="6" id="wa" placeholder="Washing Allowance" required tabindex="13" value="<?php echo $row2['wa'];?>">
					<div class="invalid-feedback">
						Enter Valid Value For Washing Allowance.
					</div>
				</div>
				<div class="col-md-3">
					<label for="fadv">F.Adv<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="fadv" class="form-control" id="fadv" placeholder="F.Adv" minlength="1" maxlength="6" required tabindex="14" value="<?php echo $row2['fadv'];?>">
					<div class="invalid-feedback">
						Enter Valid Value For F.Adv.
					</div>
				</div>
				<div class="col-md-3">
					<label for="ht">H.T.<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="ht" class="form-control" id="ht" placeholder="H.T." minlength="1" maxlength="6" required tabindex="15" value="<?php echo $row2['ht'];?>">
					<div class="invalid-feedback">
						Enter Valid Value For H.T.
					</div>
				</div>
				<div class="col-md-3">
					<label for="marriage_med">Marriage/Medical<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="marriage_med" class="form-control" id="marriage_med" placeholder="Marriage/Medical" minlength="1" maxlength="6" required tabindex="16" value="<?php echo $row2['marriage_med'];?>">
					<div class="invalid-feedback">
						Enter Valid Value For Marriage/Medical.
					</div>
				</div>
			</div>
			<div class="form-row">
				<div class="col-md-3">
					<label for="sal_adv">Salary Advance<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="sal_adv" class="form-control" minlength="1" maxlength="6" id="sal_adv" placeholder="Salary Advance" required tabindex="17" value="<?php echo $row2['sal_adv'];?>">
					<div class="invalid-feedback">
						Enter Valid Value For Salary Advance.
					</div>
				</div>
				<div class="col-md-3">
					<label for="rev_asso">Rev. Asso.<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="rev_asso" class="form-control" id="rev_asso" placeholder="Rev. Asso." minlength="1" maxlength="6" required tabindex="18" value="<?php echo $row2['rev_asso'];?>">
					<div class="invalid-feedback">
						Enter Valid Value For Rev. Asso.
					</div>
				</div>
				<div class="col-md-3">
					<label for="rev_adv">Rev. Adv.<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="rev_adv" class="form-control" id="rev_adv" placeholder="Rev. Adv." minlength="1" maxlength="6" required tabindex="19" value="<?php echo $row2['rev_adv'];?>">
					<div class="invalid-feedback">
						Enter Valid Value For Rev. Adv.
					</div>
				</div>
				<div class="col-md-3">
				<label for="qrent">Q.Rent<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="qrent" class="form-control" id="qrent" placeholder="Q Rent" minlength="1" maxlength="6" required tabindex="20" value="<?php echo $row2['qrent'];?>">
					<div class="invalid-feedback">
						Enter Valid Value For Q.Rent.
					</div>
				</div>
			</div>
			<div class="form-row">
			<div class="col-md-3">
				<label for="other2">Other #2 (Deduction)<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="other2" class="form-control" id="other2" placeholder="Other #2" minlength="1" maxlength="6" required tabindex="20" value="<?php echo $row2['other2'];?>">
					<div class="invalid-feedback">
						Enter Valid Value For Other #2.
					</div>
				</div>
				<div class="col-md-3">
				<label for="other3">Other #3 (Deduction)<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="other3" class="form-control" id="other3" placeholder="Other #3" minlength="1" maxlength="6" required tabindex="21" value="<?php echo $row2['other3'];?>">
					<div class="invalid-feedback">
						Enter Valid Value For Other #3.
					</div>
				</div>
				<div class="col-md-3">
				<label for="remarks1">Remarks #1</label>
					<input type="text" name="remarks1" class="form-control" id="remarks1" placeholder="Remarks #1" minlength="2" maxlength="100" tabindex="21" value="<?php echo $row2['remarks1'];?>">
					<div class="invalid-feedback">
						Enter Valid Text For Remarks #1.
					</div>
				</div>
				<div class="col-md-3">
				<label for="remarks2">Remarks #2</label>
					<input type="text" name="remarks2" class="form-control" id="remarks2" placeholder="Remarks #2" minlength="2" maxlength="100" tabindex="21" value="<?php echo $row2['remarks2'];?>">
					<div class="invalid-feedback">
						Enter Valid Text For Remarks #2.
					</div>
				</div>
			</div>
			<br>
			<div class="form-group">
				<div class="form-check">
					<input class="form-check-input" type="checkbox" id="check" required tabindex="22">
					<label class="form-check-label" for="invalidCheck">
					Updating Allowance Details.
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
				<button class="btn btn-primary btn-lg col-md-6" id="allowance_update" name="allowance_update" type="submit" tabindex="23" disabled>Save</button>
			</div>
			<br>
		</form>
	</div>
	<?php include "includes/footer.php";
	}
	else
		{
			header("Location:category");
		}
	?>
	
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
			var val = document.getElementById("da");
			var val2 = document.getElementById("pf");
			var val3 = document.getElementById("hra");
			var val4 = document.getElementById("check");
			var val5 = document.getElementById("fyear");
			var val6 = document.getElementById("agp");
			var val7 = document.getElementById("med");
			var val8 = document.getElementById("other1");
			var val9 = document.getElementById("wf");
			var val10 = document.getElementById("pfadv");
			var val11 = document.getElementById("lic");
			var val12 = document.getElementById("it");
			var val13 = document.getElementById("qrent");
			var val14 = document.getElementById("wa");
			var val15 = document.getElementById("fadv");
			var val16 = document.getElementById("ht");
			var val17 = document.getElementById("marriage_med");
			var val18 = document.getElementById("sal_adv");
			var val19 = document.getElementById("rev_asso");
			var val20 = document.getElementById("other2");
			var val21 = document.getElementById("other3");
			var val22 = document.getElementById("rev_adv");
			var val23 = document.getElementById("smonth");
			
			val.onchange=val2.onchange=val3.onchange=val4.onchange=val5.onchange=val6.onchange=val7.onchange=val8.onchange=val9.onchange=val10.onchange=val11.onchange=val12.onchange=val13.onchange=val14.onchange=val15.onchange=val16.onchange=val17.onchange=val18.onchange=val19.onchange=val20.onchange=val21.onchange=val22.onchange=val23.onchange = function () {
			if (val.value ==""||val2.value ==""||val3.value ==""||val5.value ==""||val4.checked == false||val6.value ==""||val7.value ==""||val8.value ==""||val9.value ==""||val10.value ==""||val11.value ==""||val12.value ==""||val13.value ==""||val14.value ==""||val15.value ==""||val16.value ==""||val17.value ==""||val18.value ==""||val19.value ==""||val20.value ==""||val21.value ==""||val22.value ==""||val23.value ==""){
			document.getElementById("allowance_update").disabled = true;
			}
			else{ document.getElementById("allowance_update").disabled = false;}
			}
	</script>