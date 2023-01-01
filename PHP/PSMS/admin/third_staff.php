<?php
include "includes/session.php";
include "includes/header.php";
include "includes/thead.php";
?>
</head>
	<body class="d-flex flex-column h-100">
	<?php include "includes/navbar.php";?>
			<!-- Begin page content -->
			<br>
			<br>
		<main role="main" class="flex-shrink-0">
			<div class="container">
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
			<span id="message"></span>
				<table id="example" class="display responsive table-bordered text-center" style="width:100%">
					<thead>
						<tr>
							<th>Name</th>
							<th>Department</th>
							<th>Designation</th>
							<th>Manage Salary</th>
							<th>Documents</th>
							<th>Profile</th>
							<th>Edit</th>
							<th>Salary Slip</th>
							<th>Delete</th>
							</tr>
					</thead>
					<tbody>
					<?php
            $sql="select * from employee where grade='Third_Grade_Staff'";
            $res=mysqli_query($conn,$sql);
            if(mysqli_num_rows($res)>0)
            {
                while($row=mysqli_fetch_assoc($res))
                {
            ?>
					<tr>
					<td><?php echo $row['emp_name'];?></td>
					<td><?php echo $row['department'];?></td>
					<td><?php echo $row['designation'];?></td>
					<td><a href="allowance?id=<?php echo $row['id']; ?>"><img src="images/allowance.png" alt="Upload Documents"></a></td>
					<td><a href="documents?id=<?php echo $row['id']; ?>"><img src="images/document.png" alt="Upload Documents"></a></td>
					<td><a href="profile?id=<?php echo $row['id']; ?>"><img src="images/profile.png" alt="View Profile"></a></td>
					<td><a href="edit?id=<?php echo $row['id']; ?>"><img src="images/edit.png" alt="Edit Profile"></a></td>
					<td><a href="salary?id=<?php echo $row['id']; ?>"><img src="images/salary.png" alt="View Salary Slip"></a></td>
					<td><a href="" id="<?php echo $row['id']; ?>" class="delete">❌Delete</a>
</td>
</tr>
			<?php
                }
            }
            ?>
					</tbody>
				</table>
                </div>
        </main>
    <br>    
    <br>    
       <?php include "includes/footer.php";?>
	
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
			xhr.open("GET","delete?id="+Number(e.target.id),true)
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
