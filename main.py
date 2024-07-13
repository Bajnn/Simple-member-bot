import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os

# This role will be able to use these commands
MEDLEM_ANSVARIG = 1261599527568412713

# Role that you want to give your members
MEDLEMS_ROLL = 1261590321351888946

# Accepted members
MEDLEMS_CHANNEL = 1261589082182516748
# Members that got their membership revoked
INDRAGEN_CHANNEL = 1261589162478276659


# Name of the server
server_name = "bajn roleplay"

load_dotenv()

intents = disnake.Intents.all()
activity = disnake.Activity(
    name="Simple medlem bot",
    type=disnake.ActivityType.playing,
)
bot = commands.Bot(intents=intents, command_prefix="!", activity=activity)
def has_medlem_ansvarig_role():
    async def predicate(interaction: disnake.ApplicationCommandInteraction):
        ansvarig_role_id = MEDLEM_ANSVARIG
        user_roles = [role.id for role in interaction.user.roles]
        return ansvarig_role_id in user_roles
    return commands.check(predicate)
@bot.slash_command(name="gemedlem")
@has_medlem_ansvarig_role()
async def medlem(interaction, user: disnake.Member):
    
    # gets the role
    role = disnake.utils.get(interaction.guild.roles, id=MEDLEMS_ROLL)
    
    # member embed
    medlems_svar = disnake.utils.get(interaction.guild.text_channels, id=MEDLEMS_CHANNEL)
    medlem_embed = disnake.Embed(title="Medlemskaps ansökan", description=f"{user.mention} din medlems ansökan har blivit godkänd, välkommen till `{server_name}`", color=0x00ff00)
    medlem_embed.set_footer(text=f"Hanterat av: {interaction.user.name}")
     
    if role not in user.roles:
        await user.add_roles(role)
        await interaction.send(f"Du gav {user.mention} medlem", ephemeral=True)
        await medlems_svar.send(embed=medlem_embed)    
        
    else:
        await interaction.send(f"{user.mention} har redan rollen", ephemeral=True)
        
@bot.slash_command(name="nekad")
@has_medlem_ansvarig_role()
async def denied(interaction, user: disnake.Member, anledning: str):
    
    # gets the role
    role = disnake.utils.get(interaction.guild.roles, id=MEDLEMS_ROLL)
    
    # member embed
    medlems_svar = disnake.utils.get(interaction.guild.text_channels, id=MEDLEMS_CHANNEL)
    medlems_embed = disnake.Embed(title="Nekad Medlemskaps ansökan", description=f"{user.mention} har blivit nekad\n**Anledning:** {anledning}", color=0x00ff00)
    medlems_embed.set_footer(text=f"Hanterat av: {interaction.user.name}")
    await interaction.send(f"Du nekade {user.mention}", ephemeral=True)
    await medlems_svar.send(embed=medlems_embed)    
        


@bot.slash_command(name="indragenmedlem")
@has_medlem_ansvarig_role()
async def revoked(interaction, user: disnake.Member, anledning: str, bevis: disnake.Attachment = None):
    
    # gets the role
    role = disnake.utils.get(interaction.guild.roles, id=MEDLEMS_ROLL)
    
    # member embed
    indragen_svar = disnake.utils.get(interaction.guild.text_channels, id=INDRAGEN_CHANNEL)
    indragen_embed = disnake.Embed(title="Indragen Medlem", description=f"{user.mention} har fått sin medlem indragen\n**Anledning:** {anledning}\n**Bevis:** {bevis}", color=0x00ff00)
    indragen_embed.set_footer(text=f"Hanterat av: {interaction.user.name}")
     
    if role in user.roles:
        await user.remove_roles(role)
        await interaction.send(f"Du drog {user.mention} medlem", ephemeral=True)
        await indragen_svar.send(embed=indragen_embed)    
        
    else:
        await interaction.send(f"{user.mention} har inte rollen", ephemeral=True)        
        
@bot.event
async def on_slash_command_error(interaction: disnake.ApplicationCommandInteraction, error):
    if isinstance(error, commands.CheckFailure):
        await interaction.send("Du har inte behörighet att använda detta kommando.", ephemeral=True)
    else:
        await interaction.send(f"Ett fel inträffade: {str(error)}", ephemeral=True)
bot.run(os.getenv("TOKEN"))

