<?php
include "../includes/config.php";
include "../includes/session.php";

if(isset($_POST['doc1_upload']))
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
		$fileName = 'Doc1.' . pathinfo($_FILES['doc1']['name'],PATHINFO_EXTENSION);
		$targetFilePath = $targetDir . $fileName;
		$fileType = pathinfo($targetFilePath,PATHINFO_EXTENSION);
		$img_size=$_FILES['doc1']['size'];

		if(!empty($_FILES["doc1"]["name"]))
		{
			// Allow certain file formats
			$allowTypes = array('jpg','png','jpeg');

			if($img_size<=1048576)
			{
				if(in_array($fileType, $allowTypes))
				{
					// Upload file to server
					if(move_uploaded_file($_FILES["doc1"]["tmp_name"], $targetFilePath))
					{
						// Insert image file name into database
						$sql = "UPDATE employee SET doc1=('".$fileName."') WHERE id = $id";
						if(mysqli_query($conn,$sql))
						{
							$_SESSION['msg']="Doc1 Has Been Uploaded Successfully.";
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