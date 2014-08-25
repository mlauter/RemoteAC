// $("#radio_on").click(function(e) {
//     console.log('clicked')
//     $.get('/switch_state',function(data){
//         if (data.running) {
//             $(e.target).text('Turn off')
//             $("#on_off_span").text('on')
//         } else {
//             $(e.target).text('Turn on')
//             $("#on_off_span").text('off')
//         }   
//     });     
// });



// if (homeMode==0){
//     $('#radio_away').prop('checked', true)
//     $('#set_temperature').hide();           
// } else {
//     $('#radio_home').prop('checked', true)
//     $('#set_temperature').show();
// }

// if (desiredTemp){
//     $('#desired_temp').val(desiredTemp)
// }

// $('#set_temperature').submit(function() {
//     var $desiredTemp = $('#desired_temp');
//     if (!$desiredTemp.val()) return false;
//     localStorage.setItem('desiredTemp',$desiredTemp.val());

//     return false;
// });


$(document).ready(function() {
    // populate the inputs with current state of the AC
    $.get('/switch_state',function(data) {
        var state_num = data.state_num;
        var goal_temp = data.goal_temp;
        if (state_num == 3) {
            $('#radio_away').prop('checked',false);
            $('#radio_home').prop('checked',true);
            $('#temperature').val(goal_temp);
        } else {
            $('#radio_away').prop('checked',true);
            $('#radio_home').prop('checked',false);
            $('#temptext').css('color','grey')
            $('#temperature').prop('disabled',true);

        }
    });
    // show temp box if home mode is checked
    $('#radio_home').click(function() {
        $('#temptext').css('color','black')
        $('#temperature').prop('disabled',false);
    });
    // hide if away mode is checked
    $('#radio_away').click(function() {
        $('#temptext').css('color','grey')
        $('#temperature').prop('disabled',true);
    });
    // submit input values to server on click 
    $('#submit').click(function() {
        var power_state = $('#radio_on').prop('checked');
        console.log(power_state);
        var mode = $('#radio_home').prop('checked');
        console.log(mode);
        var temp = $('#temperature').val();
        console.log(temp);
        $('#clock').load('index' + ' #clock');
        $.post('/switch_state',{
            'desired_power_state':power_state,
            'desired_mode_is_home':mode,
            'desired_temp':temp
        },
        function(data){
            // wait for the ac response, then repopulate the page with new info
            console.log('got response')
            $.post('/switch_state',data, function(data) {
                var is_running = data.is_running;
                var room_temp = room_temp;
                var state_num = data.state_num;
                var goal_temp = data.goal_temp;
                if (state_num == 3) {
                    $('#radio_away').prop('checked',false);
                    $('#radio_home').prop('checked',true);
                    $('#temperature').val(goal_temp);
                } else {
                    $('#radio_away').prop('checked',true);
                    $('#radio_home').prop('checked',false);
                    $('#temptext').css('color','grey')
                    $('#temperature').prop('disabled',true);

                }
            });
        });
    }); 
});