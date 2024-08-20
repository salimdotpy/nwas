
var cord_pos = {lat: 7.7200717, lng: 4.41305};

//Get location function
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.watchPosition(showPosition, showError, {enableHighAccuracy: true, maximumAge: 5000});
    } else {
        toast_it({ text: 'Geolocation is not supported by this browser.', icon: 'error' });
    }
}

function showPosition(position) {
    cord_pos = position ?
    {lat: position.coords.latitude, lng: position.coords.longitude} :
    {lat: 6.1334096, lng: 6.8075828};
}
function showError(error) {
    var x = "";
    switch (error.code) {
        case error.PERMISSION_DENIED:
            x = "User denied the request for Geolocation.";
            break;
        case error.POSITION_UNAVAILABLE:
            x = "Location information is unavailable.";
            break;
        case error.TIMEOUT:
            x = "The request to get user location timed out.";
            break;
        case error.UNKNOWN_ERROR:
            x = "An unknown error occurred.";
            break;
    }
    toast_it({ text: x, icon: 'warning' });
    cord_pos = {lat: 6.1334096, lng: 6.8075828};
}

//Map function start here-----------------------------------------------------------------------------------

var myMarker, mc = 0, map, mapType = ["hybrid","roadmap","satellite","terrain", 0];

function initMap() {
    getLocation();
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 17,
        center: cord_pos,
        mapTypeId: google.maps.MapTypeId.SATELLITE
    });
    placeMarker(cord_pos, true);
    google.maps.event.addListener(map, 'click', function (event) {
        if(pick){
            toast_it({ text: 'Click pick button to pick current coordinate!', icon: 'info' });
        }else{
            placeMarker(event.latLng, false, true);
        }
    });
}

function changeMap() {
    map.setMapTypeId(mapType[mapType[-1]]);
    if (mapType[-1] < 3) mapType[-1] += 1;
    else mapType[-1] = 0;
}
function updateLocation(){
    getLocation()
    placeMarker(cord_pos, false, false);
    map.setCenter(cord_pos);
    $.ajax({
        url: '/forgetRestPass',
        method: 'post',
        data: 'ajax=1&forgotP=1',
        success: function (res) {
            
        },
        error: function (e) {
            console.log(e);
        }
    })
}

function centerMap() {
    getLocation();
    map.setCenter(cord_pos);
    placeMarker(cord_pos, false, false);
}

function placeMarker(location, init=false, multi=false) {
    if (init) {
        myMarker = new google.maps.Marker({
            position: location,
            map: map,
            animation: google.maps.Animation.DROP
        });
        mc = 1;
    }
    else if (multi) {
        if (mc == 1) {
            myMarker.setPosition(location);
            mc = 0;
        } else {
            myMarker = new google.maps.Marker({
                position: location,
                map: map,
                animation: google.maps.Animation.RAISE
            });
        }
    }
    else if (myMarker == undefined) {
        myMarker = new google.maps.Marker({
            position: location,
            map: map,
            animation: google.maps.Animation.DROP
        });
    }
    else {
        myMarker.setPosition(location);
    }
}