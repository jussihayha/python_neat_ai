# Simple Python game with AI-playing it

### Background

This game was made for course Software Development Technologies in Haaga-Helia University of Applied Sciences.  
This repository demonstrates a simple game and how to implement NEAT-algorithm with Python.

During the process I created two separate things. A buggy singleplayer game and a less buggy, but feature poor AI
driven 'running game'.

### Objectives of the games (Singleplayer vs AI )

During the development process of the AI singleplayer version and AI-version went to different directions. The
singleplayer version has a few more features:

- you are able to shoot the enemies (you can have 5 bullets in air at the same time)
- you can increase your descend velocity -> get back to the ground faster

Also the language in the singleplayer version is finnish and I cannot be bothered to fix it all.

In the AI-version the objective is to survive as long as possible. You get points (and AI gets fitness) based on the
time you've been alive.

In the singleplayer version you get points by shooting the enemies, your goal is to get as many points as possible.

The speed of the game gradually increases in both versions.

AI-version has one thing that is massively better than the singleplayer one - that is pixel perfect collision detection.
When I first started the project I kept wondering why the AI was dying even when not touching the obstacles.  
After I drew some rectangle shapes to understand the hitboxes it hit me.

The hitboxes are massive compared to the actual player masks / images. 

I've added a couple of gifs that demonstrate the singleplayer game + the problem. 
I'll add a few gifs about the AI-version as soon as I get the images processed.

![single_player_blocks](readme_assets/single_player_hitboxes.gif)
![single_player_normal](readme_assets/single_player_normal.gif)

### Inputs and outputs

I have defined the following inputs for NEAT-activation:

- speed of the game
- distance between enemy and hero
- Y-axis location of enemy and hero

There is only one output currently. The AI must decide to jump or not.

### Used packages and gotchas

The project works atleast in Python 3.7 and 3.8.5

- pygame (for creating the game)
- neat-python
- pickle (for saving trained model locally)
- argparse (handling arguments in commandline)

### Example video 


### Installation

You need to have Python and PIP installed.  
You can find instructions on how to do that in many locations.

My recommendation is that you create a new virtual environment for this project  
so that the project lives in isolation. 

You can find many solutions on how to handle virtual environments I recommend that you
check them out. This is not mandatory for this project to work.
```
 $ git clone https://github.com/jussihayha/python-neat-ai
 $ pip install -r requirements.txt
```

### Usage 

You can use this repository for running a pretrained AI that was run for 3, 5 or 100 generations.  
If you want you can tweak the repository and train your own AI and save that model.
You can also choose to try this game for yourself. This is in file single_player.py.

#### Single player usage

Hero jumps from `spacebar`, shoots from `c` -key and stomps from `z` -key.

```
$ python single_player.py
```

#### Checking out pretrained AI

Use switch `--replay` together with a .pkl filename you want to replay. Replays the best genome in a previous run.
Default load and save location is models folder so keep that in mind.
```
$ python main.py --replay <filename>
```

#### Training a new model / AI

Use switch `--train` together with an integer number preferably over 5.  
In this projects context training means that you get to watch the AI trying to learn the game.

In previous iterations of this project 1 generation of genomes started at once, but I found
out that understanding the different genomes and 'heroes' is hard when you cannot watch them one by one.

After training is over it creates a file called winner-10.pkl to models folder (integer value of the filename changes based on your parameter).

```
$ python main.py --train 10
```

### TODO
Here are a few of the things this I still should do
- continue translating finnish to english and refactor singleplayer
- reconfigure and analyze inputs for neat activation
- work on progressing the configuration file
- add shooting and stomping capabilities in the AI-version
- add proper comments to classes and other files
- create a better AI - add complexity to the game


### Acknowledgements

Kenneth O. Stanley and Risto Miikkulainen for publishing the paper on 'Evolving Neural Networks through Augmenting Topologies'  
CodeBullet for providing humorous videos about creating and figuring out how to operate AI's in different scenarios.

I did not make the assets myself. The used background image uses GPL 3.0 and you can find it here:
https://opengameart.org/content/3-parallax-backgrounds

Other assets are from:  
https://ansimuz.itch.io/gothicvania-cemetery



