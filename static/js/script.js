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
