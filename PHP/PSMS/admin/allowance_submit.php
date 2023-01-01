<?php
include "includes/config.php";
include "includes/session.php";

if(isset($_POST['allowance_update']))
{	
	if(isset($_GET['id']))
	{
		if (!empty($_POST['salary'])) 
		{
			$id=$_GET['id'];
			$id=mysqli_real_escape_string($conn,$id);
			$id=test_input($id);

			$dap=$_POST['da'];
			$dap=mysqli_real_escape_string($conn,$dap);
			$dap=test_input($dap);
			
			$hrap=$_POST['hra'];
			$hrap=mysqli_real_escape_string($conn,$hrap);
			$hrap=test_input($hrap);

			$pfp=$_POST['pf'];
			$pfp=mysqli_real_escape_string($conn,$pfp);
			$pfp=test_input($pfp);

			$actual=$_POST['salary'];
			$actual=mysqli_real_escape_string($conn,$actual);
			$actual=test_input($actual);

			$fyear=$_POST['fyear'];
			$fyear=mysqli_real_escape_string($conn,$fyear);
			$fyear=test_input($fyear);

			$smonth=$_POST['smonth'];
			$smonth=mysqli_real_escape_string($conn,$smonth);
			$smonth=test_input($smonth);

			$agp=$_POST['agp'];
			$agp=mysqli_real_escape_string($conn,$agp);
			$agp=test_input($agp);

			$med=$_POST['med'];
			$med=mysqli_real_escape_string($conn,$med);
			$med=test_input($med);

			$other1=$_POST['other1'];
			$other1=mysqli_real_escape_string($conn,$other1);
			$other1=test_input($other1);

			$wf=$_POST['wf'];
			$wf=mysqli_real_escape_string($conn,$wf);
			$wf=test_input($wf);

			$pfadv=$_POST['pfadv'];
			$pfadv=mysqli_real_escape_string($conn,$pfadv);
			$pfadv=test_input($pfadv);

			$lic=$_POST['lic'];
			$lic=mysqli_real_escape_string($conn,$lic);
			$lic=test_input($lic);

			$it=$_POST['it'];
			$it=mysqli_real_escape_string($conn,$it);
			$it=test_input($it);

			$qrent=$_POST['qrent'];
			$qrent=mysqli_real_escape_string($conn,$qrent);
			$qrent=test_input($qrent);

			$wa=$_POST['wa'];
			$wa=mysqli_real_escape_string($conn,$wa);
			$wa=test_input($wa);

			$fadv=$_POST['fadv'];
			$fadv=mysqli_real_escape_string($conn,$fadv);
			$fadv=test_input($fadv);

			$ht=$_POST['ht'];
			$ht=mysqli_real_escape_string($conn,$ht);
			$ht=test_input($ht);

			$marriage_med=$_POST['marriage_med'];
			$marriage_med=mysqli_real_escape_string($conn,$marriage_med);
			$marriage_med=test_input($marriage_med);

			$sal_adv=$_POST['sal_adv'];
			$sal_adv=mysqli_real_escape_string($conn,$sal_adv);
			$sal_adv=test_input($sal_adv);

			$rev_asso=$_POST['rev_asso'];
			$rev_asso=mysqli_real_escape_string($conn,$rev_asso);
			$rev_asso=test_input($rev_asso);

			$rev_adv=$_POST['rev_adv'];
			$rev_adv=mysqli_real_escape_string($conn,$rev_adv);
			$rev_adv=test_input($rev_adv);

			$other2=$_POST['other2'];
			$other2=mysqli_real_escape_string($conn,$other2);
			$other2=test_input($other2);

			$other3=$_POST['other3'];
			$other3=mysqli_real_escape_string($conn,$other3);
			$other3=test_input($other3);
			
			$remarks1=$_POST['remarks1'];
			$remarks1=mysqli_real_escape_string($conn,$remarks1);
			$remarks1=test_input($remarks1);

			$remarks2=$_POST['remarks2'];
			$remarks2=mysqli_real_escape_string($conn,$remarks2);
			$remarks2=test_input($remarks2);

			//Calculation Start

			$pf = ($actual / 100) * $pfp;
			$hra = ($actual / 100) * $hrap;
			$da = ($actual / 100) * $dap;
			$gtotal = $actual + $hra + $da + $med + $wa + $other1;
			$net1 = $gtotal - $wf;
			$released = $net1;
			$dtotal =  $pf + $sal_adv + $pfadv + $it + $qrent + $rev_adv + $lic + $other2 + $other3 + $ht + $rev_asso + $marriage_med + $fadv;
			$net2 = $net1 - $dtotal;
			
			//Calculation End

			$sql2="SELECT * FROM allowance WHERE fyear=$fyear AND eid=$id and smonth= '$smonth'";

			$res2=mysqli_query($conn,$sql2);
			$row2 = mysqli_fetch_assoc($res2);

			$fyear2 = $row2['fyear'];
			$id2 = $row2['eid'];
			$smonth2 = $row2['smonth'];

			if($fyear==$fyear2 && $id==$id2 && $smonth===$smonth2)
			{
				$sql3 = "UPDATE allowance SET 
				actual='$actual',
				da='$da',
				hra='$hra',
				med='$med',
				other1='$other1',
				gtotal='$gtotal',
				wf='$wf',
				net1='$net1',
				released='$released',
				pf='$pf',
				pfadv='$pfadv',
				lic='$lic',
				it='$it',
				qrent='$qrent',
				rev_adv='$rev_adv',
				dtotal='$dtotal',
				net2='$net2',
				wa='$wa',
				fadv='$fadv',
				ht='$ht',
				marriage_med='$marriage_med',
				sal_adv='$sal_adv',
				rev_asso='$rev_asso',
				other2='$other2',
				remarks1='$remarks1',
				remarks2='$remarks2',
				agp='$agp',
				other3='$other3'
				WHERE fyear = $fyear AND eid=$id AND smonth='$smonth'";
				
				$res3=mysqli_query($conn, $sql3);
				
				if($res3) 
				{
					$_SESSION['msg']="Allowance Details Updated Successfully!";
					header("Location:category");
				}
			}
			else
			{
				$sql = "INSERT INTO allowance (eid,smonth, fyear, actual, da, hra, med, other1, gtotal, wf, net1, released, pf, pfadv, lic, it, qrent, rev_adv, dtotal, net2, wa, fadv, ht, marriage_med, sal_adv, rev_asso, other2, other3, remarks1, remarks2, agp) VALUES ('$id', '$smonth', '$fyear', '$actual', '$da', '$hra', '$med', '$other1', '$gtotal', '$wf', '$net1', '$released', '$pf', '$pfadv', '$lic', '$it', '$qrent', '$rev_adv', '$dtotal', '$net2', '$wa', '$fadv', '$ht', '$marriage_med', '$sal_adv', '$rev_asso', '$other2', '$other3', '$remarks1', '$remarks2', '$agp')";
				
				$res=mysqli_query($conn, $sql);
				if($res) 
				{
					$_SESSION['msg']="Allowance Details Added Successfully!";
					header("Location:category");
				}
			}
			if((!$res) && (!$res3)) 
			{
				$_SESSION['error']="Something Went Wrong. Try Again!";
				header("Location:category");
			}
		}
		else
		{
			$_SESSION['error']="Update Actual Salary First. Try Again!";
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
	header("Location:$logout");
	die();	
}
mysqli_close($conn);
?>