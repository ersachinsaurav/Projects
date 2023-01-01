<?php
   ob_start();
   session_start();
   error_reporting(0);
   
   if(!isset($_SESSION['login_user'])){
      header("location:http://127.0.0.1/psms/admin/login");
      die();
   }
?>