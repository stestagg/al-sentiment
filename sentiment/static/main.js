
jQuery(function(){
    var $ = jQuery;

    var updateFeed = function() {
        $("#tweets").load("/tweets");
    };

    var moreTweets = function() {
        setStatus("Fetching more..");
        // Ask server to load more tweets
        $.get("/update")
            .then(function(data) {
                if (data.success) {
                    updateFeed();
                    setStatus("Update complete");
                } else {
                    setStatus("Couldn't fetch new tweets: " + data.message);
                }
            })
            .fail(function(data) {
                setStatus("Something went wrong getting new tweets");
            })
    }

    var setStatus = function(message){
        $("#status").text(message);
    }

    updateFeed();
    $("#more-tweets").click(moreTweets);

    setStatus("Please click 'Fetch more messages' to begin");

})