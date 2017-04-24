# Keldon Hanabi Stats
http://keldon.net/hanabi/ is a site where groups of people meet up to play games of Hanabi. You can host your own games with friends or guests. Also spectating other games is available when the host of the game allows it. You can also see replays of your own games and other games that share the same deal. It all runs in your web browser.  
The site provide 3 other variations from the standard 5 suited decks. The possible variations are:

- No Variant: 5 suits
- Black Suit: 6 suits, the last suit is Black
- Rainbow: 6 suits, the last suit is Rainbow which can be clued with any color
- Black Suit (one of each): Same as Black Suit except the black suit has one copy of each rank

One of the issues of the site is that you don't know your win rate or score distribution of all the games you have played.

## Game Caching
Due to the architecture of Keldon, caching the game data is needed. Keldon does not provide names of the players you played with unless you load the game. So there is 5 network calls to keldon before getting the names. Caching some of the game data into a database makes gathering previous data faster since it does not need to be loaded again.

## Requirements

Requirements: Python 3.x, socketIO_client
