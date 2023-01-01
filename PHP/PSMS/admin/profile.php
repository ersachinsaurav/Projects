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
	
	$sql2 = "SELECT * FROM clg_details WHERE id = 1";
	$result2 = mysqli_query($conn,$sql2);
	$row2 = mysqli_fetch_assoc($result2);
	?>

	<style>
	@media print {
  		#edit, #print_profile {
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
		<h3 align="center">Employee Profile</h3>
	</div>
	<br>
	<br>
<div class="container" style="width:80%;">

<!-- Profile Start-->

<table class="table responsive" width="100%">
<tr>
  <th style="width: 30%">Name</th>
  <th style="width: 50%"><?php echo $row['emp_name'];?></th>
  <th style="width: 20%"></th>
</tr>

<tbody>
    <tr>
      <th scope="row">Father's Name</th>
      <td><?php echo $row['fname'];?></td>
      <td rowspan="4" align="center"><img src="images/<?php echo $row['id'];?>/<?php echo $row['emp_photo'];?>" class="img-responsive imgsize" id="emp_photo" /></td>
    </tr>
    <tr>
      <th scope="row">Mother's Name</th>
      <td><?php echo $row['mname'];?></td>
      </tr>
    <tr>
      <th scope="row">Spouse's Name</th>
      <td><?php echo $row['sname'];?></td>
      </tr>
	  <tr>
      <th scope="row">Gender</th>
      <td><?php echo $row['gender'];?></td>
      </tr>
	  <tr>
      <th scope="row">Date Of Birth</th>
      <td colspan="2"><?php echo $row['dob'];?></td>
      </tr>
	  <tr>
      <th scope="row">Category</th>
      <td colspan="2"><?php echo $row['category'];?></td>
      </tr>
	  <tr>
      <th scope="row">Marital Status</th>
      <td colspan="2"><?php echo $row['marital_sts'];?></td>
      </tr>
	  <tr>
      <th scope="row">Mobile #1</th>
      <td colspan="2"><?php echo $row['mob1'];?></td>
      </tr>
	  <tr>
      <th scope="row">Mobile #2</th>
      <td colspan="2"><?php echo $row['mob2'];?></td>
      </tr>
	  <tr>
      <th scope="row">Email</th>
      <td colspan="2"><?php echo $row['email'];?></td>
      </tr>
	  <tr>
      <th scope="row">Address</th>
      <td colspan="2"><?php echo $row['emp_add'];?></td>
      </tr>
	  <tr>
      <th scope="row">Date Of Appointment</th>
      <td colspan="2"><?php echo $row['doa'];?></td>
      </tr>
	  <tr>
      <th scope="row">Department</th>
      <td colspan="2"><?php echo $row['department'];?></td>
      </tr>
	  <tr>
      <th scope="row">Grade</th>
      <td colspan="2"><?php echo $row['grade'];?></td>
      </tr>
	  <tr>
      <th scope="row">Designation</th>
      <td colspan="2"><?php echo $row['designation'];?></td>
      </tr>
	  <tr>
	  <th scope="row">Employing Institution</th>
      <td colspan="2"><?php echo $row2['clg_name'];?>, <?php echo $row2['clg_add'];?></td>
      </tr>
	  <tr>
	  <th scope="row">Institution's Head</th>
      <td colspan="2"><?php echo $row2['principal'];?></td>
      </tr>
	  </tbody>
</table>

<!-- Profile End-->

		<hr class="mb-4">
		<div class="form-row">
			<a href="edit?id=<?php echo $row['id'];?>" class="btn btn-danger btn-lg col-md-6" name="edit" id="edit" name="edit">Edit</a>
			<button class="btn btn-primary btn-lg col-md-6" id="print_profile" name="print_profile" onclick="window.print();">Print</button>
		</div>
		<br>
</div>
	<?php include "includes/footer.php";
		}
		else
			{
				header("Location:category");
			}?>