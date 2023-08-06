# vim: set fenc=utf8 ts=4 sw=4 et :
import json
import dict2xml

from .autovivification import AutoVivification
from .conf import Conf
from .utils import call_plugin
from .logging import *

class Flow():

    #  The overall frame time
    newest_overall_frame_time = 0

    @staticmethod
    def get_flow_id(frame):
        flowid = [frame[d] for d in Conf.FLOW_DEF]
        valid = any([type(i) is not AutoVivification for i in flowid])
        # check if flowid is empty
        if not valid:
            return None
        return str(flowid)

    def __init__(self, first_frame):
        first_frame_time = first_frame[Conf.FRAME_TIME]
        self.__newest_frame_time = self.__first_frame_time = first_frame_time
        self.__id = self.get_flow_id(first_frame)
        if Conf.FRAMES_ARRAY:
            self.__frames = []
        else:
            self.__frames = AutoVivification()
        self.__framecount = 0

        for plugin in Conf.PLUGINS:
            call_plugin(
                plugin,
                'flow_new',
                self,
                first_frame.cast_dicts(dict)
            )

        self.add_frame(first_frame)

    def __hash__(self):
        return hash(self.__id)

    def __eq__(self, other):
        return self.__id == other.__id

    @property
    def id(self):
        return self.__id

    @property
    def frames(self):
        # clean the frame data
        if Conf.FRAMES_ARRAY:
            self.__frames = [
                f.clean_empty()
                for f in self.__frames
            ]
            ret = [
                f.cast_dicts(dict)
                for f in self.__frames
            ]
        else:
            self.__frames = self.__frames.clean_empty()
            ret = self.__frames.cast_dicts(dict)

        return ret

    @property
    def first_frame_time(self):
        return self.__first_frame_time

    @property
    def newest_frame_time(self):
        return self.__newest_frame_time

    @property
    def framecount(self):
        return self.__framecount

    def add_frame(self, frame):
        # check if frame expands flow length
        frame_time = frame[Conf.FRAME_TIME]
        self.__first_frame_time = min(self.__first_frame_time, frame_time) 
        self.__newest_frame_time = max(self.__newest_frame_time, frame_time)
        self.__framecount += 1
        # Extract data
        if Conf.FRAMES_ARRAY:
            self.__frames.append(
                frame.clean_empty()
            )
        else:
            self.__frames.merge(
                frame.clean_empty()
            )

        if Conf.COMPRESS_DATA:
            self.__frames = self.__frames.compress()

        debug(
            'flow duration: {}'.format(
                self.__newest_frame_time - self.__first_frame_time
            )
        )

        for plugin in Conf.PLUGINS:
            call_plugin(
                plugin,
                'frame_new',
                frame.cast_dicts(dict),
                self
            )

    def not_expired(self):
        return self.__newest_frame_time > (Flow.newest_overall_frame_time - Conf.FLOW_BUFFER_TIME)

    def expired(self):
        for plugin in Conf.PLUGINS:
            call_plugin(
                plugin,
                'flow_expired',
                self
            )
        self.end()

    def end(self):
        for plugin in Conf.PLUGINS:
            call_plugin(
                plugin,
                'flow_end',
                self
            )

