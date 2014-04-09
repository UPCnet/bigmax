
/*
* Defines a global namespace var to hold maxui stuff, and a function onReady that
* will be called as a result of the maxui code being completely loaded.
* Custom settings and instantiation of maxui MUST be done in the onReady function body
* Other calculations that needs maxui to be loaded MAY be done also in the onReady function body
*/

window._MAXUI.onReady = function() {
    // This is called when the code has loaded.

    var settings = {
           'language': window._MAXUI.language,
           'username' : window._MAXUI.username,
           'oAuthToken' : window._MAXUI.token,
           'oAuthGrantType' : window._MAXUI.grant,
           'maxServerURL' : window._MAXUI.server,
           'maxServerURLAlias' : '',
           'maxTalkURL': window._MAXUI.stomp,
           'avatarURLpattern' : '',
           'readContext': window._MAXUI.readContext,
           'activitySource': window._MAXUI.activitySource,
           'domain': window._MAXUI.domain
           };

    $('#activityStream').maxUI(settings);
};

/*
* Loads the maxui code asynchronously
* The generated script tag will be inserted after the first existing script tag
* found in the document.
* Modify `mui_location` according to yout settings
*/

(function(d){
var mui_location = window._MAXUI.server+'/maxui/maxui.min.js';
var mui = d.createElement('script'); mui.type = 'text/javascript'; mui.async = true;
mui.src = mui_location;
var s = d.getElementsByTagName('script')[0]; s.parentNode.insertBefore(mui, s);

}(document));
