$(document).ready(function() {
    // define ajaxStart and Stop functions
    $(document).ajaxStart(function() {
        $('body').css({'cursor':'progress'});

    }).ajaxStop(function() {
        $('body').css({'cursor':'default'});
    });
    // populate the inputs with current state of the AC
    $.get('/switch_state',function(data) {
        var stateNum = data.state_num;
        console.log(stateNum)
        var goalTemp = data.goal_temp;
        if (stateNum == 1) {
            $('#radio_on').prop('checked', false);
            $('#radio_off').prop('checked',true)
        } else {
            $('#radio_off').prop('checked',false)
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
        // check that temp is a number and is in a reasonable temperature range or set to empty string if we don't need it
        if (mode === true) {
            var temp = $('#temperature').val();
        } else {
            var temp = ''
        }

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
          timeout: 20000, 
          // give the ac 20 seconds
          success: function(data){
                console.log('got response')
            // wait for the ac response, then repopulate the page with new info
                var isRunning = data.is_running;
                var roomTemp = data.room_temp;
                var stateNum = data.state_num;
                var goalTemp = data.goal_temp;
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
            },
          error: function() {
            alert("The air conditioner did not get your request!")
          }
        });
        
    }); 
});