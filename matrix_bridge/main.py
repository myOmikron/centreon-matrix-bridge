import asyncio

import zmq
from hopfenmatrix.config import Namespace, Config
from hopfenmatrix.matrix import MatrixBot


async def listener(bot):
    while True:
        try:
            context = zmq.Socket()
            context.bind("tcp://127.0.0.1:55555")
            while True:
                msg = context.recv_json()
                print(msg)
                if msg["shared_secret"] != bot.config.centreon.shared_secret:
                    continue
                await bot.send_message(
                    message=msg["content"],
                    room_id=msg["target"],
                    formatted_message=msg["content_formatted"]
                )
        except Exception:
            continue


class MyConfig(Config):
    def __init__(self):
        super(MyConfig, self).__init__()
        self.centreon = Namespace()
        self.centreon.shared_secret = ""


async def main():
    bot = MatrixBot(display_name="Centreon Notification", config_class=MyConfig)
    bot.set_auto_join()
    bot.add_coroutine_callback(listener(bot))
    await bot.start_bot()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
