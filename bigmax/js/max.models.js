var bigmax = bigmax || {};

/**
 * @fileoverview Max backbones views definition
 */

bigmax.models = function(settings) {

    /*
    *    Main interface view, this holds
    *    All the other subviews
    *
    *    @param {el} the element where to instantiate the view
    */

    // Setup authentication settings to be accessed
    // By Backbone in the closure
    var settings = settings
    var auth = {
        username: settings.username,
        token: settings.token
    }

    // Enable POST Tunneling
    Backbone.emulateHTTP = true

    // Backbone Sync override with max custom headers
    var originalSync = Backbone.sync
    Backbone.sync = function(method, model, options) {

        options.headers = options.headers || {}
        _.extend(options.headers, {
            "X-Oauth-Token": auth.token,
            "X-Oauth-Username": auth.username,
            "X-Oauth-Scope": "widgetcli"
        })
        return originalSync.apply(this, [method, model, options])
    }

    var User = Backbone.Model.extend({
        idAttribute: 'username',
        urlRoot: '{0}/people'.format(settings.server),
        defaults: {
            username: '',
            displayName: ''
        },

        initialize: function(){

        }

    }) // End User model

    var UserRole = Backbone.Model.extend({
        idAttribute: 'username',
        initialize: function(options){
            this.urlRoot = '{0}/admin/security/roles/{1}/users'.format(settings.server, options.role)
        },

        sync: function(method, model, options) {
                switch (method) {
                    case "update":
                        method='create'
                        break;
                }
                return Backbone.sync.call(model, method, model, options);
            }


    }) // End User model

    var SecurityUserEntry = Backbone.Model.extend({
        idAttribute: 'username',
        urlRoot: '{0}/people'.format(settings.maxServerURL),
        defaults: {
            username: '',
            roles: []
        },

        initialize: function(attributes, options){
            this.roles = attributes.roles
        }

    }) // End User model
    // Collection that returns the inner `items` attribute of the
    // json returned by calls to the server, in response
    // to calls to the fetch or reset collection methods

    var MaxCollection = Backbone.Collection.extend({
        parse: function(resp, options) {
            return resp.items;
        },
    })

    var Users = Backbone.Collection.extend({
        model: User,

        initialize: function(models, options) {
            this.url = '{0}/people'.format(settings.server)
        }
    })

    var Security = Backbone.Collection.extend({
        model: SecurityUserEntry,

        initialize: function(models, options) {
            this.url = '{0}/admin/security/users'.format(settings.server)
        }
    })

    // Expose models to the world

    return {
        User: User,
        UserRole: UserRole,
        Users: Users,
        Security: Security

    }
}

