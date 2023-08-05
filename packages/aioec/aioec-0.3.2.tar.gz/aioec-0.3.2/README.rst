aioec
=====

An aiohttp-based client for the `Emote Collector API <https://emote-collector.python-for.life/api/v0/docs>`_.


Usage
-----

.. code-block:: python3

	import aioec

	client = aioec.Client(token='your token here')
	# if no token is provided, only anonymous endpoints will be available

	# this step isn't necessary but makes sure that your token is correct
	my_user_id = await client.login()
	# it returns the user ID associated with your token

	# in a coroutine...
	emote = await client.emote('Think')
	emote.name  # Think

	await emote.edit(name='Think_', description='a real happy thinker')
	# remove the description:
	await emote.edit(description=None)

	for gamewisp_emote in await client.search('GW'):
		await gamewisp_emote.delete()

	all_emotes = await client.emotes()
	popular_emotes = await client.popular()

	await client.close()

	# it's also a context manager:
	async with aioec.Client(token=my_token) as client:
		await client.delete('Think_')
	# this will automatically close the client

License
-------

MIT/X11

Copyright © 2018 Benjamin Mintz <bmintz@protonmail.com>
