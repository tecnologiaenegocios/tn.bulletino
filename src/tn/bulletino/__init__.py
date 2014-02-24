from zope.i18nmessageid import MessageFactory
_ = MessageFactory('tn.bulletino')

from five import grok
from tn.plonebehavior.template.interfaces import ITemplate
from tn.plonehtmlimagecache.interfaces import IHTMLAttribute
from tn.plonehtmlpage.html_page import IHTMLPageSchema
from tn.plonemailing.interfaces import INewsletterHTML
from tn.plonestyledpage import styled_page

import lxml.builder
import lxml.html


class HTMLPageHTMLAttribute(grok.Adapter):
    grok.context(IHTMLPageSchema)
    grok.implements(IHTMLAttribute)

    @property
    def html(self):
        return self.context.html

    @html.setter
    def html(self, value):
        self.context.html = value


class HTMLPageNewsletterHTML(grok.Adapter):
    grok.context(IHTMLPageSchema)
    grok.implements(INewsletterHTML)

    @property
    def html(self):
        html = self.context.html
        tree = lxml.html.document_fromstring(html)
        tree.make_links_absolute(self.context.absolute_url())
        return lxml.html.tostring(tree)


class StyledPageNewsletterHTML(grok.Adapter):
    grok.context(styled_page.IStyledPageSchema)
    grok.implements(INewsletterHTML)

    @property
    def html(self):
        template = ITemplate(self.context)
        html = template.compile(self.context)
        return self.add_title(html)

    def add_title(self, html):
        tree = lxml.html.document_fromstring(html)
        if not tree.xpath('/html/head/title'):
            title = lxml.builder.E.title(self.context.title)
            tree.head.insert(0, title)
        else:
            title = tree.xpath('/html/head/title')[0]
            title.text = self.context.title
        return lxml.html.tostring(tree)
