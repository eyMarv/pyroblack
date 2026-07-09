<p align="center">
    <a href="https://github.com/eyMarv/pyroblack">
        <img src="https://eyMarv.github.io/pyroblack-docs/main/_static/pyroblack.png" alt="pyroblack" width="128">
    </a>
    <br>
    <b>Telegram MTProto API Framework for Python</b>
    <br>
    <a href="https://eyMarv.github.io/pyroblack-docs">
        Documentation
    </a>
    •
    <a href="https://github.com/eyMarv/pyroblack/issues">
        Issues
    </a>
    •
    <a href="https://t.me/OpenFileZ">
        Support
    </a>
</p>

## pyroblack

> Elegant, modern and asynchronous Telegram MTProto API framework in Python for users and bots

``` python
from pyrogram import Client, filters

app = Client("my_account")


@app.on_message(filters.private)
async def hello(client, message):
    await message.reply("Hello from pyroblack!")


app.run()
```

**pyroblack** is a modern, elegant and
asynchronous [MTProto API](https://eyMarv.github.io/pyroblack-docs/topics/mtproto-vs-botapi)
framework. It enables you to easily interact with the main Telegram API through a user account (custom client) or a bot
identity (bot API alternative) using Python.

> **v2.8.0+**: Rebuilt on latest PyroTGFork base (Layer 227) for massive speed improvements — 3x faster than previous versions.

### Key Features

- **Ready**: Install pyroblack with pip and start building your applications right away.
- **Easy**: Makes the Telegram API simple and intuitive, while still allowing advanced usages.
- **Elegant**: Low-level details are abstracted and re-presented in a more convenient way.
- **Fast**: Boosted by PyroTGFork's optimized core and [TgCrypto](https://github.com/pyrogram/tgcrypto), a high-performance C cryptography library.
- **Type-hinted**: Types and methods are all type-hinted, enabling excellent editor support.
- **Async**: Fully asynchronous (also usable synchronously if wanted, for convenience).
- **Powerful**: Full access to Telegram's API to execute any official client action and more.
- **Conversations**: Built-in pyromod support — listen, ask, and wait for messages/callbacks.
- **Telethon compat**: Supports loading Telethon session strings via `is_telethon_string=True`.

### Installing

``` bash
pip3 install -U pyroblack
```

### Resources

- Check out the docs at https://eyMarv.github.io/pyroblack-docs to learn more about pyroblack, get started right
  away and discover more in-depth material for building your client applications.
- Join the official group at https://t.me/OpenFileZ and stay tuned for news, updates and announcements.
