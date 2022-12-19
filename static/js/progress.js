//

$(document).ready(function(){
    $('.toast').toast('show');
});


$(document).ready(function(event){
    // event.preventDefault();
    var source = new EventSource("/progress/{{userid}}");
    source.onmessage = function (event) {
        var json = JSON.parse(event.data);
        $("#submit_btn").prop('class', 'btn btn-outline-secondary btn-block')
        $("#submit_btn").prop('disabled', true);
        $("#spinner").css('visibility', 'visible');
        $("#prog_in").css('width', json.prog + '%');
        $("#prog_in").text(json.prog + '%');
        $("#resultArea").prop('placeholder', json.msg);
        if (json.prog == 100) {
            $("#spinner").css('visibility', 'hidden');
            $("#resultArea").text(json.result);
            $("#submit_btn").prop('class', 'btn btn-outline-primary btn-block')
            $("#submit_btn").prop('disabled', false);
            source.close()
        }
    }
});
