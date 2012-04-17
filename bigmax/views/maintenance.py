from pyramid.view import view_config
from bigmax.views.api import TemplateAPI
from max.rest.utils import findKeywords, findHashtags


@view_config(name="maintenance", renderer='bigmax:templates/maintenance.pt', permission='restricted')
def configView(context, request):

    # XXX TODO Refactor this into a maintenance webservice in MAX

    page_title = "BIG MAX Server Config"
    api = TemplateAPI(context, request, page_title)
    success = False
    message = ''
    if request.params.get('form.rebuildKeywords', None) is not None:
        db = context.db
        activities = db.activity.find({'object.content': {'$exists': True}})
        for activity in activities:

            keywords = findKeywords(activity['object']['content'])
            hashtags = findHashtags(activity['object']['content'])

            replies = activity.get('replies', {}).get('items', [])
            for reply in replies:
                keywords.extend(findKeywords(reply.get('content', u'')))
                hashtags.extend(findHashtags(reply.get('content', u'')))

            keywords = list(set(keywords))
            hashtags = list(set(hashtags))

            db.activity.update({'_id': activity['_id']}, {'$set': {'object._keywords': keywords, 'object._hashtags': hashtags}})
        success = True
        message = 'Keywords rebuilded!'

    if request.params.get('form.resetPermissions', None) is not None:
        db = context.db
        contexts = {context['url']: context for context in db.contexts.find()}
        users = db.users.find()
        for user in users:
            subscriptions = user.get('subscribedTo', {})
            items = subscriptions.get('items', [])
            if items:
                for item in items:
                    curl = item.get('url')
                    permissions = ['read']
                    context = contexts.get(curl)
                    if context:
                        if context['permissions']['write'] == 'subscribed':
                            permissions.append('write')
                        item['permissions'] = permissions
                        for field in ['displayName']:
                            if context.get(field, None):
                                item[field] = context[field]

                #Purge subscriptions without context
                items = [item for item in items if item.get('permissions', None)]

                db.users.update({'_id': user['_id']}, {'$set': {'subscribedTo.items': items}})

        success = True
        message = 'Permissions Reseted to contexts defaults'

    return dict(api=api,
                url='%s/maintenance' % api.application_url,
                success=success,
                message=message)
    return {}
