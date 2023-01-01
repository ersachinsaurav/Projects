<?php
include "../includes/config.php";
include "../includes/session.php";

if(isset($_POST['emp_photo_upload']))
{
	if(isset($_GET['id']))
	{
		$id=$_GET['id'];
		$id=mysqli_real_escape_string($conn,$id);
		$id=test_input($id);

		//Check or Create Directory
		if (!file_exists('../images/'.$id.'/')) 
		{
			mkdir('../images/'.$id.'/', 0777, true);
		}
		// File upload path
		$targetDir = '../images/'.$id.'/';
		$fileName = 'emp_photo.' . pathinfo($_FILES['emp_photo']['name'],PATHINFO_EXTENSION);
		$targetFilePath = $targetDir . $fileName;
		$fileType = pathinfo($targetFilePath,PATHINFO_EXTENSION);
		$img_size=$_FILES['emp_photo']['size'];

		if(!empty($_FILES["emp_photo"]["name"]))
		{
			// Allow certain file formats
			$allowTypes = array('jpg','png','jpeg');

			if($img_size<=1048576)
			{
				if(in_array($fileType, $allowTypes))
				{
					// Upload file to server
					if(move_uploaded_file($_FILES["emp_photo"]["tmp_name"], $targetFilePath))
					{
						// Insert image file name into database
						$sql = "UPDATE employee SET emp_photo=('".$fileName."') WHERE id = $id";
						if(mysqli_query($conn,$sql))
						{
							$_SESSION['msg']="Employee Photo Has Been Uploaded Successfully.";
							header("Location:../documents?id=$id");
						}
						else
						{
						$_SESSION['error']="Sorry, there was an error uploading your file. Try Again!";
						header("Location:../documents?id=$id");
						} 
					}
					else
					{
					$_SESSION['error']="Sorry, there was an error uploading your file. Try Again!";
					header("Location:../documents?id=$id");
					}
				}
				else
				{
				$_SESSION['error']="Only JPG, JPEG & PNG files are allowed to upload.";
				header("Location:../documents?id=$id");
				}
			}
			else
			{
			$_SESSION['error']="Sorry, Maximum 1MB File Size Is Allowed To Upload.";
			header("Location:../documents?id=$id");
			}
		}
		else 
		{
		$_SESSION['error']="Select A File To Upload.";
		header("Location:../documents?id=$id");
		}
	}
	else 
	{
	header('Location:../teaching_Staff');
	}
}
else 
{
header('Location:../teaching_Staff');
}
?>