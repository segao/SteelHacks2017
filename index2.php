<!DOCTYPE HTML>
<html lang="en-US">
<head>
    <meta charset="UTF-8">
    <title>SteelHacks 2017</title>
    <link href="https://fonts.googleapis.com/css?family=PT+Sans+Narrow:400,700" rel="stylesheet">
    <link rel="icon" type="image/x-icon" href="img/favicon.ico">
    <link href="css/styles.css" type="text/css" rel="stylesheet">
</head>
<body>
<div id = "rays">
    <div id = "ray1"></div>
    <div id = "ray2"></div>
    <div id = "ray3"></div>
    <div id = "ray4"></div>
    <div id = "ray5"></div>
    <div id = "ray6"></div>
    <div id = "ray7"></div>
    <div id = "ray8"></div>
</div>
<div id = "baby">
    <div id = "head"></div>
    <div id = "container">
        <div id = "butt"></div>
        <div id = "body"></div>
        <div id = "arm"></div>
        <div id = "leg"></div>
    </div>
</div>
<script src="js/scriptini.js"></script>
<?php
/**
 * Created by PhpStorm.
 * User: David Duan
 * Date: 2/11/2017
 * Time: 2:07 AM
 */
while (1){
    $con = mysqli_connect("localhost", "root", "david123") or die ("not connecting");
    mysqli_select_db($con, "babydata") or die("can't access db");
    $query = mysqli_query($con,"SELECT * FROM babycheck WHERE babyCheck='1'");
    $row = mysqli_fetch_array($query);
    if ($row != "") {
        break;
    }
    if(sleep(1)!=0)
    {
        echo "sleep failed script terminating";
        break;
    }
    echo"scanning";
    flush();
    ob_flush();
}

?>
<div id = "escape">THE BABY IS ON THE MOVE</div>
<script src="js/script.js"></script>
</body>
</html>
