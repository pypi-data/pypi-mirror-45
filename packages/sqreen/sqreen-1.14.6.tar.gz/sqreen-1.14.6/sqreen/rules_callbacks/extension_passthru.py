# -*- coding: utf-8 -*-
# Copyright (c) 2016, 2017, 2018, 2019 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#

import logging
from collections import Mapping

from sqreen.exceptions import InvalidArgument
from sqreen.rules import RuleCallback
from sqreen.utils import is_string

LOGGER = logging.getLogger(__name__)


class ExtensionPassthruCB(RuleCallback):
    """Daemon callback that just raises with the data the extension gives"""

    def __init__(self, *args, **kwargs):
        super(ExtensionPassthruCB, self).__init__(*args, **kwargs)

        if not isinstance(self.data, Mapping):
            msg = 'Invalid data type received: {}'
            raise InvalidArgument(msg.format(type(self.data)))

        try:
            self.cb_info_props = self.data['info_props']
        except KeyError:
            msg = "No key 'info_props' in data (had {})"
            raise InvalidArgument(msg.format(self.data.keys()))

        if not isinstance(self.cb_info_props, Mapping):
            msg = "Invalid data type received for 'info_props' in data: {}"
            raise InvalidArgument(msg.format(type(self.cb_info_props)))

    # info keys are stored like this in the rule:
    # rule = {
    #   "data": {
    #     "info_props": {
    #       "pre": { <- upon data receiving, will generate attack with this info
    #         "found": "#.cargs[0]"
    #       }
    #     }
    #   }
    #   "callbacks": { <- determines what gets sent to the daemon
    #     "pre": [
    #       "#.request_params",
    #       "#.cargs[0]",
    #       "javascript code" <- extension ignores last element
    #     ]
    #   }
    # }
    def __fetch_info_props(self, cb_name):
        ret = self.cb_info_props.get(cb_name)
        if not isinstance(ret, dict) or \
                any([not is_string(k) or not is_string(v)
                     for (k, v) in ret.items()]):
            LOGGER.warning("Invalid info props spec: %s", ret)
            return {}
        return ret

    def __build_info(self, info_props):
        # map ba expr -> its resolution, as calculated by ext
        cmd_args = self.storage.get_cmd_arguments()
        if cmd_args is None:
            cmd_args = {}

        return {
            k: cmd_args.get(ba_expr) for (k, ba_expr) in info_props.items()
        }

    def pre(self, original, *args, **kwargs):
        info_props = self.__fetch_info_props('pre')
        attack_rec = self.__build_info(info_props)

        if len(attack_rec) != 0:
            self.record_attack(attack_rec)

        # we don't support other returns
        return {'status': 'raise'}

    def post(self, original, return_value, *args, **kwargs):
        LOGGER.error("Called unsupported 'post' method")
        return

    def failing(self, original, exception, *args, **kwargs):
        LOGGER.error("Called unsupported 'failing' method")
        return
