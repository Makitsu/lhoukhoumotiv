
$("#logout").hide();

 $(document).on('click','#signin',function() {
    let user = $('#user').val()
    let password = $('#password').val();
    $.ajax({
        url: "/login",
        type: "post",
        data: {
            'user': user,
            'password':password
        },
        success: function(response) {
            if(response == 'user not registered'){
                $("#user").val("");
                $("#password").val("");
            }
            else if(response == 'wrong password'){
                $("#user").val("");
                $("#password").val("");
            }else{
                data = response[0];
                console.log(data)
                nom = data['nom'];
                prenom = data['prenom'];
                age = data['age'];
                user_id = data['user-id'];
                card = data['cards'];
                card_id = data['cards-id'];
                token = data['token']
                $('#infos').text("Bon retour, "+$("#user").val()+" ,prêt à voyager ?");
                $('#user_msg').html("<p>"+nom+" "+prenom+" ,prêt à voyager ? \n   id: "+user_id+"\n    card: "+card+"\n   token: "+token+"</p>");

                $('#myModal').show()
                $("#infos").show();
                $("#user").show();
                $("#password").show();
                $("#user").hide();
                $("#password").hide();
                $("#signin").hide();
                $("#signup").hide();
                $("#logout").show();
            }
        },
    });
});

$(document).on('click','#signup',function() {
    $.ajax({
        url: "/signup",
        type: "post",
        data: {
            'user': user,
            'password':password
        },
        success: function(response) {

        },
    });
});

$(document).on('click','#logout',function() {
    $("#logout").hide();
    $("#user").val("");
    $("#password").val("");
    $('#infos').text("")
    $("#user").show();
    $("#password").show();
    $("#signin").show();
    $("#signup").show();
});