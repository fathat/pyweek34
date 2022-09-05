# RED PLANET ATTACKS

## TODO ON THIS DOC:

Need:
- Dialog for Magnus and Ingirid
- Paper level designs
- More fleshed out background for characters.
- Maybe some martian characters (IE, at least a villain)
- Concept art for various ships and people and stuff.
- Lines for civilians

## Summary

You are ACE SPACE PILOT Magnus Thorbergottarsson. You fly a SPACE RESCUE CHOPPER, which is like a regular helicopter, but BETTER. 

The martians are invading earth. You can tell they are martians because of their VERY LARGE SPACE HELMETS. Their motives are unclear, but the president believes that they are jealous of our many great HISTORICAL SITES. Across three exciting levels, in a limited time span, you must rescue as many CIVILIANS as you can while also protecting as many REGULAR BUILDINGS, and more importantly, HISTORICAL BUILDINGS as possible.

You must also support allied troop movements, either by strafing enemy combatants on the ground, or fighting UFO's in the sky.

## Characters

### Magnus Thorbergottarsson

You. An ace pilot. Men want to be you, women want to be with you. What magnificent hair you have. Wait is that a wig?

### Ingirid Hottdottir

Your gunner/copilot and perhaps... something more? The way her hair waves in the wind... wait is that a wig?

### Frothi Meldunsson

Your commander. Talks to you over the radio. Informs you of mission goals, targets, and areas of interest to protect. Most definitely is not wearing a wig, because he's proud to be bald.

## Relationships & Plot Building

### Magnus and Ingirid

Both suffer from alopecia and are also too vain and embarassed to admit it, and thusly wear ostentatious wigs because of their poor taste. Many of their conversations are awkwardly talking about hair styles or feeling out how the other would react if they were to admit to their bald status.

Ideally they are able to both accept each other for who they are by the end of the game and explore their budding romance, but this will depend on how the player reacts to dialogue options that pop up during the mission

### Frothi Meldunsson

A tough son of a bitch, he doesn't take shit from anyone. Frequently doesn't know the common words for things, and angrily demands that the attack "the bad guys with the guns... whatever you call them" or "the floaty sky things. You know what I'm fucking talking about shitheel"

## Historical Buildings

- Giant Ferris Wheel
- Robotic Toilet Museum
- Giant Dinosaur
- Wacky Wavey Flailing Arms Man
- Rock Sculpture of John Madden
- [The Corn Palace](https://www.theactivetimes.com/travel/38-most-bizarre-tourist-attractions-america/slide-6)
- Mustard Museum
- [UFO Information Center](https://www.theactivetimes.com/travel/38-most-bizarre-tourist-attractions-america/slide-16)
- [Worlds Largest Ball of Twine](https://www.theactivetimes.com/travel/38-most-bizarre-tourist-attractions-america/slide-19)
- [Nicolas Cage's Pyramid Tomb](https://www.theactivetimes.com/travel/38-most-bizarre-tourist-attractions-america/slide-20)
- [CarHenge](https://www.theactivetimes.com/travel/38-most-bizarre-tourist-attractions-america/slide-25)

(TODO: Add more/filter)

## SPACE CHOPPER

### Flight Characteristics

Flying a space chopper is HARD WORK, only suited for the MOST SKILLED. You must be able to maintain altitude by constantly boosting and coasting. Controlling momentum is key. 

### Controls

Gamepad

- Left analog x axis controls pitch (either tilt left or tilt right)
- Right analog x axis controls which direction the helicopter is facing (left or right)
- RB shoots machine gun
- LB shoots rockets, nets, and railgun
- D-Pad changes weapon loadout
- A deploys ladder
- Back deploys drops demotivational pamphlets
- Right trigger controls throttle

Keyboard

- WSAD controls throttle and pitch
- QE or arrow keys control pitch
- Space shoots machine gun 
- Ctrl shoots rockets/nets/railgun
- Tab cycles weapons
- Enter drops demotivational packets

### Weapons

- Machine Gun: Good for strafing ground enemies and shooting at weak points on flying saucers and ground monsters. Infinite ammo, but requires a cooldown if shot non-stop. Gun points out from the front of the cockpit, so entire helicopter must be aimed at target. 
- Rockets. Carrying capacity of six. Or something. Must land on helipad to reload
- Rail-gun. Appears level 2. Very fast projectile, very powerful, however the recoil is immense and will fuck up your flight plan.
- Weighted net. Can be used to trap up UFO's or ground vehicles/monsters. Too big to stop civilians or enemy soldiers.
- Demotivational Flyers. Make those martians feel bad about themselves!!!

## Enemies

### UFO

Has a bubble on top with a pilot, and a weak bubble on the bottom for pulling up civilians with the levitation ray. Has jazzy lights in the middle. 

### Scary UFO

Ditto, but also has a Rock Launcher. To throw rocks. Shit hurts when you're in a helicopter man.

### Troop transport UFO

Drops martian soldiers and space dogs

### Martian Soldier

A martian with a gun. Why are their helmets so large?! Their heads aren't even that big you know.

### Martian Pilot

Sometimes jumps out of doomed UFOs. Like a soldier, but weaker. 

### Space Dog

A Dog raised in the hellish conditions of mars and space. Especially vicious, although the helmet required by earth's atmosphere is somewhat of an obstacle.

### Space Cat

Does nothing. Exceptionally useless.

### Mega Martian Walker

Like an AT-ST, except it looks like a martian. 

## Allied NPCs

### Soldier

They have guns and stuff. Sometimes they stay in a place and shoot, and other times the run to other places to shoot more closer.

### Tank

Shoots at the bad guys. Moves veryyyy slowly, sometimes.

(Technical detail: put on background layer so soldiers and tank can occupy same space)

### Civilians

They really want to be saved, and they sure can't do it for themselves. Good thing you're a hero with fantastic hair.

### Earth Dog

All bark, no bite. Boring.

### Anti-Air gun

Can help shoot at UFOs. Also poses a threat to you if you're not careful; either if you attack them and they turn on you, or if you get in the line of fire. 

## Levels

### Level #1 Nebraska/Kansas

The martians start by attacking the most important and more importantly, most interesting, place in the world. Defend the great historical sites and buildings, and rescue civilians.

### Level #2 Generically Asia

Like, kinda Japan, I guess. High tech. Very clean. Same: defend historical sites, rescue civilians, support ground troops.

### Level #3 Mars

We take the fight back to the Red Planet! Less civilian rescue and more crazy offense. This level should feel very cathartic as you get to fuck things up.

## Random ideas

* Enemies and civilians should occasionally have both text bubbles and thought bubbles describing their reaction to the moment
* Magnus and Ingirid should develop their relationship by talking while the action is going on. 
  * It would be funny to require the player to respond to conversation prompts while they're fighting, maybe with a 1/2/3 keypress.
* Dialog should be some sort of robotic speaking thingy (not text to speech, abstract, like in Crying Suns)


## Technical Bullshit

Two paths, must decide.

* Pyglet, glsvg, pymunk. Inkscape and illustrator for art. 

Or

* Panda3d, pymunk, use Blender for level/building design and entity art. TBD: how well does panda handle UI and can you draw 2D stuff easily with it???????