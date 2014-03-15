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
                var view = this
                view._items = []
                view.collection.fetch({
                    success: function(event) {
                        view.collection.each(function(model) {
                            view._items.push(model)
                        })
                        view.render()
                    }
                })
            },

            events: {
                'change .user-role':               'updateRole',
                'change #searchusers':             'addRow',
            },

            addRow: function(event) {
                var rendered_users = $('#user-roles tr[data-username="' + event.val + '"]')
                var roles = ['Manager', 'NonVisible']

                if (rendered_users.length == 0) {
                    newuser = '<tr data-username="' + event.val + '"><td>' + event.val + '</td>'
                    for (var i=0;i<roles.length;i++) {
                      newuser += '<td><input type="checkbox" class="user-role"'
                      newuser += ' data-role="' + roles[i] + '"></td>'
                    }
                    newuser += '</tr>'
                    $('#user-roles tr:last').after(newuser)
                }
            },
            updateRole: function(event) {
                console.log('chan')
                var $role = $(event.target)
                var role = $role.attr('data-role')
                var username = $role.closest('tr').attr('data-username')
                var value = $role.is(':checked')

                var userrole = new models.UserRole({role: role, username:username, value:value})

                if (value) {
                    userrole.save({}, { success: function(data) { } })
                } else {
                    userrole.destroy({}, { success: function(data) { } })
                }


            },
            render: function(){

                var variables = {
                    roles: [
                        {'name': 'Manager'},
                        {'name': 'NonVisible'}
                    ],
                    users: this._items
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

    var ResourcesListView = Backbone.View.extend({
            initialize: function(options){
                var view = this;
                view._items = {};
                view.apiview = options.apiview;
                $.get(view.apiview.$el.attr('data-url'), function(data) {
                    view.categories = data;
                    view.render();
                    _.each(data,function(element, index, list) {
                        _.each(element.resources, function(element, index, list) {
                            view._items[element.route_id] = element;
                        });
                    });
                });
            },
            events: {
                'click .resource-item': 'updatePanel'
            },
            updatePanel: function(event) {
                var resource = this._items[event.currentTarget.id];
                this.apiview.views.panel.update(resource);
            },
            render: function(){

                var variables = {
                    categories: this.categories
                };
                var html = templates.api_resource_list.render(variables);
                this.$el.html(html);
            },
        });

    var ResourceView = Backbone.View.extend({
            initialize: function(options){
                var view = this;
                view._items = {};
                view.resource = {};
                view.apiview = options.apiview;
            },

            update: function(resource){
                this.resource = resource;
                this.render();

            },
            getDestinationParts: function() {
                var parts = this.resource.route_url.match(/[^\/]+/g);
                var destination = [];
                _.each(parts, function(element, index, list) {
                   if (element[0] == '{') {
                    if (index > 0) {
                        if (destination[index - 1].fixed) {
                            destination[index - 1].text += '/';
                        } else {
                            destination.push({'text': '/', fixed:true, param:false});
                        }
                    }

                    destination.push({'text': element, fixed:false, param:true});
                   } else {
                    var newpart = '/' + element;
                    if (index === 0) {
                        destination.push({'text': newpart, fixed:true, param:false});
                    } else {
                        if (destination[index - 1].fixed) {
                            destination[index - 1].text += newpart;
                        } else {
                            destination.push({'text': newpart, fixed:true, param:false});
                        }
                    }

                   }
                });
                console.log(destination)
                return destination
            },
            render: function(){
                var variables = {
                    name: this.resource.route_name,
                    destination: this.getDestinationParts()
                };
                var html = templates.api_resource_panel.render(variables);
                this.$el.html(html);
            },
        });

    var ApiView = Backbone.View.extend({
            initialize: function(options){
                var mainview = this;
                mainview.render();
                mainview.views = {};
                mainview.views.list = new ResourcesListView({
                    el: jq('#backbone-container #api-resource-list'),
                    apiview: this
                });
                mainview.views.panel = new ResourceView({
                    el: jq('#backbone-container #api-resource-panel'),
                    apiview: this
                });
            },
            render: function(){

                var variables = {
                };
                var html = templates.api_main_ui.render(variables);
                this.$el.html(html);
                view = this;
            },
            activate: function(){

            }
    });


    var MainView = Backbone.View.extend({
            initialize: function(options){
                var mainview = this
                mainview.render()
                mainview.views = {}
                mainview.views.users = new UsersView({
                    el: jq('#backbone-container #users')
                })
                mainview.views.roles = new RolesView({
                    el: jq('#backbone-container #roles'),
                    collection: new models.Security()
                })

                intervalID = setInterval(function(event) {
                    if ($('#searchusers').length > 0) {
                        clearInterval(intervalID)
                        $('#searchusers').select2({
                            placeholder: 'Search users',
                            minimumInputLength: 3,
                            query: function (query) {
                                var users = new models.Users()
                                users.fetch({
                                    data: {'username': query.term},
                                    success: function(collection, response, options) {
                                        data = []
                                        users.each(function(model) {
                                            data.push({
                                                'id': model.attributes.username,
                                                'text': model.attributes.displayName
                                            })
                                        })
                                        query.callback({results: data})
                                    }
                                })
                            }
                        })
                    }
                }, 1)


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
        ApiView: ApiView
    }
}
