// $(function() {
// 	var totalExeTime = 2000;

//     function count($this){
//         var currentCount = parseInt($this.html(), 10),
//         	maxCount = $this.data('count');
        
//         $this.html(++currentCount);
//         if(currentCount !== maxCount){
//         	var ratio = totalExeTime / maxCount;
        
//             setTimeout(function(){
//             	count($this)
//            	}, ratio);
//         }
//     }        
//   $(".number").each(function() {
//       $(this).data('count', parseInt($(this).html(), 10));
//       $(this).html('0');
//       count($(this));
//   });
// });

$('.number').each(function () {
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


// $(document).ready(function() {
//     $('.select2-drug').select2({
//         placeholder: "Search drug...",
//         allowClear: true
//     });

//     // Hide the Select2 container (for testing)
//     $('.select2-drug').next('.select2').css('display', 'none');
// });


