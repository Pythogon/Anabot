import asyncio,os,discord # Importing
from discord.ext import commands
from random import randint as rand
from py_translator import Translator
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PyDictionary import PyDictionary
def r(fname):
    with open(fname, 'r') as file: # File read function
        return file.read()
p = '|'
status = {1: 'with Ciel',2: 'all alone',3: 'with you',4: 'Half Life 3', 5: 'Minceraft'}.get(rand(1,5)) # Random status

class ana(commands.Bot): # Let's define our least favourite bot
    async def on_ready(self): # Setup
        print('Logged on!')
    async def on_message(self,message): # Processisng custom features
        if message.content.startswith(f'<@{self.user.id}>'):
            await message.add_reaction('❤') # Heart on @Anabot
            return
        if message.author.bot: # Stopping bot chaining
            return
        try:
            print(f'{message.author.name} ({message.author.id}) | {message.content}') # Spying on everyone (message recording for moderation)
        except:
            print('Err #1') # Used if user uses unicode that the Python parser doesn't like
        return await bot.process_commands(message) # Command running
    async def on_command_error(self, ctx, error): # Error handling
        if isinstance(error, commands.BadArgument): # Catching one singular error type (the most common one)
            embed = discord.Embed(title='Error',color=0xff0000) # New embed
            embed.add_field(name='Bad argument',value="This command either needs an argument or the argument entered isn't quite right.") # Message
            embed.set_footer(text=f"Please try again or read {p}help if you keep getting this message. If you're sure you're doing it correctly contact Ciel as this might be a bug.")
            return await ctx.send(embed = embed) # Send
        if isinstance(error, commands.CheckFailure):
                embed = discord.Embed(title='Error',color=0xff0000) # New embed
                embed.add_field(name='No permissions',value="Sorry, but you don't have permission to use this command.") # Message
                embed.set_footer(text=f"Read {p}help to see what commands you can run. If you believe this is a mistake contact Ciel as this might be a bug.")
                return await ctx.send(embed=embed)


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
        embed=discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name=f'Please use {p}rockpaper scissors [rps] to play.', value='Try rerunning the command.', inline=True)
        await ctx.send(embed=embed)
        return
    me = rand(1,3)
    msg = {1: 'rock.',2: 'paper.',3: 'scissors.'}.get(me)
    if me == player:
        win_state = "It's a tie."
        comment = "Let's try again."
        colour = 0xffff00
    elif player == 1 and me == 3 or player == 2 and me == 1 or player == 3 and me == 2:
        win_state = 'You win...'
        comment = 'I want a rematch.'
        colour = 0x00ff40
    else:
        win_state = 'I win!'
        comment = 'Better luck next time!'
        colour = 0xff0000
    embed=discord.Embed(title=win_state, color=colour)
    embed.add_field(name=f'I picked {msg}', value=comment, inline=True)
    await ctx.send(embed=embed)


@bot.command(aliases = ['test'])
async def ping(ctx):
    """
    Test if the bot is up
    """
    embed=discord.Embed(title="Pong!", color=0x00ff40)
    embed.add_field(name="I'm here!", value=f'Do {p}help to learn about what I can do.', inline=True)
    await ctx.send(embed=embed)

@bot.command(name = 'dice', aliases = ['number','random','randint'])
async def dice_(ctx,*sides: int):
    """
    Roll a dice with x amount of sides (default 6)
    """
    if sides == ():
        sides = 6
    else:
        sides = sides[0]
    dice = rand(1,sides)
    embed=discord.Embed(title="Rolling...", color=0xff80ff)
    embed.add_field(name=f'The dice rolled {dice}.', value='Do {}dice {} to roll again!'.format(p,str(sides)), inline=True)
    await ctx.send(embed=embed)

@bot.command(aliases = ['cf','coin'])
async def coinflip(ctx):
    """
    Flip a coin
    """
    coin = {1: 'heads', 2: 'tails'}.get(rand(1,2))
    embed=discord.Embed(title='Flipping...', color=0x414fd3)
    embed.add_field(name=f'The coin landed on {coin}.',value=f'Do {p}coinflip to flip another coin!')
    await ctx.send(embed=embed)

@bot.command()
async def translate(ctx, to, *text):
    """
    Translator
    """
    text = ' '.join(text)
    try:
        embed=discord.Embed(title=f'Translating to {to}...', color=0x3bb496)
        embed.add_field(name='I think that would be:',value=interpret.translate(text=text, dest=to).text)
        await ctx.send(embed=embed)
    except:
        embed=discord.Embed(title='Error', color=0xff0000)
        embed.add_field(name=f"I can't translate into {to}, sorry!", value="It doesn't look like a valid language code. Please try again.")
        await ctx.send(embed=embed)

