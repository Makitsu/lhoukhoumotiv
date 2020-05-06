$("#porco").click(function(){
    var start_stat;
    $('#st').each(function(){
        start_stat = this.name;
    });

    $.ajax({
        url: "/station/map",
        type: "post",
        data: {
            'start_station': start_stat
        },
        success: function(response) {
        $("#map_container").html(response);
        },
    });
    $.ajax({
        url: "/station/info",
        type: "post",
        data: {
            'start_station': start_stat
        },
        success: function(response) {
            data = response;
            $("#trip_table").empty()

            for(var i = 0, size = data['arrival_code'].length; i < size ; i++){
                    var tr = $("<tr>");
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
    }).always(function(){
    $(#test2).LoadingOverlay("hide",true);
    });;


});