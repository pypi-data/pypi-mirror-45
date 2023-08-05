import sys,re
from ..util import getkey,read_file,str_indent
from .path import normalize
from html.parser import HTMLParser

__all__ = ['SVGParser']

class SVGParser(HTMLParser):
    def __init__(self,report_warnings=True):
        """Parse SVG"""
        super().__init__()
        self.stack = []
        self.attrs = []
        self.cache = []
        self.content = ''
        self.report_warnings = report_warnings

    # Override feed to return self
    def feed(self,file):
        super().feed(read_file(file))
        return self
    
    # --------- viewbox --------- #
    def viewbox(self,i):
        if self.stack[i] not in ['marker','pattern','svg','symbol','view']:
            return None
        if 'viewBox' in self.attrs[i]:
            return self.attrs[i]['viewBox']
        if 'viewbox' in self.attrs[i]:
            return self.attrs[i]['viewbox']
        return None

    def extract_viewbox(self,i):
        if self.stack[i] not in ['marker','pattern','svg','symbol','view']:
            return None
        if 'viewBox' in self.attrs[i]:
            vb = self.attrs[i]['viewBox']
            del self.attrs[i]['viewBox']
            return vb
        if 'viewbox' in self.attrs[i]:
            vb = self.attrs[i]['viewbox']
            del self.attrs[i]['viewbox']
            return vb
        return None
    
    def retrieve_viewbox(self):
        for i in reversed(range(len(self.stack))):
            x = self.viewbox(i)
            if x is not None:
                return x
        return None


    # --------- Handle start-tag --------- #
    def handle_starttag(self,tag,attrs):
        attrs = dict(attrs)
        if tag == 'path' and 'd' in attrs:
            viewbox = self.retrieve_viewbox()
            if viewbox is not None:
                attrs['d'] = normalize(attrs['d'],viewbox)
        self.stack.append(tag)
        self.attrs.append(attrs)
        self.cache.append('')


    # --------- Handle end-tag --------- #
    def handle_endtag(self,tag):
        for i in reversed(range(len(self.stack))):
            if self.stack[i]==tag:
                break
        else:
            if self.report_warnings == True:
                print(f"Table Parse Warning: {tag} Tags Imbalanced",file=sys.stderr)
            return
        viewbox = self.extract_viewbox(i)
        if viewbox is not None:
            self.attrs[i]['viewBox'] = re.sub(r'\d+(?: +|,)\d+$','1 1',viewbox.strip())
        attrs = ''.join(' %s="%s"'%(k,v.replace('"',"'")) for k,v in self.attrs[i].items())
        if len(self.cache[i]) > 0:
            ele = f"<{tag}{attrs}>\n{str_indent(self.cache[i])}\n</{tag}>"
        else:
            ele = f"<{tag}{attrs}>{self.cache[i]}</{tag}>"
        if i == 0:
            if len(self.content) > 0:
                ele = '\n'+ele
            self.content += ele
        else:
            if len(self.cache[i-1]) > 0:
                ele = '\n'+ele
            self.cache[i-1] += ele
        self.stack = self.stack[:i]
        self.cache = self.cache[:i]
        self.attrs = self.attrs[:i]
    
    
    # --------- Handle tag-contents --------- #
    def handle_data(self,data):
        text = data.strip()
        if len(text) == 0:return
        self.cache[-1]+=text
