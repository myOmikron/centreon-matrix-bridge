import json

from django.http import JsonResponse
from django.views import View
from zmq import Context
from zmq.backend.cython.constants import PAIR


class SendMessage(View):
    def post(self, request, *args, **kwargs):
        message = request.POST
        msg = {
            "shared_secret": message["shared_secret"],
            "target": message["target"],
        }
        color = "#00ff00" if message["level"] == "OK" or message["level"] == "UP" else "#ffff00" if \
            message["level"] == "WARNING" else "#ff0000" if message["level"] == "DOWN" or message["level"] \
                                == "CRITICAL" else "#a0a0a0" if message["level"] == "UNKNOWN" else "#000000"
        if message["type"] == "host":
            msg["content"] = f"Host {message['level']} ALERT\n" \
                      f"\n" \
                      f"Host: {message['host']}\n" \
                      f"Alias: {message['alias']}\n" \
                      f"Output: {message['output']}\n"
            msg["content_formatted"] = f"<strong><font color=\"{color}\">Host {message['level']} ALERT</font>" \
                                       f"</strong><br /><pre><code>Host: {message['host']}<br />Alias: " \
                                       f"{message['alias']}<br />Output: {message['output']}</code></pre>"
        else:
            msg["content"] = f"Service {message['level']} ALERT\n" \
                      f"\n" \
                      f"Host: {message['host']}\n" \
                      f"Service: {message['description']}\n" \
                      f"Output: {message['output']}\n"
            msg["content_formatted"] = f"<strong><font color=\"{color}\">Service {message['level']} ALERT</font>" \
                                       f"</strong><br /><pre><code>Host: {message['host']}<br />Service: " \
                                       f"{message['description']}<br />Output: {message['output']}</code></pre>"
        ctx = Context.instance()
        socket = ctx.socket(PAIR)
        socket.connect("tcp://127.0.0.1:55555")
        socket.send_string(json.dumps(msg))
        socket.close()
        return JsonResponse({"result": True})
