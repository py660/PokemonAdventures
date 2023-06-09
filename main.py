import os
import random
import shutil
import sys
import threading
from time import sleep
from ascii_magic import AsciiArt
from getkey import getkey, keys
from replit import clear, db
from termcolor import colored
from color import Foreground
from style import Style

# DON'T CHANGE!!!!!
authors = [
  "Idkwhttph",
  "SalladShooter",
  "python660",
  "QwertyQwerty88",
  "not-ethan",
  "ParanormalCoder"
]

##### ALL DEBUG FEATURES MUST CHECK debug == True #####
# this is to disable people from directly accessing dev tools.
debug = os.environ["REPL_OWNER"] in authors


if not db.get("Intro_once") and debug:
  skipintro = (input(f"{Foreground.RED}Skip intro (debug)?{Foreground.RESET}") + "n")[0].lower() == "y"


def printInMiddle(text, columns=shutil.get_terminal_size().columns):
  # Get the current width of the console
  console_width = columns

  # Calculate the padding for the left side
  padding = (console_width - len(text)) // 2 + 5

  # Print the padded text
  print(' ' * padding + text)


def write(string: str, speed: int=.05) -> None:
  for char in string:
    sys.stdout.write(char)
    sys.stdout.flush()
    sleep(speed)


def button(string: str) -> str:
  return f"[{Foreground.BLUE}{string}{Foreground.RESET}]"


def enter_to_continue():
  write(f"{Style.BOLD}Press {button('ENTER')} to continue{Style.RESET}\n")
  input()
  clear()


def options(prompt: str, options: list[str]) -> tuple[int, str, int]:
  while True:
    if prompt:
      write(prompt + "\n")
    for i in range(len(options)):
      write(f"{button(str(i + 1))} {options[i]}\n", speed=0)
    picked = input()
    if picked.isdigit() and 0 < int(picked) <= len(options):
      picked = int(picked)
      break
    else:
      print(f"{Foreground.RED}Invalid input.{Foreground.RESET}")
      enter_to_continue()
  return picked - 1, options[picked - 1], picked


gen_pokemon_cnt = 0


global pokemon_slot,pokemon
pokemon = {
  "Pikachu": {
    "abilities": "Electro Ball",
    "special_ability": {"Thunder Wave": "A 50/50 Chance to paralyze a pokemon"},
    "damage": 50,
    "enemy_pokemon_paralyze": False,
    "paralyze_chance": 0,
    "health": 145,
    "max-health": 145,
    "exp": 1
  },
  "Charmander": {
    "abilities": "Ember",
    "special_ability": {"Smokescreen": "Can lower the opponent's accuracy"},
    "damage": 50,
    "enemy_pokemon_paralyze": False,
    "paralyze_chance": 0,
    "health": 145,
    "max-health": 145,
    "exp": 1
  },
  "Squirtle": {
    "abilities": "Water Gun",
    "special_ability": {"Withdraw": "Can raise its defense"},
    "damage": 50,
    "enemy_pokemon_paralyze": False,
    "paralyze_chance": 0,
    "health": 140,
    "max-health": 140,
    "exp": 1
  },
  "Bulbasaur": {
    "abilities": "Tackle",
    "special_ability": {},
    "damage": 40,
    "enemy_pokemon_paralyze": False,
    "paralyze_chance": 0,
    "health": 120,
    "max-health": 120,
    "exp": 1
  },
  "Jigglypuff": {
    "abilities": "Tackle",
    "special_ability": {},
    "damage": 40,
    "enemy_pokemon_paralyze": False,
    "paralyze_chance": 0,
    "health": 120,
    "max-health": 120,
    "exp": 1
  },
  "Psyduck": {
    "abilities": "Tackle",
    "special_ability": {},
    "damage": 40,
    "enemy_pokemon_paralyze": False,
    "paralyze_chance": 0,
    "health": 120,
    "max-health": 120,
    "exp": 1
  },
  "Geodude": {
    "abilities": "Tackle",
    "special_ability": {},
    "damage": 40,
    "enemy_pokemon_paralyze": False,
    "paralyze_chance": 0,
    "health": 120,
    "max-health": 120,
    "exp": 1
  },
  "Snorlax": {
    "abilities": "Tackle",
    "special_ability": {},
    "damage": 40,
    "enemy_pokemon_paralyze": False,
    "paralyze_chance": 0,
    "health": 120,
    "max-health": 120,
    "exp": 1
  },
  "Magikarp": {
    "abilities": "Tackle",
    "special_ability": {},
    "damage": 40,
    "enemy_pokemon_paralyze": False,
    "paralyze_chance": 0,
    "health": 120,
    "max-health": 120,
    "exp": 1
  }
}

