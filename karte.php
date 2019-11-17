<!-- Theme Made By www.w3schools.com -->
<!--Quelle Template: https://www.w3schools.com/bootstrap/bootstrap_theme_company.asp-->
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>Bachelorarbeit</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Leaflet Imports-->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.5.1/dist/leaflet.css" integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ==" crossorigin=""/>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"
    integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo"
    crossorigin="anonymous"></script>
    <script src="https://unpkg.com/leaflet@1.5.1/dist/leaflet.js"
    integrity="sha512-GffPMF3RvMeYyc1LWMHtK8EbPv0iNZ8/oTtHPx9/cc2ILxQ+u905qIwdpULaqDkyBKgOaB57QTMg7ztg8Jm2Og=="
    crossorigin=""></script>

    <!-- Bootstrap und Fonts Imports-->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">
    <link href="https://fonts.googleapis.com/css?family=Montserrat" rel="stylesheet" type="text/css">
    <link href="https://fonts.googleapis.com/css?family=Lato" rel="stylesheet" type="text/css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script>

    <!-- CSS Import-->
    <link rel="stylesheet" href="karte-css.css">
  </head>

  <body id="myPage" data-spy="scroll" data-target=".navbar" data-offset="60">
    <!-- Container (Header Line Section) -->
    <nav class="navbar navbar-fixed-top">
        <p class="navbar logo">Technik <b>Hochschule Mainz</b> University of Applied Sciences</p>
    </nav>

    <!-- Container (Heading Section) -->
    <div class="jumbotron text-center">
      <h1>Räumliche Verortung von textbasierten Social Media Einträgen</h1> 
      <h2 class="header">Bachelorarbeit von Svenja Ruthmann</h2> 
    </div>

    <!-- Container (Map Section) -->
    <div id="mapContainer" class="container-fluid">
      <h1 class = "h2">Locations der Tweets </h2>
      <div id="map"></div>
      <div id="dTable">
        <table id="table" class="table table-bordered table-striped">
          <thead id="thead"></thead>
        </table>
      </div>
    </div>

    <?php       
      if (isset($_GET['abgeschickt'])) {
        //Copy settings from start page
        $account = $_GET['police'];
        $anzahl = $_GET['anzahlTweets'];
        
        //Run Python programs
        shell_exec("python GetTweets.py $account $anzahl");
        shell_exec('python DetectPositionGerman.py');
        shell_exec('python DetectCoordinates.py');
      }
      else {
        print "<p>Sie müssen zuerst Daten eingeben. Gehen Sie bitte 
        <a href=\"startseite.html\">zum Portal</a>
        </p>; "; 
      }
      
    ?>

    <script>
      //Creating a table with column headers for the tweets
      var thead = document.getElementById("thead");
      var row = thead.insertRow(0);
      var tweetID = row.insertCell(0);
      var tweetText = row.insertCell(1);
      var tweetUser = row.insertCell(2);
      var tweetDate = row.insertCell(3);
      var tweetLoc = row.insertCell(4);
      tweetID.innerHTML = "ID";
      tweetText.innerHTML = "Text";
      tweetUser.innerHTML = "User";
      tweetDate.innerHTML = "Date";
      tweetLoc.innerHTML = "Ort";
      num = 1;

      //If all scripts have been executed, the map will be loaded
      $(document).ready(function () {
        //Insert the map
        var map = L.map('map', {
          center: [50, 8],
          zoom: 8
          });
        L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          'attribution': 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
          }).addTo(map);
        
        //Create a marker group to store the markers
        var markerGroup = new L.featureGroup();

        <?php
          //open a file and read a line to the end of the file
          $fcoordinates = fopen("coordinates.txt","r");
          while(! feof($fcoordinates)){
            $line=fgets($fcoordinates);	
            if($line != ""){
        ?>		
              //load a line in Json-Format
              var line = JSON.stringify(<?php print($line);?>);
              var line = JSON.parse(line);

              //store line in variables
              var text = line.text;
              var date = line.date;
              var author = line.author;
              var location = line.location;
              var label = line.locLabel;
              var latitude = line.latitude;
              var longitude = line.longitude;

              //create a marker at the location and add it to marker group
              var marker = L.marker([latitude, longitude], {
              clickable: true
              })
              .bindPopup("ID: " + num + "<br> User: "+ author + "<br> Erscheinungsdatum: " + date + "<br> Ort: " + label)
              .addTo(map);

              marker.addTo(markerGroup)

              //add information of this location in the table
              var table = document.getElementById("table");
              var row = table.insertRow(num);
              var tweetID = row.insertCell(0);
              var tweetText = row.insertCell(1);
              var tweetUser = row.insertCell(2);
              var tweetDate = row.insertCell(3);
              var tweetLoc = row.insertCell(4);
              tweetID.innerHTML = num;
              tweetText.innerHTML = text;
              tweetUser.innerHTML = author;
              tweetDate.innerHTML = date;
              tweetLoc.innerHTML = label;
              num += 1;

        <?php
            }
          }	
          //close file
          fclose($fcoordinates);
        ?>
        
        //Focus map on marker
        map.fitBounds(markerGroup.getBounds());
      });
        
    </script>

    <!--Button back to start page-->
    <a href="startseite.html" class="btn btn-default btn-lg">Zurück zur Startseite</a>


    <!-- Source of Template -->
    <footer class="container-fluid text-center">
      <a href="#myPage" title="To Top">
        <span class="glyphicon glyphicon-chevron-up"></span>
      </a>
      <p>Bootstrap Theme Made By <a href="https://www.w3schools.com" title="Visit w3schools">www.w3schools.com</a></p>
    </footer>

  </body>
</html>