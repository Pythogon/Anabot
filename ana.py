import discord,asyncio
from random import randint as rand
def r(fname):
    with open(fname, 'r') as file:
        return file.read()
p = '++'
class bote(discord.Client):
    async def on_ready(self):
        print('Logged on!')
        await client.change_presence(activity=discord.Game(name='++help'))
        
    async def on_message(self, message):
        channel = message.channel
        try: print(str(message.author.id) + ':', message.content)
        except: print('Error')
        if message.author.id == 156019409658314752:
            await message.add_reaction('❤')
            
        if message.content.startswith(p) is not True:
            return
        
        m = message.content.replace(p,'').lower()
        if m == 'ping':
            await channel.send('Pong!')

        if m == 'help':
            await channel.send(r('help.txt'))

        if m == 'dice':
            await channel.send('\U0001F3B2 Rolling a 6 sided dice...')
            asyncio.sleep(3)
            await channel.send('\U0001F3B2 The dice rolled '+ str(rand(1,6)) + '!')

        if m.startswith('rps'):
            player = {'r': 1,
             'p': 2,
             's': 3}.get(m[4:],4)
            if player == 4:
                await channel.send('\U0001F6AB Please use ++rps `<r/p/s>` to play.')
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
client = bote()
client.run(r('token.txt'))
