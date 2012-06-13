from zope.i18nmessageid import MessageFactory
_ = MessageFactory('tn.bulletino')

from five import grok
from tn.plonehtmlimagecache.interfaces import IHTMLAttribute
from tn.plonehtmlpage.html_page import IHTMLPageSchema
from tn.plonemailing.interfaces import INewsletterHTML
from tn.plonestyledpage import styled_page


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
            'doctype': u'',
            'html_attrs': u'',
            'head': self.get_head(),
            'body': self.get_body(),
        }

    def get_head(self):
        return u"<head>%(title)s%(style)s</head>" % {
            'title': self.get_title(),
            'style': self.get_style(),
        }

    def get_title(self):
        return u"<title>%s</title>" % self.context.title

    def get_style(self):
        escaped_styles = styled_page.getEscapedStyles(self.context)
        cdata_block = u"/*<![CDATA[*/%s/*]]>*/" % escaped_styles
        return u'<style type="text/css" media="all">%s</style>' % cdata_block

    def get_body(self):
        return u'<body id="%s">%s</body>' % (
            styled_page.getUniqueId(self.context), self.context.body.output
        )
