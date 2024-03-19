import discord

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True

client = discord.Client(intents=intents)

role_id = 123123123123123 # Айди роли, которую нужно выдавать
channel_id = 123123123123123 # Айди канала, куда нужно отправить сообщение

@client.event
async def on_ready():
    print(f'Вошел как {client.user.name}')
    await check_reaction_role_setup()

async def check_reaction_role_setup() -> None:
    channel = client.get_channel(channel_id)
    try:
        if channel:
            async for message in channel.history(limit=200):
                if message.author == client.user and message.content.startswith('Для получения роли подписчика'):
                    return
            await setup_reactions()
    except Exception as e:
        print(f'Ошибка проверки настройки роли по реакции: {e}')

async def setup_reactions() -> None:
    try:
        channel = client.get_channel(channel_id)
        if channel:
            message = await channel.send('Для получения роли подписчика, нажмите на эмодзи глаз под этим сообщением.')
            await message.add_reaction('👀')
    except Exception as e:
        print(f'Ошибка при установке реакций: {e}')

@client.event
async def on_raw_reaction_add(payload):
    if payload.member.id != client.user.id and payload.channel_id == channel_id and str(payload.emoji) == '👀':
        try:
            guild = client.get_guild(payload.guild_id)
            role = guild.get_role(role_id)
            if role:
                await payload.member.add_roles(role)
        except Exception as e:
            print(f'Ошибка добавления роли: {e}')

@client.event
async def on_raw_reaction_remove(payload):
    if payload.channel_id == channel_id and str(payload.emoji) == '👀':
        try:
            guild = client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if member:
                role = guild.get_role(role_id)
                if role:
                    await member.remove_roles(role)
        except Exception as e:
            print(f'Ошибка удаление роли: {e}')

client.run('TOKEN')
