
# Simple Python game with AI-playing it

### Background
This game was made for course Software Development Technologies in Haaga-Helia University of Applied Sciences.  
This repository demonstrates a simple game and how to implement NEAT-algorithm with Python.

### Objective of the game
During the development process of the AI singleplayer version and AI-version went to different directions.
Currently the singleplayer version is a bit more spaghetti (AI version is also spaghetti, but not so al-dente).

Also the language in the singleplayer version is finnish and I cannot be bothered to fix it all. 

In the AI-version the objective is to survive as long as possible. You get points (and AI gets fitness) based on 
the time you've been alive.

In the singleplayer version you get points by shooting the enemies, your goal is to get as many points as possible.

The speed of the game gradually increases in both versions.

### Inputs and outputs

I have defined the following inputs for NEAT-activation:
- speed of the game
- distance between enemy and hero
- Y-axis location of enemy and hero  

There is only one output currently.
The AI must decide to jump or not.

### Used packages
- pygame (for creating the game)
- neat-python
- pickle (for saving trained model locally)
- argparse (handling arguments in commandline)

### Example video
Before installing, you can see the game in action in www.youtube.com

### Installation
I recommend that you create a separate environment for this.
```
 $ venv venv sbin activate jtaoin
 $ git clone https://github.com/jussihayha/python-neat-ai
 $ pip install -r requirements.txt

```

### Usage

You can use this repository for running a pretrained AI that was run for 1000 generations.  
You can also choose to try this game for yourself. This is in file single_player.py. 

#### Single player usage
Hero jumps from `spacebar` and shoots from `z` -key.
```
$ python single_player.py
```

#### Checking out pretrained AI
Use switch `--replay` together with a .pkl filename you want to replay.
Replays the best genome in a previous run. 
```
$ python main.py --replay <filename>
```

#### Training a new model / AI
Use switch `--train` together with an integer number preferably over 10.
After training is over it creates a file called winner-10.pkl (integer value of the filename changes based on your parameter).
```
$ python main.py --train 1000
```

### TODO
- continue translating finnish to english
- reconfigure and analyze inputs for neat activation
- work on progressing the configuration file
- add shooting and stomping capabilities in the AI-version

### Acknowledgements
Kenneth O. Stanley and Risto Miikkulainen for publishing the paper on 'Evolving Neural Networks through Augmenting Topologies'  
CodeBullet for providing humorous videos about creating and figuring out how to operate AI's in different scenarios.

I did not make the assets myself. 
The used background image uses GPL 3.0 and you can find it here:
https://opengameart.org/content/3-parallax-backgrounds

Other assets are from:  
https://ansimuz.itch.io/gothicvania-cemetery



