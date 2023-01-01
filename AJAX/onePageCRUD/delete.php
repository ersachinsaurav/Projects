<?php
include("config.php");
if(isset($_POST['delete'])){
$id = $_POST['id'];

$query = $conn->query("DELETE from user where id = '$id'");
echo'true';exit;
}
mysqli_close($conn);
?>