/**
 * Created by Hannah on 3/21/2015.
 */

window.App = Ember.Application.create({
    rootElement: '#app'
});

// Load sample date from fixture
App.ApplicationAdapter = DS.FixtureAdapter.extend();
// App.Store = DS.Store.extend({
	// revision: 12,
	// adapter: DS.RESTAdapter.create({
		// url: 'http://localhost:8000'
	// })
// });
