/**
 * Created by Hannah on 3/21/2015.
 */

// Set-up router
App.Router.map(function() {
    this.resource('home', { path: '/' }, function () {});
    this.resource('about', { path: '/about' }, function () {});
});

App.HomeRoute = Ember.Route.extend({
	model: function() {
		//return this.store.find('band', 1);s
		//return $.post('http://localhost:8000/bands', {}, function(response) {}, 'json');

		var isAuthorizedPromise = new Ember.RSVP.Promise(function(resolve, reject) {
		    Ember.$.ajax({
		        url: "http://localhost:8000/spotify/authorize/status",
		        type: "GET",
		        // dataType: 'json'
		        // TODO: Remove after hosted? Cross-domain?
		        data: {},
		        //dataType: 'jsonp'
                // TODO: Success
                success: function(response) {
                    resolve(response.is_authorized)
                },
                // TODO: Failure
                error: function(reason) {
                    reject(reason)
                }
            })
		});

		return Ember.RSVP.hash({
		    isAuthorized: isAuthorizedPromise
		});
	},
	setupController: function(controller, model) {

        controller.set("model", model);

        // Lazy load generated band so rest of page display first
        controller.generateBandName.call(controller);
    },
});

App.AboutRoute = Ember.Route.extend({
});