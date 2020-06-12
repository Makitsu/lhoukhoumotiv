var departure;
var arrival;
var first_research = true

const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds))
}


$(document).on('change','#list_stations',function() {
    departure = $(this).val()
    $("#list_arrival").empty()
    $("#list_arrival").append($("<option value=\"\" disabled>Select a train station</option>"));
    //provide map
    $.ajax({
        url: "/station/map",
        type: "post",
        data: {
            'start_station': departure
        },
        success: function(response) {
        $("#map_container").html(response);
        },
    });
    //create destination list
    $.ajax({
        url: "/station/connection",
        type: "POST",
        data: {
            "start_station": departure
        },
        success: function (response) {
            var tr = $("#list_arrival");
            for (var i in response){
                tr.append($("<option value=\""+response[i]+"\">"+response[i]+"</option>"));
            }
        },

    });
});

$(document).on('change','#list_stations',function() {
    departure = $(this).val()
    $('#map_container').fadeOut(500);
    //provide map

    $.ajax({
        url: "/station/map",
        type: "post",
        data: {
            'start_station': departure
        },
        success: function(response) {
        $("#map_container").html(response);
        },
    });
    //create destination list
    $.ajax({
        url: "/station/connection",
        type: "POST",
        data: {
            "start_station": departure
        },
        success: function (response) {
            var tr = $("#list_arrival");
            for (var i in response){
                tr.append($("<option value=\""+response[i]+"\">"+response[i]+"</option>"));
            }
        },
    });

    sleep(500).then(() => {
          $("#map_container").fadeIn(500);
    })



});

$(document).on('change','#list_arrival',function() {
    arrival = $('#list_arrival').val();
    arrival = arrival.join(',')
    //
    $('#map_container').fadeOut(200);

    //generate map
    $.ajax({
        url: "/station/map/selection",
        type: "post",
        data: {
            'start_station': departure,
            'stop_station' : arrival
        },
        success: function(response) {

        $("#map_container").html(response);
        },
    });

    $("#map_container").fadeIn(200);
});

$(document).on('click','#trip_table tr', function() {
    var city;
    city = $("td").first().text().toLowerCase();
    alert(city)
    window.open(
      'destination?city='+city,
      '_blank' // <- This is what makes it open in a new window.
    );

});

