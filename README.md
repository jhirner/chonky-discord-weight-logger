# Chonky Weight Logger

## What is Chonky?
Chonky is a simple weight-logging app powered by Discord. It consists of two portions:
* *A bot* that monitors your private Discord server for weight information. When new weight information is received, it is saved to a SQLite database.
* *A dashboard* to retrieve the data and display it in a web interface.

## A note on security.
Chonky's dashboard is currently built using the stock implementation of the Python Dash library, which is powered by a development Flask server. It is not adequately secured for production, public-facing use. As a result, **Chonky should not be deployed to the public-facing internet** without modification.

Chonky is intended for private deployment behind a firewall with local-only access.

## Installation
Chonky is available as a Python script or with a Dockerfile for containerized implementation. To install it:
1. Clone this repository to a directory of your choice.
2. In the `source` folder, copy `env.example` to a new file named `.env`. In the next step, we'll use this file will store the credentials for your private Discord server.
2. Set up your Discord developer credentials & private server.
	* Create a new bot application in the [Discord Developer Portal](https://discord.com/developers/applications/).
	* Having done that, visit the *bot* tab in the Discord Developer portal. Copy the bot's Token and paste it into `.env` as the DISCORD_TOKEN variable.
	* Create a new Discord server that you will use for logging weights. In the `.env` file, paste in the exact name of the server.
	* Add your new Discord bot to your private Discord server. [Here](https://realpython.com/how-to-make-a-discord-bot-python/#adding-a-bot-to-a-guild) is a nice overview of how to do this.
	* Create as many different channels as you have users to track. For example, your channels might be "#me" and "#the-dog" to track weights for you and your dog.
3. Decide if you want a pure Python or a containerized implementation:
	* *For Python installation*: Navigate to the saved folder and install the requirements with `pip install -r requirements.txt`.
	* *For containerized installation*: Make the Docker container with `docker build --tag chonky-bot .`
		* *Note*: The example Dockerfile is intended for use with amd64 system architecture. For deployment on alternative hardware (e.g.: a Raspberry Pi), you'll need to change the first line of the Dockerfile. One that works well in testing is `FROM leberkaas/python-armed`.
4. Run Chonky!
	* *For Python installation*, execute `python3 chonky-dash.py` and `python3 chonky-discord.py`.
	* *For containerized installation*, execute `docker run --network host --volume ~/GitHub/discord-weight-logger/docker-data/:/data chonky-bot`.
		* The `--network host` flag enables ready access to the dashboard through the host computer's IP address.
		* the `--volume` flag ensures persistant storage of the database outside of the container. The format is `--volume host-path:container-path`, and may be edited to your needs.
5. Log your weight in your private Discord server. Chonky will respond with confirmation or an error message.
6. Check the dashboard to monitor your weight over time. By default, the dashboard will be served to localhost:8050. You may configure your local network to enable access from other devices on your home network, but public-facing access is not recommended. (Please see the Note on Security, above)

## License
Chonky is licensed under MIT license, copyright 2021 Joshua Hirner.
	
