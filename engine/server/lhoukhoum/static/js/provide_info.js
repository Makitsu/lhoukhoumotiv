//<script src="{{ url_for('static', filename='js/provide_info.js') }}"></script>

$(document).ready(function() {
    var city_name = window.location.search.substr(1).split("=")[1];
    console.log(city_name);

    $.ajax({
        url: "/station/info",
        type: "POST",
        data: {
            'city_name': city_name
        },
        success: function(response) {
            data = response
            //alert('fonctionne')
            $( "#city_welcome" ).append(data['city_name']);
            $( "#city_region" ).append(data['region']);
            $( "#city_departement" ).append(data['departement']);
            $( "#city_population" ).append(data['population']);
            $( "#city_densite" ).append(data['densite']);
            $( "#city_gentile" ).append(data['gentile']);
            $( "#city_altitude" ).append(data['altitude']);
            $( "#city_superficie" ).append(data['superficie']);
            $('#background').css({'background-image': data['city_img']});
            },
        error: function(output){
            console.log('error');
        },
    });
});

