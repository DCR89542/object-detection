<?php
if(isset($_POST['save_image']) && $_POST['save_image']=="Upload Image")
{
	$dir='uploads\';
	$image_path=$dir.basename($_FILES['imageFile']['name']);
	
	if(move_uploaded_file($_FILES['imageFile']['tmp_name'],$image_path))
	{
		echo 'uploaded succesfully.';
	}
}
?>