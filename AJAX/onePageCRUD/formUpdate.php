<?php
include("config.php");
$id = $_POST["id"];
$result = mysqli_query($conn,"SELECT * FROM user where id = $id");
while($row = mysqli_fetch_assoc($result)) {
?>

<div class="py-5 text-center">
    <h2>User Modification</h2>
</div>
<div class="row">
    <div class="col-md-12">
        <div class="row">
            <div class="col-md-6 mb-3">
                <label for="name">Name</label>
                <input type="text" class="form-control" id="name" placeholder="Name.." value="<?php echo $row["name"];?>" required>
                <input type="hidden" id="id" value="<?php echo $row["id"];?>">
                <div class="error-msg error-name"></div>
            </div>
            <div class="col-md-6 mb-3">
                <label for="mobile">Mobile</label>
                <input type="text" class="form-control" id="mobile" placeholder="Mobile.." value="<?php echo $row["contact_number"];?>" required>
                <div class="error-msg error-mobile"></div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-6 mb-3">
                <label for="gender">Gender</label>
                <select class="custom-select d-block w-100" id="gender" required>
                    <option value="<?php echo $row["gender"];?>" hidden><?php echo $row["gender"];?></option>
                    <option value="">- Select Gender-</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Transgender">Transgender</option>
                </select>
                <div class="error-msg error-gender"></div>
            </div>
            <div class="col-md-6 mb-3">
                <label for="date_of_birth">Date of Birth</label>
                <input type="date" class="form-control" id="dob" value="<?php echo $row["date_of_birth"];?>" required>
                <div class="error-msg error-dob"></div>
            </div>
        </div>
        <div class="mb-3">
            <label for="email">Email</label>
            <input type="email" class="form-control" id="email" placeholder="you@example.com" value="<?php echo $row["email"];?>" required>
            <div class="error-msg error-email"></div>
        </div>
        <div class="row">
            <div class="col-md-4 mb-3">
                <label for="country">Country</label>
                <select class="custom-select d-block w-100" id="country" required>
                    <?php
                        $country_id = $row["country"];
                        $query = $conn->query("SELECT * FROM countries where id = '$country_id'");
                        while($countryRow = $query->fetch_assoc()){
                            echo'<option value="'.$countryRow['id'].'" hidden>'.$countryRow['name'].'</option>';
                            }
                        ?>
                        <option value="">- Select Country -</option>
                    <?php
                        $query = $conn->query("SELECT * FROM countries");
                        while($countryRow = $query->fetch_assoc()){
                            echo'<option value="'.$countryRow['id'].'">'.$countryRow['name'].'</option>';
                            }
                        ?>
                </select>
                <div class="error-msg error-country"></div>
            </div>
            <div class="col-md-4 mb-3">
                <label for="state">State</label>
                <select class="custom-select d-block w-100" id="state" required>
                    <?php
                        $state_id = $row["state"];
                        $query = $conn->query("SELECT * FROM states where id = '$state_id'");
                        while($stateRow = $query->fetch_assoc()){
                            echo'<option value="'.$stateRow['id'].'" hidden>'.$stateRow['name'].'</option>';
                            }
                        ?>
                    <option value="">- Select State -</option>
                    <?php
                        $query = $conn->query("SELECT * FROM states where country_id = '$country_id'");
                        while($stateRow = $query->fetch_assoc()){
                            echo'<option value="'.$stateRow['id'].'">'.$stateRow['name'].'</option>';
                            }
                        ?>

                </select>
                <div class="error-msg error-state"></div>
            </div>
            <div class="col-md-4 mb-3">
                <label for="city">City</label>
                <select class="custom-select d-block w-100" id="city" required>
                    <?php
                        $city_id = $row["city"];
                        $query = $conn->query("SELECT * FROM cities where id = '$city_id'");
                        while($cityRow = $query->fetch_assoc()){
                            echo'<option value="'.$cityRow['id'].'" hidden>'.$cityRow['name'].'</option>';
                            }
                        ?>
                    <option value="">- Select City -</option>
                    <?php
                        $query = $conn->query("SELECT * FROM cities where state_id = '$state_id'");
                        while($cityRow = $query->fetch_assoc()){
                            echo'<option value="'.$cityRow['id'].'">'.$cityRow['name'].'</option>';
                            }
                        ?>                
                </select>
                <div class="error-msg error-city"></div>
            </div>
            <div class="col-12">
                <div class="error"></div>
            </div>
        </div>
        <hr class="mb-4">
        <button class="btn btn-primary btn-lg btn-block" type="button" id="update">Update</button>
    </div>
</div>
<script type="text/javascript" src="updateValidation.js"></script>

<?php
}
?>