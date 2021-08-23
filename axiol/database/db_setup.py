from core.bot import Bot
from utils.logger import log
from database.db_wrapper import collections, database


class Updater(Bot):

    def __init__(self):
        super(Updater, self).__init__(prefix=' ')
        self.remove_command('help')

    async def on_ready(self):
        log.inform("Starting DB Update...")
        await update_db([guild.id for guild in self.guilds])
        await self.close()
        quit()


async def update_db(guild_ids):
    """Updating leveling, plugin, prefix and permission data."""
    plugins_update = []
    permissions_update = []
    leveling_update = []

    for guild_id in guild_ids:
        plugin_count = (
            await collections.plugins
            .count_documents({"_id": guild_id}, limit=1)
        )

        if not plugin_count:
            collections.plugins.insert_one(
                {
                    "_id": guild_id,
                    "Leveling": False,
                    "Moderation": True,
                    "ReactionRoles": True,
                    "Welcome": False,
                    "Verification": False,
                    "Chatbot": True,
                    "AutoMod": False,
                    "Karma": False,
                    "Fun": True,
                    "Giveaway": True
                }
            )

            plugins_update.append(guild_id)
            log.success(f"{guild_id} - Plugins 🔧")

        permission_count = (
            await collections.permissions
            .count_documents({"_id": guild_id}, limit=1)
        )

        if not permission_count:
            collections.permissions.insert_one(
                {
                    "_id": guild_id,
                    "Leveling": {},
                    "Moderation": {},
                    "ReactionRoles": {},
                    "Welcome": {},
                    "Verification": {},
                    "Chatbot": {},
                    "Commands": {},
                    "AutoMod": {},
                    "Karma": {},
                    "Fun": {},
                    "Giveaway": {}
                }
            )

            permissions_update.append(guild_id)
            log.success(f"{guild_id} - Permissions 🔨")

        guild_plugins = (
            await collections.plugins
            .find_one({"_id": guild_id})
        )

        if (
            guild_plugins.get("Leveling")
            and str(guild_id) not in (
                await database.leveling.list_collection_names()
            )
        ):
            guild_level_db = (
                await database.leveling
                .create_collection(str(guild_id))
            )

            await guild_level_db.insert_one(
                {
                    "_id": 0,
                    "xprange": [15, 25],
                    "alertchannel": None,
                    "blacklistedchannels": [],
                    "alerts": True
                }
            )

            leveling_update.append(guild_id)
            log.success(f"{guild_id} - Leveling 📊")

        # Only use this when working locally
        try:
            await collections.prefixes.insert_one(
                {
                    "_id": guild_id,
                    "prefix": "ax"
                }
            )

            log.success(f"{guild_id} - Prefix ⚪")

        except Exception as e:
            log.warn(f"{guild_id} - Prefix ⚪ ({e.__cause__})")

    log.inform(
        "Update results\n"
        f"{len(plugins_update)} plugins\n"
        f"{len(permissions_update)} permissions\n"
        f"{len(leveling_update)} leveling"
    )


def main():
    client = Updater()  # Setting up a impossible prefix to avoid problems
    client.run()


if __name__ == '__main__':
    main()
