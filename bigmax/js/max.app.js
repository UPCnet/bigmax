(function(){

    window.App = {
        Models: {},
        Collections: {},
        Views: {},
        Router: {}
    };

    App.Router = Backbone.Router.extend({

        initialize: function(el) {
              this.views = bigmax.views(window._MAXUI);
              this.mainview = new this.views.MainView({el: '#backbone-container'})
        },
        routes: {
            '': 'index',
            'roles': 'roles',
            'users': 'users'
        },
        index: function(){
            this.mainview.views.users.activate()
        },
        roles: function(){
            this.mainview.views.roles.activate()
        },
        users: function(){
            this.mainview.views.users.activate()
        }
    });

    new App.Router;
    Backbone.history.start();

})();
