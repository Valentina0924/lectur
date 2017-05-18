var map;
var tipo_funcion;
var objetoE;
var marker_f;
function myMap(){

// alert("llamado")
var mapProp= {
    center:new google.maps.LatLng(51.508742,-0.120850),
    zoom:13,
};


 map=new google.maps.Map(document.getElementById("googleMap"),mapProp);



var retro= [
          {elementType: 'geometry', stylers: [{color: '#ebe3cd'}]},
          {elementType: 'labels.text.fill', stylers: [{color: '#523735'}]},
          {elementType: 'labels.text.stroke', stylers: [{color: '#f5f1e6'}]},
          {
            featureType: 'administrative',
            elementType: 'geometry.stroke',
            stylers: [{color: '#c9b2a6'}]
          },
          {
            featureType: 'administrative.land_parcel',
            elementType: 'geometry.stroke',
            stylers: [{color: '#dcd2be'}]
          },
          {
            featureType: 'administrative.land_parcel',
            elementType: 'labels.text.fill',
            stylers: [{color: '#ae9e90'}]
          },
          {
            featureType: 'landscape.natural',
            elementType: 'geometry',
            stylers: [{color: '#dfd2ae'}]
          },
          {
            featureType: 'poi',
            elementType: 'geometry',
            stylers: [{color: '#dfd2ae'}]
          },
          {
            featureType: 'poi',
            elementType: 'labels.text.fill',
            stylers: [{color: '#93817c'}]
          },
          {
            featureType: 'poi.park',
            elementType: 'geometry.fill',
            stylers: [{color: '#a5b076'}]
          },
          {
            featureType: 'poi.park',
            elementType: 'labels.text.fill',
            stylers: [{color: '#447530'}]
          },
          {
            featureType: 'road',
            elementType: 'geometry',
            stylers: [{color: '#f5f1e6'}]
          },
          {
            featureType: 'road.arterial',
            elementType: 'geometry',
            stylers: [{color: '#fdfcf8'}]
          },
          {
            featureType: 'road.highway',
            elementType: 'geometry',
            stylers: [{color: '#f8c967'}]
          },
          {
            featureType: 'road.highway',
            elementType: 'geometry.stroke',
            stylers: [{color: '#e9bc62'}]
          },
          {
            featureType: 'road.highway.controlled_access',
            elementType: 'geometry',
            stylers: [{color: '#e98d58'}]
          },
          {
            featureType: 'road.highway.controlled_access',
            elementType: 'geometry.stroke',
            stylers: [{color: '#db8555'}]
          },
          {
            featureType: 'road.local',
            elementType: 'labels.text.fill',
            stylers: [{color: '#806b63'}]
          },
          {
            featureType: 'transit.line',
            elementType: 'geometry',
            stylers: [{color: '#dfd2ae'}]
          },
          {
            featureType: 'transit.line',
            elementType: 'labels.text.fill',
            stylers: [{color: '#8f7d77'}]
          },
          {
            featureType: 'transit.line',
            elementType: 'labels.text.stroke',
            stylers: [{color: '#ebe3cd'}]
          },
          {
            featureType: 'transit.station',
            elementType: 'geometry',
            stylers: [{color: '#dfd2ae'}]
          },
          {
            featureType: 'water',
            elementType: 'geometry.fill',
            stylers: [{color: '#b9d3c2'}]
          },
          {
            featureType: 'water',
            elementType: 'labels.text.fill',
            stylers: [{color: '#92998d'}]
          }];
map.setOptions({styles: retro});


getPosition();
google.maps.event.addListener(map, 'click', function(event) {
   eventoClick(map, event.latLng);
 });
}


function getPosition() {

   var options = {
      enableHighAccuracy: true,
      maximumAge: 3600000
   }

   var watchID = navigator.geolocation.getCurrentPosition(onSuccess, onError, options);

   function onSuccess(position) {

      // alert('Latitude: '          + position.coords.latitude          + '\n' +
      //    'Longitude: '         + position.coords.longitude         + '\n' +
      //    'Altitude: '          + position.coords.altitude          + '\n' +
      //    'Accuracy: '          + position.coords.accuracy          + '\n' +
      //    'Altitude Accuracy: ' + position.coords.altitudeAccuracy  + '\n' +
      //    'Heading: '           + position.coords.heading           + '\n' +
      //    'Speed: '             + position.coords.speed             + '\n' +
      //    'Timestamp: '         + position.timestamp                + '\n');
         var lat =position.coords.latitude;
        var lon=position.coords.longitude;
        var c = new google.maps.LatLng(lat,lon);
        map.setCenter(c);
        addMarker(lat, lon);

         };



   function onError(error) {
      alert('code: '    + error.code    + '\n' + 'message: ' + error.message + '\n');
   }
}

