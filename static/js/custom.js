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

$(document).on('click', '.view-record', function () {
   

    console.log("CLICK WORKING");

    let animal = $(this).attr('data-animal');
    let total = $(this).attr('data-total');
    let date = $(this).attr('data-date');
    let notes = $(this).attr('data-notes');
    let created = $(this).attr('data-created');

    console.log(animal);

    $('#modal-animal').html(animal);

    $('#modal-total').html(total);

    $('#modal-date').html(date);

    $('#modal-notes').html(notes ? notes : '-');

    $('#modal-created').html(created);

});
