import discord
from discord.ext import commands, tasks
import datetime
from discord_slash import SlashCommand
from discord_slash import SlashContext
from discord_slash import utils
import os
import re
import datetime
from pykakasi import kakasi

kakasi = kakasi()
kakasi.setMode('J', 'H') 
conv = kakasi.getConverter()

def to_h(self, text):
    return conv.do(text)

commands.Bot.to_h = to_h

async def fetch_message(self, url):
    id_regex = re.compile(r'(?:(?P<channel_id>[0-9]{15,21})-)?(?P<message_id>[0-9]{15,21})$')
    link_regex = re.compile(
        r'https?://(?:(ptb|canary|www)\.)?discord(?:app)?\.com/channels/'
        r'(?:[0-9]{15,21}|@me)'
        r'/(?P<channel_id>[0-9]{15,21})/(?P<message_id>[0-9]{15,21})/?$'
    )
    match = id_regex.match(url) or link_regex.match(url)
    channel_id = match.group("channel_id")
    message_id = int(match.group("message_id"))

    channel = await bot.fetch_channel(channel_id)
    message = await channel.fetch_message(message_id)
    return message

commands.Bot.fetch_message = fetch_message


TOKEN = os.environ.get("TOKEN")
bot = commands.Bot(command_prefix='c/', intents=discord.Intents.all())

slash = SlashCommand(bot, sync_commands=True)

bot.ready = False

time_remove_role_regix = re.compile(
    r'(?P<user_id>[0-9]{15,21})/'
    r'(?P<role_id>[0-9]{15,21})/'
    r'(?P<datetime>[0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}\:[0-9]{2}\:[0-9]{2}\.[0-9]{6})'
)

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


@bot.check
def check_commands(ctx):
    return ctx.guild.id == 733707710784340100


@bot.event
async def on_ready():
    if bot.ready:
        return
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

    # approve関連
    bot.approve_ch = bot.get_channel(815906779736178728)
    bot.wait_until_approve_role = bot.guild.get_role(830362058838245436)

    # ボイスチャット時間報酬関連
    bot.voice_time_ch = bot.get_channel(814705911032578118)
    bot.voice_money_min = 200
    bot.voice_money_max = 400
    bot.voice_give_per = 20

    # NG_WORD 関連
    bot.ng_word_ch = bot.get_channel(818012708167221248)
    bot.ng_words = []
    async for msg in bot.ng_word_ch.history(limit=None):
        bot.ng_words.append(msg.content)
    
    # ロール自動削除系
    bot.time_remove_role_ch = await bot.fetch_channel(827091732268974110)
    bot.time_remove_role = {}
    bot.time_remove_role_guild = await bot.fetch_guild(733707710784340100)
    
    async for msg in bot.time_remove_role_ch.history(limit=None):
        match = time_remove_role_regix.match(msg.content)
        bot.time_remove_role[datetime.datetime.strptime(match.group('datetime'), '%Y-%m-%d %H:%M:%S.%f')] = dict(
            user_id = int(match.group('user_id')),
            role_id = int(match.group('role_id')),
            message = msg
        )
    
    # しりとり関連
    bot.siritori_ch = bot.get_channel(827104884246708254)
    bot.siritori_list = []
    async for msg in bot.siritori_ch.history(limit=None):
        if msg.author.bot or msg.content.startswith(bot.command_prefix) or msg.content.startswith('!') or msg.content in bot.siritori_list:
            continue
        bot.siritori_list.insert(0, msg.content)
    bot.siritori = True
      
    # その他
    bot.ready = True
    print("ready")
    
    time_action_loop.stop()
    time_action_loop.start()
    return

@tasks.loop(seconds=60.0)
async def time_action_loop():
    delete_keys = []
    now = datetime.datetime.utcnow()
    for _datatime in bot.time_remove_role.keys():
        if now > _datatime:
            try:
                member = await bot.time_remove_role_guild.fetch_member(bot.time_remove_role[_datatime]['user_id'])
                role = bot.time_remove_role_guild.get_role(bot.time_remove_role[_datatime]['role_id'])
                await member.remove_roles(role)
                await bot.time_remove_role[_datatime]['message'].delete()
                delete_keys.append(_datatime)
            except:
                traceback.print_exc()
        
    for key in delete_keys:
        del bot.time_remove_role[key]

@bot.event
async def on_slash_command(ctx):
    if not ctx.guild.id == 733707710784340100:
        return

    used_command = ctx.name
    used_subcommand = ctx.subcommand_name
    used_channel = ctx.channel.mention
    used_author = ctx.author.mention
    embed = discord.Embed(title='コマンドが実行されました')
    embed.add_field(name='コマンド名', value=used_command)
    embed.add_field(name='サブコマンド名', value=used_subcommand)
    embed.add_field(name='使用されたチャンネル', value=used_channel)
    embed.add_field(name='使用者', value=used_author)
    await bot.history_channel.send(embed=embed, allowed_mentions=discord.AllowedMentions.none())


bot.run(TOKEN)
