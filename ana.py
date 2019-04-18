import asyncio,os,discord
from discord.ext import commands
from random import randint as rand
from py_translator import Translator
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PyDictionary import PyDictionary
def r(fname):
    with open(fname, 'r') as file:
        return file.read()
p = '[]'
status = {1: 'with Ciel',2: 'all alone',3: 'with you',4: 'Half Life 3', 5: 'Minceraft'}.get(rand(1,5))

class ana(commands.Bot):
    async def on_ready(self):
        print('Logged on!')
    async def on_message(self,message):
        if message.content.startswith(f'<@{self.user.id}>'):
            await message.add_reaction('❤')
            return
        if message.author.bot:
            return
        try:
            print(f'{message.author.name} ({message.author.id}) | {message.content}')
        except:
            print('Err #1')
        return await bot.process_commands(message)
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return await ctx.send('\U0001F6AB This command either needs an argument or the argument entered is incorrect. Please try again.')
    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        if message.author.bot:
            return
        if message.channel.id == 567685702205046785:
            await message.add_reaction(reaction.emoji)
            return
        starboard = bot.get_channel(568450985098215425)
        if len(message.reactions) == 3:
            msg = await starboard.send(f'{message.author.name} ({message.author.id}) | {message.content}')
            await starboard.send(msg.jump_url)
            await msg.add_reaction('⭐')


bot = ana(activity=discord.Game(name=f'{status} | {p}help'), command_prefix=p)

@bot.command(aliases = ['cc'])
@commands.has_permissions(manage_messages=True)
async def clearchat(ctx):
    """
    Clears chat (Admin only)
    """
    tosend = '-CC-'
    for x in range(300):
        tosend = f'{tosend}\n-'
    tosend = f'{tosend}\nCleared chat.'
    await ctx.send(tosend)

@bot.command(aliases = ['rps'])
async def rockpaperscissors(ctx, rps):
    """
    Rock paper scissors
    """
    player = {'r': 1,
    'p': 2,
    's': 3}.get(rps,4)
    if player == 4:
        await ctx.send(f'\U0001F6AB Please use4 {p}rps `<r/p/s>` to play.')
        return
    me = rand(1,3)
    await ctx.send('I pick ' + {1: 'rock.',2: 'paper.',3: 'scissors.'}.get(me))
    asyncio.sleep(3)
    if me == player:
        await ctx.send("\U0001F610 It's a tie.")
    elif player == 1 and me == 3 or player == 2 and me == 1 or player == 3 and me == 2:
        await ctx.send('\U0001F622 You win...')
    else:
        await ctx.send('\U0000263A I win!')

@bot.command(aliases = ['test'])
async def ping(ctx):
    """
    Test if the bot is up
    """
    await ctx.send('Pong!')

@bot.command(aliases = ['number'])
async def dice(ctx,*sides: int):
    """
    Roll a dice with x amount of sides (default 6)
    """

    await ctx.send('Rolling...')
    dice = int(rand(1,sides))
    asyncio.sleep(5)
    await ctx.send(f'{dice}!')

@bot.command(aliases = ['cf','coin'])
async def coinflip(ctx):
    """
    Flip a coin
    """
    coin = {1: 'heads', 2: 'tails'}.get(rand(1,2))
    await ctx.send(f"<:coins:567649563968667648> It's {coin}.")

@bot.command()
async def translate(ctx, to, *text):
    """
    Translator
    """
    text = ' '.join(text)
    try:
        await ctx.send(f'That would be `{interpret.translate(text=text, dest=to).text}`')
    except:
        await ctx.send(f"\U0001F6AB Sorry but {to} isn't a valid language code. Please try again.")

@bot.command(name='colour', aliases = ['color'])
async def colour_(ctx, *colour):
    """
    Visualise a hex code
    """
    try:
        if colour == ():
            await ctx.send('No arguments provided. Generating random colour.')
            raise
        colour = ''.join(list(colour))
        try:
            int(colour,16)
        except:
            colour = 'Err2'
        if len(colour) is not 6:
            await ctx.send(f"\U0001F6AB Sorry, but your argument doesn't match a 6 digit hex code, generating a random one. If you would like to visualise a colour then do {p}colour <6 letter hex code>.")
            raise
    except:
        colour = rand(1,16777215)
        colour = hex(colour)[2:]
    object = svg2rlg(f'http://www.thecolorapi.com/id?format=svg&hex={colour}')
    renderPM.drawToFile(object, 'colour.png', fmt='PNG')
    await ctx.send(file=discord.File('colour.png'))
    os.remove('colour.png')
    await ctx.send(f'Enjoy this lovely shade of #{str(colour)}!')

@bot.command(name='order', aliases = ['food','foodme'])
async def order_(ctx, *order):
    """
    Order food from FoodNet
    """
    kitchen = bot.get_channel(567702425717178391)
    if order == ():
        await ctx.send(f"You can't order nothing. Do {p}order <your order>.")
        return
    order = ' '.join(list(order))
    await ctx.send('Order processed! Please wait with us while we deliver it to you.')
    await kitchen.send(f'{ctx.author.name} has ordered {order} in {ctx.channel.name}.')

@bot.command()
async def avatar(ctx, user: discord.User):
    """
    Fetch a user's avatar
    """
    url = user.avatar_url
    await ctx.send(url)

@bot.command()
async def invite(ctx):
    """
    Invite users to the server!
    """
    invite_link = 'https://discord.gg/Vfyc358'
    await ctx.send('The bot is private, but you can still invite people to the server!\nOur invite link is {}, feel free to invite anyone!'.format(invite_link))

@bot.command(name = 'dictionary', aliases=['dict','define'])
async def pydict(ctx, word):
    """
    Get word definitions (unstable)
    """
    try:
        meaning = dictionary.meaning(word)
    except:
        await ctx.send("Sorry, but that's not a word I know.")
    grape = ''
    orange = list(meaning.items())
    for x in range(len(list(orange))):
            pear = list(orange[x])
            carrot = str(pear[0])
            grape += f'__**{carrot}**__\n\n'
            for z in range(len(pear[1])):
                berry = str(pear[1][z])
                grape += f'{z+1}: {berry}\n'
            grape += '\n'
    await ctx.send(f'{grape}Source: WordNet')

@bot.command(aliases=['copy','repeat'])
async def echo(ctx, *tosay):
    """
    Get the bot to say anything you want
    """
    tosay = ' '.join(tosay)
    tosay = tosay.replace('@everyone','`@everyone`')
    tosay = tosay.replace('@here','`@here`')
    await ctx.send('{}\n*Echoed from <@{}>.*'.format(tosay, ctx.author.id))


tokens = r('token.txt').split('\n')
interpret = Translator()
dictionary = PyDictionary()
bot.run(tokens[0])
