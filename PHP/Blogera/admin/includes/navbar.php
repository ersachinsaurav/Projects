<?php
include "header.php";
if(isset($_SESSION['username']))
{
?>

    <nav class="teal">
        <div class="nav-wrapperr">
            <div class="container">
                <a href="" class="brand-logo center">Blogera</a>
                <a href="" class="button-collapse show-on-large" data-activates="sidenav"><i class="material-icons">menu</i></a>

            </div>
        </div>
    </nav>
    <ul class="side-nav fixed" id="sidenav">
        <li>
            <div class="user-view">
                <div class="background">
                    <img src="../img/img8.jpg" alt="" class="responsive-img">
                </div>
                <a href=""><img src="../img/img29.jpg" alt="" class="circle"></a>
                <span class="name white-text"><?php echo $_SESSION['username'];?></span>
                <span class="email white-text">
<?php
$user=$_SESSION['username'];
$sql="select email from users where username='$user'";
$res=mysqli_query($conn,$sql);
$row=mysqli_fetch_assoc($res);
echo $row['email'];
?>
</span>
            </div>
        </li>
        <li>
            <a href="dashboard.php">Dashboard</a>
        </li>
        <li>
            <a href="post.php">Posts</a>
        </li>
        <li>
            <a href="image.php">Images</a>
        </li>
        <li>
            <a href="comment.php">Comments</a>
        </li>
        <li>
            <a href="setting.php">Settings</a>
        </li>
        <div class="divider"></div>
        <li><a href="logout.php">Logout</a></li>
    </ul>

    <?php
}
else
    {
        $_SESSION['message']="<div class='chip red white-text'>Please Login To Continue.</div>";
        header("Location: ../login.php");
    }
?>