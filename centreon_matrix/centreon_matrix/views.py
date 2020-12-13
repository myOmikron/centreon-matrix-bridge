import json

from django.http import JsonResponse
from django.views import View


class SendMessage(View):
    def post(self, request, *args, **kwargs):
        message = json.loads(request.POST)
        msg = {}
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
            msg["content_formatted"] = f"<strong><font color=\"{color}\">Service {message['level']}</font>" \
                                       f"</strong> ALERT<br /><pre><code>Host: {message['host']}<br />Service: " \
                                       f"{message['description']}<br />Output: {message['output']}</code></pre>"
        with open("../../handler.fifo") as fh:
            fh.write(json.dumps(msg))
        return JsonResponse({"result": True})
