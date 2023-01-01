<?php
include "includes/header.php";
if(isset($_GET['id']))
{
    $id=$_GET['id'];
    $id=mysqli_real_escape_string($conn,$id);
    $id=htmlentities($id);
    $sql="update comment set status=0 where id=$id";
    $res=mysqli_query($conn,$sql);
    if($res)
    {
        echo "<div class='chip green white-text'>Comment Removed.</div>";
    }
    else
    {
        echo "<div class='chip red white-text'>Something Went Wrong, Try Again.</div>";
    }
}
?>