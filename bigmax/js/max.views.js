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
                'click .panel.resource': 'updatePanel'
            },
            updatePanel: function(event) {
                $target = $(event.currentTarget)
                $item = $target.find('.resource-item');
                $('.panel.resource.active').toggleClass('active', false)
                $target.toggleClass('active', true)
                var resource = this._items[$item[0].id];
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
            events: {
                'click #methods-list .btn': 'setActiveMethod',
                'click #roles-list .btn': 'setActiveRole',
                'click #request-submit .btn': 'makeRequest'
            },

            makeRequest: function(event) {
                event.preventDefault()
                event.stopPropagation()
                var url = view.apiview.$el.attr('data-url')
                url = url.substr(0, url.length - 4) + 'request'

                url_parts = {}
                _.each($('#resource-uri input.param'), function(element, index, list) {
                    var $input = $(element)
                    var param_name = $input.attr('data-param')
                    var param_value = $input.val()
                    url_parts[param_name] = param_value
                })

                headers = {}
                _.each($('#request-headers .form-group'), function(element, index, list) {
                    var $header = $(element)
                    var header_name = $header.attr('id')
                    var header_value = $header.find('input.param').val()
                    headers[header_name] = header_value
                })


                var request_data = {
                    url: this.resource.route_url,
                    url_params: url_parts,
                    headers: headers,
                    method: this.active_method
                }
                if (this.active_method == 'POST' || this.active_method == 'PUT') {
                    request_data['postdata'] = $('#request-data textarea').val()
                }
                jQuery.ajax({
                    url: url,
                    type: 'POST',
                    data: JSON.stringify(request_data),
                    async: true,
                    dataType: 'json'
                })
                .done(function (data) {
                    var response_html = data.response_html
                    if (data.response_type == 'text')
                        response_html = '<pre>' + response_html + '</pre>'

                    $('#request-results #response-content').html(response_html)
                    $('#request-results #response-raw pre').html(data.response_raw)
                    $('#request-results #response-content').attr('data-type', data.response_type)
                    $('#request-results #http-request-headers').html(data.request_headers)
                    $('#request-results #http-response-headers').html(data.response_headers)


                })
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
                return destination
            },
            setActiveRole: function() {
                var roles = this.getAvailableRoles()
                if (arguments.length == 0) {
                    if (_.where(roles, {role_name:'Everyone'}).length > 0) {
                        this.active_role = 'Everyone'
                    } else {
                        this.active_role = roles[0].role_name
                    }

                } else {
                    $input = $(arguments[0].currentTarget).find('input')
                    this.active_role = $input.attr('data-value')
                    this.renderMethodDetails()
                }
            },
            getAvailableRoles: function() {
                var roless = []
                view = this
                _.each(this.resource.methods[this.active_method], function(element, index, list) {
                    var role = {role_name: index, active: index == view.active_role}
                    roless.push(role)
                })
                return roless
            },
            setActiveMethod: function() {
                var methods = this.getAvailableMethods()
                if (arguments.length == 0) {
                    if (methods.GET.available) {
                        this.active_method = 'GET'
                    }
                    else if (methods.POST.available) {
                        this.active_method = 'POST'
                    }
                    else if (methods.PUT.available) {
                        this.active_method = 'PÛT'
                    }
                    else if (methods.DELETE.available) {
                        this.active_method = 'DELETE'
                    }
                    else if (methods.HEAD.available) {
                        this.active_method = 'DELETE'
                    }
                } else {
                    $input = $(arguments[0].currentTarget).find('input')
                    this.active_method = $input.attr('data-value')
                    this.renderMethodDetails()
                }
            },
            getAvailableMethods: function() {
                view = this
                var methods = {
                    'GET': {'available': false, 'active': false},
                    'POST': {'available': false, 'active': false},
                    'PUT': {'available': false, 'active': false},
                    'DELETE': {'available': false, 'active': false},
                    'HEAD': {'available': false, 'active': false}
                }
                _.each(this.resource.methods, function(element, index, list) {
                    methods[index].available = true
                    if (view.active_method === index) {
                        methods[index].active = true
                    }
                })
                return methods
            },
            getHeaders: function() {
                var headers = [
                    {'header':'X-Oauth-Username', value: _MAXUI.username},
                    {'header':'X-Oauth-Token', value: _MAXUI.token},
                    {'header':'X-Oauth-Scope', value: 'widgetcli'}
                ]
                return headers
            },
            getMethodDetailsHTML: function() {
                var current_role_method = this.resource.methods[this.active_method][this.active_role]

                var variables = {
                    description: current_role_method.description,
                    headers: this.getHeaders(),
                    postdata: this.active_method == 'POST' || this.active_method == 'PUT'
                }
                return templates.api_resource_panel_details.render(variables);
            },
            renderMethodDetails: function() {
                var html = this.getMethodDetailsHTML()
                this.$el.find('#resource-details').html(html);

            },
            render: function(){
                this.setActiveMethod()
                var methods = this.getAvailableMethods()
                this.setActiveRole()
                var roles = this.getAvailableRoles()

                var variables = {
                    id: this.resource.route_id,
                    name: this.resource.route_name,
                    destination: this.getDestinationParts(),
                    methods: methods,
                    roles: roles,
                    details: this.getMethodDetailsHTML()
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
