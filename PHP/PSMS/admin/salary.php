<?php 
	include "includes/session.php";
	include "includes/header.php";
	if(isset($_GET['id']))
	{
	$check=0;
	$id=$_GET['id'];
	$id=mysqli_real_escape_string($conn,$id);
	$id=test_input($id);
	
	if(isset($_POST['view_salary']))
	{
		$fyear=$_POST['fyear'];
		$fyear=mysqli_real_escape_string($conn,$fyear);
		$fyear=test_input($fyear);

		$smonth=$_POST['smonth'];
		$smonth=mysqli_real_escape_string($conn,$smonth);
		$smonth=test_input($smonth);
		
		$sql = "SELECT * FROM employee WHERE id = $id";
		$result = mysqli_query($conn,$sql);
		$row = mysqli_fetch_assoc($result);
	
		$sql2 = "SELECT * FROM allowance WHERE eid = $id AND smonth='$smonth' AND fyear=$fyear";
		$result2 = mysqli_query($conn,$sql2);
		$row2 = mysqli_fetch_assoc($result2);
	
		$sql3 = "SELECT * FROM clg_details WHERE id = 1";
		$result3 = mysqli_query($conn,$sql3);
		$row3 = mysqli_fetch_assoc($result3);

		$check=1;
	}
?>
<style>
	@media print {
  		#hide, #allowance_edit, #print_profile{
    	display: none;
		}
}
</style>
</head>
<body class="d-flex flex-column h-100">
	<?php include "includes/navbar.php";?>
	<br>
	<br>
	<div>
		<h3 align="center">Salary Slip</h3>
	</div>
	<br>
	<div class="container" style="width:80%;">
	
	<!--Start Section To Be Hidden During Print-->
	<section id="hide">
		<b>
			<p align="center" class="alert alert-info">Select Month And Fill Year To Generate Salary Slip And Then Click View.</p>
		</b>
		<br>
		
		<form action="" method="POST" class="needs-validation" novalidate enctype="multipart/form-data" autocomplete="off" id="generate">
		<div class="form-row">
		<div class="col-md-4">
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
				<div class="col-md-4">
					<label for="fyear">Financial Year<span style="color:red; font-weight:bold;">*</span></label>
					<input type="text" name="fyear" class="form-control" id="fyear" placeholder="Financial Year" minlength="4" maxlength="4" required tabindex="2">
					<div class="invalid-feedback">
						Enter Valid Value For Year.
					</div>
				</div>
				<div class="col-md-1">
				</div>
				<div class="col-md-3">
				<br>
				<button class="btn btn-primary btn-lg col-md-12" id="view_salary" name="view_salary" type="submit" tabindex="3" disabled>View</button>
				</div>
			</div>
			<br>
		</form>
	</section>
	<!--End Section To Be Hidden During Print-->
	
