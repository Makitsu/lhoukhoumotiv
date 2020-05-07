//<script src="{{ url_for('static', filename='js/provide_info.js') }}"></script>

$(document).ready(function() {
    var city_name = 'Strasbourg';
        $.ajax({
            url: "/station/info",
            type: "POST",
            data: {
                'city_name': city_name
            },
            success: function(response) {
                $( "#city_info" ).html(response);
                $( "#city_name" ).append( "<p>Test</p>" );
            },
            error: function(output){
                console.log('error');
            },
        });
    });
})
