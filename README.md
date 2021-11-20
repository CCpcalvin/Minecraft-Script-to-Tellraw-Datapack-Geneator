# Minecraft Script to Tellraw Datapack Generator
by CCpcalvin

---

## Table of Contents

- [Minecraft Script to Tellraw Datapack Generator](#minecraft-script-to-tellraw-datapack-generator)
  - [Table of Contents](#table-of-contents)
  - [What is this generator do?](#what-is-this-generator-do)
  - [Quickstart](#quickstart)
  - [Advanced Usage](#advanced-usage)
    - [Principle of this generator](#principle-of-this-generator)
    - [Inside ```script.txt```](#inside-scripttxt)
    - [Behavior of delimiter](#behavior-of-delimiter)
    - [Changing input file](#changing-input-file)
  - [List of functions available:](#list-of-functions-available)
    - [Tellraw text:](#tellraw-text)
    - [Changing time interval](#changing-time-interval)
    - [Title](#title)
    - [Running another command](#running-another-command)
    - [Comment](#comment)
    - [Ending the dialogue](#ending-the-dialogue)
    - [Writing command in multiple lines](#writing-command-in-multiple-lines)
    - [Creating a new folder](#creating-a-new-folder)
  - [Config File Settings](#config-file-settings)
    - [Changing the delimiter](#changing-the-delimiter)
    - [Automating apply the style to text](#automating-apply-the-style-to-text)
    - [Replacing existed file](#replacing-existed-file)

## What is this generator do?

```tellraw``` is the command in Minecraft to print the message in Minecraft. This command is essential especially for making map since it can be used to tell the player about the progress of the map, or the dialogue between NPC, or anything else. This generator can turn a script into multiple functions in a datapack of a Minecraft map so that we can execute multiple ```tellraw```functions in one command.

## Quickstart

To use this generator, we need to install ```python3```. We first need to create ```script.txt``` file inside the folder containing multiple ```.py``` files. This file is used to input the script. Now we may write some lines inside the ```script.txt``` such as

```
Calvin: hello
Even: hello world
Calvin: hello Even
```

By running ```python tellraw.py```, it will create two folders, namely ```start``` and ```scene_1``` folders. Then you need to put those two folders inside the ```data``` folder of the datapack (by the way you can change the name of these two folders to prevent crashes of the name). Then in Minecraft, after reloading the datapack, by running ```/function start:scene_1```, then those messages will pop up on the screen one by one with constant time intervals. 

## Advanced Usage

### Principle of this generator

You may visit this [wiki](https://minecraft.fandom.com/wiki/**Data_Pack**) page for some basic information about datapack and this [wiki](https://minecraft.fandom.com/wiki/Function_(Java_Edition)) for the basic information of function in datapack. A ```.mcfunction``` file contains a chain of command that can be executed inside Minecraft at the same time. This generator can generate multiple ```.mcfunction``` files with integer names inside the ```scene_1``` folders (actually this generator can generate multiple scene folders. More detail can be found below). For a pure tellraw-purpose datapack, a ```<n>.mcfunction``` may look like:

```
tellraw @a {"text":"Ryan: Hello World"}
schedule function scene_1:<n+1> 4s
```

Here ```<n>, <n+1>``` are the placeholders. The first line of the code is the ```tellraw``` command that prints ```Ryan: Hello World``` and the second line of the code is to tell Minecraft to run next ```.mcfunction``` file in 4 seconds. Therefore by running the heading ```.mcfunction``` file, the ```tellraw``` command will be executed in every 4 seconds. The command ```/function start:scene_1``` basically is to tell Minecraft to execute the heading ```.mcfunction``` file.

### Inside ```script.txt```

Beyond ```tellraw```, we can add more stuff inside ```script.txt```. The program will run each line into one ```.mcfunction``` file. The basic format of each line in script.txt is

```
<function 1> \ <function 2> \ <function 3> \ ... 
```

Here ```<function 1>, <function 2>, <function 3> ``` are the placeholders containing different actions to perform in one ```.mcfunction``` file. Each function has the format ```<tag>=<action>, <optional arg>```. ```<tag>``` is the placeholder of string to tell what command to be added inside a ```.mcfunction``` file. If we omit the ```<type_of_action>=```, then the program will automatically consider the string inside an argument is something to print out by ```tellraw```. For example, 

```
tell()=" Ryan: Hello World "
```

and

```
Ryan: Hello World
```

will generate the same ```.mcfunction``` file. Note that ```tell``` is the tag to indicate ```tellraw``` command.

There are many ```<type>``` in this program. They will be discussed below.

Also, notice that a blank new line and ```\t``` in ```script.txt``` will be ignored in this program.

### Behavior of delimiter

The program will use ```\``` as the delimiter. You can change another symbol in symbol in the config file. 

### Changing input file

You can change the input file by running ```python tellraw.py <input_file_name>```. The third argument can be omitted and it will set ```script.txt``` as the input file.

## List of functions available:

Beware that the space bar cannot be omitted. Only ```<variable>``` can be replaced. You can replace the empty string for ```<optional_argument>```.

### Tellraw text:

We can use ```tell(<optional_argument>)=" <message> " ``` or ```tellraw(<optional_argument>)=" <message> "``` or omit the tag to indicate that it is a ```tellraw``` command. Note that the space cannot be omitted. The advantage to use a tag instead of omitting it is we can change the font and the text color by some optional arguments. For example,

```
tell(c=Blue, b)=" Even " \ :Hello \ tell(i, u, c=#28D7CC, click(run=/weather clear))=" World "
```

to print:



There are lots of optional arguments in this function:
1. Font related
   - ```c=<color>``` or ```color=<color>```: to change the color. ```<color>``` can be a word or a hex color code. Only word inside the list: [Red, Green, Blue, White, Yellow, Dark_Red, Dark_Green, Dark_Blue, and Gold] is accepted, and it is case-insensitive. 
   - ```b``` or ```bold```: to have bold text
   - ```i``` or ```italic```: to have italic text
   - ```u``` or ```underlined```: to have underlined text
   - ```s``` or ```strikethrough```: to have strikethrough text
   - ```o``` or ```obfuscated```: to have obfuscated text

2. Event-related
   - ```click(<action>=<value>)```: to control what action to be performed when click the text. There are a few possible actions to be performed in this program
     - ```open```: to open a url. ```<value>``` should a url.
     - ```run```: to run a command as the player who clicks the text. ```<value>``` should be a command
     - ```suggest```: to suggest a command to the player who click the text. ```<value>``` should be a command
     - ```copy```: to copy any string to the player's clipboard. ```<value>``` can be any string.

Note that the program will read the line from left to right. Make sure to arrange the function in order. Also, you can print line-break with ```\n``` as the message.

### Changing time interval

We use ```t=<time>``` or ```time=<time>``` to indicate how much time to wait to execute the next ```.mcfunction``` file. Without this tag, the function will automatically take 4 seconds to execute the next file. For example,

```
Even: Hello World \ t=2s
Calvin: Hello Even \ t=35t
Ryan: Hello everyone \ t=2d
```

We need to indicate the unit in time. There are three possible units: ```t, s, d```. ```t``` stands for tick (roughly 20 ticks for 1 second. This can be changed by ```gamerule``` command), ```s``` stands for second and ```d``` stands for Minecraft-day (roughly 20 minutes).

### Title

Sometimes you may want to use ```title``` instead of ```tellraw```. We can use  ```title(<optional argument>)=" <title> "``` to indicate the main title. If we want to add subtitle, we can use ```sub(<optional argument>)=" <subtitle> ")``` or ```subtitle(<optional argument>)=" <subtitle> "```.

```
sub(c=black, o)=" The doom's day " \ title(in=20, out=20, dur=80, c=blue, b, u)=" Chapter 0 " \ t=5s
```

Both commands accepts the same font-related optional arguments as ```tellraw```. Note that we must provide:

- ```in=<time>```: to indicate the fade-in duration. The unit is tick and it must be an integer.
- ```out=<time>```: to indicate the fade-out duration. The unit is tick and it must be an integer.
- ```dur=<time>```: to indicate the duration of title that is visible and not in fade in time and fade out time. The unit is tick and it must be an integer.

### Running another command

Sometimes you may want to execute some commands other than ```tellraw``` or ```title``` command, in that case, we can use ```run=<command>```. For example,

```
Even: Give you some healing \ t=3s
Calvin: Thanks you \ run=effect give @a minecraft:regeneration 5 1 true
```

Then at the same time that print "Calvin: Thanks you", it also gives the regeneration to all the players.

### Comment

Sometimes you may want to comment on some commands. The way to do it is to use ```-- <comment> --```. The program will ignore the whole sequence. It can also be used to a new line.

```
-- Even appear and talk to Ryan --
Even: Hello Ryan \ t=2s \-- Even should face to Ryan --\
Ryan: Hello Even\ t=3s 
```

### Ending the dialogue

Sometimes you may want to end the dialogue(more precisely ending the chain of command). You can use ```end``` tag. For example:

```
Even: Hello Calvin \ end 
Calvin: Hello Even
```

Although the program will also produce ```2.mcfunction``` that contain a ```tellraw``` command, "Calvin: Hello Even" will not print out because of the ```end``` tag in the first line.

### Writing command in multiple lines

Sometimes you want to add lots of things in one ```.mcfunction```. To have a good and clean style, we can use ```cont``` or tag **at the end of the line** to indicate that functions in the next line should also be written in the same ```.mcfunction``` as the pervious line. For example:

```
-- Boss fight start --
tell(c=red)=" Boss "\ :Let's get started!! \ cont 
	run=function trackboss:start \-- Start tracking boss health --\ cont 
	run=function bossbar:on \-- Enable bossbar and write the boss' health to bossbar --\ cont 
	run=function boss_fight_bgm:start \-- Start bgm --\ end 
```

will give out a ```.mcfunction``` file that contains:

```
tellraw @a ["", {"text": "boss", "color": "red"}, ":Let's get started!!"] 
function trackboss:start
function bossbar:on
function boss_fight_bgm:start
```

### Creating a new folder

For a long script, you may not want to put all ```.mcfunction``` in the same folder. We can use ```create=<folder_name>``` to tell the program to create a new folder and put the remaining ```.mcfunction``` to the new folder. Make sure that you do not have the folder with the same name, otherwise, the program will replace the origin folder to new folder or exit depend on the value of ```REPLACE```. Note that ```<folder_name>``` is case-insensitive and the program will turn all characters to lowercase since namespaces in Minecraft do not allow any uppercase letter.

```
create=scene_1 \ cont 
-- Even appear and talk to Ryan --
Even: Hello Ryan \ t=2s \-- Even should face to Ryan --\
Ryan: Hello Even\ end 

create=scene_2 \ cont
-- Boss fight start --
tell(c=red)=" Ryan " \ :Let's get started!! \ cont 
	run=function trackboss:start \-- Start tracking boss health --\ cont 
	run=function bossbar:on \-- Enable bossbar and write the boss' health to bossbar --\ cont 
	run=function boss_fight_bgm:start \-- Start bgm --\ end 
```

This tag also add a function in ```start``` folder so that by running ```\function start:scene_2``` to execute the heading of scene 2.

## Config File Settings

We can change the behaviour of the program in ```config.txt``` file.

### Changing the delimiter

Write ```DELIMITER="<symbol>"``` to change the delimiter

### Automating apply the style to text

You may want to automatically apply the particular text style for particular word. To do this, we write:

```
tell(<optional argument>)=" <string> "
```

in ```config.txt``` file. The ```<style_argument>``` is the same as the optional argument in ```tell``` tag. For example:

```
tell(c=red, b)=" Ryan " 
tell(c=green, u)=" Even "
```

In this case, the program will turn all "Ryan" to red bold text and all "Even" to green underlined text.

### Replacing existed file

By default, the program will exit when there is a crash of the folder name. By writing ```REPLACE = "yes"``` in ```config.txt```, it will replace the existed file instead of exiting.
