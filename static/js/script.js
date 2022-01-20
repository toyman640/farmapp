$(function() {
	var totalExeTime = 2000;

    function count($this){
        var currentCount = parseInt($this.html(), 10),
        	maxCount = $this.data('count');
        
        $this.html(++currentCount);
        if(currentCount !== maxCount){
        	var ratio = totalExeTime / maxCount;
        
            setTimeout(function(){
            	count($this)
           	}, ratio);
        }
    }        
  $(".number").each(function() {
      $(this).data('count', parseInt($(this).html(), 10));
      $(this).html('0');
      count($(this));
  });
});