<?php
include "../includes/config.php";

// File upload path
$targetDir = '../images/';
$fileName = 'logo.' . pathinfo($_FILES['logo']['name'],PATHINFO_EXTENSION);
$targetFilePath = $targetDir . $fileName;
$fileType = pathinfo($targetFilePath,PATHINFO_EXTENSION);
$img_size=$_FILES['logo']['size'];

if(isset($_POST["logo_upload"]))
{
	if(!empty($_FILES["logo"]["name"]))
	{
		// Allow certain file formats
		$allowTypes = array('jpg','png','jpeg');
			
		if($img_size<=1048576)
		{
			if(in_array($fileType, $allowTypes))
			{
				// Upload file to server
				if(move_uploaded_file($_FILES["logo"]["tmp_name"], $targetFilePath))
				{
					// Insert image file name into database
					$sql = "UPDATE clg_details SET logo=('".$fileName."') WHERE id = 1";
					if(mysqli_query($conn,$sql))
					{
						$_SESSION['msg']="Logo has been uploaded successfully.";
						header("Location:../image_update");
					}
					else
					{
						$_SESSION['error']="Sorry, there was an error uploading your file. Try Again!";
						header("Location:../image_update");
					} 
				}
				else
				{
					$_SESSION['error']="Sorry, there was an error uploading your file. Try Again!";
					header("Location:../image_update");
				}
			}
			else
			{
				$_SESSION['error']="Only JPG, JPEG & PNG files are allowed to upload.";
				header("Location:../image_update");
			}
		}
		else
		{
			$_SESSION['error']="Sorry, Maximum 1MB File Size Is Allowed To Upload.";
			header("Location:../image_update");
		}
	}
	else 
	{
		$_SESSION['error']="Select A File To Upload.";
		header("Location:../image_update");
	}
}
else 
{
	header("Location:$logout");
}
?>