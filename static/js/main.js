  $(document).ready( function () {

        $(window).scroll(function(){
            parallaxScroll();
        });
         
        function parallaxScroll(){ 
            var scrolled = $(window).scrollTop();
            //$('#parallax-bg1').css('top',(0-(scrolled*.25))+'px');
            //$(window).css('background-position-y', (0-(scrolled*1.25))+'px');            
            $('body').css('background-position', 'center '+(0-(scrolled*0.45))+'px');
            
        }

        function bindShiftAnchors() {
            $('td.shift a').unbind().click(function(e) {
                e.preventDefault();
                $(this).removeClass().addClass("busy").text("loading");
                $(this).parent().load(this.getAttribute("href"), null, bindShiftAnchors);
                //shiftSwap(this,this.getAttribute("href"));
            })
        }

        parallaxScroll();
        bindShiftAnchors();
       
    });