function watchPosition() {

   var options = {
      maximumAge: 3600000,
      timeout: 3000,
      enableHighAccuracy: true,
   }

   var watchID = navigator.geolocation.watchPosition(onSuccess, onError, options);

   function onSuccess(position) {

      // alert('Latitude: '          + position.coords.latitude          + '\n' +
      //    'Longitude: '         + position.coords.longitude         + '\n' +
      //    'Altitude: '          + position.coords.altitude          + '\n' +
      //    'Accuracy: '          + position.coords.accuracy          + '\n' +
      //    'Altitude Accuracy: ' + position.coords.altitudeAccuracy  + '\n' +
      //    'Heading: '           + position.coords.heading           + '\n' +
      //    'Speed: '             + position.coords.speed             + '\n' +
      //    'Timestamp: '         + position.timestamp                + '\n');


         var lat =position.coords.latitude;
        var lon=position.coords.longitude;
        var c = new google.maps.LatLng(lat,lon);
        map.setCenter(c);

   };



   function onError(error) {
      alert('code: '    + error.code    + '\n' +'message: ' + error.message + '\n');
   }

}





function addMarker(lat, lon) {

  var myCenter = new google.maps.LatLng(lat,lon);
  var marker = new google.maps.Marker({
    position: myCenter,
    icon: "http://127.0.0.1:8000/static/imagenes/libro.png",
    draggable: false,
    animation: google.maps.Animation.BOUNCE
  });

  marker_f=marker;
  marker.setMap(map);
}



function placeMarker(map, location) {
  var marker = new google.maps.Marker({
    position: location,
    animation: google.maps.Animation.DROP,
    draggable: false,    
    icon: "http://127.0.0.1:8000/static/imagenes/libro.png",
    map: map
  });
  marker_f=marker;

  var infowindow = new google.maps.InfoWindow({
    content: 'Latitude: ' + location.lat() + '<br>Longitude: ' + location.lng()
  });
  infowindow.open(map,marker);
}

function moveMarker(map, location) {
  //alert(aaaa);
}


function eventoClick(map, location){
switch(tipo_funcion){
  case 1: // poner marcadores
   placeMarker(map, location);
 //   objetoE.actualizar_coordenadas(map, location);
  break;

  case 2: // poner marcadores
    $("#id_latitud").val(location.lat());
    $("#id_longitud").val(location.lng());
    var latlng = new google.maps.LatLng(location.lat(),location.lng());
    marker_f.setPosition(latlng);
  //  marker_f.setPosition();
  break;
}

}



function agregarMarkeralClick()
{
  tipo_funcion=2;
    $("#id_latitud").val(marker_f.getPosition().lat());
    $("#id_longitud").val(marker_f.getPosition().lng());

}




function createMarker(lat, lon,nom) {

  var myCenter = new google.maps.LatLng(lat,lon);

  var marker = new google.maps.Marker({
    position: myCenter,
    icon: "http://127.0.0.1:8000/static/imagenes/libro.png",
    draggable: false,
  });
  marker.setMap(map);
  var infowindow = new google.maps.InfoWindow({
    content: nom
  });
  infowindow.open(map,marker);
  //alert(lat+" ___ "+lon+" ___ "+nom)
    return marker;
}

function createMarkerComunidad(lat, lon,nom, contenido, urlimagen, urlcomunidad) {

  var myCenter = new google.maps.LatLng(lat,lon);

  var marker = new google.maps.Marker({
    position: myCenter,
    icon: "http://127.0.0.1:8000/static/imagenes/libro.png",
    draggable: false,
  });
  marker.setMap(map);
  var infowindow = new google.maps.InfoWindow({
    content: nom
  });
  infowindow.open(map,marker);

   google.maps.event.addListener(marker, 'click', function(event) {
        mostrarVentanaMarcador(nom, contenido, urlimagen, urlcomunidad);
   });

  //alert(lat+" ___ "+lon+" ___ "+nom)
    return marker;
}


function changeVisibilityMarker(marker, visible){
  //alert(marker.map+" _ "+visible)
  if(marker!=null){
    if(visible){
      marker.setAnimation(google.maps.Animation.BOUNCE);
       marker.setIcon("http://127.0.0.1:8000/static/imagenes/libro-2.png");     
      if(marker.map==null){
              marker.setMap(map);
            }
    }else{
      if(marker.map!=null){
        marker.setAnimation(null);
        marker.setIcon("http://127.0.0.1:8000/static/imagenes/libro.png");
          //    marker.setMap(null);
            }
    }
  }
}

function ocultarMarker_f(){
  marker_f.setMap(null);
}




