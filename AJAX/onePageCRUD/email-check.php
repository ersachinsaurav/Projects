<?php
include("config.php");
if (isset($_POST['email_check'])) {
    $email = $_POST['email'];
    
    function email_validation($str)
    {
        return (!preg_match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,3})$^", $str)) ? FALSE : TRUE;
    }
    if (!email_validation(("$email"))) {
        echo "Invalid email address.";
        exit;
    }
    
    $checkMail = $conn->query("SELECT COUNT(email) FROM user where email='$email'");
    $row       = $checkMail->fetch_assoc();
    $count     = $row['COUNT(email)'];
    if ($count == "1") {
        echo "E-Mail Already Exist !";
        exit;
    } else {
        echo "true";
        exit;
    }
}
if (isset($_POST['update_email_check'])) {
    $email = $_POST['email'];
    $id    = $_POST['id'];
    
    function email_validation($str)
    {
        return (!preg_match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,3})$^", $str)) ? FALSE : TRUE;
    }
    if (!email_validation(("$email"))) {
        echo "Invalid email address.";
        exit;
    }
    
    $checkMail = $conn->query("SELECT COUNT(email) FROM user where email='$email' and id = '$id'");
    $row       = $checkMail->fetch_assoc();
    $count     = $row['COUNT(email)'];
    if ($count != 1) {
        $checkMail = $conn->query("SELECT COUNT(email) FROM user where email='$email'");
        $row       = $checkMail->fetch_assoc();
        $count     = $row['COUNT(email)'];
        if ($count == 1) {
            echo "E-Mail Already Exist !";
            exit;
        } else {
            echo "true";
            exit;
        }
    } else {
        echo "true";
        exit;
    }
}
mysqli_close($conn);
?>