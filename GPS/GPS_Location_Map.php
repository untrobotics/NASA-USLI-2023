<?php
  require("../template/top.php");

$num_points = 10;
$sql = "SELECT latitude, longitude FROM `locationData`  \n"
    . "ORDER BY `locationData`.`timestamp` DESC LIMIT 10";
    
$latitudes = array();
$longitudes = array();

$rand_offset = 0;
if ($hide_location)
    while ($rand_offset == 0)
        $rand_offset = rand(-20,20);

if ($result = $db->query($sql)) 
{
    for($i = 0; $i < $num_points; $i++)
    {
        $row = $result->fetch_assoc();
        $latitudes[] = round($row["latitude"],6);
        $longitudes[] = round($row["longitude"],6);
        if($latitudes[$i] == 0)
        {
            unset($latitudes[$i]);
            unset($longitudes[$i]);
            continue;
        }
        $latitudes[$i] += $rand_offset;
        $longitudes[$i] += $rand_offset;
    }
}
else
    echo "Fail";

if (count($latitudes) < $num_points)
    $num_points = count($latitudes);
    
$result->free();
$conn->close();

$lat_center = $lon_center = 0;
$lat_max = $lon_max = -100;
$lat_min = $lon_min = 100;

$locations = array();
for($i = 0; $i < $num_points; $i++)
{
    if($latitudes[$i] == 0)
    {
        echo "<p>" . $latitudes[$i] . "</p>";
        continue;
    }
    $locations[] = array('Marker',$latitudes[$i],$longitudes[$i],$i);
   
    $lat_center += $latitudes[$i];
    $lon_center +=$longitudes[$i];
        
}
$lat_center /= $num_points;
$lon_center /= $num_points;



$dist_from_center = array();
for($i = 0; $i < $num_points; $i++)
    $dist_from_center[] = sqrt( pow( ($latitudes[$i] - $lat_center), 2) + pow( ($longitudes[$i] - $lon_center), 2) );

$radius = max($dist_from_center) * 101139;
?>

<script>
var multiMarker = new Boolean(<?php echo $multi_marker?>);
function initMap() {
  if (multiMarker === 0) {
    var point = { lat: <?php echo $lat_center?>, lng: <?php echo $lon_center?>};
     
    var map = new google.maps.Map(document.getElementById("map"), {
      zoom: 15,
      scaleControl: true,
      center: point,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });
    
    const marker = new google.maps.Marker({
      position: point,
      map: map,
    });
     
    google.maps.event.addListener(marker, "click", (event) => {
      window.open("https://www.google.com/maps/search/?api=1&query=<?php echo $lat_center?>,<?php echo $lon_center?>", '_blank');
    });
      
    const circle = new google.maps.Circle({
      strokeColor: "#FF0000",
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: "#FF0000",
      fillOpacity: 0.35,
      map,
      center: point,
      radius: <?php echo $radius?>,
    });
  }
  else {
    var locations = <?php echo json_encode($locations, JSON_NUMERIC_CHECK)?>;
    var center_point = { lat: <?php echo $lat_center?>, lng: <?php echo $lon_center?>};
    console.log("Locations:");
    console.log(locations);
      
    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 15,
      center: center_point,
    });
        
    var infowindow = new google.maps.InfoWindow();
    
    var marker, i;
        
    for (i = 0; i < locations.length; i++) {  
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(locations[i][1], locations[i][2]),
        map: map
      });
          
      google.maps.event.addListener(marker, 'click', (function() {
        window.open("https://www.google.com/maps/search/?api=1&query=<?php echo $lat_center?>,<?php echo $lon_center?>", '_blank');
          
      }
    ))};
        
    const circle = new google.maps.Circle({
      strokeColor: "#FF0000",
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: "#FF0000",
      fillOpacity: 0.35,
      map,
      center: center_point,
      radius: <?php echo $radius?>,
    });
  }
}

window.initMap = initMap;
</script>