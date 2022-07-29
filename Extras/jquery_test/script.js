$(document).ready(function() {
    $('h1').hover(
        // defines the fucionts on action
        function() {
            $(this).css("color", "green");
        },
        // defines the call back function
        function() { 
            $(this).css("color", "red");    
        }
    );

    $('button').click(
        function() {
            alert("clicked");
        }
    );


});