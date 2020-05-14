
 $(document).on('click','#signin',function() {
    let user = $('#user').val();
    let password = $('#password').val();

    if($('#signin').text() == 'Sign in'){
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
                    $('#user_msg').html("<p> User not registered </p>");
                    $('#myModal').show()
                }
                else if(response == 'wrong password'){
                    $("#password").val("");
                    $('#user_msg').html("<p> Wrong password </p>");
                    $('#myModal').show()
                }else{
//                    window.onbeforeunload = function() {
//                        localStorage.setItem("name", $('#inputName').val());
//                        localStorage.setItem("email", $('#inputEmail').val());
//                        localStorage.setItem("phone", $('#inputPhone').val());
//                        localStorage.setItem("subject", $('#inputSubject').val());
//                        localStorage.setItem("detail", $('#inputDetail').val());
//                        // ...
//                    }

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
                    $("#signup").hide();
                    $("#signin").text('Log out');
                    window.location.reload();

                }
            },
        });
    }else{
        $.ajax({
            url: "/logout",
            type: "post",
            data: {
            },
            success: function(response) {
                alert('log out')
            },
        });
        location.reload();
        $("#user").val("");
        $("#password").val("");
        $('#infos').text("")
        $("#user").show();
        $("#password").show();
        $("#signin").text('Sign in');
        $("#signup").show();
    }

});

$(document).on('click','#signup',function() {
    let user = $('#user').val();
    let password = $('#password').val();

    $.ajax({
        url: "/signup",
        type: "post",
        data: {
            'user': user,
            'password':password
        },
        success: function(response) {
            if(response == 'user created'){
                $('#user_msg').html("<p> Welcome "+user+"! </p>");
                $('#myModal').show()
            }
            else if(response == 'user already registered'){
                $('#user_msg').html("<p> User already registered </p>");
                $('#myModal').show()
            }else{

            }
        },
    });
});
