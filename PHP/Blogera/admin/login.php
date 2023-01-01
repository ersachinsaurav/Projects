<?php
include "includes/header.php";
if(!isset($_SESSION['username']))
{
?>

<body style="background-image:url('../img/back.jpg'); background-size:cover;">

<div class="row" style="margin-top:100px;">
<div class="col offset-13 m8 offset-m2 s12">
<div class="card-panel center blue lighten-2" style="margin-bottom:0px;">
<ul class="tabs  blue lighten-2">
<li class="tab"><a href="#login" class="black-text"><b>Login</b></a>
</li>
<li class="tab"><a href="#signup" class="black-text"><b>Sign Up</b></a>
</li>
</ul>
</div>
</div>

 <!--Login & Sign Up Area-->

<div class="col offset-13 m8 offset-m2 s12" id="login">
<div class="card-panel center" style="margin-top:1px;">
<h5>Login To Continue</h5>
<?php
if(isset($_SESSION['message']))
{
  echo $_SESSION['message'];
  unset($_SESSION['message']);
}
?>

<form action="login_check.php" method="POST">
<div class="input-field">
<input type="text" name="username" id="username" placeholder="Enter Username" required>
</div>
<div class="input-field">
<input type="password" name="password" id="password" placeholder="Enter Password" required>
</div>
<input type="submit" name="login" class="btn" value="Login">
</form>
</div>
</div>
<div class="col offset-13 m8 offset-m2 s12" id="signup">
<div class="card-panel center" style="margin-top:1px;"  >
<h5>Sign Up Now</h5>
<form action="signup.php" method="POST">
<div class="input-field">
<input type="email" maxlength="40" name="email" id="email" placeholder="Enter Email" class="validate" required>
<label for="email" data-error="Invalid Email Format." data-success="Valid Email Format."></label>
</div>
<div class="input-field">
<input type="text" minlength="3" maxlength="20" name="username" id="username" placeholder="Enter Username" class="validate" required>
<label for="username" data-error="Username Should Be Of Minimum 3 Characters & Max 20 Characters." data-success="Valid Username Format"></label>
</div>
<div class="input-field">
<input type="password" minlength="6" maxlength="20" name="password" id="password" placeholder="Enter Password" class="validate" required>
<label for="password" data-error="Password Should Be Of Minimum 6 Characters & Max 20 Characters." data-success="Valid Password Format"></label>
</div>
<input type="submit" name="signup" class="btn" value="Sign Up">
</form>

</div>
</div>
</div>
<?php
include "includes/footer.php";
}
else
{
  header("Location: dashboard.php");
}
?>