# Imports
import discord
import os
import random
from discord.ext import commands
from dotenv import load_dotenv

# Setup
load_dotenv()
TOKEN = os.getenv('TOKEN')
SERVER_NAME = os.getenv('SERVER_NAME')
SERVER_ID = os.getenv('SERVER_ID')

# Create Bot
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    server = discord.utils.get(bot.guilds, name=SERVER_NAME)

    # Print Welcome Message.
    print(f'{bot.user.display_name} has connected to {SERVER_NAME}!')

    # Print Server Members.
    print('Server Members:')
    for member in server.members:
        print(' - ' + member.name)


@bot.command(name='ping', brief='Pong!')
async def ping(ctx):
    await ctx.send('Pong!')


@bot.command(name='bonk', brief='Bonk!')
async def bonk(ctx, user: discord.Member):
    await ctx.send(user.display_name + ' was Bonked!')


@bot.command(name='getid', brief='Get the ID of the user specified')
async def getid(ctx, user: discord.Member):
    await ctx.send(user.id)


@bot.command(name='shuffle', brief='Shuffles a sentence.')
async def shuffle(ctx, *, args):
    phrase = args.split(' ')
    words = random.sample(phrase, len(phrase))
    separator = ' '
    await ctx.send('`' + separator.join(words) + '`')


@bot.command(name='roll', brief='Rolls dice in the format XdX.')
async def roll(ctx, dice, *args):
    try:
        dIndex = int(dice.index('d'))
        num1 = int(dice[0: dIndex])
        num2 = int(dice[dIndex + 1:])
        output = 0
        for i in range(num1):
            output += random.randint(1, num2)
        await ctx.send(f'`{dice}: {output}`')

    except ValueError:
        await ctx.send('`Enter in the format: !roll XdX`')


@bot.command(name='file', brief='Attempts to print the contents of a file.')
async def file(ctx, filename, *args):
    f = open(filename + '.txt')
    for line in f:
        await ctx.send('`' + line + '`')
    f.close()


@bot.command(name='start', brief='Starts a game of Tic Tac Toe.')
async def start(ctx, user: discord.Member):

    if user.id == ctx.message.author.id:
        await ctx.send('Cannot create a game with yourself')
        return

    currentGames = readFile('gameInfo.txt')
    gameid = 1

    # Loop through all the previous games
    for line in currentGames:
        # Check that it isn't a duplicate game.
        lSplit = line.split('/')
        players = [int(lSplit[1]), int(lSplit[2])]
        if user.id in players and ctx.message.author.id in players:
            await ctx.send('You already have a game running with that person.')
            return

        gameid = int(lSplit[0]) + 1

    output = str(gameid) + '/' + str(user.id) + '/' + str(ctx.message.author.id)
    if random.randint(0, 1):
        output += '/0/'
        first = user.display_name
    else:
        output += '/1/'
        first = ctx.message.author.display_name
    output += '         \n'
    currentGames.append(output)

    writeFile('gameInfo.txt', currentGames)

    await ctx.send(f'`Started a game between {user.display_name} and {ctx.message.author.display_name} '
                   f'with ID {gameid}`')
    await ctx.send(f'`{first} goes first.`')


@bot.command(name='play', brief='Make a move in a naughts and crosses game')
async def play(ctx, gameid: int, move: int, *args):

    # Search the current games for the one requested.
    currentGames = readFile('gameInfo.txt')
    found = False
    for i in range(len(currentGames)):
        game = currentGames[i].split('/')
        if int(game[0]) == gameid:
            found = True
            break
    # If the game is found, `i` will refer to its index in the list.

    if not found:
        await ctx.send('Invalid game code')
        return

    # Find the ID of the next player in that game.
    playerNum = int(game[3]) # 0 or 1
    playerID = int(game[playerNum + 1])
    if ctx.message.author.id != playerID:
        await ctx.send('You are not the next player in that game.')
        return

    # Create the board.
    board = []
    for character in game[4]:
        board.append(character)

    # If the player attempts to play in a taken space.
    if board[move - 1] != ' ':
        await ctx.send('That is not a valid position.')
        await sendBoard(ctx, game[4])
        return

    if playerNum == 0:
        game[3] = '1'
        board[move - 1] = 'O'
    else:
        game[3] = '0'
        board[move - 1] = 'X'

    separator = ""
    game[4] = separator.join(board)
    await sendBoard(ctx, game[4])

    # See if the user won.
    if checkVictory(board):
        await ctx.send(ctx.message.author.display_name + ' won the game!')
        removeGame(int(gameid))
        return

    # Check to see if the game can continue.
    if ' ' in board:
        separator = '/'
        currentGames[i] = separator.join(game)
        writeFile('gameInfo.txt', currentGames)
        if playerNum == 0:
            nextPlayer = bot.get_user(int(game[2])).display_name
        else:
            nextPlayer = bot.get_user(int(game[1])).display_name
        await ctx.send('`' + nextPlayer + '\'s turn next.`')
        return

    # If not the game ends as a draw.
    await ctx.send('It was a Draw!')
    removeGame(int(gameid))


@bot.command(name='current', brief='Displays the sender\'s current games.')
async def current(ctx):
    lines = readFile('gameInfo.txt')
    currentId = ctx.message.author.id
    found = False
    for line in lines:
        lSplit = line.split('/')
        if currentId in [int(lSplit[1]), int(lSplit[2])]:
            found = True
            currentPlayer = await bot.fetch_user(lSplit[int(lSplit[3]) + 1])
            await ctx.send('`ID: ' + lSplit[0] + '\n' + currentPlayer.display_name + '\'s move `')
            await sendBoard(ctx, lSplit[4])

    if not found:
        await ctx.send('No current games for ' + ctx.message.author.display_name)


@commands.has_permissions(administrator=True)
@bot.command(name='clear', brief='Clears the naughts and crosses games')
async def clear(ctx):
    f = open('gameInfo.txt', 'w')
    f.close()
    await ctx.send('Cleared the naughts and crosses games')


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await bot.process_commands(message)


async def sendBoard(ctx, board):
    await ctx.send(f"""
```
  {board[0]}   |   {board[1]}   |   {board[2]}
--------------------
  {board[3]}   |   {board[4]}   |   {board[5]}
--------------------
  {board[6]}   |   {board[7]}   |   {board[8]}
```
""")


def checkVictory(board):
    # Sideways
    if board[0] != ' ' and board[0] == board[1] and board[1] == board[2]:
        return True
    if board[3] != ' ' and board[3] == board[4] and board[4] == board[5]:
        return True
    if board[6] != ' ' and board[6] == board[7] and board[7] == board[8]:
        return True

    # Vertical
    if board[0] != ' ' and board[0] == board[3] and board[3] == board[6]:
        return True
    if board[1] != ' ' and board[1] == board[4] and board[4] == board[7]:
        return True
    if board[2] != ' ' and board[2] == board[5] and board[5] == board[8]:
        return True

    # Diagonal
    if board[0] != ' ' and board[0] == board[4] and board[4] == board[8]:
        return True
    if board[2] != ' ' and board[2] == board[4] and board[4] == board[6]:
        return True

    return False


def removeGame(gameid):
    lines = readFile('gameInfo.txt')
    output = ''
    for line in lines:
        if int(line[0]) != gameid:
            output += line
    writeFile('gameInfo.txt', output)


def readFile(filename):
    f = open(filename)
    output = []
    for line in f:
        output.append(line)
    return output


def writeFile(filename, content):
    f = open(filename, 'w')
    f.writelines(content)
    f.close()

bot.run(TOKEN)