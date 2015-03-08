/**
 * Created by Hannah on 3/17/2015.
 */

// Create Ember application
window.Todos = Ember.Application.create();

// Load sample date from Fixture
Todos.ApplicationAdapter = DS.FixtureAdapter.extend();