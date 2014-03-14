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
              this.apiview = new this.views.ApiView({el: '#backbone-container'})
        },
        routes: {
            '': 'index',
        },
        index: function(){
            this.apiview.activate()
        },
    });

    new App.Router;
    Backbone.history.start();

})();


function adaptURIInputSizes(input) {
    var $input = $(input)
    $input.css({width: ($input.val().length * 8) + 8});
}

$(document).ready(function(event) {

    $('#backbone-container').on('keyup', '#resource-uri input.param', function(event) {
        adaptURIInputSizes(event.currentTarget)
    })
    .on('keypress', '#resource-uri input.param', function(event) {
        adaptURIInputSizes(event.currentTarget)
    })
})

