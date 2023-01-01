<?php
$servername = "localhost";
$username = "root";
$password = "";
$database = "psms";
$conn = mysqli_connect($servername, $username, $password, $database);
mysqli_query($conn,"set sql_mode=''");

ob_start();
session_start();
error_reporting(0);

$logout="http://127.0.0.1/psms/admin/login";

function test_input($data) 
{
	$data = trim($data);
	$data = stripslashes($data);
	$data = htmlspecialchars($data);
	return $data;
}
?>