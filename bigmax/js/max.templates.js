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
  }

  return templates

}
