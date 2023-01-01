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
		<mainrole="main" class="flex-shrink-0">
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
							<th>EID</th>
							<th>Name</th>
							<th>Grade</th>
							<th>Dept.</th>
							<th>Desg.</th>
							<th>DOB</th>
							<th>DOA</th>
							<th>Actual</th>
							<th>AGP</th>
							<th>HRA</th>
							<th>DA</th>
							<th>Med</th>
							<th>WA</th>
							<th>Other#1</th>
							<th>G.Total</th>
							<th>W/F</th>
							<th>Released</th>
							<th>PF</th>
							<th>PF Adv</th>
							<th>LIC</th>
							<th>F.Adv</th>
							<th>HT</th>
							<th>IT</th>
							<th>Marriage/Med</th>
							<th>Sal.Adv</th>
							<th>Rev.Asso</th>
							<th>Q.Rent</th>
							<th>Rev/Adv</th>
							<th>Other#2</th>
							<th>Other#3</th>
							<th>Remarks#1</th>
							<th>Remarks#2</th>
							</tr>
					</thead>
					<tbody>
					<?php
            $sql="SELECT * FROM employee INNER JOIN allowance ON employee.id=allowance.eid";
            $res=mysqli_query($conn,$sql);
            if(mysqli_num_rows($res)>0)
            {
                while($row=mysqli_fetch_assoc($res))
                {
            ?>
					<tr>
							<td><?php echo $row['eid'];?></td>
							<td><?php echo $row['emp_name'];?></td>
							<td><?php echo $row['grade'];?></td>
							<td><?php echo $row['department'];?></td>
							<td><?php echo $row['designation'];?></td>
							<td><?php echo $row['dob'];?></td>
							<td><?php echo $row['doa'];?></td>
							<td><?php echo $row['actual'];?></td>
							<td><?php echo $row['agp'];?></td>
							<td><?php echo $row['hra'];?></td>
							<td><?php echo $row['da'];?></td>
							<td><?php echo $row['med'];?></td>
							<td><?php echo $row['wa'];?></td>
							<td><?php echo $row['other1'];?></td>
							<td><?php echo $row['gtotal'];?></td>
							<td><?php echo $row['wf'];?></td>
							<td><?php echo $row['released'];?></td>
							<td><?php echo $row['pf'];?></td>
							<td><?php echo $row['pfadv'];?></td>
							<td><?php echo $row['lic'];?></td>
							<td><?php echo $row['fadv'];?></td>
							<td><?php echo $row['ht'];?></td>
							<td><?php echo $row['it'];?></td>
							<td><?php echo $row['marriage_med'];?></td>
							<td><?php echo $row['sal_adv'];?></td>
							<td><?php echo $row['rev_asso'];?></td>
							<td><?php echo $row['qrent'];?></td>
							<td><?php echo $row['rev_adv'];?></td>
							<td><?php echo $row['other2'];?></td>
							<td><?php echo $row['other3'];?></td>
							<td><?php echo $row['remarks1'];?></td>
							<td><?php echo $row['remarks2'];?></td>
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
