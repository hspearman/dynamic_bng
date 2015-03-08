/**
 * Created by Hannah on 3/29/2015.
 */

App.HomeController = Ember.Controller.extend({
	// TODO: Reset on page re-entry
	isLoadingBand: true,
	actions: {
		authorize: function() {
		    // TODO: Dialog
		    // window.location.replace('https://accounts.spotify.com/authorize?client_id=04339da82c884355a79da568a4dfcddf&response_type=code&redirect_uri=https://localhost:8000&scopes=user-library-read&show_dialog=True');

		    spotify_authorize_url = 'https://accounts.spotify.com/authorize';

            // TODO: Inject constants
		    // TODO: Investigate security
            // Build query string
            queryString = '?';
            queryParams = {
                "client_id": "04339da82c884355a79da568a4dfcddf",
                "response_type": "code",
                "redirect_uri": "http://localhost:8000/spotify/authorize",
                "scope": "user-library-read",
                "show_dialog": true
            }
            for (var param in queryParams) {
                if (queryParams.hasOwnProperty(param)) {
                    if (queryString !== "?") {
                        queryString += "&"
                    }
                    // TODO: Format function
                    queryString += param + '=' + queryParams[param];
                }
            }

            spotify_authorize_url += queryString;
            window.location.replace(spotify_authorize_url);
            /*$.ajax({
                url: "http://localhost:8000/spotify/authorize",
                type: "POST",
                success: function(data) {
                }
                // TODO: Failure
            });*/
		},
        generateBandName: function() {
            this.generateBandName();
        }
	},
    generateBandName: function() {

        var controller = this;
        this.set("isLoadingBand", true);

        return new Ember.RSVP.Promise(function(resolve, reject) {
            Ember.$.ajax({
                url: "http://localhost:8000/bands/random",
                type: "POST",
                // dataType: 'json'
                // TODO: Remove after hosted? Cross-domain?
                data: {},
                //dataType: 'jsonp'
                // TODO: Success
                success: function(response) {
                    resolve(response)
                },
                // TODO: Failure
                error: function(reason) {
                    reject(reason)
                }
            })
        }).then(
            // Success
            function(value) {
                controller.setProperties({
                    "model.band": value,
                    "isLoadingBand": false
                });
            },
            // Failure
            function(value) {
                // TODO: Handle failure
                controller.set("isLoadingBand", false);
            }
        );
    },
    formatQuote: function() {

        var formatQuote = ""

        var quote = this.get("model.band.quote");
        if (undefined !== quote &&
            null !== quote) {
            formatQuote = quote.replace("{{band}}", this.get("model.band.name"));
        }

        return formatQuote;
        
    }.property("model.band"),
    isAuthorizedAndLoading: function() {
        return this.get("model.isAuthorized") && this.get("isLoadingBand") ;
    }.property("model.isAuthorized", "isLoadingBand")
});