db["pokemon_exp"] = db.get("pokemon_exp", dict())
db["pokemon_level"] = db.get("pokemon_level", dict())
db["inventory"] = db.get("inventory", {"Pokeballs": 50, "Potions": 2})
db["your_pokemon"] = db.get("your_pokemon")
if (not db["your_pokemon"]) and ("Intro_once" in db.keys()):
  del db["Intro_once"]
db["pokedex"] = db.get("pokedex")

# Create a variable to store the player's active Pokemon's index
active_pokemon_index = 0
pokemon_slot = ["", "", "", ""]
def battle(active_pokemon_index):
  gen_pokemon_cnt = 0
  # Check if the player has any Pokemon in their slots
  if all(slot == "" for slot in pokemon_slot):
    print("You do not have any Pokemon in your slots!")
  else:
    while True:
      # Check if all of the player's Pokemon have fainted
      if not any(slot != "" for slot in pokemon_slot):
        print("All your Pokemon have fainted!")
        break
      # Generate an enemy Pokemon with a random rarity
      if gen_pokemon_cnt == 0:
        
        # BEFORE ENTERING BATTLE LOOP, GET ACTIVE POKEMON:
        try:
          active_pokemon # no need to define an unused variable
        except UnboundLocalError as e:
          # Select your pokemo
          active_pokemon = "placeholderPokemon"  # Initialize to empty string  
          clear()
          pkchoice = options(f"{Style.BOLD}Please select your Pokémon:", pokemon_slot)[0]
          clear()
          active_pokemon = pokemon_slot[pkchoice]
           
        enemy_tier = random.randint(1, 100)
        if enemy_tier == 1:
          #enemy_pokemon = random.choice(['Mew', 'Mewtwo'])
          enemy_pokemon = random.choice([x for x in pokemon if x not in pokemon_slot]) #TMP
          rarity = "yellow"
        elif 2 <= enemy_tier <= 14:
          #enemy_pokemon = random.choice(pokemon + ['Lapras', 'Dragonite'])
          enemy_pokemon = random.choice([x for x in pokemon if x not in pokemon_slot]) #TMP
          rarity = "blue"
        elif 15 <= enemy_tier <= 49:
          #enemy_pokemon = random.choice(pokemon)
          enemy_pokemon = random.choice([x for x in pokemon if x not in pokemon_slot]) #TMP
          rarity = "green"
        else:
          #enemy_pokemon = random.choice(['Rattata', 'Spinarak', 'Pidgey', 'Zigzagoon'])
          enemy_pokemon = random.choice([x for x in pokemon if x not in pokemon_slot]) #TMP
          rarity = "white"
        # Retrieve the stats for the enemy Pokemon from the stats dictionary
        enemy_stats = pokemon.get(enemy_pokemon, {"abilities": "Tackle", "special_ability": {}, "damage": 40, "enemy_pokemon_paralyze": False, "paralyze_chance": 0,'health': 120}) # please add hp and retrieve the stats for the hp to work
        enemy_stats["level"] = random.sample(range(db["pokemon_level"][active_pokemon] - 3, db["pokemon_level"][active_pokemon] + 2), 1, counts=(2, 3, 6, 4, 1))
        clear()
        # Initialize the player's choice to an invalid value
        gen_pokemon_cnt = 1
        
              
      pokemon_hp = dict([(pk, pokemon[pk]["health"]) for pk in pokemon.keys()])
      max_hp = dict([(pk, pokemon[pk]["max-health"]) for pk in pokemon.keys()])
      #active_pokemon_hp = pokemon_hp[active_pokemon]
      enemy_hp = enemy_stats["health"]
      # Enter the battle turn loop
      clear()
      # Print the player's active Pokemon's name and HP
      print(f"{Style.BOLD}{Foreground.RESET}Your active Pokemon:")
      print(f"{Style.BOLD}{active_pokemon} - HP: {pokemon_hp[active_pokemon]}{Style.RESET}")
      print(f"{Style.RESET}------------------------")
      print(f"{Style.BOLD}{Foreground.RESET}Enemy Pokemon:")
      #print(rarity)
      print(f"{Style.BOLD}{colored(enemy_pokemon, rarity, attrs=['blink'])}{Style.BOLD} - HP: {enemy_hp}{Style.RESET}")
      print(f"{Style.RESET}------------------------")
      # Prompt the player for their action
      actions = [
        f"{Foreground.RED}Attack{Foreground.RESET}",
        f"Use {Foreground.MAGENTA}Potion{Foreground.RESET}",
        "Switch Pokémon",
        "Run away"
      ]
      choice = options(f"{Style.BOLD}What do you want to do?", actions)
      if choice == 0:
        # Resolve the player's attack
        player_damage = pokemon[active_pokemon]['damage']
        print(f'You attack the {Style.BOLD}{colored(enemy_pokemon, rarity, attrs=["blink"])}{Style.RESET} with {Style.BOLD}{pokemon[active_pokemon]["abilities"]}{Style.RESET} for {Style.BOLD}{Foreground.RED}{player_damage} damage!{Foreground.RESET}{Style.RESET}')
        enemy_hp -= player_damage
        sleep(1.5)
      elif choice == 1:
        # Resolve the player's potion use
        print('Using a potion to heal your Pokémon...')
        sleep(2)
        potion_amount = db['inventory']['Potions']
        if potion_amount > 0:
        # Heal the player's active Pokemon by 20 HP (or to their maximum HP if they are already at or above 80 HP)
          pokemon_hp[active_pokemon] = min(pokemon_hp[active_pokemon] + 20, max_hp[active_pokemon])
          print(f'{active_pokemon} healed 20 HP!')
          db['inventory']['Potions'] -= 1
          sleep(1.5)
        else:
          # The player doesn't have any Potions left...
          print('You do not have any Potions left!')
          enter_to_continue()
          continue
      elif choice == 2:
        # Resolve the player's Pokemon switch
        print(f'{Style.BOLD}{Foreground.RESET}Please select your Pokemon:')
        for i, slot in enumerate(pokemon_slot):
          #print(pokemon_slot)
          if slot:
            print(f'[{i+1}] {slot} - HP: {pokemon_hp[slot]}')
            # YEE HAW INDENTATION ERROR FIXED
        try:
          new_active_pokemon_index = int(input()) - 1
          if new_active_pokemon_index < 0 or new_active_pokemon_index >= len(pokemon_slot):
          # The player entered an invalid index...
            print('Invalid input!')
            enter_to_continue()
          else:
            new_active_pokemon = pokemon_slot[new_active_pokemon_index]
            #if new_active_pokemon == active_pokemon:
            ## The player selected their current active Pokemon...
            #  print('That is already your active Pokemon!')
            
            # #### Just let the player waste time
            
            if pokemon_hp[new_active_pokemon] <= 0:
            # The player's selected Pokemon has fainted...
              print(f'{new_active_pokemon} has fainted and cannot battle!')
            else:
            # Switch the player's active Pokemon
              print(f'Go, {new_active_pokemon}!')
              active_pokemon = new_active_pokemon
              #active_pokemon_hp = pokemon_hp[active_pokemon]
              sleep(1)
              continue
        except Exception:
          print("Invalid input!")
          enter_to_continue()
      elif choice == 3:
        # The player ran away from the battle
        print('You ran away from the battle!')
        enter_to_continue()
        return
      
      if enemy_hp <= 0:
        # The player defeated the enemy Pokemon!
          print(f'{Style.BOLD}{colored(enemy_pokemon, rarity, attrs=["blink"])}{Style.RESET} has fainted!')
          sleep(2)
          clear()
          # Award the player money and experience points
          add_money(random.randint(5, 20))
          add_exp(random.randint(10, 30))
          print(f'You defeated a wild {Style.BOLD}{colored(enemy_pokemon, rarity, attrs = ["blink"])}{Foreground.RESET} and earned {Style.BOLD}{Foreground.GREEN}{db["$kash"]} money {Foreground.RESET}and {Style.BOLD}{Foreground.YELLOW}{db["exp"]} experience points{Foreground.RESET}!')
          enter_to_continue()
          break
          
          # Check if the player's active Pokemon leveled up
          active_pokemon_exp = db["pokemon_exp"][active_pokemon]
          active_pokemon_level = db["pokemon_level"][active_pokemon]
          active_pokemon_max_hp = max_hp[active_pokemon]
          exp_needed = 50 + ((active_pokemon_level - 1) * 25)
          if active_pokemon_exp + db["pokemon_exp"][active_pokemon] >= exp_needed:
          # The player's active Pokemon leveled up!
            db["pokemon_exp"][active_pokemon] += 1
            active_pokemon_level += 1
            db["pokemon_exp"][active_pokemon] = min(active_pokemon_exp + db["pokemon_exp"][active_pokemon] - exp_needed, exp_needed)
            active_pokemon_exp = [active_pokemon]
            max_hp_increase = random.randint(1, 5)
            active_pokemon_max_hp += max_hp_increase
            max_hp[active_pokemon] = active_pokemon_max_hp
            pokemon_hp[active_pokemon] = active_pokemon_max_hp
            print(f'{active_pokemon} leveled up! Its level is now {Foreground.BLUE}{Style.BOLD}{active_pokemon_level}{Foreground.RESET}!')
          # Check if the player has any Pokeballs
          pokeball_amount = db['inventory']['Pokeball']
          if pokeball_amount > 0:
          # The player has at least one Pokeball, so give them a chance to catch the enemy Pokemon
            catch_chance = 0.5 if rarity == 'Foreground.YELLOW' or rarity == 'Foreground.BLUE' else 0.3
            if random.random() < catch_chance:
              print(f"Congratulations! You caught a wild {enemy_pokemon}!")
              pokemon_slot[pokemon_slot.index('')] = enemy_pokemon
              pokemon_hp[enemy_pokemon] = enemy_stats['health']
              db["pokemon_exp"][enemy_pokemon] = 0
              db["pokemon_level"][enemy_pokemon] = enemy_stats['level']
              db['inventory']['Pokeball'] -= 1
          else:
            print(f"{Style.BOLD}{colored(enemy_pokemon, rarity, attrs = ['blink'])}{Foreground.RESET} broke free!")
            sleep(2)
      else:
        # The enemy Pokemon is still alive...
          print(f'{Style.BOLD}{Foreground.RESET}The {colored(enemy_pokemon, rarity, attrs=["blink"])} attacks with {enemy_stats["abilities"]}')
          sleep(1)
          print(f'{Foreground.RESET}The {Style.BOLD}{colored(enemy_pokemon, rarity, attrs=["blink"])}{Foreground.RESET} dealt {Style.BOLD}{Foreground.RED}{enemy_stats["damage"]} damage!{Foreground.RESET}')
          pokemon_hp[active_pokemon] -= enemy_stats["damage"]
          sleep(2)
          clear()
          # Check if the player's active Pokemon was paralyzed by the enemy Pokemon's special ability
          if active_pokemon in enemy_stats['special_ability'] and not enemy_stats['enemy_pokemon_paralyze']:
            if random.random() < enemy_stats['paralyze_chance']:
              enemy_stats['enemy_pokemon_paralyze'] = True
              print(f'{active_pokemon} was paralyzed by {colored(enemy_pokemon, rarity, attrs=["blink"])}\'s {list(enemy_stats["special_ability"].keys())[0]}!')
            sleep(2)

  return


