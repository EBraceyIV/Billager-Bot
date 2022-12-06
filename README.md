# Billager-Bot
# Billager-Bot
Billager Bot, your very good friend. A Discord Bot built using the discord.py library, designed for use in a private server for my friends and I. Feel free to use and modify it if you want to. Runs on Python 3.10 with a handful of dependencies for certain features. I wrote this bot to learn more about Python and to create something fun that would provide entertainment and utility. Should work for the most part. This is the 2.0 version, rewritten for the Discord.py 2.0+ versions using slash command, UIKit, etc..

## Features
BBot offers a nice collection of rudimentary features including the following:
### Lore
You know how you always have that one friend who keeps a "quote note" in their phone for wacky out-of-context stuff people say? This is a more refined system of that concept. Add, edit, and eliminate "lore" - formatted embed messages - to keep an ongoing record of what's been going on or notable events.

### Score
Not to be misconstrued with any form of a social credit system, this score-keeping function allows for a simple way of rewarding or punishing other users for their actions. Mostly used as +1 for good jokes, -1 for bad jokes. A scoreboard can be viewed at any time. Every Friday evening a callout post is made that publicly shames the user with the lowest score. The scoreboard resets monthly.

### More
No, not a "everything else" catch-all, but the More Board. A basic homebrew "star board" or soft pin kind of channel. React with enough stars to a message to send it to the More Board. Named this to fit the rhyming theme between Lore and Score.

### Voice
There is a handful of audio clips which can be played on command. No music streaming ability because I considered it unnecessary for the scope of this bot given complexity and availability of other music bots.

### Poll
Build and conduct custom polls for other users with UI elements like buttons and modals. Polls are pinned while active.

## Roadmap
I intend to continue development of BBot in my spare time for the foreseeable future. I have a handful of ideas for things to add and improve upon.
These include but are not limited to:
- Re-implment BBux using the new UI elements
- Migrating from a shelve file read/write system to something for refined like SQLite
- More BBux minigames (Blackjack?) and prizes (trading cards?)
- Enhancing the prize system with more flavor  
- A potential TTS system for the voice client
- A more modular approach to permissions and output settings
- Expanding output text and messages with more variety
- Integrate my NAS to pull from a local music library, UI elemenet navigation through folders
- Probably other things I don't remember at the time of writing this
