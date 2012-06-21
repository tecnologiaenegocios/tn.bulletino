from five import grok
from Products.statusmessages.interfaces import IStatusMessage
from plone.directives import form
from tn.bulletino import _
from tn.plonemailing import interfaces as pminterfaces
from tn.plonemailing import behaviors
from z3c.form import button

import zope.schema
import zope.component


class TestSubscriber(object):
    grok.implements(pminterfaces.ISubscriber)

    def __init__(self, email, format, prefs_url, removal_url):
        self.name = u'Test Subscriber'
        self.email = email
        self.format = format
        self.preferences_url = prefs_url
        self.removal_url = removal_url


class ITestSchema(form.Schema):

    test_recipient_address = zope.schema.TextLine(
        title=_(u'Test recipient'),
        required=True,
    )

    formats = zope.schema.Tuple(
        title=_(u'Formats'),
        value_type=zope.schema.Choice(
            values=[u'html', u'text']
        ),
        missing_value=(),
        required=True,
    )


class ISendSchema(form.Schema):
    pass


class TestForm(form.SchemaForm):
    grok.require('tn.bulletino.SendContent')
    grok.context(behaviors.INewsletterFromContentMarker)

    schema = ITestSchema
    ignoreContext = True
    prefix = 'test'

    label = _(u'Test your newsletter')
    description = _(u'Send this newsletter to your own e-mail address in '
                    u'order to see how it will appear to your audience.')

    @button.buttonAndHandler(_(u'Perform test'))
    def handleTest(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        subscribers = [
            TestSubscriber(data['test_recipient_address'],
                           format,
                           None,
                           self.context.absolute_url())
            for format in data['formats']
        ]

        mailing = zope.component.getUtility(pminterfaces.IMailing)
        mailing.send(self.context, subscribers=subscribers,
                     suppress_events=True)

        IStatusMessage(self.request).add(_(u'Message successfully sent.'),
                                         type='info')
        self.redirect(self.context.absolute_url())


class SendForm(form.SchemaForm):
    grok.require('tn.bulletino.SendContent')
    grok.context(behaviors.INewsletterFromContentMarker)

    schema = ISendSchema
    ignoreContext = True
    prefix = 'send'

    label = _(u'Send your newsletter to all subscribers')
    description = _(u"By pressing the button below you will send this "
                    u'newsletter to all of your audience.')

    @button.buttonAndHandler(_(u'Send to all recipients'))
    def handleSend(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        mailing = zope.component.getUtility(pminterfaces.IMailing)
        mailing.send(self.context)

        IStatusMessage(self.request).add(_(u'Message successfully sent.'),
                                         type='info')
        self.redirect(self.context.absolute_url())


class Send(grok.View):
    grok.require('tn.bulletino.SendContent')
    grok.context(behaviors.INewsletterFromContentMarker)

    def update(self):
        super(Send, self).update()
        self.test_form.update()
        self.send_form.update()

    def __init__(self, context, request):
        super(Send, self).__init__(context, request)
        self.test_form = TestForm(context, request)
        self.send_form = SendForm(context, request)

    def subscriber_stats(self):
        formats = {}
        for subscriber in self.subscribers():
            if subscriber.format not in formats:
                formats[subscriber.format] = 0
            formats[subscriber.format] += 1
        return formats

    def subscribers(self):
        mailing = zope.component.getUtility(pminterfaces.IMailing)
        return mailing.iterSubscribers(self.context)
