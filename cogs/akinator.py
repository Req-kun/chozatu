import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashCommand
from discord_slash import SlashContext
from akinator.async_aki import Akinator
import akinator

answers = {
    '0️⃣': 'y',
    '1️⃣': 'n',
    '2️⃣': 'p',
    '3️⃣': 'pn',
    '4️⃣': 'i',
    '5️⃣': '5️⃣'
}
sentakusi = 'はい - :zero:\nいいえ - :one:\n多分そう - :two:\n多分ちがう - :three:\nわからない - :four:\n\n戻る - :five:'
aki = Akinator()
class Akinator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_subcommand(base="fun", name="akinator",
    base_description="楽しもう！", description="アキネイター",
    guild_ids=[733707710784340100],
    options=[
        {
            "name": "accuracy",
            "description": "精度",
            "type": 4,
            "required": True,
            "choices": [
                {
                    "name": "SuperLow",
                    "value": 50
                },
                {
                    "name": "Low",
                    "value": 70
                },
                {
                    "name": "middle",
                    "value": 80
                },
                {
                    "name": "High",
                    "value": 90
                },
                {
                    "name": "SuperHigh",
                    "value": 95
                }
            ]
        }
    ])
    async def _akinator(self, ctx, accuracy):
        await ctx.respond(eat=True)
        author = ctx.author
        msg = await ctx.send(embed=discord.Embed(title='準備中...').set_author(name=f'{author.display_name}({author.id})', icon_url=author.avatar_url))

        for r in answers.keys():
            await msg.add_reaction(r)


        q = await aki.start_game(language='jp')

        while aki.progression <= 80:
            await msg.edit(embed=
                discord.Embed(
                    title=q,
                    description=sentakusi
                ).set_author(
                    name=f'{author.display_name}({author.id})',
                    icon_url=author.avatar_url
                ).set_footer(
                    text='進行率: %7.3f' % aki.progression + f'% (回答: {accuracy}%)'
                )
            )

            r, u = await self.bot.wait_for('reaction_add', check=lambda r, u: u.id == author.id and r.emoji in answers.keys())

            emoji = r.emoji

            await msg.remove_reaction(emoji, author)


            if emoji == "5️⃣":
                try:
                    q = await aki.back()
                except akinator.CantGoBackAnyFurther:
                    pass
            else:
                q = await aki.answer(answers[emoji])
        await aki.win()

        await msg.clear_reactions()
        await msg.edit(
            embed=discord.Embed(
                title=f'それは {aki.first_guess["name"]} ({aki.first_guess["description"]})ですか？',
                description=f'はい - {list(answers.keys())[0]}\nいいえ - {list(answers.keys())[1]}',
            ).set_author(
                name=f'{author.display_name}({author.id})',
                icon_url=author.avatar_url
            ).set_image(url=aki.first_guess["absolute_picture_path"])
        )
        for r in list(answers.keys())[:2]:
            await msg.add_reaction(r)
        r, u = await self.bot.wait_for('reaction_add', check=lambda r, u: r.emoji in list(answers.keys())[:2] and u.id == author.id)


        if answers[r.emoji] == "y":
            await msg.edit(
                embed=discord.Embed(
                    title='Yay!',
                    color=0x00ffff
                ).set_author(
                    name=f'{author.display_name}({author.id})',
                    icon_url=author.avatar_url
                )
            )
        else:
            await msg.edit(
                embed=discord.Embed(
                    title='Oof...',
                    color=0xff0000
                ).set_author(
                    name=f'{author.display_name}({author.id})',
                    icon_url=author.avatar_url
                )
            )
        return



def setup(bot):
    bot.add_cog(Akinator(bot))
