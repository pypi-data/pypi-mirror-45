.. image:: https://img.shields.io/pypi/v/snails.svg?style=flat-square
    :target: https://pypi.python.org/pypi/snails

Sometimes you want to write a dumb email handler.

Good for: low volume, minimal parsing, interacting with legacy email-based systems
Bad for: high volume, production use, 100% RFC compliance


Requires Python 3.7+

::

    pip install snails

=======
 Usage
=======

.. code-block:: python

    import snails


    def handle(msg: snails.Message) -> None:
        print(f"To: {msg['to']}")
        print(f"From: {msg['from']}")
        print("Subject: {msg['subject']}")
        for p in msg.get_payload():
            print(p.get_payload(decode=True))


    # manage your own mailbox start/stop
    mailbox = snails.Mailbox(handle, "127.0.0.1", 10025)
    mailbox.start()

    # drop this in __main__, runs and blocks until Ctrl+C
    snails.serve(handle, "127.0.0.1", 10025)

==========
 Advanced
==========

Not much else to do here.  You can return an SMTP status string, but by default if you don't raise an exception it'll
return "250 OK" and raising an exception returns "500 ..."

.. code-block:: python

    # calls Mailbox.stop when the python interpreter cleans up
    snails.serve(h, "localhost", 25, cleanup_at_exit=True)

    # blocks until KeyboardInterrupt
    snails.serve(h, "localhost", 25, block=True)

    # create a mailbox and start it, and return the object for use
    mailbox = snails.serve(h, "localhost", 25, block=False, cleanup_at_exit=True)
    ...  # your code here
    mailbox.stop()

    # create a mailbox without starting it
    mailbox = snails.Mailbox(h, "localhost", 25)
    ...  # your code here
    mailbox.start()
    ... # other code
    mailbox.stop()