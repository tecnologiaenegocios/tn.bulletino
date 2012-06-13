from zope.i18nmessageid import MessageFactory
_ = MessageFactory('tn.bulletino')

from five import grok
from plone.app.dexterity.behaviors.metadata import ICategorization
from tn.plonehtmlimagecache.interfaces import IHTMLAttribute
from tn.plonehtmlpage.html_page import IHTMLPageSchema
from tn.plonemailing.interfaces import INewsletterHTML
from tn.plonestyledpage import styled_page

import zope.component
import zope.globalrequest


apply = lambda f: f()


class HTMLAttributeMixin(object):

    @apply
    def html():
        def get(self): return self.context.html
        def set(self, value): self.context.html = value
        return property(get, set)


class HTMLPageHTMLAttribute(grok.Adapter, HTMLAttributeMixin):
    grok.context(IHTMLPageSchema)
    grok.implements(IHTMLAttribute)


class HTMLPageNewsletterHTML(grok.Adapter, HTMLAttributeMixin):
    grok.context(IHTMLPageSchema)
    grok.implements(INewsletterHTML)


class StyledPageNewsletterHTML(grok.Adapter):
    grok.context(styled_page.IStyledPageSchema)
    grok.implements(INewsletterHTML)

    @property
    def html(self):
        return u"%(doctype)s\n<html %(html_attrs)s>%(head)s%(body)s</html>" % {
            'doctype': u'<!DOCTYPE html>',
            'html_attrs': u'lang="%s"' % self.get_language(),
            'head': self.get_head(),
            'body': u'<body>%s</body>' % self.context.body.output
        }

    def get_language(self):
        metadata = ICategorization(self.context, None)
        if metadata and metadata.language:
            return metadata.language
        return self.get_language_from_portal()

    def get_language_from_portal(self):
        request = zope.globalrequest.getRequest()
        portal_state = zope.component.getMultiAdapter(
            (self.context, request),
            name="plone_portal_state"
        )
        return portal_state.default_language()

    def get_head(self):
        return u"<head><title>%(title)s</title>%(style)s</head>" % {
            'title': self.context.title,
            'style': styled_page.getStyleBlock(self.context)
        }
