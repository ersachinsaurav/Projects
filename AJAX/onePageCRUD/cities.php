<?php
include("config.php");
$state = $_POST["state"];
$result = mysqli_query($conn,"SELECT * FROM cities where state_id = $state");
?>
<option value="">Select City</option>
<?php
while($row = mysqli_fetch_array($result)) {
?>
<option value="<?php echo $row["id"];?>"><?php echo $row["name"];?></option>
<?php
}
?>