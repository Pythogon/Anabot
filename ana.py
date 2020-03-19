##############################
#             Ana            #
##############################
import asyncio,os,discord,json # Importing

from datetime import datetime
from random import randint as rand

from discord.ext import commands
from py_translator import Translator
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PyDictionary import PyDictionary
from forex_python.converter import CurrencyRates as CR
from names import get_first_name

def r(fname):
    with open(f'local_Store/{fname}', 'r') as file: # File read function
        return file.read()

def jsonread(fpath):
    with open(fpath, 'r') as json_file:
        return json.load(json_file)

def jsonwrite(fpath, data):
    with open(fpath, 'w') as outfile:
        json.dump(data,outfile)

def getStatus():
    return {1: 'over things',2: 'Netflix',3: 'you',4: 'the data stream', 5: 'the cats', 6: 'Dekeullan', 7: 'the stars', 8: 'my language', 9: 'out for cats'}.get(rand(1,9))

p = '}'

##############################
#           Errors           #
##############################

class Error(Exception):
    pass
class NothingOrderedError(Error):
    pass
class RNAE(Error): # Rates Not Available Error
    pass
class NAE1(Error): # No Account Error First Person
    pass
class NAE3(Error): # No Account Error Third Person
    pass

##############################
#            Class           #
##############################

class ana(commands.Bot):
    """ Let's define our least favourite bot """
    async def on_ready(self):
        """ Setup """
        print('Logged on!')

        while bot.is_ready():
            """ Random statusinator """
            await asyncio.sleep(30)
            activity = discord.Activity(name=f'{getStatus()} | {p}help',type=discord.ActivityType.watching)
            await bot.change_presence(activity = activity)

    async def on_message(self,message):
        """ Let's messagehandle """
        if message.author.bot:
            return # Bots don't really exist
        alter = message.content.replace(f'<@{self.user.id}>', '') # Testing for a mention
        if alter is not message.content:
            await message.add_reaction('❤') # Anabot hearter mark 2
        try:
            chat = f'{message.author.name} ({message.channel.name} | {message.guild.name}) | {message.content}' # Recording all chat for training and quality purposes
        except:
            chat = 'Err #1' # Used if user uses unicode that the Python parser doesn't like
        print(chat)

        return await bot.process_commands(message) # Let's see if the user is trying to run a command
    async def on_command_error(self, ctx, error): # Error handling
        embed = discord.Embed(title='Error',color=0xff0000)
        if isinstance(error, commands.BadArgument): # Catching one singular error type (the most common one)
            embed.add_field(name='Bad argument',value="This command either needs an argument or the argument entered isn't quite right.") # Message
            embed.set_footer(text=f"Please try again or read {p}help if you keep getting this message. If you're sure you're doing it correctly contact Ash as this might be a bug.")
            return await ctx.send(embed = embed) # Send
        if isinstance(error, commands.CheckFailure): # These are pretty self explanatory
            embed.add_field(name='No permissions',value="Sorry, but you don't have permission to use this command.")
            embed.set_footer(text=f'Read {p}help to see what commands you can run. If you believe this is a mistake contact Ash as this might be a bug.')
            return await ctx.send(embed=embed)
        if isinstance(error, RNAE):
            embed.add_field(name='Incorrect currency codes',value="Sorry, but the currency codes you entered aren't correct.")
            return await ctx.send(embed=embed)
        if isinstance(error, NothingOrderedError):
            embed.add_field(name="Nothing ordered", value='You have to order something.')
            embed.set_footer(text=f'To order something, do {p}order [your order].')
            return await ctx.send(embed=embed)
        if isinstance(error, NAE3):
            embed.add_field(name="No account", value="The person you're trying to interract with doesn't have an account.")
            embed.set_footer(text=f'Tell them to run {p}daily.')
            return await ctx.send(embed=embed)
        if isinstance(error, commands.CommandOnCooldown):
            embed.add_field(name="Command on cooldown", value = "You can't use this command again yet.")
            return await ctx.send(embed=embed)

    async def on_reaction_add(self, reaction, user):
        """ Listening for reactions """
        message = reaction.message # Getting Message objext
        if message.author.bot:
            return # Bots can't have anything special
        if message.channel.id == 567685702205046785:
            await message.add_reaction(reaction.emoji) # Polls
            return

    async def on_guild_join(self, guild): # Join message
        count = len(bot.guilds)
        log = bot.get_channel(569264606015520778)
        e = discord.Embed(title = 'Guild joined!', color = 0x00ff00)
        e.add_field(name = f'Joined {guild.name} ({guild.id}).', value = f'New guild count: {count}.')
        await log.send(embed=e)

    async def on_guild_remove(self, guild): # Leave message
        count = len(bot.guilds)
        log = bot.get_channel(569264606015520778)
        e = discord.Embed(title = 'Guild left...', color = 0xff0000)
        e.add_field(name = f'Left {guild.name} ({guild.id}).', value = f'New guild count: {count}.')
        await log.send(embed=e)

