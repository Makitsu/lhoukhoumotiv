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
        success: function(answer) {
            data = answer
            alert('fonctionne')
            $( "#city_welcome" ).append(data['city_name']);
            $( "#city_region" ).append(data['region']);
            $( "#city_departement" ).append(data['departement']);
            $( "#city_population" ).append(data['population']);
            $( "#city_densite" ).append(data['densite']);
            $( "#city_gentile" ).append(data['gentile']);
            $( "#city_altitude" ).append(data['altitude']);
            $( "#city_superficie" ).append(data['superficie']);
            $('#background').css({'background-image': data['city_img']});
            if (data['items']['availability'] != 0) {
                alert(data['items']['link'][0])
                for (let i = 0; i < 13; i++){
                    let str = "img_src_%s".replace('%s',(i + 1).toString())
                    let str2 = "img_title_%s".replace('%s',(i + 1).toString())
                    console.log(str)
                    document.getElementById(str).title = data['items']['name'][i];
                    document.getElementById(str).onclick = function() {window.open(data['items']['link'][i], '_blank')};
                    document.getElementById(str).src = data['items']['img'][i];
                    document.getElementById(str2).append(data['items']['name'][i]);
                }

            } else {
                document.getElementById("#items_container").style.display = "none";
              }
            },
        error: function(output){
            console.log('error');
        },
    });
});

