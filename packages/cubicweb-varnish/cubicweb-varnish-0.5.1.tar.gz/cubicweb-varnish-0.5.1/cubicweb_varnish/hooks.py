# copyright 2011-2017 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-varnish specific hooks and operations"""

from __future__ import with_statement

from six.moves.urllib.parse import urlparse

from cubicweb.predicates import adaptable
from cubicweb.server import hook

from cubicweb_varnish.varnishadm import varnish_cli_connect_from_config


class PurgeUrlsOnUpdate(hook.Hook):
    """an entity was updated, purge related urls"""
    __regid__ = 'varnish.purge'
    category = 'varnish'
    __select__ = hook.Hook.__select__ & adaptable('IVarnish')
    events = ('before_update_entity',)

    def __call__(self):
        invalidate_cache_op = InvalidateVarnishCacheOp.get_instance(self._cw)
        ivarnish = self.entity.cw_adapt_to('IVarnish')
        for url in ivarnish.urls_to_purge():
            invalidate_cache_op.add_data(url)

# XXX need to think other hook events (after_delete_entity, after_*_relation)


# operations #################################################################
class InvalidateVarnishCacheOp(hook.DataOperationMixIn, hook.Operation):
    def precommit_event(self):
        config = self.cnx.vreg.config
        varnish_version = config.get('varnish-version', 5)
        if varnish_version == 2:
            purge_cmd = 'purge.url'
        elif varnish_version == 3:
            purge_cmd = 'ban.url'
        elif varnish_version >= 4:
            purge_cmd = 'ban req.url ~'
        else:
            raise ValueError('Unsupported varnish version %s'
                             % varnish_version)
        cnxs = varnish_cli_connect_from_config(config)
        for url in self.get_data():
            for varnish_cli in cnxs:
                varnish_cli.execute(purge_cmd, '^%s$' % urlparse(url).path)
        for varnish_cli in cnxs:
            varnish_cli.close()
