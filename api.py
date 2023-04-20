import threading
from flask import Flask, request
import discord


app = Flask(__name__)
client = discord.Client(intents=discord.Intents.all())

@app.route('/api', methods=['POST'])
def handle_request():
    data = request.get_json()
    # Send embed to discord channel
    async def send_embed():
        vouchbtn_instance = vouchbtn(data)  # Pass data to the vouchbtn constructor
        channel = client.get_channel(1086651597708333117)
        embed = discord.Embed(title="New Vouch Form Submission!", color=0x00ffff)
        embed.add_field(name="User who is giving vouch:-", value=f"Username:- {data['discord_username']}#{data['discord_discriminator']}",inline=False)
        embed.add_field(name="",value=f"Discord ID:- {data['discord_id']}",inline=True)
        embed.add_field(name="" , value=f"Vouches Left:- {data['vouches_left']}",inline=False)
        embed.add_field(name="User who is being vouch:-", value=f"Discord ID:- {data['vouch_user_id']}",inline=False)
        embed.add_field(name="", value=f"Discord Username:- {data['vouch_username']}#{data['vouch_discriminator']}",inline=False)
        await channel.send(embed=embed , view=vouchbtn_instance)
    client.loop.create_task(send_embed())
    return data

# make button for embed approved and denied add role to user if approved
class vouchbtn(discord.ui.View):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.value = None

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green)
    async def approve(self,interaction: discord.Interaction , button: discord.ui.Button):
        self.value = "Approved"
        await interaction.response.send_message("Vouch has been approved", ephemeral=False)


        guild = client.get_guild(1074296554149654580)
        role = guild.get_role(1098306389237055579)
        member = guild.get_member(int(self.data['vouch_user_id']))
        await member.add_roles(role)
        user = client.get_user(int(self.data['vouch_user_id']))
        await user.send(f"Your vouch from {self.data['discord_username']}#{self.data['discord_discriminator']} has been approved and Mystic role has been added to you")


    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red)
    async def deny(self,interaction: discord.Interaction , button: discord.ui.Button):
        self.value = "Denied"
        await interaction.response.send_message("Vouch has been denied", ephemeral=False)
        user = client.get_user(int(self.data['vouch_user_id']))
        await user.send(f"Your vouch from {self.data['discord_username']}#{self.data['discord_discriminator']} has been denied")
        
































def run_flask():
    app.run()

def run_discord():
    client.run('MTA4NzM5NjQwOTU5MjAwMDYxMg.GqwHMC.IOPKuPRYwzMp2W3tVRb1PYbiz-nczBCwxgACHA')

# run flask in a thread so it doesn't block the discord bot
threading.Thread(target=run_flask).start()
# run discord bot
run_discord()
