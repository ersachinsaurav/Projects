<?php
include("config.php");
if (isset($_POST['mobile_check'])) {
    if (strlen(trim($_POST["mobile"])) != 10) {
        echo 'Invalid Mobile Number';
        exit;
    } else {
        $mobile = $_POST['mobile'];
        $CH     = substr($mobile, 0, 1);
        if ($CH < 6) {
            echo 'Incorrect Mobile Number';
            exit;
        }
    }
    $checkMob = $conn->query("SELECT COUNT(contact_number) FROM user where contact_number='$mobile'");
    $row      = $checkMob->fetch_assoc();
    $count    = $row['COUNT(contact_number)'];
    if ($count == "1") {
        echo "Number Already Exist!";
        exit;
    } else {
        echo "true";
        exit;
    }
}
if (isset($_POST['update_mobile_check'])) {
    if (strlen(trim($_POST["mobile"])) != 10) {
        echo 'Invalid Mobile Number';
        exit;
    } else {
        $mobile = $_POST['mobile'];
        $id     = $_POST['id'];
        $CH     = substr($mobile, 0, 1);
        if ($CH < 6) {
            echo 'Incorrect Mobile Number';
            exit;
        }
    }
    $checkMob = $conn->query("SELECT COUNT(contact_number) FROM user where contact_number='$mobile' and id = '$id'");
    $row      = $checkMob->fetch_assoc();
    $count    = $row['COUNT(contact_number)'];
    if ($count != "1") {
        $checkMob = $conn->query("SELECT COUNT(contact_number) FROM user where contact_number='$mobile'");
        $row      = $checkMob->fetch_assoc();
        $count    = $row['COUNT(contact_number)'];
        if ($count == "1") {
            echo "Number Already Exist!";
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