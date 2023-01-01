<?php
include("config.php");
$country = $_POST["country"];
$result = mysqli_query($conn,"SELECT * FROM states where country_id = $country");
?>
<option value="">Select State</option>
<?php
while($row = mysqli_fetch_array($result)) {
?>
    <option value="<?php echo $row["id"];?>"><?php echo $row["name"];?></option>
<?php
}
?>