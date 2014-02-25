function set_value_from(form, field, settings) {

    settings[field] = $form.find('#'+field+'.form-control').val()
}


$(document).ready(function() {
    $('[rel="tooltip"]').tooltip();

    $form = $('form#maxui-settings')
    $form.on('change', '.form-control', function(event) {
        settings = {}
        set_value_from($form, 'language', settings)
        set_value_from($form, 'activitySource', settings)
        set_value_from($form, 'readContext', settings)
        set_value_from($form, 'activitySortOrder', settings)
        reloadWidget(settings)
        url = $form.attr('data-session-update')
        $.post(url, settings)
    })

});


function reloadWidget(new_settings) {
    $('#activityStream').replaceWith(' <div id="activityStream"></div>')
    console.log(new_settings)
    var settings = {
           'language': new_settings.language,
           'domain': window._MAXUI.domain,
           'username' : window._MAXUI.username,
           'oAuthToken' : window._MAXUI.token,
           'oAuthGrantType' : window._MAXUI.grant,
           'maxServerURL' : window._MAXUI.server,
           'maxServerURLAlias' : '',
           'maxTalkURL': window._MAXUI.stomp,
           'avatarURLpattern' : '',
           'readContext': new_settings.readContext,
           'activitySource': new_settings.activitySource,
           'activitySortOrder': new_settings.activitySortOrder
           }

    $('#activityStream').animate({'opacity': 0}, 200, function(event) {
        $('#activityStream').maxUI(settings)
        $('#activityStream').animate({'opacity': 1}, 200)
    })


}