bot = ana(activity=discord.Activity(name=f'{getStatus()} | {p}help',type=discord.ActivityType.watching), command_prefix=p)
text_ = f'{p}help || Anabot v1.0  (^ = must own a pet, * = must have a bank account)'

##############################
#             Help           #
##############################
bot.remove_command('help') # Removing default help (I don't like it)
@bot.command(name = 'help') # New help command (help is a registered keyword so we just need to pretend we have a function called 'help')
async def help_command(ctx):
    """ Basic bitch help command (by Ash) """
    title = discord.Embed(title = 'Help', color = 0x00ff00) # Title embed
    title.add_field(name = 'Welcome to Anabot!', value = f"To see commands, do {p}<category>. \nCommands: \n1. {p}general \n2. {p}utility \n3. {p}fun \n4. {p}eco", inline = True)
    title.set_footer(text = text_)
    await ctx.send(embed = title)

@bot.command(name = 'general')
async def general_help(ctx):
    general = discord.Embed(title = 'General Commands', color = 0x00ff00) # General commands (+random commands)
    general.add_field(name = f'{p}help', value = 'Shows these messages.', inline = True)
    general.add_field(name = f'{p}ping', value = 'Test bot connection.', inline = True)
    general.add_field(name = f'{p}invite', value = 'Invite the bot to your server!', inline = True)
    general.add_field(name = f'{p}dice <sides>', value = 'Rolls a dice with given number of sides (default is 6).', inline = True)
    general.add_field(name = f'{p}coinflip', value = 'Flip a coin!', inline = True)
    general.set_footer(text = text_)
    await ctx.send(embed = general)

@bot.command(name = 'utility')
async def utility_help(ctx):
    utility = discord.Embed(title='Utility Commands', color=0x00ff00) # Utility commands
    utility.add_field(name = f'{p}translate <to> <text>', value = 'Translate anything quickly and easily.', inline = True)
    utility.add_field(name = f'{p}colour [6 letter hex code]', value = 'Visualise any colour or randomly generate one!', inline = True)
    utility.add_field(name = f'{p}avatar <@user>', value = "Fetch  a user's avatar.", inline = True)
    utility.add_field(name = f'{p}dictionary <word>', value = 'Define a word (source: WordNet).', inline = True)
    utility.add_field(name = f'{p}currency <amount> <from> <to>', value = 'Convert amounts between currencies (source: Forex).', inline = True)
    utility.set_footer(text = text_)
    await ctx.send(embed = utility)

@bot.command(name = 'fun')
async def fun_help(ctx):
    fun = discord.Embed(title = 'Fun and Games', color = 0x00ff00) # Fun stuff
    fun.add_field(name = f'{p}rockpaperscissors <r, p or s>', value = 'Play a friendly game of rock paper scissors with me!', inline = True)
    fun.add_field(name = f'{p}echo <text>', value = 'Get me to repeat anything you want in an embed.', inline = True)
    fun.add_field(name = f'{p}gaydar <@user>', value = 'Tells you how gay someone is.', inline = True)
    fun.add_field(name = f'{p}rate <@user>', value = 'Rates someone out of 5 stars.', inline = True)
    fun.set_footer(text = text_)
    await ctx.send(embed = fun)

