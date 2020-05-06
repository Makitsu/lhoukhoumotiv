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

$(document).on('change','#list_arrival',function() {
    arrival = $('#list_arrival').children("option:selected").val();
    alert(departure)
    alert(arrival)
    //generate map
    $.ajax({
        url: "/station/map/absolute",
        type: "post",
        data: {
            'start_station': departure,
            'stop_station': arrival
        },
        success: function(response) {
        $("#map_container").html(response);
        },
    });
});

$(document).on('change','#trip_date',function() {
    date = $(this).val()
    $("#list_arrival").empty()
    //calculate destination price
    if($(this).prop("checked") == true){
        $.ajax({
            url: "/station/info/price",
            type: "POST",
            data: {
                'start_station': arrival,
                'stop_station': departure,
                'trip_date': date
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
    }
    else if($(this).prop("checked") == false){
        alert("pricing api not activated");
    }
});