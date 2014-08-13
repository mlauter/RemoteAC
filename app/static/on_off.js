$("#on_off_switch").click(function(e) {
    console.log('clicked')
    $.get('/switch_state',function(data){
        if (data.running) {
            $(e.target).text('Turn off')
            $("#on_off_span").text('on')
        } else {
            $(e.target).text('Turn on')
            $("#on_off_span").text('off')
        }   
    });     
});


$('#radio_home').click(function() {
    $('#set_temperature').show();
    localStorage.setItem('homeMode',1)
});

$('#radio_away').click(function() {
    $('#set_temperature').hide();
    localStorage.setItem('homeMode',0)
});    

var homeMode = localStorage.getItem('homeMode');
var desiredTemp = localStorage.getItem('desiredTemp');

if (homeMode==0){
    $('#radio_away').prop('checked', true)
    $('#set_temperature').hide();           
} else {
    $('#radio_home').prop('checked', true)
    $('#set_temperature').show();
}

if (desiredTemp){
    $('#desired_temp').val(desiredTemp)
}

$('#set_temperature').submit(function() {
    var $desiredTemp = $('#desired_temp');
    if (!$desiredTemp.val()) return false;
    localStorage.setItem('desiredTemp',$desiredTemp.val());

    return false;
});