@bot.command(name = 'eco')
async def eco_help(ctx):
    eco = discord.Embed(title = 'Economy', color = 0x00ff00) # Economy
    eco.add_field(name = f'{p}daily', value = 'Get your daily Hoops or register your user ID into the bank.', inline = True)
    eco.add_field(name = f'{p}balance', value = 'Check your balance.*', inline = True)
    eco.add_field(name = f'{p}dicebet', value = 'Bet on the value of a dice and get paid depending on how close you got!*', inline = True)
    eco.set_footer(text = text_)
    await ctx.send(embed = eco)

@bot.command(name = 'pet')
async def pet_help(ctx):
    pet = discord.Embed(title = 'Pets', color = 0x00ff00)
    pet.add_field(name = f'{p}stats', value = "Check your pet's stats or get one if you don't have one!")
    pet.add_field(name = f'{p}feed', value = "Feed your pet to bond with them!^")
    pet.set_footer(text = text_)
    await ctx.send (embed = pet)

@bot.command(name = 'info') # Info about the bot
async def info_(ctx):
    e = discord.Embed(title = 'About me:', color = 0x00ffff) # Pretty self explanatory if you look at any documentation ever
    e.add_field(name = 'Owner', value = 'Ásh (User 156019409658314752)')
    e.add_field(name = 'Github Repo', value = 'https://github.com/Pythogon/Anabot')
    await ctx.send(embed=e)

##############################
#           Owner            #
##############################

@bot.command()
@commands.is_owner()
async def restart(ctx):
    os.system('git pull')
    os.system('pm2 restart ana')

@bot.command()
@commands.is_owner()
async def ratemanip(ctx, user: discord.User, cmd, level: int):
    """ Hacking the database (part 1) """
    fpath = f'local_Store/{cmd}.txt' # Setting path to the json
    scores = jsonread(fpath) # Grabbing dictionary data
    scores[str(user.id)] = str(level)
    jsonwrite(fpath, scores) # Forcewrite their score
    embed=discord.Embed(title = f'Manual override for {user.name}:', color = 0xff0000)
    embed.add_field(name = f"Override on '{cmd}' succesful.", value = f"New value: {level}.")
    embed.set_footer(text = 'Make sure nobody finds out about this~')
    await ctx.send(embed=embed)

@bot.command()
@commands.is_owner()
async def ecomanip(ctx, user: discord.User, variable, value):
    """ Hacking the database (part 2) See comments on part 1 for more info """
    fpath = f'local_Store/Eco/{user.id}'
    try:
        data = jsonread(fpath)
    except:
        raise NAE3 # Doesn't do anything
    data[variable] = value
    jsonwrite(fpath,data)
    embed=discord.Embed(title = f'Manual override for {user.name}:', color = 0xff0000)
    embed.add_field(name = f"Override on '{variable}' succesful.", value = f"New value: {value}.")
    await ctx.send(embed=embed)

@bot.command()
@commands.is_owner()
async def forceleave(ctx, guildid: int):
    """ Leaves a guild based on ID, who knows, might need it some day """
    toleave = bot.get_guild(guildid)
    await toleave.leave()

##############################
#           General          #
##############################

