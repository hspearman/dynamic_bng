/**
 * Created by Hannah on 3/17/2015.
 */

Todos.EditTodoView = Ember.TextField.extend({
    actions: {
        didInsertElement: function () {
            this.$().focus();
        }
    }
});

Ember.Handlebars.helper('edit-todo', Todos.EditTodoView);