<?php
if(isset($_POST['detect']) && $_POST['detect']=="Detect")
{
	$dir='uploads/';
	$image_path=$dir.basename($_FILES['imageInput']['name']);


	if(move_uploaded_file($_FILES['imageInput']['tmp_name'],$image_path))
	{
		echo 'uploaded succesfully.';
	}
}
?>