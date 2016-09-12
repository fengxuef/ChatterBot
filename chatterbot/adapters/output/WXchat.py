from chatterbot.adapters.output import OutputAdapter
from chatterbot.utils.read_input import input_function

resp_templ=u"""
<xml>
    <ToUserName>
        <![CDATA[{fromUser}]]>
    </ToUserName>
    <FromUserName>
        <![CDATA[{toUser}]]>
    </FromUserName>
    <CreateTime>{createTime}</CreateTime>
    <MsgType>
        <![CDATA[text]]>
    </MsgType>
    <Content><![CDATA[{content}]]></Content>
</xml>
"""
from debuglogger import logfile

class WXChat(OutputAdapter):
    """
    A simple adapter that allows ChatterBot to
    communicate through the terminal.
    """

    def process_response(self, statement):
        """
        Print the response to the user's input.
        """
        statement.add_extra_data("content", statement.text)
        print >> logfile, statement.extra_data
        return resp_templ.format(**statement.extra_data)
