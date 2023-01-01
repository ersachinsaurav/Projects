<div class="py-5 text-center">
    <h2>User Registration</h2>
</div>
<div class="row">
    <div class="col-md-12">
        <div class="row">
            <div class="col-md-6 mb-3">
                <label for="name">Name</label>
                <input type="text" class="form-control" id="name" placeholder="Name.." value="" required>
                <div class="error-msg error-name"></div>
            </div>
            <div class="col-md-6 mb-3">
                <label for="mobile">Mobile</label>
                <input type="text" class="form-control" id="mobile" placeholder="Mobile.." value="" required>
                <div class="error-msg error-mobile"></div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-6 mb-3">
                <label for="gender">Gender</label>
                <select class="custom-select d-block w-100" id="gender" required>
                    <option value="">- Select Gender-</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Transgender">Transgender</option>
                </select>
                <div class="error-msg error-gender"></div>
            </div>
            <div class="col-md-6 mb-3">
                <label for="date_of_birth">Date of Birth</label>
                <input type="date" class="form-control" id="dob" value="" required>
                <div class="error-msg error-dob"></div>
            </div>
        </div>
        <div class="mb-3">
            <label for="email">Email</label>
            <input type="email" class="form-control" id="email" placeholder="you@example.com" value="" required>
            <div class="error-msg error-email"></div>
        </div>
        <div class="row">
            <div class="col-md-4 mb-3">
                <label for="country">Country</label>
                <select class="custom-select d-block w-100" id="country" required>
                    <option value="">- Select Country -</option>
                    <?php
                        include("config.php");
                        $query = $conn->query("SELECT * FROM countries");
                        while($row = $query->fetch_assoc()){
                            echo'<option value="'.$row['id'].'">'.$row['name'].'</option>';
                            }
                        ?>
                </select>
                <div class="error-msg error-country"></div>
            </div>
            <div class="col-md-4 mb-3">
                <label for="state">State</label>
                <select class="custom-select d-block w-100" id="state" required>
                    <option value="">- Select State -</option>
                </select>
                <div class="error-msg error-state"></div>
            </div>
            <div class="col-md-4 mb-3">
                <label for="city">City</label>
                <select class="custom-select d-block w-100" id="city" required>
                    <option value="">- Select City -</option>
                </select>
                <div class="error-msg error-city"></div>
            </div>
            <div class="col-12">
                <div class="error"></div>
            </div>
        </div>
        <hr class="mb-4">
        <button class="btn btn-primary btn-lg btn-block" type="button" id="register">Register</button>
    </div>
</div>