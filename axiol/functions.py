from variables import DEFAULT_PREFIX
from database import PREFIXES, LEVELDATABASE, PLUGINS, PERMISSIONS

def getprefix(ctx):
    try:
        return PREFIXES.find_one({"_id": ctx.guild.id}).get("prefix")
    except AttributeError:
        return DEFAULT_PREFIX
    

def getxprange(message):
    col = LEVELDATABASE.get_collection(str(message.guild.id))
    settings = col.find_one({"_id": 0})
    xprange =settings.get("xprange")
    return xprange


#Some functions to counter errors and warning while working locally :p

#Adding new plugin
def updateplugins(plugin):
    PLUGINS.update_many(
        { plugin: { "$exists": False } },
            {
                "$set": { plugin : False }
            }
    )


#updating leveling, plugin and permission data
def updatedb(serverid):

    if not PLUGINS.count_documents({"_id": serverid}, limit=1):
        PLUGINS.insert_one({

                    "_id":serverid,
                    "Leveling":False,
                    "Moderation": False,
                    "Reaction Roles": False,
                    "Welcome": False,
                    "Verification": False,
                    "Chatbot": False,
                })
        print(f"✅{serverid} - Plugins 🔧")

    
    if not PERMISSIONS.count_documents({"_id": serverid}, limit=1):
        PERMISSIONS.insert_one({
            "_id": serverid,
            "Leveling": {},
            "Moderation": {},
            "Reaction Roles": {},
            "Welcome": {},
            "Verification": {},
            "Chatbot": {},
            "Commands": {},
        })
        print(f"✅{serverid} - Permissions 🔨")


    if PLUGINS.find_one({"_id": serverid}).get("Leveling"):
        try:
            GuildLevelDB = LEVELDATABASE.create_collection(str(serverid))
            GuildLevelDB.insert_one({

                "_id": 0,
                "xprange": [15, 25],
                "alertchannel": None,
                "blacklistedchannels": [],
                "alerts": True
                }) 
            print(f"✅{serverid} - Leveling 📊")
        except:
            print(f"❌{serverid} - Leveling 📊")
    
    try:
        PREFIXES.insert_one({
            "_id": serverid,
            "prefix": "ax"
        })
        print(f"✅{serverid} - Prefix ⚪")

    except:
        print(f"❌{serverid} - Prefix ⚪")


serveridlist = []
#for i in serveridlist:
   #updatedb(i)
#updateplugins("Karma")