@bot.command(aliases = ['test'])
async def ping(ctx):
    """ Basic ping message, pretty easy to understand looking at all the other things """
    embed=discord.Embed(title="Pong!", color=0x00ff40)
    embed.add_field(name="I'm here!", value=f'Do {p}help to learn about what I can do.', inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def invite(ctx):
    """ Inviting users to the server and inviting bot to servers """
    embed=discord.Embed(title="Invite the bot to your server!", url="https://discordapp.com/oauth2/authorize?client_id=567418835976847360&scope=bot&permissions=8", color=0x00ffff)
    e = discord.Embed(title='Join our Discord server for fun times and updates.', url = 'https://discord.gg/Vfyc358/', color = 0x00ffff)
    await ctx.send(embed=embed)
    await ctx.send(embed=e) # 2 embeds, oo fancy

##############################
#           Random           #
##############################

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

##############################
#           Utility          #
##############################

@bot.command()
async def translate(ctx, to, source, *text):
    """
    Translator
    """
    text = ' '.join(text)
    try:
        embed=discord.Embed(title=f'Translating to {to} from {source}...', color=0x3bb496)
        embed.add_field(name='I think that would be:',value=interpret.translate(text, to, source).text)
        await ctx.send(embed=embed)
    except:
        embed=discord.Embed(title='Error', color=0xff0000)
        embed.add_field(name=f"One or more of your language codes are incorrect, sorry!", value="Please try again.")
        await ctx.send(embed=embed)

@bot.command(name='colour', aliases = ['color'])
async def colour_(ctx, *colour: str):
    """
    Visualise a hex code
    """
    try:
        if colour == '':
            reason = 0
            raise ValueError
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

@bot.command()
async def avatar(ctx, user: discord.User):
    """
    Fetch a user's avatar
    """
    url = user.avatar_url
    await ctx.send(url)

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

@bot.command(name = 'currency', aliases=['forex','convert','con'])
async def currency_(ctx, amount: int, currencyfrom, currencyto):
    if len(currencyfrom) is not 3 or len(currencyto) is not 3:
        raise RNAE
    try:
        end = currency.convert(currencyfrom, currencyto, amount)
        rate = currency.get_rate(currencyfrom, currencyto)
    except:
        raise RNAE
    embed = discord.Embed(title='Converting {} to {}...'.format(currencyfrom, currencyto),color=0xad2d5f)
    embed.add_field(name='{} {} is {:.2f} {}'.format(amount,currencyfrom,end,currencyto),value='Rate: 1 {} to {:.2f} {}'.format(currencyfrom,rate,currencyto))
    embed.set_footer(text='Source: Forex')
    await ctx.send(embed=embed)


##############################
#             Fun            #
##############################

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
    fpath = 'local_Store/gay.txt'
    try:
        scores = jsonread(fpath)
    except:
        await ctx.send('ERR')
    try:
        score = int(scores[str(user.id)])
        embed = discord.Embed(title=f"Someone's already asked about {user.name}. How gay are they again?", color = 0xbdbdbd)
        embed.add_field(name = 'Fetching...', value = "Please wait, this won't take long.")
    except:
        embed = discord.Embed(title=f"Nobody's asked me about {user.name} yet. Let's have a look.", color = 0xbdbdbd)
        embed.add_field(name = 'Calculating...', value = "Please wait, this won't take long.")
        score = rand(1,10)
        scores[str(user.id)] = str(score)
        jsonwrite(fpath, scores)
    msg = await ctx.send(embed=embed)
    await asyncio.sleep(2)
    await msg.edit(embed=getGay(score, user, p))

@bot.command(aliases=['rateme','howhot','smashorpass'])
async def rate(ctx, user: discord.User):
    """
    What does Anabot think of you?
    """
    fpath = 'local_Store/rate.txt'
    try:
        scores = jsonread(fpath)
    except:
        await ctx.send('ERR')
    try:
        score = int(scores[str(user.id)])
        embed = discord.Embed(title=f"Someone's already asked about {user.name}. How did I rate them?", color = 0xbdbdbd)
        embed.add_field(name = 'Fetching...', value = "Please wait, this won't take long.")
    except:
        embed = discord.Embed(title=f"Nobody's asked me about {user.name} yet. Let's have a look.", color = 0xbdbdbd)
        embed.add_field(name = 'Calculating...', value = "Please wait, this won't take long.")
        score = rand(1,5)
        scores[str(user.id)] = str(score)
        jsonwrite(fpath, scores)
    msg = await ctx.send(embed=embed)
    await asyncio.sleep(2)
    await msg.edit(embed=getRate(score, user, p))

##############################
#             Eco            #
##############################

@bot.command()
@commands.cooldown(1, 60*60*24, commands.BucketType.user)
async def daily(ctx):
    fpath = f'local_Store/Eco/{ctx.author.id}'
    try:
        data = jsonread(fpath)
    except:
        default = {'bal': '0'}
        jsonwrite(fpath, default)
        data = jsonread(fpath)
        e = discord.Embed(title = 'No bank account found.', color = 0xff0000)
        e.add_field(name = 'Generating new account file...', value = 'Please wait with me.')
        await ctx.send(embed=e)
    bal = int(data['bal'])
    bal += 1000
    data['bal'] = str(bal)
    jsonwrite(fpath, data)
    e = discord.Embed(title = 'Success!', color = 0x00ffff)
    e.add_field(name = 'Okay, your daily has been succesfully added to your account.', value = f'New balance: ◯{bal}.')
    await ctx.send(embed=e)

@bot.command(aliases = ['bal','cash','money','bank'])
async def balance(ctx):
    fpath = f'local_Store/Eco/{ctx.author.id}'
    try:
        data = jsonread(fpath)
    except:
        embed = discord.Embed(title = 'Error', color = 0xff0000)
        embed.add_field(name="No account", value=f"You don't have an account. Do {p}daily to make one.")
        embed.set_footer(text = "If you're sure you definitely set up an account, contact Ash.")
        return await ctx.send(embed=embed)
    bal = data['bal']
    e = discord.Embed(title = 'Your balance:', color = 0x00ffff)
    e.add_field(name = f'◯{bal}', value = f'Protip: Make sure to do {p}daily every day for the most rewards.')
    await ctx.send(embed=e)

@bot.command()
async def dicebet(ctx, choice: int, bet: int):
    '''
    Bet on a 10 sided dice roll and get paid depending on how close your guess was
    '''
    fpath = f'local_Store/Eco/{ctx.author.id}'
    if choice > 10 or choice < 1: raise commands.BadArgument
    if choice % 1 is not 0: raise commands.BadArgument
    if bet < 100:
        e = discord.Embed(title = 'Error', color = 0xff0000)
        e.add_field(name = 'Bet too small', value = "Your bet isn't quite large enough. It has to be at least ◯100.")
        return await ctx.send(embed=e)
    try:
        data = jsonread(fpath)
    except:
        embed = discord.Embed(title = 'Error', color = 0xff0000)
        embed.add_field(name="No account", value=f"You don't have an account. Do {p}daily to make one.")
        embed.set_footer(text = "If you're sure you definitely set up an account, contact Ash.")
        return await ctx.send(embed=embed)
    bal = int(data['bal'])
    if bet > bal: raise DebtError
    bal -= bet
    roll = rand(1,10)
    if roll == choice:
        payback = 5*bet
        bal += payback
        bonus = payback - bet
        pack = ['Jackpot!',0x46ff00]
    elif roll == choice + 1 or roll == choice - 1:
        pack = ['Close...',0xffff00]
        payback = 2*bet
        bal += payback
        bonus = payback - bet
    else:
        pack = ['Too bad...',0xffffff]
        bonus = 0
    bal = int(bal)
    data['bal'] = str(bal)
    embed = discord.Embed(title=pack[0],color=pack[1])
    embed.add_field(name = 'You picked {} and the roll was {}.'.format(choice, roll), value = 'Earnings: ◯{}'.format(bonus))
    embed.set_footer(text = 'New balance: ◯{}.'.format(bal))
    jsonwrite(fpath, data)
    await ctx.send(embed=embed)

##############################
#             Pet            #
##############################

@bot.command()
async def stats(ctx):
    fpath = f'local_Store/Pets/{ctx.author.id}'
    try:
        data = jsonread(fpath)
    except:
        embed = discord.Embed(title = 'Pet Stats')
        embed.add_field(name = 'No pet found!', value = 'Generating a new one...')
        await ctx.send(embed=embed)
        data = {}
        data['name'] = get_first_name()
        data['personality'] = rand(1,5)
        data['rp'] = "0"
        jsonwrite(fpath, data)
    embed = discord.Embed(title = 'Pet Stats', color = 0x46ff00)
    embed.add_field(name = 'Name:', value = data['name'])
    embed.add_field(name = "Personality:", value = getName(int(data['personality'])))
    embed.add_field(name = "Relationship Points (RP):", value = data['rp'])
    embed.set_footer(text = f'Do {p}pet for help on pets.')
    await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1, 3600*5, commands.BucketType.user)
