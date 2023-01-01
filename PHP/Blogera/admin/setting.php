<?php
include "includes/navbar.php";
if(isset($_SESSION['username']))
	{
?>

<div class="main">
<div class="card-panel">
<h4 class="center">Settings</h4>
<?php 
if(isset($_SESSION['message']))
{
    echo $_SESSION['message'];
    unset ($_SESSION['message']);
}
?>
<form action="setting.php" method="POST">
<h5>Change Password</h5>
<br>
<input type="password" name="password" placeholder="Enter New Password" required>
<input type="password" name="con_password" placeholder="Re Enter New Password" required>
<div class="center">
<input type="submit" name="update_password" value="Change Password" class="btn">
</div>
</form>
</div>
</div>

<?php
	}
	else
		{
			$_SESSION['message']="<div class='chip red white-text'>Please Login To Continue.</div>";
			header("Location: login.php");
		}
	include "includes/footer.php";
	?>

<?php
if(isset($_POST['update_password']))
{
    $password=$_POST['password'];
	$password=mysqli_real_escape_string($conn,$password);
    $password=htmlentities($password);
    $con_password=$_POST['con_password'];
	$con_password=mysqli_real_escape_string($conn,$con_password);
    $con_password=htmlentities($con_password);
    if($con_password===$password)
    {
        $username=$_SESSION['username'];
        $password=password_hash($password,PASSWORD_BCRYPT);
        $sql="update users set password='$password' where username='$username'";
        $res=mysqli_query($conn,$sql);
        if($res)
        {
            $_SESSION['message']="<div class='chip green white-text'>Password Changed Successfully.</div>";
    	    header("Location: setting.php");  
        }
        else
        {
            $_SESSION['message']="<div class='chip red white-text'>Something Went Wrong, Try Again.</div>";
            header("Location: setting.php");
        }
        
    }
    else
    {
        $_SESSION['message']="<div class='chip red white-text'>Passwords Don't Match.</div>";
	    header("Location: setting.php");
    }    
}
?>