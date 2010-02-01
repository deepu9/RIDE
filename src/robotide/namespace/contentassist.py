#  Copyright 2008-2009 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from robotide import utils


class ContentAssistItem(object):

    def __init__(self, source, name, details=''):
        self.source = source
        self.name = name
        self.details = details

    def get_details(self):
        return self.details


class _KeywordContent(object):

    def __init__(self, item, source, source_type):
        self.name = self._get_name(item)
        self.source = source
        self.longname = "%s.%s" % (source, self.name)
        self.doc = self._get_doc(item)
        self.shortdoc = self.doc and self.doc.splitlines()[0] or ''
        self.args = self._format_args(self._parse_args(item))
        self._source_type = source_type

    def get_details(self):
        doc = utils.html_escape(self.doc, formatting=True)
        return 'Source: %s &lt;%s&gt;<br><br>Arguments: %s<br><br>%s' % \
                (self.source, self._source_type, self.args, doc)

    def _get_name(self, item):
        return item.name

    def _get_doc(self, item):
        return item.doc

    def _format_args(self, args):
        return '[ %s ]' % ' | '.join(args)

    def is_library_keyword(self):
        return False


class UserKeywordContent(_KeywordContent):

    def _get_doc(self, uk):
        return uk.doc

    def _parse_args(self, uk):
        return [ self._format_arg(arg) for arg in uk.settings.args.value ]

    def _format_arg(self, arg):
        argstr = ''
        if arg and arg[0] == '@':
            argstr += '*'
        tokens = arg.split('=', 1)
        name = tokens[0]
        def_value = len(tokens) > 1 and tokens[1] or ''
        argstr += name[2:-1] # Strip ${} or @{}
        if def_value:
            argstr += '=%s' % def_value
        return argstr

