var current_station;
var data = [];
$(function() {
    $('#list_stations').on('input',function() {
        var opt = $('option[value="'+$(this).val()+'"]');
        current_station = opt.attr('value');
        $('#st').each(function(){
            this.name = opt.attr('value');
        });
    });
});