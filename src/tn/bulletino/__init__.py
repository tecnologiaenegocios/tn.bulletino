from zope.i18nmessageid import MessageFactory
_ = MessageFactory('tn.bulletino')

from five import grok
from plone.app.dexterity.behaviors.metadata import ICategorization
from tn.plonebehavior.template import ITemplatingMarker
from tn.plonebehavior.template import getTemplate
from tn.plonehtmlimagecache.interfaces import IHTMLAttribute
from tn.plonehtmlpage.html_page import IHTMLPageSchema
from tn.plonemailing.interfaces import INewsletterHTML
from tn.plonestyledpage import styled_page

import lxml.builder
import lxml.html
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
        if ITemplatingMarker.providedBy(self.context):
            html = getTemplate(self.context).compile(self.context)
            return self.add_title(html)
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

    def add_title(self, html):
        tree = lxml.html.document_fromstring(html)
        if not tree.xpath('/html/head/title'):
            title = lxml.builder.E.title(self.context.title)
            tree.head.insert(0, title)
        else:
            title = tree.xpath('/html/head/title')[0]
            title.text = self.context.title
        return lxml.html.tostring(tree)
