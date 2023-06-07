import replit
import random

player_name = input("What is your name, trainer? ")
print(f"Welcome to the world of Pokemon, {player_name}!")

# List of Pokemon characters
pokemon = ["Pikachu", "Charmander", "Squirtle", "Bulbasaur"]

# Dictionary of locations and corresponding Pokemon
places = {"forest": ["Pikachu", "Charmander"], "lake": ["Squirtle", "Bulbasaur"]}

# Randomly assign a location to player
location = random.choice(list(places.keys()))
print(f"You have been dropped off in a {location}.")

# Get corresponding Pokemon for the location
location_pokemon = places[location]

# Battle a random location Pokemon
opponent = random.choice(location_pokemon)
print(f"A wild {opponent} has appeared!")
print("Battle start...")

# Player's Pokemon stats
player_hp = 100
player_attack = 20

# Opponent's Pokemon stats
opponent_hp = 50
opponent_attack = 10

# Battle loop
while player_hp > 0 and opponent_hp > 0:
  # Player's turn
  player_damage = random.randint(1, player_attack)
  opponent_hp -= player_damage
  print(f"You attacked {opponent} and did {player_damage} damage!")

  if opponent_hp <= 0:
    print(f"{opponent} has fainted!")
    break

  # Opponent's turn
  opponent_damage = random.randint(1, opponent_attack)
  player_hp -= opponent_damage
  print(f"{opponent} attacked you and did {opponent_damage} damage.")

  if player_hp <= 0:
    print("You have fainted. Game over.")
    break

# Update database with player progress
replit.db[player_name] = {"location": location, "pokemon": location_pokemon, "hp": player_hp}
# Create a list of available actions
actions = ["explore", "catch pokemon", "check stats", "heal pokemon", "quit"]

# Create a dictionary of Pokemon stats
stats = {"Pikachu": {"hp": 120, "attack": 30}, "Charmander": {"hp": 130, "attack": 25},
         "Squirtle": {"hp": 150, "attack": 20}, "Bulbasaur": {"hp": 140, "attack": 22}}

# Create a variable to store the player's Pokemon
my_pokemon = None

# Create a loop to allow the player to take actions
while True:
  # Get the player's chosen action
  print("What do you want to do?")
  for i, action in enumerate(actions):
    print(f"{i+1}. {action}")
  choice = int(input()) - 1
  action = actions[choice]

  # Explore the location
  if action == "explore":
    print(f"You are currently in the {location}.")
    if my_pokemon is None:
      print("You don't have a Pokemon yet. Look for one to catch!")
    else:
      print(f"You have a {my_pokemon} with stats hp:{stats[my_pokemon]['hp']} attack:{stats[my_pokemon]['attack']}")

  # Attempt to catch a Pokemon
  elif action == "catch pokemon":
    if my_pokemon is not None:
      print(f"You already have a {my_pokemon}.")
    else:
      if location in places.keys():
        wild_pokemon = random.choice(places[location])
        print(f"A wild {wild_pokemon} appeared!")
        catch_chance = random.randint(1, 10)
        if catch_chance < 5:
          print(f"{wild_pokemon} escaped! Better luck next time.")
        else:
          print(f"You caught {wild_pokemon}!")
          my_pokemon = wild_pokemon
      else:
        print("There are no Pokemon to catch here.")

  # Check the player's Pokemon stats
  elif action == "check stats":
    if my_pokemon is None:
      print("You don't have a Pokemon yet. Look for one to catch!")
    else:
      print(f"You have a {my_pokemon} with stats hp:{stats[my_pokemon]['hp']} attack:{stats[my_pokemon]['attack']}")

  # Heal the player's Pokemon
  elif action == "heal pokemon":
    if my_pokemon is None:
      print("You don't have a Pokemon yet. Look for one to catch!")
    else:
      print(f"You healed your {my_pokemon} to full health!")
      stats[my_pokemon]['hp'] = 100

  # Quit the game
  elif action == "quit":
    print("Thanks for playing!")
    break

# Create a dictionary of gym leaders and their Pokemon
gym_leaders = {"Brock": ["Geodude", "Onix"], "Misty": ["Staryu", "Starmie"], "Lt. Surge": ["Voltorb", "Pikachu", "Raichu"]}

# Create a variable to keep track of defeated gym leaders
defeated_leaders = []

# Create a loop to allow the player to challenge gym leaders
while True:
  # Choose a random gym leader who has not yet been defeated
  available_leaders = [leader for leader in gym_leaders.keys() if leader not in defeated_leaders]
  if len(available_leaders) == 0:
    break
  leader = random.choice(available_leaders)

  # Announce the gym leader and their Pokemon
  print(f"You have encountered gym leader {leader}!")
  leader_pokemon = gym_leaders[leader]
  print(f"{leader} has the following Pokemon: {', '.join(leader_pokemon)}.")

  # Determine if the player's Pokemon can defeat the gym leader
  if my_pokemon is not None:
    player_hp = stats[my_pokemon]['hp']
    player_attack = stats[my_pokemon]['attack']
    for pokemon in leader_pokemon:
      leader_hp = stats[pokemon]['hp']
      leader_attack = stats[pokemon]['attack']
      while player_hp > 0 and leader_hp > 0:
        # Player's turn
        player_damage = random.randint(1, player_attack)
        leader_hp -= player_damage
        print(f"You attacked {pokemon} and did {player_damage} damage!")
        if leader_hp <= 0:
          print(f"{pokemon} has fainted!")
          break
        # Leader's turn
        leader_damage = random.randint(1, leader_attack)
        player_hp -= leader_damage
        print(f"{pokemon} attacked you and did {leader_damage} damage.")
        if player_hp <= 0:
          print("You have fainted. Game over.")
          break
    # The player has won!
    if player_hp > 0:
      print(f"Congratulations! You have defeated gym leader {leader}.")
      defeated_leaders.append(leader)
  else:
    print("You don't have a Pokemon yet. Look for one to catch!")

# The player has defeated all gym leaders!
print("You have defeated all gym leaders and become the champion of the Pokemon league!")