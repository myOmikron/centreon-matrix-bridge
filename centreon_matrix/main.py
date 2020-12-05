import asyncio
import json
import os

import aiofiles
from hopfenmatrix.api_wrapper import ApiWrapper


async def socket_listener(api: ApiWrapper):
    while True:
        path = "/tmp/centreon_matrix_bridge.fifo"
        if os.path.exists(path):
            os.remove(path)
        try:
            os.mkfifo(path)

            async with aiofiles.open(path, "r") as fifo:
                async for line in fifo:
                    message = json.loads(line)
                    color = "#00ff00" if message["level"] == "OK" or message["level"] == "UP" else "#ffff00" if \
                        message["level"] == "WARNING" else "#ff0000" if message["level"] == "DOWN" or \
                        message["level"] == "CRITICAL" else "#a0a0a0" if message["level"] == "UNKNOWN" else "#000000"
                    if message["type"] == "host":
                        content = f"Host {message['level']} ALERT\n" \
                                  f"\n" \
                                  f"Host: {message['host']}\n" \
                                  f"Alias: {message['alias']}\n" \
                                  f"Output: {message['output']}\n"
                        content_formatted = f"<strong><font color=\"{color}\">Host {message['level']} ALERT</font>" \
                                            f"</strong><br /><pre><code>Host: {message['host']}<br />Alias: " \
                                            f"{message['alias']}<br />Output: {message['output']}</code></pre>"
                    else:
                        content = f"Service {message['level']} ALERT\n" \
                                  f"\n" \
                                  f"Host: {message['host']}\n" \
                                  f"Service: {message['description']}\n" \
                                  f"Output: {message['output']}\n"
                        content_formatted = f"<strong><font color=\"{color}\">Service {message['level']}</font>" \
                                            f"</strong> ALERT<br /><pre><code>Host: {message['host']}<br />Service: "\
                                            f"{message['description']}<br />Output: {message['output']}</code></pre>"
                    await api.send_message(
                        message=content,
                        room_id=message["target"],
                        formatted_message=content_formatted
                    )
        except FileExistsError or Exception:
            pass


async def main():
    bot = ApiWrapper(display_name="Centreon Notification")
    bot.set_auto_join()
    bot.add_coroutine_callback(socket_listener(bot))
    await bot.start_bot()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
