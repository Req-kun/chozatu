import discord
from discord.ext import commands
import datetime
from discord_slash import SlashCommand
from discord_slash import SlashContext
from discord_slash import utils
import bottle
import os
bottle.BaseRequest.MEMFILE_MAX = 9999999999999999999999999999999999999999999999999999999999999999999999999999 # (or whatever you want)

TOKEN = os.environ.get("TOKEN")
bot = commands.Bot(command_prefix='c/', intents=discord.Intents.all())

from glob import glob
files = glob('./cogs/*')

count = 0
for f in files:
    if f.endswith('.py'):
        f = f[len('./cogs/'):-(len('.py'))]
        if f == 'template':
            continue
        bot.load_extension(f'cogs.{f}')
        print(f'cogs.{f} was loaded!')
        count += 1



print('#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#')
print(f'\n    ALL COG WAS LOADED\n    COG COUNT : {count}\n    {datetime.datetime.now().strftime("%H : %M : %S")}\n')
print('#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#')

@bot.event
async def on_ready():
    #bot_id, token, guild_id
    #await utils.manage_commands.remove_all_commands_in(804649928638595093, TOKEN, 733707710784340100)

    bot.guild = bot.get_guild(733707710784340100)

    # 運営ロールオブジェクトの取得
    bot.unei_role = bot.guild.get_role(738956776258535575)

    # slashコマンド実行履歴を送信するチャンネル関連
    ch = await bot.fetch_channel(805254420169752596)
    bot.history_channel = ch

    # yutronコマンド関連
    bot.yutron_backup = bot.get_channel(805397016578097222)
    bot.yutron_images = []
    async for msg in bot.yutron_backup.history(limit=None):
        if msg.content.startswith('https://'):
            bot.yutron_images.append(msg.content)

    # scsコマンド関連
    bot.scs_backup = bot.get_channel(809788276801667083)
    bot.scs_images = []
    async for msg in bot.scs_backup.history(limit=None):
            if msg.content.startswith('https://'):
                bot.scs_images.append(msg.content)

    # rule コマンド関連
    rule_basic_ch = bot.get_channel(734062426873397248)
    rule_basic_msg = await rule_basic_ch.fetch_message(741993354795024394)

    rule_mcserver_ch = bot.get_channel(792674991426502656)
    rule_mcserver_msg = await rule_mcserver_ch.fetch_message(792675496071921676)

    rule_siritori_ch = bot.get_channel(745645296968794233)
    rule_siritori_msg = await rule_siritori_ch.fetch_message(745645905192943721)

    bot.rules = {
        "basic": rule_basic_msg.content,
        "mcserver": rule_mcserver_msg.content,
        "siritori": rule_siritori_msg.content
    }

    # pin機能関連
    bot.pin_ch = bot.get_channel(805787370150559784)
    webhooks = await bot.pin_ch.webhooks()
    bot.pin_webhook = discord.utils.get(webhooks, name='超雑談鯖_pin_wh')

    # 起動情報関連
    ready_ch = bot.get_channel(807444910621720606)
    await ready_ch.send('<a:server_rotation:774429204673724416>起動')

    #運営部屋取得
    bot.unei_ch = bot.get_channel(738397603439444028)

    # その他
    print("ready")
    return

@bot.event
async def on_slash_command(ctx):
    used_command = ctx.name
    used_channel = ctx.channel.mention
    used_author = ctx.author.mention
    embed = discord.Embed(title='コマンドが実行されました')
    embed.add_field(name='コマンド名', value=used_command)
    embed.add_field(name='使用されたチャンネル', value=used_channel)
    embed.add_field(name='使用者', value=used_author)
    await bot.history_channel.send(embed=embed, allowed_mentions=discord.AllowedMentions.none())


bot.run(TOKEN)