def catch_pokemon(area): # parameter will be used later.
  tier = random.randint(1, 100)
  #print('tier =', tier)
  if tier == 1:
    pokemon = random.choice('mew','mewtwo')  # legendary
    rarity = 'Foreground.YELLOW'
    #print('rarity =', rarity)
    battle()
    
  elif 2 <= tier <= 14:
    pokemon = random.choice(pokemon)# + ["Lapras", "Dragonite"])  # rare
    rarity = 'Foreground.BLUE'
    #print('rarity =', rarity)
    battle()
  elif 15 <= tier <= 49:
    pokemon = random.choice(pokemon) # uncommon
    rarity = 'Foreground.GREEN'
    #print('rarity =', rarity)
    battle()
  else:
    pokemon = random.choice(pokemon)#["Rattata", "Spinarak", "Pidgey", "Zigzagoon"])# common
    rarity = 'Foreground.RESET'
    #print('rarity =', rarity)
    battle()
  if not all(slot == '' for slot in pokemon_slot):
    print(f"Congratulations! You caught a {colored(pokemon, rarity, attrs=['blink'])} in Route {area}.")


def heal_pokemon():
  """Heal all of the player's Pokemon"""
  for pokemon_name in pokemon_slot:
    if pokemon_name:
      # Heal the Pokemon based on their max HP
      max_hp = db.get(f"{pokemon_name}_max_hp")
      db[f"{pokemon_name}_current_hp"] = max_hp
  print(f"{Style.BOLD}Your Pokémon have been fully healed!{Foreground.RESET}")
    