<br><br><br>
<!--Salary Slip Area Start-->
<?php if (!empty($row) && !empty($row2) && !empty($row3)) { ?>
<section id="show">
<table class="table responsive table-bordered" width="100%">
<tr>
  <th style="width: 25%" class="text-center"><img src="../register/images/<?php echo $row3['logo'];?>" alt="" width="80" height="80"></th>
  <th colspan="2" style="width: 50%" class="text-center align-middle"><?php echo $row3['clg_name'];?><br><?php echo $row3['clg_add'];?></th>
  <th style="width: 25%" class="text-center align-middle"><?php echo $row2['smonth'];?><br><?php echo $row2['fyear'];?></th>
</tr>

<tbody>
	<tr>
	<th>Employee Name</th>
	<td><?php echo $row['emp_name'];?></td>
	<th>Grade</th>
    <td><?php echo $row['grade'];?></td>
    </tr>
	<tr>
	<th>Department</th>
	<td><?php echo $row['department'];?></td>
	<th>Designation</th>
    <td><?php echo $row['designation'];?></td>
    </tr>
	<tr>
	<th>Appointment Date</th>
	<td><?php echo $row['doa'];?></td>
	<th>Date Of Birth</th>
    <td><?php echo $row['dob'];?></td>
    </tr>
    <tr bgcolor="#f0f0fc">
	<th colspan="2" class="text-center">Earnings</th>
	<th colspan="2" class="text-center">Deductions</th>
    </tr>
	<tr>
	<th>Basic</th>
	<td><?php echo $row2['actual'];?></td>
	<th>PF</th>
    <td><?php echo $row2['pf'];?></td>
    </tr>
	<tr>
	<th>DA</th>
	<td><?php echo $row2['da'];?></td>
	<th>PF Adv.</th>
    <td><?php echo $row2['pfadv'];?></td>
    </tr>
	<tr>
	<th>HRA</th>
	<td><?php echo $row2['hra'];?></td>
	<th>Sal. Adv.</th>
    <td><?php echo $row2['sal_adv'];?></td>
    </tr>
	<tr>
	<th>Medical</th>
	<td><?php echo $row2['med'];?></td>
	<th>IT</th>
    <td><?php echo $row2['it'];?></td>
    </tr>
	<tr>
	<th>WA</th>
	<td><?php echo $row2['wa'];?></td>
	<th>Q.Rent</th>
    <td><?php echo $row2['qrent'];?></td>
    </tr>
	<tr>
	<th>Other #1</th>
	<td><?php echo $row2['other1'];?></td>
	<th>Rev.Adv.</th>
    <td><?php echo $row2['rev_adv'];?></td>
    </tr>
	<tr>
	<th></th>
	<td></td>
	<th>Rev.Asso.</th>
    <td><?php echo $row2['rev_asso'];?></td>
    </tr>
	<tr>
	<th></th>
	<td></td>
	<th>WF</th>
    <td><?php echo $row2['wf'];?></td>
    </tr>
	<tr>
	<th></th>
	<td></td>
	<th>LIC</th>
    <td><?php echo $row2['lic'];?></td>
    </tr>
	<tr>
	<th></th>
	<td></td>
	<th>Marriage/Medical</th>
    <td><?php echo $row2['marriage_med'];?></td>
    </tr>
	<tr>
	<th></th>
	<td></td>
	<th>HT</th>
    <td><?php echo $row2['ht'];?></td>
    </tr>
	<tr>
	<th></th>
	<td></td>
	<th>F.Adv.</th>
    <td><?php echo $row2['fadv'];?></td>
    </tr>
	<tr>
	<th></th>
	<td></td>
	<th>Other #1</th>
    <td><?php echo $row2['fadv'];?></td>
    </tr>
	<tr>
	<th></th>
	<td></td>
	<th>Other #2</th>
    <td><?php echo $row2['other3'];?></td>
    </tr>
	<tr>
	<th>Total Earnings</th>
	<td><?php echo $row2['net1'];?></td>
	<th>Total Deductions</th>
    <td><?php echo $row2['dtotal'];?></td>
    </tr>
	<tr bgcolor="#f0f0fc">
	<td colspan="2"></td>
    <th>Net Salary</th>
	<td><?php echo $row2['net2'];?></td>
	</tr>
</tbody>
</table>
<hr class="mb-4">
		<div class="form-row">
			<a href="allowance?id=<?php echo $row2['eid'];?>" class="btn btn-danger btn-lg col-md-6" name="allowance_edit" id="allowance_edit" name="allowance_edit">Edit Allowance</a>
			<button class="btn btn-primary btn-lg col-md-6" id="print_profile" name="print_profile" onclick="window.print();">Print</button>
		</div>
</section>
<?php }
else if($check==1)
{
echo"<b>
<p align='center' class='alert alert-danger'>Some Data Missing! Update All First</p>
</b>";
}
else
{

}?>
<!--Salary Slip Area End-->

</div>
<br>
<br>
<br>

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
			var val = document.getElementById("fyear");
			var val2 = document.getElementById("smonth");
			
			val.onchange=val2.onchange = function () {
			if (val.value ==""||val2.value ==""){
			document.getElementById("view_salary").disabled = true;
			}
			else{ document.getElementById("view_salary").disabled = false;}
			}
	</script>