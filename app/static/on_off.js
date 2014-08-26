$(document).ready(function() {
    // populate the inputs with current state of the AC
    $.get('/switch_state',function(data) {
        var stateNum = data.stateNum;
        console.log(stateNum)
        var goalTemp = data.goalTemp;
        if (stateNum == 1) {
            $('#radio_on').prop('checked', false);
        } else {
            $('#radio_on').prop('checked', true);            
        }
        if (stateNum == 3) {
            $('#radio_away').prop('checked',false);
            $('#radio_home').prop('checked',true);
            $('#temperature').val(goalTemp);
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
        $('#radio_on').click()
    });
    // hide if away mode is checked
    $('#radio_away').click(function() {
        $('#temptext').css('color','grey')
        $('#temperature').prop('disabled',true);
        $('#temperature').val('');
    });

    // reset to away if off is clicked
    $('#radio_off').click(function() {
        $('#radio_away').click();
    });
    // submit input values to server on click 
    $('#submit').click(function() {
        var powerState = $('#radio_on').prop('checked');
        console.log(powerState);
        var mode = $('#radio_home').prop('checked');
        console.log(mode);
        var temp = $('#temperature').val();
        console.log(temp);
        var dataToSend = {
            'desired_power_state':powerState,
            'desired_mode_is_home':mode,
            'desired_temp':temp
        };

        // reload the clock
        $('#clock').load('index' + ' #clock');
        // post to switch_state route

        $.ajax({
          url:'/switch_state',
          type:"POST",
          data:JSON.stringify(dataToSend),
          contentType:"application/json; charset=utf-8",
          async: false,
          success: function(data){
                console.log('got response')
            // wait for the ac response, then repopulate the page with new info
                var isRunning = data.isRunning;
                var roomTemp = data.roomTemp;
                var stateNum = data.stateNum;
                var goalTemp = data.goalTemp;
                $('#room_temp_span').html(roomTemp)
                if (isRunning == 1) {
                    $('#on_off_span').html('on')
                } else {
                    $('#on_off_span').html('off')                    
                }
                if (stateNum == 3) {
                    $('#radio_away').prop('checked',false);
                    $('#radio_home').prop('checked',true);
                    $('#temperature').val(goalTemp);
                } else {
                    $('#radio_away').prop('checked',true);
                    $('#radio_home').prop('checked',false);
                    $('#temptext').css('color','grey')
                    $('#temperature').prop('disabled',true);
                }
            }
        });
    }); 
});