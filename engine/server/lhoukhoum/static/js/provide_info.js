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
            if (data['items']['availability'] != 0) {
                alert('good')
                alert(data['items']['name'][0])
                $( "#item_name_1" ).append(data['items']['name'][0]);
                document.getElementById("img_src_1").src = data['items']['img'][0];
                document.getElementById("img_href_1").href = data['items']['link'][0];
                $( "#item_name_2" ).append(data['items']['name'][1]);
                document.getElementById("img_src_2").src = data['items']['img'][1];
                document.getElementById("img_href_2").href = data['items']['link'][1];
                $( "#item_name_3" ).append(data['items']['name'][2]);
                document.getElementById("img_src_3").src = data['items']['img'][2];
                document.getElementById("img_href_3").href = data['items']['link'][2];
                $( "#item_name_4" ).append(data['items']['name'][3]);
                document.getElementById("img_src_4").src = data['items']['img'][3];
                document.getElementById("img_href_4").href = data['items']['link'][3];
               $( "#item_name_5" ).append(data['items']['name'][4]);
                document.getElementById("img_src_5").src = data['items']['img'][4];
                document.getElementById("img_href_5").href = data['items']['link'][4];
                $( "#item_name_6" ).append(data['items']['name'][5]);
                document.getElementById("img_src_6").src = data['items']['img'][5];
                document.getElementById("img_href_6").href = data['items']['link'][5];
                $( "#item_name_7" ).append(data['items']['name'][6]);
                document.getElementById("img_src_7").src = data['items']['img'][6];
                document.getElementById("img_href_7").href = data['items']['link'][6];
                $( "#item_name_8" ).append(data['items']['name'][7]);
                document.getElementById("img_src_8").src = data['items']['img'][7];
                document.getElementById("img_href_8").href = data['items']['link'][7];
                $( "#item_name_9" ).append(data['items']['name'][8]);
                document.getElementById("img_src_9").src = data['items']['img'][8];
                document.getElementById("img_href_9").href = data['items']['link'][8];
                $( "#item_name_10" ).append(data['items']['name'][9]);
                document.getElementById("img_src_10").src = data['items']['img'][9];
                document.getElementById("img_href_10").href = data['items']['link'][9];
                $( "#item_name_11" ).append(data['items']['name'][10]);
                document.getElementById("img_src_11").src = data['items']['img'][10];
                document.getElementById("img_href_11").href = data['items']['link'][10];
                $( "#item_name_12" ).append(data['items']['name'][11]);
                document.getElementById("img_src_12").src = data['items']['img'][11];
                document.getElementById("img_href_12").href = data['items']['link'][11];
            } else {
                document.getElementById("#items_container").style.display = "none";
              }
            },
        error: function(output){
            console.log('error');
        },
    });
});

