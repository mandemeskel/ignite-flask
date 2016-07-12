var app = angular.module( "ignite", [] ),
    DEVELOPING = true,
    BASE_URL = "http://192.168.42.64:8080", //"http://localhost:8080",
    BASE_API_URL = "/api";

if( !DEVELOPING )
    BASE_URL = "https://lnchlist.appspot.com";

BASE_API_URL = BASE_URL + BASE_API_URL;


/**
 * Start the app
 */
app.run( function() {
    // TODO: remove loading screen
} );


/**
 * The ajaxService handles all the server calls.
 * @param  {Object} $http   namesapce that allows access to Angular's ajax api
 * @return {Object}         a collection of functions that make unique calls to the server
 */
app.service( "ajaxService", function( $http ) {

    return ({

        sendForm : function( method, url, data, onSuccess, onFail ) {

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

            return this.sendForm(
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

        }

    })

});


// TODO: call server, get topics for front page
app.controller( "mainCtrlr", function( $scope, ajaxService ) {

    $scope.front_page_topics = [];

    $scope.displayFrontPageTopics = function( response ) {

        var data = response.data;

        if( DEVELOPING )
            console.log( "success, response:", data );

        if( data.status == true )
            $scope.front_page_topics = data.topics;
        else
            console.log( "no front page topics", data.msg );

    };

    $scope.subscriber = {
        email : ""
    };

    $scope.addSubscriber = function() {

        if( DEVELOPING )
            console.log( "addSubscriber", $scope.subscriber, $.param( $scope.subscriber ) );

        ajaxService.sendForm(
            "POST",
            "../api/subscribe",
            $.param( $scope.subscriber )
        );

    };

    ajaxService.getTopics(
        $scope.displayFrontPageTopics
    );

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
