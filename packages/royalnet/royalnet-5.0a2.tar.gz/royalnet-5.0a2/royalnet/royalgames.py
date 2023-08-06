import os
import asyncio
import logging
from royalnet.bots import DiscordBot, DiscordConfig, TelegramBot, TelegramConfig
from royalnet.commands import *
from royalnet.commands.debug_create import DebugCreateCommand
from royalnet.commands.error_handler import ErrorHandlerCommand
from royalnet.network import RoyalnetServer, RoyalnetConfig
from royalnet.database import DatabaseConfig
from royalnet.database.tables import Royal, Telegram, Discord

loop = asyncio.get_event_loop()

log = logging.root
stream_handler = logging.StreamHandler()
stream_handler.formatter = logging.Formatter("{asctime}\t{name}\t{levelname}\t{message}", style="{")
log.addHandler(stream_handler)
log.setLevel(logging.INFO)

commands = [PingCommand, ShipCommand, SmecdsCommand, ColorCommand, CiaoruoziCommand, DebugCreateCommand, SyncCommand,
            AuthorCommand, DiarioCommand, RageCommand, DateparserCommand, ReminderCommand, KvactiveCommand, KvCommand,
            KvrollCommand, VideoinfoCommand, SummonCommand, PlayCommand, SkipCommand, PlaymodeCommand,
            VideochannelCommand]

address, port = "localhost", 1234

master = RoyalnetServer(address, port, "sas")
ds_bot = DiscordBot(discord_config=DiscordConfig(os.environ["DS_AK"]),
                    royalnet_config=RoyalnetConfig(f"ws://{address}:{port}", "sas"),
                    database_config=DatabaseConfig(os.environ["DB_PATH"], Royal, Discord, "discord_id"),
                    commands=commands,
                    error_command=ErrorHandlerCommand,
                    missing_command=MissingCommand)
tg_bot = TelegramBot(telegram_config=TelegramConfig(os.environ["TG_AK"]),
                     royalnet_config=RoyalnetConfig(f"ws://{address}:{port}", "sas"),
                     database_config=DatabaseConfig(os.environ["DB_PATH"], Royal, Telegram, "tg_id"),
                     commands=commands,
                     error_command=ErrorHandlerCommand,
                     missing_command=MissingCommand)
print(tg_bot.botfather_command_string)
loop.run_until_complete(master.start())
loop.create_task(tg_bot.run())
loop.create_task(ds_bot.run())
print("Starting loop...")
loop.run_forever()
