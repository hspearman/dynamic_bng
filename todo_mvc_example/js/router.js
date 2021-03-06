/**
 * Created by Hannah on 3/17/2015.
 */

// Set-up router
Todos.Router.map(function() {
    this.resource('todos', { path: '/' }, function () {
        this.route('active');
        this.route('completed');
    });
});

// Todos route
Todos.TodosRoute = Ember.Route.extend({
    model: function() {
        return this.store.find('todo');
    }
});

Todos.TodosIndexRoute = Ember.Route.extend({
    model: function() {
        return this.modelFor('todos');
    }
});

Todos.TodosActiveRoute = Ember.Route.extend({
    model: function(){
        return this.store.filter('todo', function(todo) {
            return !todo.get('isCompleted');
        });
    },
    renderTemplate: function(controller) {
        this.render('todos/index', {controller: controller});
    }
});

Todos.TodosCompletedRoute = Ember.Route.extend({
    model: function() {
        return this.store.filter('todo', function(todo) {
            return todo.get('isCompleted');
        });
    },
    renderTemplate: function(controller) {
        this.render('todos/index', {controller: controller});
    }
});