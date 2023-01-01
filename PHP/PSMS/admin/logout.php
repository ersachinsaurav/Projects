<?php

ob_start();
session_start();
error_reporting(0);

   if(session_destroy()) {
      header("Location:http://127.0.0.1/psms/admin/login");
   }
?>