<?php
include "includes/header.php";

if(isset($_POST['signup']))
{
    $email=$_POST['email'];
    $username=$_POST['username'];
    $password=$_POST['password'];
    $email=mysqli_real_escape_string($conn,$email);
    $username=mysqli_real_escape_string($conn,$username);
    $password=mysqli_real_escape_string($conn,$password);
    $email=htmlentities($email);
    $username=htmlentities($username);
    $password=htmlentities($password);
    $password=password_hash($password,PASSWORD_BCRYPT);
    
    $sql3="select * from users where username='$username'";
    $res3=mysqli_query($conn,$sql3);
    
    $sql2="select * from users where email='$email'";
    $res2=mysqli_query($conn,$sql2);

    if(mysqli_num_rows($res2)>0)
    {
        $_SESSION['message']="<div class='chip red white-text'>Account already exist, please login to your account to continue.";
        header("Location: login.php");
    }

    elseif(mysqli_num_rows($res3)>0)
    {
        $_SESSION['message']="<div class='chip red white-text'>Username already exist, please register with another username.</div>";
        header("Location: login.php");
    }

    else
    {
        $sql="insert into users(email,username,password) values('$email','$username','$password')";
        $res=mysqli_query($conn,$sql);
    
        if($res)
        {
            $_SESSION['message']="<div class='chip green white-text'>You've been successfully registered, login to continue.</div>";
            header("Location: login.php");
        }
        else
        {
            $_SESSION['message']="<div class='chip red white-text'>Something went wrong, please register again.</div>";
            header("Location: login.php");
        }
    }
}

?>