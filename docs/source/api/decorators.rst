Decorators
==========

Decorators are able to register callback functions for handling updates in a much easier and cleaner way compared to
:doc:`Handlers <handlers>`; they do so by instantiating the correct handler and calling
:meth:`~pyrogram.Client.add_handler` automatically. All you need to do is adding the decorators on top of your
functions.

.. code-block:: python

    from pyrogram import Client

    app = Client("my_account")


    @app.on_message()
    def log(client, message):
        print(message)


    app.run()

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

.. currentmodule:: pyrogram

Index
-----

.. hlist::
    :columns: 3

    - :meth:`~Client.on_bot_business_connect`
    - :meth:`~Client.on_message`
    - :meth:`~Client.on_bot_business_message`
    - :meth:`~Client.on_edited_message`
    - :meth:`~Client.on_edited_bot_business_message`
    - :meth:`~Client.on_callback_query`
    - :meth:`~Client.on_message_reaction_updated`
    - :meth:`~Client.on_message_reaction_count_updated`
    - :meth:`~Client.on_inline_query`
    - :meth:`~Client.on_chosen_inline_result`
    - :meth:`~Client.on_chat_member_updated`
    - :meth:`~Client.on_chat_join_request`
    - :meth:`~Client.on_deleted_messages`
    - :meth:`~Client.on_deleted_bot_business_message`
    - :meth:`~Client.on_user_status`
    - :meth:`~Client.on_story`
    - :meth:`~Client.on_poll`
    - :meth:`~Client.on_disconnect`
    - :meth:`~Client.on_invoke_err`
    - :meth:`~Client.on_raw_update`

-----

Details
-------

.. Decorators
.. autodecorator:: pyrogram.Client.on_bot_business_connect()
.. autodecorator:: pyrogram.Client.on_message()
.. autodecorator:: pyrogram.Client.on_bot_business_message()
.. autodecorator:: pyrogram.Client.on_edited_message()
.. autodecorator:: pyrogram.Client.on_edited_bot_business_message()
.. autodecorator:: pyrogram.Client.on_callback_query()
.. autodecorator:: pyrogram.Client.on_message_reaction_updated()
.. autodecorator:: pyrogram.Client.on_message_reaction_count_updated()
.. autodecorator:: pyrogram.Client.on_inline_query()
.. autodecorator:: pyrogram.Client.on_chosen_inline_result()
.. autodecorator:: pyrogram.Client.on_chat_member_updated()
.. autodecorator:: pyrogram.Client.on_chat_join_request()
.. autodecorator:: pyrogram.Client.on_deleted_messages()
.. autodecorator:: pyrogram.Client.on_edited_bot_business_message()
.. autodecorator:: pyrogram.Client.on_user_status()
.. autodecorator:: pyrogram.Client.on_story()
.. autodecorator:: pyrogram.Client.on_poll()
.. autodecorator:: pyrogram.Client.on_disconnect()
.. autodecorator:: pyrogram.Client.on_invoke_err()
.. autodecorator:: pyrogram.Client.on_raw_update()

-----

Alternative spellings
---------------------

The other Pyrogram forks (kurigram, wzgram, DzGram) name several of these
decorators without the ``bot_`` infix, and use ``on_message_reaction`` where
pyroblack uses ``on_message_reaction_updated``. Those spellings are bound as
aliases of the same decorator, so a bot written against another fork registers
its handlers unchanged:

=================================  ================================================
Alias                              pyroblack decorator
=================================  ================================================
``on_business_connect``            :meth:`~Client.on_bot_business_connect`
``on_business_connection``         :meth:`~Client.on_bot_business_connection`
``on_business_message``            :meth:`~Client.on_bot_business_message`
``on_deleted_business_messages``   :meth:`~Client.on_deleted_bot_business_messages`
``on_edited_business_message``     :meth:`~Client.on_edited_bot_business_message`
``on_message_reaction``            :meth:`~Client.on_message_reaction_updated`
``on_message_reaction_count``      :meth:`~Client.on_message_reaction_count_updated`
``on_purchased_paid_media``        :meth:`~Client.on_bot_purchased_paid_media`
=================================  ================================================
