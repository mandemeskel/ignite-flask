var app = angular.module( "ignite", [] ),
    DEVELOPING = true,
    BASE_URL = "http://localhost:3636", //"http://192.168.42.64:8080", //"http://localhost:8080",
    BASE_API_URL = "/api";

if( !DEVELOPING )
    BASE_URL = "https://lnchlist.appspot.com";

// BASE_API_URL = BASE_URL + BASE_API_URL;


/**
 * Start the app
 */
app.run( function() {
    // TODO: add loading screen
} );


/**
 * The ajaxService handles all the server calls.
 * @param  {Object} $http   namesapce that allows access to Angular's ajax api
 * @return {Object}         a collection of functions that make unique calls to the server
 */
app.service( "ajaxService", function( $http, $location ) {

    return ({

        request : function( method, url, data, onSuccess, onFail ) {

            if( onSuccess == null )
                onSuccess = handleAJAXSuccess;

            if( onFail == null )
                onFail = handleAJAXFail;

            var request = $http({
                method: method,
                url: url,
                data: data,
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            });

            return request.then( onSuccess, onFail );

        },

        // TODO: add arg to change number topics requested, default is 9
        getTopics : function( onSuccess, onFail ) {

            return this.request(
                "GET",
                BASE_API_URL + "/topics",
                "",
                onSuccess,
                onFail
            )

            // if( onSuccess == null )
            //     onSuccess = handleAJAXSuccess;
            //
            // if( onFail == null )
            //     onFail = handleAJAXFail;
            //
            // var request = $http({
            //     method: "GET",
            //     url: BASE_API_URL + "/topics",
            //     data: ""
            //     // headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            // });
            //
            // return request.then( onSuccess, onFail );

        },

        getTopic: function( topic_key, onSuccess, onFail ) {

            var action = BASE_API_URL + "/topic/" + topic_key;

            // update browser url to topic
            $location.path( action );

            return this.request(
                "GET",
                action,
                "",
                onSuccess,
                onFail
            );

        }

    })

});


// TODO: call server, get topics for front page
app.controller( "mainCtrlr", function( $scope, $location, ajaxService ) {

    function toggle( obj, path ) {
        if( path == undefined )
            path = "";
        // hide other views
        $scope.hideOtherSections( obj );
        // toggle this view
        obj.show = !obj.show;
        // update url for back/forward btn
        $location.path( path );
        return obj.show;
    }

    $scope.topic = {
        topic : undefined,
        show : false,
        toggle: function(){ toggle( this, "") }
    };

    $scope.topics = {
        front_page_topics: [],
        show: true,
        toggle: function(){ toggle( this, "") }
    }

    $scope.hideOtherSections = function() {
        $scope.topic.show = false;
        $scope.topics.show = false;
    }

    function displayFrontPageTopics( response ) {

        var data = response.data;

        if( DEVELOPING )
            console.log( "success, response:", data );

        if( data.status == true ) {
            $scope.topics.show = true;
            $scope.topics.front_page_topics = data.topics;
            console.log( $scope.topics );
        } else
            console.log( "no front page topics", data.msg );

    };

    $scope.subscriber = {
        email : ""
    };

    $scope.addSubscriber = function() {

        if( DEVELOPING )
            console.log( "addSubscriber", $scope.subscriber, $.param( $scope.subscriber ) );

        ajaxService.request(
            "POST",
            "../api/subscribe",
            $.param( $scope.subscriber )
        );

    };

    ajaxService.getTopics(
        displayFrontPageTopics
    );

    function displayTopic( response ) {

        if( DEVELOPING )
            console.log( "displayTopic topic: ", response.data )

        $scope.topic.topic = response.data;
        $scope.topic.show = true;
        $scope.topics.show = false;

    }

    // TODO: let the user know, the request has been set, and that we are waiting
    $scope.topicClicked = function( event, topic_key ) {

        if( DEVELOPING )
            console.log( "getTopic, key:", topic_key )

        event.preventDefault();

        ajaxService.getTopic( topic_key, displayTopic )

    }


});


// default success handler for the AJAX requests
function handleAJAXSuccess( data, status, headers, config ) {

    if( DEVELOPING )
        console.log( "success", status, data );

}


// default error handler for the AJAX requests
function handleAJAXFail( data, status, headers, config ) {

    if( DEVELOPING )
        console.log( "error", status, data );

}
