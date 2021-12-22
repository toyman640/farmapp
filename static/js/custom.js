$(".button").click(function() {
    var id = $(this).attr("id").split("_")[1]
    $(`#exampleModalt_${id}`).show();
  });
  
  $(".ebcf_close").click(function() {
    $(".ebcf_modal").hide();
  });