async def feed(ctx):
    fpath = f'local_Store/Pets/{ctx.author.id}'
    try:
        data = jsonread(fpath)
    except:
        embed = discord.Embed(title = 'Feeding time for...', color = 0xff0000)
        embed.add_field(name = 'No pet found.', value = f'Do {p}stats to get a pet.')
        return await ctx.send(embed=embed)
    score = int(data['rp'])
    rp_increase = rand(2,5)*10
    e = int(data['rp'])
    name = data['name']
    data['rp'] = str(e + rp_increase)
    rp = data['rp']
    embed = discord.Embed(title = f'Feeding time for {name}!')
    embed.add_field(name = f'+{rp_increase} RP!', value = f'New RP: {rp}.')
    embed.set_footer(text = 'You can come back in 5 hours.')
    await ctx.send(embed = embed)
    jsonwrite(fpath, data)

##############################
#          Functions         #
##############################

def getGay(l, user, prefix):
    varset = {1: ['{} is as straight as an arrow.',0xffffff],
    2: ['{} is straight.',0xffe9ff],
    3: ['{} is straight... probably.',0xffcbff],
    4: ["I think {}'s straight, but I don't know.",0xff97ff],
    5: ['Actually, I think {} has a bit of gay in them.',0xff83ff],
    6: ["I think {}'s gay, but I don't know.",0xff76ff],
    7: ['{} is probably gay.',0xff4eff],
    8: ['{} is gay.',0xff3eff],
    9: ['{} is definitely gay.',0xff21ff],
    10: ['{} is fabulous~',0xff00ff],
    -9223372036854775808: ['{} causes an integer overflow error.',0xff0000]}.get(l)
    embed = discord.Embed(title = varset[0].format(user.name), color = varset[1])
    embed.add_field(name = f'Score: {l} out of 10', value = f'Do you want to know how gay someone is? Do {prefix}gaydar [@user].')
    return embed

def getRate(l, user, prefix):
    varset = {0: ["I wouldn't touch {} with a 10 foot pole.", 0x46ff00,'☆☆☆☆☆'],
    1: ["I really don't want to talk about {}.",0x5fa8ff,'★☆☆☆☆'],
    2: ["Sorry, {}... but I'll pass.",0xfffb00,'★★☆☆☆'],
    3: ["{} is okay, that's all I can really say about them.", 0xffc100,'★★★☆☆'],
    4: ["I think {} is great.", 0xff5900,'★★★★☆'],
    5: ['{} is literal fire~',0xff3131,'★★★★★'],
    6: ['{} is too cute for words~'],0xff0000,'★★★★★★'}.get(l)
    embed = discord.Embed(title = varset[0].format(user.name), color = varset[1])
    embed.add_field(name = f'Rating: {varset[2]}', value = f'Do you want to know what I think about someone? Do {prefix}rate [@user].')
    return embed

def getName(l):
    return {1: 'Calm', 2: 'Friendly', 3: 'Fun', 4: 'Excitable', 5: 'Hyper'}.get(l)

##############################
#             Run            #
##############################

tokens = r('token.txt').strip()
interpret = Translator()
dictionary = PyDictionary()
currency = CR()
bot.run(tokens)
