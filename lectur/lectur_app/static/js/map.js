
function myMap(){

var mapProp= {
    center:new google.maps.LatLng(3.4391842,-76.5112785),
    zoom:13,
};


var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);
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
}

function getPosition() {

   var options = {
      enableHighAccuracy: true,
      maximumAge: 3600000
   }

   var watchID = navigator.geolocation.getCurrentPosition(onSuccess, onError, options);

   function onSuccess(position) {

  //     alert('Latitude: '          + position.coords.latitude          + '\n' +
  //        'Longitude: '         + position.coords.longitude         + '\n' +
  //        'Altitude: '          + position.coords.altitude          + '\n' +
  //        'Accuracy: '          + position.coords.accuracy          + '\n' +
  //        'Altitude Accuracy: ' + position.coords.altitudeAccuracy  + '\n' +
  //        'Heading: '           + position.coords.heading           + '\n' +
  //        'Speed: '             + position.coords.speed             + '\n' +
  //        'Timestamp: '         + position.timestamp                + '\n');
  //  };

   var c = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
   map.setCenter(c);

   function onError(error) {
      alert('code: '    + error.code    + '\n' + 'message: ' + error.message + '\n');
   }
}}

function watchPosition() {

   var options = {
      maximumAge: 3600000,
      timeout: 3000,
      enableHighAccuracy: true,
   }

   var watchID = navigator.geolocation.watchPosition(onSuccess, onError, options);

   function onSuccess(position) {

  //     alert('Latitude: '          + position.coords.latitude          + '\n' +
  //        'Longitude: '         + position.coords.longitude         + '\n' +
  //        'Altitude: '          + position.coords.altitude          + '\n' +
  //        'Accuracy: '          + position.coords.accuracy          + '\n' +
  //        'Altitude Accuracy: ' + position.coords.altitudeAccuracy  + '\n' +
  //        'Heading: '           + position.coords.heading           + '\n' +
  //        'Speed: '             + position.coords.speed             + '\n' +
  //        'Timestamp: '         + position.timestamp                + '\n');
  //  };

  var c = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
  map.setCenter(c);

   function onError(error) {
      alert('code: '    + error.code    + '\n' +'message: ' + error.message + '\n');
   }

}

}



function addMarker(lat, lon) {

  var myCenter = new google.maps.LatLng(lat,lon);
  var marker = new google.maps.Marker({
    position: myCenter,
    animation: google.maps.Animation.BOUNCE
  });
  marker.setMap(map);
}
