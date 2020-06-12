
$(document).ready(function(){
    var stations_name = $('#stations_name').data("playlist").split(',');
    var stations_pos = $('#stations_pos').data("playlist");
    var map = L.map(
        "map",
        {
            center: [49.21164026, 3.98878814],
            crs: L.CRS.EPSG3857,
            zoom: 6,
            zoomControl: true,
            preferCanvas: false,
        }
    );
    var tile_layer = L.tileLayer(
        "https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}{r}.png",
        {"attribution": "\u0026copy; \u003ca href=\"https://www.openstreetmap.org/copyright\"\u003eOpenStreetMap\u003c/a\u003e contributors \u0026copy; \u003ca href=\"https://carto.com/attributions\"\u003eCARTO\u003c/a\u003e", "detectRetina": false, "maxNativeZoom": 18, "maxZoom": 18, "minZoom": 0, "noWrap": false, "opacity": 1, "subdomains": "abc", "tms": false}
    ).addTo(map);

    var route = L.featureGroup().addTo(map)

    var markers = []
    function add_destination(name,position){
        var marker_destination = L.marker(
            [position[1],position[0]],
            {}
        );
        markers.push(marker_destination)
        var custom_icon = L.icon({"iconSize": [20, 20], "iconUrl":"static/img/placeholder.png"});
         marker_destination.setIcon(custom_icon);
        var popup = L.popup({"maxWidth": "100%"});
        var city = name.toLowerCase().replace(' ','');
        var html = $('<a id="html_'+name+'" style="width: 100.0%; height: 100.0%;" href="destination?city='+city+'" target="_blank""><br>'+name+'<br></a>')[0];

        popup.setContent(html);
        marker_destination.bindPopup(popup);
        route.addLayer(marker_destination);
    }
    var destination_length = stations_name.length;
    for (var i = 0; i < destination_length; i++) {
        var name = stations_name[i].replace("\"","").replace("'","").replace("'","").replace(']','').replace('[','')
        console.log(name)
        console.log(stations_pos[i])
        add_destination(name,stations_pos[i])
    }


    map.fitBounds(route.getBounds());

});





