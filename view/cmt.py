#!/usr/bin/env python
#    This file is part of le(n)x.

#    le(n)x is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    le(n)x is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with le(n)x.  If not, see <http://www.gnu.org/licenses/>.

# (C) 2009-2010 by Stefan Marsiske, <stefan.marsiske@gmail.com>

import re, urllib2

CMTRE = re.compile(r'^\W*(https?:\/\/)?(.+\.co-ment.com)(/text)?(\/[a-zA-Z0-9]+)(/.+/?)?\W*$', re.I | re.U)
from lenx.view.doc import DOC, Doc, unescape
from lenx.view.db import Docs

class Coment(DOC):
    def __init__(self, docid=None, *args,**kwargs):
        self.__dict__['type'] = 'co-ment'
        if docid:
            hostValidator = CMTRE.search(docid)
            if hostValidator:
                if hostValidator.group(1) or hostValidator.group(3) or hostValidator.group(5):
                    docid=("%s%s" % (hostValidator.group(2), hostValidator.group(4))).encode('utf8')
                    kwargs['docid']=docid
                url="https://%s/text/%s/view/" % (hostValidator.group(2), hostValidator.group(4))
                if not Docs.find_one({"docid": docid}):
                    context = urllib2.urlopen(url).read()
                    soup = BeautifulSoup(context)
                    self.__dict__['title']=unescape(unicode(''.join(soup.title.findAll(text=True)))).strip().encode('utf8')

                    dataurl = "https://%s/text%s/comments/" % (hostValidator.group(2), hostValidator.group(4))
                    data = urllib2.urlopen(dataurl).read()
                    soup = BeautifulSoup(data)

                    kwargs['raw'] = '<html><head><title>%s</title><meta http-equiv="content-type" content="text/html; charset=utf-8" /></head><body>%s</body></html>' % (self.title, unescape(unicode(soup.find(attrs={'id' : 'textcontainer'}))).encode('utf8'))
                    kwargs['docid']=docid
                    super(Coment,self).__init__(*args, **kwargs)
                    if not 'stems' in self.__dict__ or not self.stems:
                        # let's calculate and cache the results
                        models.tfidf.add_input_document(self.termcnt.keys())
                        self.save()
                    return
            kwargs['docid']=docid
        super(Coment,self).__init__(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.title)

from django.core.management import setup_environ
from lenx import settings
setup_environ(settings)
from lenx.brain import cache as Cache
CACHE=Cache.Cache(settings.CACHE_PATH)
from BeautifulSoup import BeautifulSoup
from datetime import date
import urllib2
import models

if __name__ == "__main__":
    url='https://actamotion.co-ment.com/text/LbtpIg2HWfs/view/'
    Coment(url=url)