# Pokeball option
# Set starting amount of money
try:
  monnae = db['$kash']
  expehrienssssse = db['exp']
except:
  db['$kash'] = 0
  db['exp'] = 0

# Add money
def add_money(amount):
  current_money = db.get('$kash')
  current_money += amount
  db['$kash'] = current_money

# Subtract money
def subtract_money(amount):
  current_money = db.get('$kash')
  current_money -= amount
  db['$kash'] = current_money

def add_exp(amount):
  current_exp = db.get('exp')
  current_exp += amount
  db['exp'] = current_exp

# Subtract money
def subtract_exp(amount):
  current_exp = db.get('exp')
  current_exp -= amount
  db['exp'] = current_exp

# Buy Pokeballs
def buy_pokeballs():
  pokeball_cost = 10
  current_money = db.get('$kash')
  num_pokeballs_to_buy = int(input(f"Pokéballs cost {pokeball_cost} each. How many do you want to buy? (You have {Foreground.GREEN}{Style.BOLD}{current_money} $kash {Foreground.RESET})"))
  
  total_cost = num_pokeballs_to_buy * pokeball_cost
  
  if current_money < total_cost:
    print("You don't have enough $kash to buy that many Pokeballs.")
  else:
    subtract_money(total_cost)
    current_pokeball_inventory = db.get('Pokeball')
    db['Pokeball'] = current_pokeball_inventory + num_pokeballs_to_buy
    print(f"You bought {Style.BOLD}{Foreground.RED}{num_pokeballs_to_buy} Pokéballs{Foreground.RESET}!")



