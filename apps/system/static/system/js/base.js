$(document).ready(() => {
    let x = window.matchMedia("(min-width:992px)");
    $(window).resize(() => {
        if (x.matches) {
            $('#menu-wrapper').css({"display":"block","opacity":"1"});
            $('.menu-content').css({ "left": "0"});   
        } else {
            $('#menu-wrapper').css({"display":"none","opacity":"0"});
            $('.menu-content').css({ "left": "-100" }); 
        }
        location.reload();
    })
    
    $('#menu-wrapper').click((e) => {   
        if (!x.matches) {
            if (e.target == $("#menu-wrapper")[0]) {
                $('#menu-wrapper').fadeOut();
                $('.menu-content').animate({ left: '-100%'});
            }        
        }
    });

    $('.open-btn').click((e) => {
        if (!x.matches) {
            $('#menu-wrapper').fadeIn(); 
            $('.menu-content').animate({left:"0"}) 
           
        } else {
            $('#menu-wrapper').css({"display":"none","opacity":"0"});
            $('.menu-content').css({ "left": "-100" }); 
        }
        console.log("button")      
    });
});