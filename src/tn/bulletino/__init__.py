from zope.i18nmessageid import MessageFactory
_ = MessageFactory('tn.bulletino')

from five import grok
from tn.plonehtmlimagecache.interfaces import IHTMLAttribute
from tn.plonehtmlpage.html_page import IHTMLPageSchema
from tn.plonemailing.interfaces import INewsletterHTML


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
