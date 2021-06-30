<?php
if(isset($_POST['detect']) && $_POST['detect']=="Detect")
{
	$dir='uploads/';
	$image_path=$dir.basename($_FILES['imageInput']['name']);


	if(move_uploaded_file($_FILES['imageInput']['tmp_name'],$image_path))
	{
		echo 'uploaded succesfully.';
		$command = "cd backend/ && python yolo.py ".$_FILES['imageInput']['name'];
		$last_line = system($command, $retval);
		if($retval == 0){
			header("Location: viewResult.php");
		}
		else {
			echo "Error Occurred";
		}
	}
}
?>