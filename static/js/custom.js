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




// Handle line update forms
document.querySelectorAll('.line-update-form').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        
        fetch(window.location.href, {
            method: 'POST',
            body: formData,
            headers: {'X-Requested-With': 'XMLHttpRequest'}
        })
        .then(res => res.json())
        .then(data => {
            if(data.status === 'success') {
                document.getElementById('successMessage').textContent = data.message;
                $('#successModal').modal('show');
                
                // Close modal after 3 seconds
                setTimeout(() => {
                    $('#successModal').modal('hide');
                }, 3000);
            }
        });
    });
});