@bot.command(name='colour', aliases = ['color'])
async def colour_(ctx, *colour):
    """
    Visualise a hex code
    """
    try:
        if colour == ():
            reason = 0
            raise ValueError
        colour = ''.join(list(colour))
        try:
            int(colour,16)
        except:
            reason = 1
            raise ValueError
        if len(colour) is not 6:
            reason = 1
            raise ValueError
        embed = discord.Embed(title="Here's the colour you asked for!", color=0xffffff)
        embed.add_field(name=f"Enjoy the wonderful shade of #{colour}.", value=f"If you'd like a random colour do {p}colour without an argument.")
    except ValueError:
        colour = rand(1,16777215)
        colour = hex(colour)
        if reason == 0:
            name = 'No arguments provided.'
        else:
            name = 'Invalid hex code provided.'
        embed = discord.Embed(title=name, color=0xffffff)
        colour = colour[2:]
        embed.add_field(name=f"Enjoy the wonderful shade of #{colour}.", value=f"If you'd like a specific colour do {p}colour [6 letter hex]")
    object = svg2rlg(f'http://www.thecolorapi.com/id?format=svg&hex={colour}')
    renderPM.drawToFile(object, 'colour.png', fmt='PNG')
    await ctx.send(embed=embed)
    await ctx.send(file=discord.File('colour.png'))
    os.remove('colour.png')

@bot.command(name='order', aliases = ['food','foodme'])
async def order_(ctx, *order):
    """
    Order food from FoodNet
    """
    kitchen = bot.get_channel(567702425717178391)
    if order == ():
        embed=discord.Embed(title='Error',color=0xff0000)
        embed.add_field(name="You can't order nothing.", value=f'Do {p}order [your order].')
        await ctx.send(embed=embed)
        return
    order = ' '.join(list(order))
    embed = discord.Embed(title='Order processed!',color=0x00ff40)
    embed.add_field(name="We'll get that delivered ASAP.",value="Please keep in mind it may take longer if we aren't available.")
    await ctx.send(embed=embed)
    staff_message=discord.Embed(title='New order!',color=0xffffff)
    staff_message.add_field(name=f'{ctx.author.name} ordered {order} in #{ctx.channel.name}.',value='Get to work~')
    await kitchen.send(embed=staff_message)

@bot.command()
async def avatar(ctx, user: discord.User):
    """
    Fetch a user's avatar
    """
    url = user.avatar_url
    await ctx.send(url)

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    '''
    You know what this does
    '''
    embed=discord.Embed(title='Shutting down...',color=0xff0000)
    embed.add_field(name="Goodbye!", value='To restart me go to the console and do python3 ana.py.')
    await ctx.send(embed=embed)
    exit()

@bot.command()
async def invite(ctx):
    """
    Invite users to the server!
    """
    embed=discord.Embed(title="Invite people!", url="https://discord.gg/Vfyc358", color=0x00ffff)
    embed.add_field(name='Invite people to join Be today.', value="Sadly, the bot's private right now so there's no bot invite link.", inline=True)
    await ctx.send(embed=embed)

@bot.command(name = 'dictionary', aliases=['dict','define'])
async def pydict(ctx, word):
    """
    Get word definitions (unstable)
    """
    try:
        meaning = dictionary.meaning(word)
    except:
        await ctx.send("Sorry, but that's not a word I know.")
    orange = list(meaning.items())
    for x in range(len(list(orange))):
            pear = list(orange[x])
            carrot = str(pear[0])
            embed = discord.Embed(title=carrot,colour=0xffffff,inline=True)
            for z in range(len(pear[1])):
                berry = str(pear[1][z])
                embed.add_field(name=f'{z+1}',value = berry)
            embed.set_footer(text='Source: WordNet')
            await ctx.send(embed=embed)

@bot.command(aliases=['copy','repeat'])
async def echo(ctx, *tosay):
    """
    Get the bot to say anything you want
    """
    tosay = ' '.join(tosay)
    embed = discord.Embed(title=tosay,color=0xffef73)
    embed.add_field(name=f'Echoed from {ctx.author.name}',value=f'Do you want me to say something? If so do {p}echo [text to say].')
    await ctx.send(embed=embed)

@bot.command(aliases=['howgay','gay'])
async def gaydar(ctx, user: discord.User):
    """
    Tells you how gay someone is according to Anabot's revolutionary random number generator
    """
    score = {156019409658314752: 10}.get(user.id, rand(1,10))
    varset = {1: ['{} is as straight as an arrow',0xffffff],
    2: ['{} is straight',0xffe9ff],
    3: ['{} is straight... probably',0xffcbff],
    4: ["I think {}'s straight, but I don't know",0xff97ff],
    5: ['Actually, I think {} has a bit of gay in them',0xff83ff],
    6: ["I think {}'s gay, but I don't know",0xff76ff],
    7: ['{} is probably gay',0xff4eff],
    8: ['{} is gay',0xff3eff],
    9: ['{} is definitely gay',0xff21ff],
    10: ['{} is fabulous~',0xff00ff]}.get(score)
    embed = discord.Embed(title = varset[0].format(user.name), color = varset[1])
    embed.add_field(name = f'Score: {score}', value = f'Do you want to know how gay someone is? Do {p}gaydar [@user].')
    await ctx.send(embed=embed)


tokens = r('token.txt').split('\n')
interpret = Translator()
dictionary = PyDictionary()
bot.run(tokens[0])
