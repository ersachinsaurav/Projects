<style>
    .mcpl{
        cursor: pointer;
    }
</style>
<?php
include("config.php");
$sn = 1;
$query = $conn->query("SELECT * FROM user");
while($row = $query->fetch_assoc()){
    echo'
        <div class="row border-bottom">
            <div class="col-1">'.$sn++.'</div>
            <div class="col-3">'.$row['name'].'</div>
            <div class="col-4">'.$row['email'].'</div>
            <div class="col-2">'.$row['contact_number'].'</div>
            <div class="col-1 mcpl" onclick="Edit('.$row['id'].')">Edit</div>
            <div class="col-1 mcpl" onclick="Del('.$row['id'].')">Delete</div>
        </div>
    ';
}
?>