from chatterbot.adapters.input import InputAdapter
from chatterbot.conversation import Statement
from lxml import etree
import time

from debuglogger import logfile

class WXChat(InputAdapter):
    """
    An input adapter that allows a ChatterBot instance to get
    input statements from a HipChat room.
    """
    def process_input(self, payload, **kwargs):

        xml = etree.fromstring(payload)
        msgType = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text
        createTime = int(time.time())

        assert msgType == 'text'

        content = xml.find("Content").text.lower()

        statement = Statement(content)
        statement.add_extra_data("fromUser", fromUser)
        statement.add_extra_data("toUser", toUser)
        statement.add_extra_data("createTime", createTime)

        print >> logfile, statement.extra_data
        return statement
