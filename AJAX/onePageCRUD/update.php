<?php
include("config.php");
if(isset($_POST['user'])){
$id = $_POST['id'];
$name = $_POST['name'];
$mobile = $_POST['mobile'];
$gender = $_POST['gender'];
$dob = $_POST['dob'];
$email = $_POST['email'];
$country = $_POST['country'];
$state = $_POST['state'];
$city = $_POST['city'];

$query = $conn->query("UPDATE user SET name='$name',email='$email',contact_number='$mobile',date_of_birth='$dob',gender='$gender',country='$country',state='$state',city='$city' where id = '$id'");
echo'true';exit;
}
mysqli_close($conn);?>