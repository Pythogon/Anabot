import discord,asyncio,os,cairosvg
from random import randint as rand
from translate import Translator
def r(fname):
    with open(fname, 'r') as file:
        return file.read()
p = '='
class bote(discord.Client):
    async def on_ready(self):
        print('Logged on!')
        status = {1: 'with Ciel',2: 'all alone',3: 'with you',4: 'Half Life 3', 5: 'Minceraft'}.get(rand(1,5))
        await client.change_presence(activity=discord.Game(name=status + ' | '+ p + 'help'))

    async def on_message(self, message):
        channel = message.channel
        m = message.content.replace(p,'').lower()
        try: print(str(message.author.id) + ':', message.content)
        except: print('Error')

        if message.author.bot:
            return

        if channel.id == 567685702205046785:
            await message.add_reaction('👍')
            await message.add_reaction('👎')
            return

        if message.author.id == 156019409658314752:
            await message.add_reaction('❤')

        if message.content.startswith(p) is not True:
            return

        if m == 'ping':
            await channel.send('Pong!')

        if m == 'help':
            await channel.send(r("help.txt"))

        if m == 'dice':
            await channel.send('\U0001F3B2 Rolling a 6 sided dice...')
            asyncio.sleep(3)
            await channel.send('\U0001F3B2 The dice rolled '+ str(rand(1,6)) + '!')

        if m.startswith('rps'):
            player = {'r': 1,
             'p': 2,
             's': 3}.get(m[4:],4)
            if player == 4:
                await channel.send('\U0001F6AB Please use '+ p + 'rps `<r/p/s>` to play.')
                return
            me = rand(1,3)
            await channel.send('I pick ' + {1: 'rock.',2: 'paper.',3: 'scissors.'}.get(me))
            asyncio.sleep(3)

            if me == player:
                await channel.send("\U0001F610 It's a tie.")

            elif player == 1 and me == 3 or player == 2 and me == 1 or player == 3 and me == 2:
                await channel.send('\U0001F622 You win...')

            else:
                await channel.send('\U0000263A I win!')

        if m == 'coinflip':
            coin = rand(1,2)
            if coin == 1:
                coin = 'heads!'
            else:
                coin = 'tails!'
            await channel.send('Flipping...')
            asyncio.sleep(3)
            await channel.send("<:coins:567649563968667648> It's " + coin)

        if m.startswith('colour'):
            args = m[7:]
            if args == '':
                c = rand(1,16777215)
                c = hex(c).split('x')[-1]
            else:
                try:
                    if len(args) is not 6:
                        raise ValueError
                    int(args,16)
                except:
                    await channel.send('\U0001F6AB Sorry. Either do '+ p + 'colour or ' + p + 'colour <6 letter hex> to use this command.')
                    return
                c = args
            cairosvg.svg2png(url='http://www.thecolorapi.com/id?format=svg&hex='+c,write_to='image.png')
            await channel.send(file=discord.File('image.png'))
            os.remove('image.png')
            await channel.send('Enjoy this lovely shade of #'+str(c)+'!')

        if m.startswith('order'):
            args = m[6:]
            if args == '':
                await channel.send('\U0001F6AB Sorry, but you need to order something.')
                return
            else:
                kitchen = client.get_channel(567702425717178391)
                await kitchen.send(message.author.name + ' has ordered '+ args +' in <#'+str(channel.id)+'>.')
                await channel.send("\U0001F44D We'll get that to you ASAP!")

        if m.startswith('translate'):
            lang = m[10:11]
            todo = m[13:]
            if len(lang) is not 2:
                    raise ValueError
            trans = Translator(to_lang=lang)
            await channel.send('That would be ' + trans.translate(todo))
            await channel.send("\U0001F6AB something there didn't quite work. Please check your language code.")

client = bote()
file = r('token.txt').strip().split('\n')
client.run(file[0])
