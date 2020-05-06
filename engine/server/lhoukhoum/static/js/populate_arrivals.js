var departure;
var arrival;
$(document).on('change','#list_stations',function() {
    departure = $(this).val()
    $("#arrivals").empty()
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

    //calculate destination price
    $.ajax({
        url: "/station/info",
        type: "POST",
        data: {
            'start_station': departure
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


$(document).on('change','#list_arrival',function() {
    arrival = $(this).val()
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

    var table = document.getElementById("trip_table").rows;
    console.log(arrival)

    for (var i = table.length-1; i >=0; i--) {

        var equals = table[i].cells[0].innerHTML.localeCompare(arrival)
        console.log(equals)
        if(equals != 0){
           var nb = table[i].rowIndex;
           console.log("#r"+i.toString());
           $("#r"+i.toString()).remove();
        }

    }
    console.log(document.getElementById("trip_table"))
;

});