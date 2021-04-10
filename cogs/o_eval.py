from discord.ext import commands
import asyncio
import traceback
import discord
import textwrap
from contextlib import redirect_stdout
import io
import subprocess
import re
pat = re.compile(r'(ctx|channel|ctx\.channel)\.send')

# to expose to the eval command
class Eval(commands.Cog):
    """Admin-only commands that make the bot dynamic."""

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    async def run_process(self, command):
        try:
            process = await asyncio.create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = await process.communicate()
        except NotImplementedError:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = await self.bot.loop.run_in_executor(None, process.communicate)

        return [output.decode() for output in result]

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    async def cog_check(self, ctx):
        return True

    def get_syntax_error(self, e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

    @commands.command(pass_context=True, hidden=True, name='eval')
    async def _eval(self, ctx, *, body: str):
        """Evaluates a code"""
        # 俺、くろ
        if not ctx.author.id in [539126298614956082, 699414261075804201]:
            return
        for ng in ['bot.http', 'http.token', 'bot.http.token', 'token']:
            if ng in ctx.message.content:
                await ctx.send(content='使用不可能な文字列が含まれています。', delete_after=3.0)
                return
                
        env = {
            'self': self,
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())
        
        if not body.startswith('```'):
            
            if body.startswith('await'):
                body = body[len('await')+1:]
                
                # send
                if pat.match(body):
                    try:
                        return await eval(body, env)
                    except:
                        return await ctx.send(f'```py\n{traceback.format_exc()}\n```')
                
                else:
                    try:
                        ret = await eval(body, env)
                        return await ctx.send(f'```py\n{ret}\n```')
                    except:
                        return await ctx.send(f'```py\n{traceback.format_exc()}\n```')
            else:
                # 変数代入
                if re.compile(f'({"|".join(globals().keys())})' + r'(\..{1,})? ?=').match(body):
                    try:
                        return exec(body)
                    except:
                        return await ctx.send(f'```py\n{traceback.format_exc()}\n```')
                try:
                    return await ctx.send(f'```py\n{eval(body, env)}\n```')
                except:
                    return await ctx.send(f'```py\n{traceback.format_exc()}\n```')
                    
        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

def setup(bot):
    return bot.add_cog(Eval(bot))