try:
  intro_once_backup = db['Intro_once']
    #wait a minute, why am I doing this?
  pokemon_slot = db["pokemon_slot"]
except KeyError:
  if not skipintro:
    console_width = min(shutil.get_terminal_size().columns, 76)
    my_art = AsciiArt.from_image('logo/pokeball.png')
    my_art.to_terminal(columns=console_width)
  
    #my_art2 = AsciiArt.from_image('logo/pka.jpeg')
    #my_art2.to_terminal(columns=console_width)
    write(f'{Style.BOLD}Welcome to {Foreground.BLUE}Pokémon Adventures{Foreground.RESET}! This is a text-based game where you can {Foreground.RED}battle{Foreground.RESET} with other Pokémon and Pokémon Trainers along the way! I hope you will enjoy the game! \n\nMade by:{Foreground.RESET}\n');
    for author in authors:
      write(f' - {author}\n')
  
  enter_to_continue()
  write(f"{Style.BOLD}In this world, you use Pokémon to battle! Go ahead and pick one out.")
  print("\n")
  print("Select One:")
  print(f"{Style.BOLD} {button('1')} {Foreground.YELLOW}Pikachu{Foreground.RESET}")
  print(f"{Style.BOLD} {button('2')} {Foreground.BLUE}Squirtle{Foreground.RESET}")
  print(f"{Style.BOLD} {button('3')} {Foreground.GREEN}Bulbasaur{Foreground.RESET}")
  # Enumerate pokemon #im back
  print('\n')
  selection = "0"
  while (selection.isdigit() and int(selection) not in tuple(range(1, 4))) or not selection.isdigit():
    selection = input("Enter your selection: ")
  selection = int(selection)
  db['your_pokemon'] = ['easter egg #1', 'Pikachu', 'Squirtle', 'Bulbasaur'][selection]
  print(f"You chose: {[Foreground.RED, Foreground.YELLOW, Foreground.BLUE, Foreground.GREEN][selection]}{db['your_pokemon']}{Foreground.RESET}.")
  print()
  enter_to_continue()
  db['Intro_once'] = 1
  pokemon_slot[0] = db["your_pokemon"]
  db["pokemon_exp"][db["your_pokemon"]] = 0
  db["pokemon_level"][db["your_pokemon"]] = 5
  db["pokemon_slot"] = pokemon_slot
  #Defines pokemon_slot in db for future use


