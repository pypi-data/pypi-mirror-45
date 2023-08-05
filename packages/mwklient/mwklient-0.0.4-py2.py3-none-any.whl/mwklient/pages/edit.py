import time
from six import text_type
from mwklient.util import parse_timestamp
import mwklient.listing
import mwklient.errors


class Mixin:

    def text(self,
             section=None,
             expandtemplates=False,
             cache=True,
             slot='main'):
        """Get the current wikitext of the page, or of a specific section.

        If the page does not exist, an empty string is returned. By
        default, results will be cached and if you call text() again
        with the same section and expandtemplates the result will come
        from the cache. The cache is stored on the instance, so it
        lives as long as the instance does.

        Args:
            section (int): numbered section or `None` to get the whole page
            (default: `None`)
            expandtemplates (bool): set to `True` to expand templates
            (default: `False`)
            cache (bool): set to `False` to disable caching (default: `True`)
        """

        if not self.can('read'):
            raise mwklient.errors.InsufficientPermission(self)
        if not self.exists:
            return u''
        if section is not None:  # can be 0
            section = text_type(section)

        key = hash((section, expandtemplates))
        if cache and key in self._textcache:
            return self._textcache[key]

        revs = self.revisions(
            prop='content|timestamp', limit=1, section=section, slots=slot)
        try:
            rev = next(revs)
            if 'slots' in rev:
                text = rev['slots'][slot]['*']
            else:
                text = rev['*']
            self.last_rev_time = rev['timestamp']
        except StopIteration:
            text = u''
            self.last_rev_time = None
        if not expandtemplates:
            self.edit_time = time.gmtime()
        else:
            # The 'rvexpandtemplates' option was removed in MediaWiki 1.32, so
            # we have to make an extra API call.
            # See: https://github.com/mwclient/mwclient/issues/214
            text = self.site.expandtemplates(text)

        if cache:
            self._textcache[key] = text
        return text

    def __check_edit__(self):
        if not self.site.logged_in and self.site.force_login:
            raise mwklient.errors.AssertUserFailedError()
        if self.site.blocked:
            raise mwklient.errors.UserBlocked(self.site.blocked)
        if not self.can('edit'):
            raise mwklient.errors.ProtectedPageError(self)

        if not self.site.writeapi:
            raise mwklient.errors.NoWriteApi(self)

    def __do_edit__(self, **kwargs):
        result = self.site.post(
            'edit',
            token=self.__get_token__('edit'),
            **kwargs)
        if result['edit'].get('result').lower() == 'failure':
            raise mwklient.errors.EditError(self, result['edit'])
        return result

    def save(self,
             text,
             summary=u'',
             minor=False,
             bot=True,
             section=None,
             **kwargs):
        """Update the text of a section or the whole page by performing an edit
         operation.
        """

        self.__check_edit__()

        data = {}
        if minor:
            data['minor'] = '1'
        if not minor:
            data['notminor'] = '1'
        if self.last_rev_time:
            data['basetimestamp'] = time.strftime('%Y%m%d%H%M%S',
                                                  self.last_rev_time)
        if self.edit_time:
            data['starttimestamp'] = time.strftime('%Y%m%d%H%M%S',
                                                   self.edit_time)
        if bot:
            data['bot'] = '1'
        if section:
            data['section'] = section

        data['title'] = self.name
        data['text'] = text
        data['summary'] = summary
        data.update(kwargs)

        if self.site.force_login:
            data['assert'] = 'user'

        try:
            result = self.__do_edit__(**data)
        except mwklient.errors.APIError as err:
            if err.code == 'badtoken':
                # Retry, but only once to avoid an infinite loop
                self.__get_token__('edit', force=True)
                try:
                    result = self.__do_edit__()
                except mwklient.errors.APIError as err:
                    self.handle_edit_error(err, summary)
            else:
                self.handle_edit_error(err, summary)

        # 'newtimestamp' is not included if no change was made
        if 'newtimestamp' in result['edit'].keys():
            self.last_rev_time = parse_timestamp(
                result['edit'].get('newtimestamp'))

        # clear the page text cache
        self._textcache = {}
        return result['edit']

    def undo(self, rev_id, summary=u'', bot=False, **kwargs):
        """Revert an edit with revision id `rev`
        """

        self.__check_edit__()
        data = {}
        if self.last_rev_time:
            data['basetimestamp'] = time.strftime('%Y%m%d%H%M%S',
                                                  self.last_rev_time)
        if self.edit_time:
            data['starttimestamp'] = time.strftime('%Y%m%d%H%M%S',
                                                   self.edit_time)

        data['undo'] = rev_id
        data['bot'] = '1' if bot else '0'
        data['title'] = self.name
        data['summary'] = summary
        data.update(kwargs)

        if self.site.force_login:
            data['assert'] = 'user'

        try:
            result = self.__do_edit__(**data)
        except mwklient.errors.APIError as err:
            if err.code == 'badtoken':
                # Retry, but only once to avoid an infinite loop
                self.__get_token__('edit', force=True)
                try:
                    result = self.__do_edit__(**data)
                except mwklient.errors.APIError as err:
                    self.handle_edit_error(err, summary)
            else:
                self.handle_edit_error(err, summary)

        # 'newtimestamp' is not included if no change was made
        if 'newtimestamp' in result['edit'].keys():
            self.last_rev_time = parse_timestamp(
                result['edit'].get('newtimestamp'))

        # clear the page text cache
        self._textcache = {}
        return result['edit']

    def handle_edit_error(self, err, summary):
        if err.code == 'editconflict':
            raise mwklient.errors.EditError(self, summary, err.info)
        if err.code in {
                'protectedtitle', 'cantcreate', 'cantcreate-anon',
                'noimageredirect-anon', 'noimageredirect', 'noedit-anon',
                'noedit', 'protectedpage', 'cascadeprotected',
                'customcssjsprotected', 'protectednamespace-interface',
                'protectednamespace'
        }:
            raise mwklient.errors.ProtectedPageError(self, err.code, err.info)
        if err.code == 'assertuserfailed':
            raise mwklient.errors.AssertUserFailedError()
        raise err
