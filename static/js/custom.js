$(".button").click(function() {
    var id = $(this).attr("id").split("_")[1]
    $(`#exampleModalt_${id}`).show();
  });
  
  $(".ebcf_close").click(function() {
    $(".ebcf_modal").hide();
  });


  
$('.counter').each(function () {
    $(this).prop('Counter',0).animate({
        Counter: $(this).text()
    }, {
        duration: 20000,
        easing: 'swing',
        step: function (now) {
            $(this).text(Math.ceil(now));
        }
    });
});