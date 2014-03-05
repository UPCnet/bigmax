$(document).ready(function() {

    $('#user-roles').on('change', '.user-role', function(event) {
        var post_url = $('#user-roles').attr('data-url')
        var $role = $(event.target)
        $.post(post_url, {
            role: $role.attr('data-role'),
            username: $role.closest('tr').attr('data-username'),
            value: $role.is(':checked')})
    })

    $('#searchusers').select2({
        placeholder: 'Search users',
        minimumInputLength: 1,
        ajax: {
            url: $('#searchusers').attr('data-url'),
            dataType: 'json',
            data: function (term, page) {
                return {
                    query: term
                };
            },
            results: function (data, page) {
                return {results: data};
            }
        }
    })

    $('#searchusers').on('change', function(event) {
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
    })

})
