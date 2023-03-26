<?php
if($_SERVER["REQUEST_METHOD"]=="POST")
{
	$api_key = $_POST["api_key"];
	if($api_key == $search_key)
	{
		file_put_contents("last_coord", $_POST["latitude"].",".$_POST["longitude"]);
	}
	else{
		http_response_code(401);
	}
}
else{
	http_response_code(405);
}