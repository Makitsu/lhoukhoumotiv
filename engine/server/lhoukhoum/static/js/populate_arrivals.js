var departure;
var arrival;
$(document).on('change','#list_stations',function() {
    departure = $(this).val()
    $("#list_arrival").empty()
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
    $("#list_arrival").empty()
    $('#map_container').fadeOut(200);
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
            $("#list_arrival").prop("disabled",false);
        },

    });
    $("#map_container").fadeIn(200);
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
        $("#trip_date").prop("disabled",false);
        $("#map_container").html(response);
        },
    });

    $("#map_container").fadeIn(200);
});

$(document).on('change','#trip_date',function() {
    var date = new Date($('#trip_date').val());
    day = date.getDate();
    month = ("0" + day).slice(-2);
    month = date.getMonth() + 1;
    day = ("0" + day).slice(-2);
    year = date.getFullYear();
    //alert([year, month, day].join('-'));
    let selected_date = [year, month, day].join('-')+'T05:00:00+0200'
    //calculate destination price
    $.ajax({
        url: "/station/price",
        type: "POST",
        data: {
            'start_station': departure,
            'stop_station': arrival,
            'trip_date': selected_date
        },
        success: function(response) {

            data = response;
            $("#trip_table").empty()

            for(var i = 0, size = data['arrival_code'].length; i < size ; i++){
                    var tr = $("<tr id=\"r"+i.toString()+"\" >");
                    tr.append($("<td width=\"25%\">").text(data['arrival_code'][i]));
                    tr.append($("<td width=\"25%\">").text(data['price'][i]));
                    tr.append($("<td width=\"25%\">").text(data['type'][i]));
                    tr.append($("<td width=\"25%\">").text(data['category'][i]));

                    $("#trip_table").append(tr);
            }
        },
        error: function(output){
            console.log('error');
        },
    });
});

$(document).on('click','#trip_table tr', function() {
    var city = $("td").first().text();
    //alert(city)
    window.location.href='station/destination/'+city.toLowerCase();
});


