var bigmax = bigmax || {};

/**
 * @fileoverview Max backbones views definition
 */

bigmax.views = function(settings) {

    var settings = settings
    var models = bigmax.models(settings)
    var templates = bigmax.templates()
    var jq = jQuery

    var UsersView = Backbone.View.extend({
            initialize: function(options){
                var usersview = this
                this.render()
            },
            render: function(){

                var variables = {
                }
                var html = templates.users_list_ui.render(variables)
                this.$el.html(html)
            },
            activate: function(){
                var $container = this.$el.closest('#backbone-container')
                // Change tab
                $container.find('.nav-tabs li.active').toggleClass('active', false)
                $container.find('.nav-tabs li#users-tab').toggleClass('active', true)
                // Change tab content
                $container.find('.tab-content .tab-pane.active').toggleClass('active', false)
                this.$el.toggleClass('active', true)

            }
        })

    var RolesView = Backbone.View.extend({
            initialize: function(options){
                var rolesview = this
                this.render()
            },
            render: function(){

                var variables = {
                }
                var html = templates.users_roles_ui.render(variables)
                this.$el.html(html)
            },
            activate: function(){
                var $container = this.$el.closest('#backbone-container')
                // Change tab
                $container.find('.nav-tabs li.active').toggleClass('active', false)
                $container.find('.nav-tabs li#roles-tab').toggleClass('active', true)
                // Change tab content
                $container.find('.tab-content .tab-pane.active').toggleClass('active', false)
                this.$el.toggleClass('active', true)
            }
        })

    var MainView = Backbone.View.extend({
            initialize: function(options){
                var mainview = this
                mainview.render()
                mainview.views = {}
                mainview.views.users = new UsersView({
                    el: jq('#backbone-container #users')
                })
                mainview.views.roles = new RolesView({
                    el: jq('#backbone-container #roles')
                })

            },
            render: function(){

                var variables = {
                }
                var html = templates.users_main_ui.render(variables)
                this.$el.html(html)
            }
        })



    return {
        MainView: MainView,
    }
}
