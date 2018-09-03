import discord, asyncio, os, sys
from discord.ext import commands
from discord.ext.commands import Bot

scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
bot = commands.Bot(command_prefix='Z!')

@bot.event
async def on_ready():
	print (bot.user.name, "právě vstal z hrobu")

@bot.command(pass_context=True, brief='I\'l tell you your user id')
async def id(ctx):
	await bot.say("Tvoje ID je {}".format(ctx.message.author.id))

@bot.command(pass_context=True, brief='Might add some role')
async def addrole(ctx, user: discord.User):
	if ("Bot testing squad" in [role.name for role in user.roles]):
		await bot.say(user.name + ' už tuto roli má')

	elif ("Bot testing squad" in [role.name for role in ctx.message.author.roles]):
		role = discord.utils.get(user.server.roles, name="Bot testing squad")
		await bot.add_roles(user, role)
		await bot.say('Uživateli {} byla přidána role {}'.format(user.name, role.name))

	else:
		await bot.say('Na to nemáš právo')
@addrole.error
async def addrole_error(error, ctx):
	await bot.delete_message(ctx.message)
	await bot.say('Tato funkce má jako povinný parametr mention uživatele!')

@bot.command(pass_context=True, brief='Might get some roles of user')
async def removerole(ctx):
	if(ctx.message.author.id in ['221553148102180864']):
		role = discord.utils.get(user.server.roles, name="Bot testing squad")
		await bot.remove_roles(user, role)
		await bot.say('Uživateli {} byla odebrána role {}'.format(user.name, role.name))
	else:
		await bot.say('Na to nemáš právo.')

@removerole.error
async def removerole_error(error, ctx):	
	role = discord.utils.get(ctx.message.server.roles, name="Bot testing squad")
	await bot.remove_roles(ctx.message.author, role)
	await bot.say('Uživateli {} byla odebrána role {}'.format(ctx.message.author.name, role.name))

@bot.command(pass_context=True, brief='Might get some roles of user')
async def getroles(ctx, user: discord.User):
	text = ""
	for role in user.roles:
		if user.roles.index(role) + 1 < len(user.roles):
			text += role.name + ", "
		else:
			text += role.name
	await bot.say(text)

@bot.command(pass_context=True, brief="Displays all roles on server")
async def serverroles(ctx):
	roles = dict()
	for member in ctx.message.server.members:
		for role in member.roles:
			if not role.name == '@everyone':
				if not role.name in list(roles.keys()):
					roles[role.name] = [member.name]
				else:
					roles[role.name].append(member.name)
	server_roles = discord.Embed(title='Role serveru', colour=0x0000FF)
	for role in list(roles.keys()):
		text = ''
		for member in roles[role]:
			if roles[role].index(member) + 1 < len(roles[role]):
				text += member + ', '
			else:
				text += member
		server_roles.add_field(name=role, value=text)
	await bot.send_message(ctx.message.channel, embed=server_roles)

@bot.command(pass_context=True, brief="Displays all roles on server")
async def hierarchy(ctx):
	server_hierarchy = discord.Embed(title='Hierarchie rolí serveru', colour=0xFFFFFF)
	for role in ctx.message.server.role_hierarchy:
		server_hierarchy.add_field(name=(ctx.message.server.role_hierarchy.index(role)+1), value=role.name)
	await bot.send_message(ctx.message.channel, embed=server_hierarchy)

@bot.command(pass_context=True)
async def shutdown(ctx):
	if (ctx.message.author.id == "221553148102180864"):
		await bot.say("Mizím :wave:")
		await bot.close()
		await bot.logout()
	else:
		await bot.say("Nejsi můj senpai :sob:")

@bot.command(pass_context=True)
async def game(ctx, *,game_name):
	if(ctx.message.author.id in ['221553148102180864', '360407653362565123']):
		await bot.change_presence(game=discord.Game(name=game_name), afk=True)

bot.run('')
#bot invite: https://discordapp.com/oauth2/authorize?client_id=484813265495523328&scope=bot&permissions=1342303232