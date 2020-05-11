 // Example starter JavaScript for disabling form submissions if there are invalid fields

$(document).on('click','#api_call', function(ev) {
    ev.preventDefault();
    let departure = $('#list_stations').val()
    let arrival = $('#list_arrival').val();
    arrival = arrival.join(',')
    let date = new Date($('#trip_date').val());
    day = date.getDate();
    month = ("0" + day).slice(-2);
    month = date.getMonth() + 1;
    day = ("0" + day).slice(-2);
    year = date.getFullYear();
    console.log(departure)
    console.log(arrival)
    console.log(date)
    if(departure != '' && arrival != '' && date !='Invalid Date'){
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
                alert(data)
                data = response;

                $("#trip_table").empty()

                for(var i = 0, size = data['city'].length; i < size ; i++){
                        var tr = $("<tr id=\"r"+i.toString()+"\" >");
                        tr.append($("<td width=\"20%\">").text(data['city'][i]));
                        tr.append($("<td width=\"20%\">").text(data['time'][i]));
                        tr.append($("<td width=\"20%\">").text(data['price'][i]));
                        tr.append($("<td width=\"20%\">").text(data['type'][i]));
                        tr.append($("<td width=\"20%\">").text(data['category'][i]));

                        $("#trip_table").append(tr);
                }
            },
            error: function(output){
                console.log('error');
            },
        });
     
    }
});