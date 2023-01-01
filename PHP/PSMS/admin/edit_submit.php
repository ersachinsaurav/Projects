<?php
include "includes/config.php";
include "includes/session.php";
if(isset($_POST['employee_edit']))
{
	if(isset($_GET['id']))
	{
		$id=$_GET['id'];
		$id=mysqli_real_escape_string($conn,$id);
		$id=test_input($id);

		$emp_name=$_POST['emp_name'];
		$emp_name=mysqli_real_escape_string($conn,$emp_name);
		$emp_name=test_input($emp_name);
		
		$mname=$_POST['mname'];
		$mname=mysqli_real_escape_string($conn,$mname);
		$mname=test_input($mname);

		$fname=$_POST['fname'];
		$fname=mysqli_real_escape_string($conn,$fname);
		$fname=test_input($fname);

		$sname=$_POST['sname'];
		$sname=mysqli_real_escape_string($conn,$sname);
		$sname=test_input($sname);

		$dob=$_POST['dob'];
		$dob=mysqli_real_escape_string($conn,$dob);
		$dob=test_input($dob);
		
		$emp_add=$_POST['emp_add'];
		$emp_add=mysqli_real_escape_string($conn,$emp_add);
		$emp_add=test_input($emp_add);
		
		$category=$_POST['category'];
		$category=mysqli_real_escape_string($conn,$category);
		$category=test_input($category);
		
		$designation=$_POST['designation'];
		$designation=mysqli_real_escape_string($conn,$designation);
		$designation=test_input($designation);
		
		$marital_sts=$_POST['marital_sts'];
		$marital_sts=mysqli_real_escape_string($conn,$marital_sts);
		$marital_sts=test_input($marital_sts);
		
		$mob1=$_POST['mob1'];
		$mob1=mysqli_real_escape_string($conn,$mob1);
		$mob1=test_input($mob1);
		
		$mob2=$_POST['mob2'];
		$mob2=mysqli_real_escape_string($conn,$mob2);
		$mob2=test_input($mob2);
		
		$email=$_POST['email'];
		$email=mysqli_real_escape_string($conn,$email);
		$email=test_input($email);
		
		$salary=$_POST['salary'];
		$salary=mysqli_real_escape_string($conn,$salary);
		$salary=test_input($salary);
		
		$gender=$_POST['gender'];
		$gender=mysqli_real_escape_string($conn,$gender);
		$gender=test_input($gender);
		
		$doa=$_POST['doa'];
		$doa=mysqli_real_escape_string($conn,$doa);
		$doa=test_input($doa);
		
		$grade=$_POST['grade'];
		$grade=mysqli_real_escape_string($conn,$grade);
		$grade=test_input($grade);
		
		$department=$_POST['department'];
		$department=mysqli_real_escape_string($conn,$department);
		$department=test_input($department);
		
		$sql = "UPDATE employee SET 
		emp_name='$emp_name', 
		mname='$mname', 
		fname='$fname', 
		sname='$sname', 
		dob='$dob', 
		emp_add='$emp_add', 
		category='$category', 
		designation='$designation', 
		marital_sts='$marital_sts', 
		mob1='$mob1', 
		mob2='$mob2', 
		email='$email', 
		gender='$gender', 
		salary='$salary', 
		grade='$grade', 
		doa='$doa', 
		department='$department'
		
		WHERE id=$id";
		
		$res=mysqli_query($conn, $sql);

		if($res) 
		{
			$_SESSION['msg']="Employee Details Updated Successfully!";
			header("Location:category");
		}
		else
		{
			$_SESSION['error']="Something Went Wrong. Try Again!";
			header("Location:category");
		}
	}
	else
	{
		header("Location:category");
	}
}
else
{
	header("Location:category");
}
mysqli_close($conn);
?>