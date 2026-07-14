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

// Updated Note Modal Logic
$('#noteModal').on('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = $(event.relatedTarget); 
    var modal = $(this);

    // Retrieve values directly from attributes
    var title = button.attr('data-title');
    var spec = button.attr('data-spec');
    
    // Find the hidden div within the clicked card
    var noteContent = button.find('.record-note').text().trim();

    // Set the modal content
    modal.find('.modal-title').text(title + (spec ? ' (' + spec + ')' : '') + ' Note');
    modal.find('#noteModalBody').text(noteContent || "No notes available.");
});