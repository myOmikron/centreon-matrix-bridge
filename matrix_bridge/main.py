import asyncio
import logging

import zmq
from hopfenmatrix.config import Namespace, Config
from hopfenmatrix.matrix import MatrixBot
from zmq.backend.cython.constants import PAIR

logger = logging.getLogger(__name__)


async def listener(bot):
    while True:
        try:
            context = zmq.Context.instance()
            socket = context.socket(PAIR)
            socket.bind("tcp://127.0.0.1:55555")
            while True:
                msg = socket.recv_json()
                logger.info(f"Received {msg}")
                if msg["shared_secret"] != bot.config.centreon.shared_secret:
                    logger.warning(f"The shared_secret is not the one I know!")
                    continue
                await bot.send_message(
                    message=msg["content"],
                    room_id=msg["target"],
                    formatted_message=msg["content_formatted"]
                )
        except Exception as err:
            logger.error(err)
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
