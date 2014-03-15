var bigmax = bigmax || {};

bigmax.templates = function() {


var MSTCH_BIGMAX_USERS_MAIN_UI = '\
  <div class="container">\
    <div class="row">\
       <div class=".col-md-12">\
          <h1>User administration</h1>\
          <ul class="nav nav-tabs">\
            <li class="active" id="users-tab"><a href="#users">Users</a></li>\
            <li id="roles-tab"><a href="#roles">Roles</a></li>\
          </ul>\
          <div class="tab-content">\
              <div class="tab-pane active row" id="users">\
              </div>\
              <div class="tab-pane" id="roles">\
              </div>\
          </div>\
       </div>\
    </div>\
  </div>\
';

var MSTCH_BIGMAX_API_MAIN_UI = '\
<div class="container">\
    <div class="row">\
        <div class="col-md-12">\
            <h1>API resource tester</h1>\
        </div>\
    </div>\
    <div class="row">\
        <div class="col-md-3" id="api-resource-list">\
        </div>\
        <div class="col-md-9" id="api-resource-panel">\
        </div>\
    </div>\
</div>\
';

var MSTCH_BIGMAX_API_RESOURCE_PANEL = '\
{{#name}}\
<div class="panel panel-defaulte">\
    <form class="form-horizontal" role="form">\
       <div class="form-group" id="resource-name">\
          <label for="resource-name" class="col-sm-2 control-label">Resource</label>\
          <div class="col-sm-10">\
            <h5>{{name}}</h5>\
          </div>\
        </div>\
\
       <div class="form-group" id="resource-uri">\
          <label for="resource-uri" class="col-sm-2 control-label">Destination</label>\
          <div class="col-sm-10">\
              {{#destination}}\
                  {{#fixed}}<span class="fixed">{{text}}</span>{{/fixed}}\
                  {{#param}}<input class="param form-control" value="{{text}}"/>{{/param}}\
              {{/destination}}\
          </div>\
        </div>\
\
        <div class="form-group" id="resource-method">\
          <label for="resource-method" class="col-sm-2 control-label">Request Method</label>\
          <div class="col-sm-10">\
            <label class="radio-inline">\
              <input type="radio" id="inlineRadio1" name="request-method" value="GET"> GET\
            </label>\
            <label class="radio-inline">\
              <input type="radio" id="inlineRadio2" name="request-method" value="POST"> POST\
            </label>\
            <label class="radio-inline">\
              <input type="radio" id="inlineRadio3" name="request-method" value="PUT"> PUT\
            </label>\
            <label class="radio-inline">\
              <input type="radio" id="inlineRadio3" name="request-method" value="PUT"> DELETE\
            </label>\
          </div>\
        </div>\
\
       <div class="form-group" id="resource-description">\
          <label for="resource-description" class="col-sm-2 control-label">Description</label>\
          <div class="col-sm-10">\
            <p>Adds a post to the user activities</p>\
          </div>\
        </div>\
\
       <div class="form-group" id="request-headers">\
          <label for="request-headers" class="col-sm-2 control-label">Headers</label>\
          <div class="col-sm-10">\
\
             <div class="form-group" id="oauth-username">\
                <label class="col-sm-3 control-label fixed">X-Oauth-Username</label>\
                <div class="col-sm-9">\
                  <input class="param form-control" type="text">\
                </div>\
              </div>\
       \
               <div class="form-group" id="oauth-token">\
                  <label class="col-sm-3 control-label fixed">X-Oauth-Token</label>\
                  <div class="col-sm-9">\
                    <input class="param form-control" type="text">\
                  </div>\
                </div>\
       \
             <div class="form-group" id="oauth-scope">\
                <label class="col-sm-3 control-label fixed">X-Oauth-Scope</label>\
                <div class="col-sm-9">\
                  <input class="param form-control" type="text">\
                </div>\
              </div>\
       \
          </div>\
        </div>\
\
       <div class="form-group" id="request-data">\
          <label for="resource-description" class="col-sm-2 control-label">Description</label>\
          <div class="col-sm-10">\
            <textarea class="form-control">\
{\
    "hola": "que tal"\
}\
            </textarea>\
          </div>\
        </div>\
\
       <div class="form-group" id="request-submit">\
          <label class="col-sm-2 control-label"></label>\
          <div class="col-sm-10">\
            <button type="submit" class="btn btn-large btn-primary" id="execute_button" data-bind="visible:isIdle, enable:url" disabled="">\
                <i class="glyphicon glyphicon-random"></i>\
                Launch Request\
              </button>\
          </div>\
        </div>\
\
    </form>\
</div>\
{{/name}}\
';

var MSTCH_BIGMAX_API_RESOURCE_LIST = '\
<div class="panel-group" id="categories">\
    {{#categories}}\
      <div class="panel panel-default">\
\
        <div class="panel-heading">\
          <h4 class="panel-title">\
            <a data-toggle="collapse" data-parent="#categories" href="#{{id}}">\
              {{name}}\
            </a>\
          </h4>\
        </div>\
\
        <div id="{{id}}"\
             class="panel-collapse collapse">\
          <div class="panel-body resources-panel">\
                <div class="panel-group" id="{{id}}-resources">\
                    {{#resources}}\
\
                      <div class="panel panel-default resource">\
                        <div class="panel-heading">\
                          <h4 class="panel-title">\
                            <a data-toggle="collapse" class="resource-item" id="{{route_id}}" data-parent="#{{id}}-resources">\
                              <span class="glyphicon glyphicon-paperclip"></span> {{route_name}}\
                            </a>\
                          </h4>\
                        </div>\
                        <div id="{{resource_name}}"\
                             class="panel-collapse collapse">\
                          <div class="panel-body">\
\
                          </div>\
                        </div>\
                      </div>\
\
                    {{/resources}}\
                </div>\
          </div>\
        </div>\
      </div>\
    {{/categories}}\
</div><!-- #accordion-->\
';

var MSTCH_BIGMAX_USERS_LIST_UI = '\
<div class="container">\
  <div class="row">\
    <div class="col-md-12">\
    Users List\
    </div>\
  </div>\
</div>\
';

var MSTCH_BIGMAX_USERS_ROLES_UI = '\
<div class="container">\
  <div class="row">\
    <div class="col-md-12">\
        <table class="table" id="user-roles" data-url="${api.context_url}/api-role">\
            <thead>\
              <tr>\
                <th></th>\
                {{#roles}}<th>{{name}}</th>{{/roles}}\
              </tr>\
            </thead>\
            <tbody>\
            {{#users}}\
            <tr data-username="{{id}}">\
              <td>{{id}}</td>\
              {{#roles}}\
              <td>\
                  <input type="checkbox"\
                         class="user-role"\
                         {{#active}}checked="checked{{/active}}"\
                         data-role="{{name}}">\
              </td>\
              {{/roles}}\
            </tr>\
            {{/users}}\
            </tbody>\
          </table>\
    </div>\
  </div>\
  <div class="row">\
    <div class="form-group col-xs-4">\
      <input type="text" class="form-control" id="searchusers" placeholder="Search Users" data-url="/api-users">\
    </div>\
  </div>\
</div>\
';
var templates = {
         users_main_ui: Hogan.compile(MSTCH_BIGMAX_USERS_MAIN_UI),
         users_list_ui: Hogan.compile(MSTCH_BIGMAX_USERS_LIST_UI),
         users_roles_ui: Hogan.compile(MSTCH_BIGMAX_USERS_ROLES_UI),
         api_main_ui: Hogan.compile(MSTCH_BIGMAX_API_MAIN_UI),
         api_resource_list: Hogan.compile(MSTCH_BIGMAX_API_RESOURCE_LIST),
         api_resource_panel: Hogan.compile(MSTCH_BIGMAX_API_RESOURCE_PANEL),
  }

  return templates

}