console_width = min(shutil.get_terminal_size().columns, 76)
my_art = AsciiArt.from_image('logo/pokeball.png')
my_art.to_terminal(columns=console_width)

print("-" * console_width)
printInMiddle(f"{Foreground.BLUE}Pokémon_adventures.exe{Foreground.RESET}", columns=console_width)
print("Made by:")
for author in authors:
  match author: 
    case "Idkwhttph":
      print(f"- {Foreground.BLUE}@{author}{Foreground.RESET}")
    case "QwertyQwerty88":
      print(f"- {Foreground.MAGENTA}@{author}{Foreground.RESET}")
    case "python660":
      print(f"- {Foreground.BLUE}@{author}{Foreground.RESET}")
    case _:
      print(f"- @{author}")
print()
enter_to_continue()


while True:
  menu = [
    "Your Pokémon",
    "The Pokédex",
    "Travel",
    f"{Foreground.BLUE}Catch Pokémon{Foreground.RESET}",
    f"{Foreground.RED}Quit{Foreground.RESET}"
  ]
  if debug:
    menu.append(f"{Foreground.RED}SHOW DEVTOOLS{Foreground.RESET}")
  solution_get_input = options("", menu)[0]
    
  if solution_get_input == 0:
    print(f'{Style.BOLD}Your pokemon:')
    print(db['your_pokemon'])
    enter_to_continue()
  elif solution_get_input == 1:
    print('The Pokédex')
    print('Joe Mama - Ultimate Power')
    enter_to_continue()
  elif solution_get_input == 2:
    print('Travelling to Route 1')
    enter_to_continue()
  elif solution_get_input == 3:
    battle(active_pokemon_index)
  elif solution_get_input == 4:
    exit()
  elif solution_get_input == 5 and debug:
    debug_options = [
      "PRINT DB",
      "CLEAR DB",
      "GET DB URL",
      "EXECUTE CODE"
    ]
    solution_get_input = options(f"{Foreground.RED}{Style.BOLD}--- DEVTOOLS ---{Foreground.RESET}", debug_options)[0]
    
    if solution_get_input == 0:
      print(repr(dict(db)))
      enter_to_continue()
    elif solution_get_input == 1:
      for i in db.keys():
        del db[i]
      print(f"Database cleared. Press {button('ENTER')} to restart.")
      enter_to_continue()
      exit(0)
    elif solution_get_input == 2:
      print(os.environ.get("REPLIT_DB_URL", "Invalid URL"))
      enter_to_continue()
    elif solution_get_input == 3:
      print("type 'exit()' to exit debug console")
      try:
        while True:
          exec(input(">> "))
      except:
        print("Exited debug console")
        enter_to_continue()
