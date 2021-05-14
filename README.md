
# Simple Python game with AI-playing it

### Background
This game was made for course <strong>Lisää kurssin nimi </strong> in Haaga-Helia University of Applied Sciences.  
The purpose of this repository is demonstrate a simple game and how to implement NEAT-algorithm with Python. 

### Used packages
- pygame (for creating the game)
- neat-python
- pickle (for saving trained model locally)

### Example video
Before installing you can see the game in action in www.youtube.com

### Installation
```
 $ luo enviroment
 $ asenna requiremens.txt
 $ kuinka ajaa ilman ai, kuinka ajaa ai:n kanssa ja kuinka ajaa esimerkki
```

### Usage

You can use this repository for running a pretrained AI that was run for over 10000 generations. You can also choose to try this game for yourself. This is in file single_player.py. 

#### Single player usage
```
$ python single_player.py
```

#### Checking out pretrained AI
```
$ python main.py run_trained
```

#### Training a new model / AI
First argument is `train` and second is the number of generations you want.
```
$ python main.py train 10000
```

### TODO
Currently the codebase and assets are a mixture of english and finnish language. My intention is that I will change the language to english, but unfortunately that has proven to be some what slow, and my progress in getting this thing to work properly has been slow.

### Acknowledgements
Kenneth O. Stanley and Risto Miikkulainen for publishing the paper on 'Evolving Neural Networks through Augmenting Topologies'  
CodeBullet for providing humorous videos about creating and figuring out how to operate AI's in different scenarios.  
<strong> Googlaa kuka teki noi assetit </strong>


