import asyncio
import json

from hopfenmatrix.config import Namespace, Config
from hopfenmatrix.matrix import MatrixBot


async def listener(bot):
    while True:
        with open("../handler.fifo") as fh:
            lines = fh.readlines()
            for line in lines:
                res = json.loads(line)
                await bot.send_message(
                    message=res["content"],
                    room_id=res["target"],
                    formatted_message=res["content_formatted"]
                )


class MyConfig(Config):
    def __init__(self):
        super(MyConfig, self).__init__()
        centreon = Namespace()
        centreon.shared_secret = ""


async def main():
    bot = MatrixBot(display_name="Centreon Notification", config_class=MyConfig)
    bot.set_auto_join()
    bot.add_coroutine_callback(listener(bot))
    await bot.start_bot()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
