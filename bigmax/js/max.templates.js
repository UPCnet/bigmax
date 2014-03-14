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
<div class="panel panel-defaulte">\
    <form class="form-horizontal" role="form">\
       <div class="form-group" id="resource-name">\
          <label for="resource-name" class="col-sm-2 control-label">Resource</label>\
          <div class="col-sm-10">\
            <h5>User Activities</h5>\
          </div>\
        </div>\
\
       <div class="form-group" id="resource-uri">\
          <label for="resource-uri" class="col-sm-2 control-label">Destination</label>\
          <div class="col-sm-10">\
              <span class="fixed">/people/</span>\
              <input class="param form-control" value="{username}"/>\
              <span class="fixed">/device/</span>\
              <input class="param form-control" value="{platform}"/>\
              <span class="fixed">/</span>\
              <input class="param form-control" value="{token}"/>\
          </div>\
        </div>\
\
        <div class="form-group" id="resource-method">\
          <label for="resource-method" class="col-sm-2 control-label">Request Method</label>\
          <div class="col-sm-10">\
            <label class="checkbox-inline">
              <input type="checkbox" id="inlineCheckbox1" value="option1"> 1
            </label>
            <label class="checkbox-inline">
              <input type="checkbox" id="inlineCheckbox2" value="option2"> 2
            </label>
            <label class="checkbox-inline">
              <input type="checkbox" id="inlineCheckbox3" value="option3"> 3
            </label>
          </div>\
        </div>\
    </form>\
</div>\
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
                            <a data-toggle="collapse" data-parent="#{{id}}-resources" href="#{{resource_id}}">\
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
