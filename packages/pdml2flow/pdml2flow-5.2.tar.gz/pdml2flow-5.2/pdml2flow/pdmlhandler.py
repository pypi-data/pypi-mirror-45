#!/usr/bin/env python3
# vim: set fenc=utf8 ts=4 sw=4 et :
import xml.sax
import functools

from .autovivification import AutoVivification
from .utils import autoconvert, call_plugin
from .conf import Conf
from .flow import Flow
from .logging import *

class PdmlHandler(xml.sax.ContentHandler):

    def __init__(self):
        self.__frame = AutoVivification()
        self.__flows = {}

    # Call when an element starts
    def startElement(self, tag, attributes):
        if tag == 'packet':
            self.__frame = AutoVivification()
        else:
            if 'name' in  attributes:
                name = attributes.getValue('name')
                if len(name) > 0:
                    merge = False
                    # Build object tree
                    new = AutoVivification()
                    name_access = functools.reduce(
                        lambda x,y: x[y], [new] + name.split(Conf.PDML_NESTCHAR)
                    )
                    # Extract raw data
                    if 'show' in attributes:
                        show = attributes.getValue('show')
                        if len(show) > Conf.DATA_MAXLEN:
                            show = Conf.DATA_TOO_LONG
                        if len(show) > 0:
                            debug('{}.raw: {}'.format(name, show))
                            name_access['raw'] = [autoconvert(show)]
                            merge = True
                    # Extract showname
                    if 'showname' in attributes and Conf.EXTRACT_SHOW:
                        showname = attributes.getValue('showname')
                        if len(showname) > Conf.DATA_MAXLEN:
                            showname = Conf.DATA_TOO_LONG
                        if len(showname) > 0:
                            debug('{}.show: {}'.format(name, showname))
                            name_access['show'] = [showname]
                            merge = True
                    if merge:
                        self.__frame.merge(new)

    # Call when an elements ends
    def endElement(self, tag):
        if tag == 'packet':
            # advance time
            try:
                Flow.newest_overall_frame_time = max(
                    Flow.newest_overall_frame_time,
                    self.__frame[Conf.FRAME_TIME]
                )
            except TypeError:
                warning(
                    'Dropping frame because of invalid time ({}) in {}'.format(
                        self.__frame[Conf.FRAME_TIME],
                        Conf.FRAME_TIME
                    )
                )
                return

            # write out expired flows
            new_flows = {}
            for (flowid, flow) in self.__flows.items():
                if flow.not_expired():
                    new_flows[flowid] = flow
                else:
                    flow.expired()
            self.__flows = new_flows
            # the flow definition
            flowid = Flow.get_flow_id(self.__frame)
            # ignore frames without a flowid
            if flowid:
                try: 
                    flow = self.__flows[flowid]
                    self.__flows[flowid].add_frame(self.__frame)
                    debug('old flow: {}'.format(flowid))
                except KeyError:
                    # flow unknown add new flow
                    flow = self.__flows[flowid] = Flow(self.__frame)
                    debug('new flow: {}'.format(flowid))
            else:
                for plugin in Conf.PLUGINS:
                    call_plugin(
                        plugin,
                        'frame_new',
                        self.__frame.cast_dicts(dict),
                        None
                    )

    def endDocument(self):
        for (flowid, flow) in self.__flows.items():
            flow.end()

        for plugin in Conf.PLUGINS:
            call_plugin(
                plugin,
                '__deinit__'
            )
