# src-api-501-final
This is a project I wrote for a graduate level software development class. As of right now, the only things I have here are the things I designed for this project and no extra fetures. However, I may change this in the future by implementing more features, adding more thorough documentation, etc. Call it a speedrun.com game finder, the title I went with was mainly for the sake of the class.

## What is this?
This is a tool that returns a list of games/categories from speedrun.com filtered by your preferences. You can filter by run time (shorter vs. longer categories), the platform, and whether or not you need the game to allow emulation.

## How to download/run?
1. Have python 3+ installed.
2. Download the zip of everything and throw it in a folder somewhere.
3. pip install requests.
4. Run main.py.
5. Cope with how slow the web requests to speedrun.com are.

## How to use?
1. Enter the platform(s) that you want to search. I recommend checking speedrun.com for specifics on how it's written. For example, put "Nintendo DS", not "DS". Yet "Wii" on its own is fine... whatever, it's gracious with minor spelling mistakes and will ask you if you're ok with what you put.
2. Enter whether or not the games must allow emulation. By default it will check all games, you need to specify if the game must allow it.
3. Enter the range of times you want the game/category to be. It will ask you to put times in again if you format it wrong or if you put a higher number for the minimum than the maximum. The minimum time is inclusive, the maximum time is exclusive.
4. Enter the number of games/categories to return. A negative number will search until all possible games/categories are searched through whereas a positive number will limit the search accordingly.
5. Wait. The more games that need to be searched, the longer this will take (especially if you want all possible games/categories)
6. Do whatever you want with the list of games/categories that have (hopefully) been returned! If nothing was found, it will say so.

## Why does your readme/documentation suck?
Why are you asking?
