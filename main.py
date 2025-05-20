import pygame, random, math, pickle, sys
from pygame.locals import *
from map import *
from timers import Timer
from time import sleep

RESOLUTION = WIDTH, HEIGHT = 350, 350
FPS = 20

sys.setrecursionlimit(2000)

print("Initializing Pygame...")

pygame.init()
pygame.mixer.init(44100, -16, 1, 2048)
pygame.mixer.Sound
display = pygame.display.set_mode(RESOLUTION, flags = pygame.SCALED | pygame.RESIZABLE)
screen = pygame.surface.Surface(RESOLUTION)
pygame.display.set_caption('Retraich')
clock = pygame.time.Clock()

retrofont = pygame.font.Font('Fonts/retroville.ttf', 20)
retrofontmedium = pygame.font.Font('Fonts/retroville.ttf', 16)
retrofontsmall = pygame.font.Font('Fonts/retroville.ttf', 12)
retrofonttiny = pygame.font.Font('Fonts/retroville.ttf', 10)

joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

def blit_text(text):
  display.fill("Black")
  display.blit(retrofonttiny.render(text, False, "Yellow"), (0, 0))
  pygame.display.flip()

blit_text("Loading Sound Effects...")
sleep(0.02)

sword_sfx = pygame.mixer.Sound("Sounds/sfx/sword.wav")
bow_sfx = pygame.mixer.Sound("Sounds/sfx/bow.wav")
hit_sfx = pygame.mixer.Sound("Sounds/sfx/hit.wav")
hurt_sfx = pygame.mixer.Sound("Sounds/sfx/hurt.wav")
break_sfx = pygame.mixer.Sound("Sounds/sfx/break.wav")
kill_sfx = pygame.mixer.Sound("Sounds/sfx/kill.wav")
scroll_sfx = pygame.mixer.Sound("Sounds/sfx/scroll.wav")
collect_sfx = pygame.mixer.Sound("Sounds/sfx/collect.wav")
collect2_sfx = pygame.mixer.Sound("Sounds/sfx/collect2.wav")
collect3_sfx = pygame.mixer.Sound("Sounds/sfx/collect3.wav")
collect4_sfx = pygame.mixer.Sound("Sounds/sfx/collect4.wav")
grappling_sfx = pygame.mixer.Sound("Sounds/sfx/grappling.wav")
grapple_sfx = pygame.mixer.Sound("Sounds/sfx/grapple.wav")
change_by_sfx = pygame.mixer.Sound("Sounds/sfx/change by.wav")
one_up_sfx = pygame.mixer.Sound("Sounds/sfx/1 up.wav")
secret_sfx = pygame.mixer.Sound("Sounds/sfx/secret.wav")
click_sfx = pygame.mixer.Sound("Sounds/sfx/click.wav")
select_sfx = pygame.mixer.Sound("Sounds/sfx/select.wav")
select2_sfx = pygame.mixer.Sound("Sounds/sfx/blip2.wav")
blip_sfx = pygame.mixer.Sound("Sounds/sfx/blip.wav")
beep_sfx = pygame.mixer.Sound("Sounds/sfx/beep.wav")

blit_text("Loading Assets...")
sleep(0.02)

icon = pygame.image.load("Assets/icon.png").convert_alpha()
pygame.display.set_icon(icon)

clouds = pygame.image.load("Assets/clouds.png").convert_alpha()
logo = pygame.image.load("Assets/logo.png").convert_alpha()
manzara = pygame.image.load("Assets/manzara.png").convert_alpha()
manzara2 = pygame.image.load("Assets/manzara2.png").convert_alpha()
manzara3 = pygame.image.load("Assets/manzara3.png").convert_alpha()
blue_line = pygame.image.load("Assets/blue line.png").convert_alpha()
tuff = pygame.image.load("Assets/tuff/walkback0.png").convert_alpha()
heart = pygame.image.load("Assets/heart.png").convert_alpha()

texts = [
  "     A New Story of Tuff~",
  " ",
  "                                A story of a boy,~",
  "                                   Tuff, in search~",
  "                        of vast riches which~",
  "                         fell from the sky as~",
  "                                   pieces of stars~",
  " ", 
  " "," ",
  "Push the START button                 ",
  " ", " ", " ", " ",
  "You're out to seize all                  ",
  " ",
  "of the lost pieces of...                  ",
  " ",
  "... the RENK GEMS.                             ",
  " ", " ", " ",
  "          They're scattered around",
  " ",
  "                        the world filled with",
  " ",
  "                              vicious monsters.",
  " ", " ",
  "To stop them, you need to ...       ",
  " ",
  "...unite all 4 Renk gems,                  ",
  " ",
  "and take down Valmore who          ",
  " ",
  "wreaked havoc on tree country",
  " ",
  "Only you can save it.                        ",
  " ", " ", " ", " ", " ",
  "Retraich TM - by Tunari-",
  "No rights reserved!-"
]

texts_end = [
  " ", " ",
  "This ends the story", "of Retraich.",
  " ", " ", " ",
  "Finally, no more evil lurking",
  "in the dark",
  "Peace and harmony returns",
  "to the nation.",
  " ", " ", " ", " ", " ", " ", " ", " ",
  "Game created by Kaan, Tunari-",
  " ", " ", " ", " ",
  "Another quest awaits in Retraich 2-",
  "Push START button",
]

def maxint(int, max):
  if int > max: return max
  else: return int

def minint(int, min):
  if int < min: return min
  else: return int

game_over_controller_delay = Timer()

blit_text("Loading Memory Space - JSON Serializer ReadableBuffer...")
sleep(0.13)

saves = {
  "save1": {
    "save": "save1", "name": "N E W   S A V E",
    "x": WIDTH/2, "y": WIDTH/2, "position": [0, 0], "minimaps": [0, 0], "direction": "front",
    "hearts": 5, "wealth": 0, "weapon": "sword", "items": ["sword"], "arrows": 3, "theme": "Legends of the Renk Gems", "Immobilize": False,
    "actors": [], "past_actors": [], "renks": {"renk 1": False, "renk 2": False, "renk 3": False, "renk 4": False},
  },
  #"save1": {
  #  "save": "save1", "name": "N E W   S A V E",
  #  "x": WIDTH/2, "y": WIDTH/2, "position": [0, 0], "minimaps": [0, 0], "direction": "front",
  #  "hearts": 4, "wealth": 26, "weapon": "sword", "items": ["sword", "bow", "grapple hook", "healing potion", "adham sword"], "arrows": 72, "theme": "Sword of Adham", "Immobilize": False,
  #  "actors": [], "past_actors": [], "renks": {"renk 1": True, "renk 2": True, "renk 3": True, "renk 4": False},
  #},
  "save2": {
    "save": "save2", "name": "N E W   S A V E",
    "x": WIDTH/2, "y": WIDTH/2, "position": [0, 0], "minimaps": [0, 0], "direction": "front",
    "hearts": 5, "wealth": 0, "weapon": "sword", "items": ["sword"], "arrows": 3, "theme": "Legends of the Renk Gems", "Immobilize": False,
    "actors": [], "past_actors": [], "renks": {"renk 1": False, "renk 2": False, "renk 3": False, "renk 4": False},
  },
  "save3": {
    "save": "save3", "name": "N E W   S A V E",
    "x": WIDTH/2, "y": WIDTH/2, "position": [0, 0], "minimaps": [0, 0], "direction": "front",
    "hearts": 5, "wealth": 0, "weapon": "sword", "items": ["sword"], "arrows": 3, "theme": "Legends of the Renk Gems", "Immobilize": False,
    "actors": [], "past_actors": [], "renks": {"renk 1": False, "renk 2": False, "renk 3": False, "renk 4": False},
  },
  "savedefault": {
    "save": "savedefault", "name": "N E W   S A V E",
    "x": WIDTH/2, "y": WIDTH/2, "position": [0, 0], "minimaps": [0, 0], "direction": "front",
    "hearts": 5, "wealth": 0, "weapon": "sword", "items": ["sword"], "arrows": 3, "theme": "Legends of the Renk Gems", "Immobilize": False,
    "actors": [], "past_actors": [], "renks": {"renk 1": False, "renk 2": False, "renk 3": False, "renk 4": False},
  },
}

monster_types = {
  "madpuff":      {"hearts": 3, "speed": 2, "can shoot": False, "drop": "diamond"},
  "croaker":      {"hearts": 2, "speed": 5, "can shoot": False, "drop": "diamond"},
  "regall":       {"hearts": 5, "speed": 0, "can shoot": True, "drop": "-"},

  "scorpio":      {"hearts": 2, "speed": 6, "can shoot": False, "drop": "diamond"},
  "husk":         {"hearts": 6, "speed": 1, "can shoot": False, "drop": "arrow"},
  "yuma":         {"hearts": 4, "speed": 0, "can shoot": True, "drop": "-"},

  "foxox":        {"hearts": 3, "speed": 4, "can shoot": True, "drop": "diamond"},
  "sharpy":       {"hearts": 2, "speed": 5, "can shoot": False, "drop": "arrow"},

  "xroaker":      {"hearts": 3, "speed": 6, "can shoot": False, "drop": "diamond"},
  "regalios":     {"hearts": 1, "speed": 0, "can shoot": True, "drop": "-"},
  "madpuff weak": {"hearts": 1, "speed": 2, "can shoot": False, "drop": "-"},

  "madpuff renk": {"hearts": 35, "speed": 1, "can shoot": True, "drop": "renk 4"},
}

container_types = {
  "chest": {"contents": ["diamonds"], "price": 0, "sound": hurt_sfx},
  "arrow chest": {"contents": ["diamond", "diamond", "diamond", "arrow"], "price": 0, "sound": hurt_sfx},
  "vessel": {"contents": ["arrow"], "price": 0, "sound": break_sfx},
  "heart chest": {"contents": ["heart"], "price": 0, "sound": hurt_sfx},

  "fragile granite": {"contents": [], "price": 0, "sound": secret_sfx},
  "fragile granite 2": {"contents": [], "price": 0, "sound": secret_sfx},
  "fragile granite 3": {"contents": [], "price": 0, "sound": secret_sfx},
  "fragile boulder": {"contents": [], "price": 0, "sound": secret_sfx},
  "fragile boulder hpp": {"contents": ["healing potion priceless"], "price": 0, "sound": secret_sfx},
  "fragile wall horizontal": {"contents": [], "price": 0, "sound": secret_sfx},
  "fragile wall vertical": {"contents": [], "price": 0, "sound": secret_sfx},
  "fragile block heart": {"contents": ["heart"], "price": 0, "sound": secret_sfx},
  "fragile block diamonds": {"contents": ["diamonds"], "price": 0, "sound": secret_sfx},

  "ship": {"contents": [], "price": 0, "sound": secret_sfx},
}

collictible_types = {
  "diamond":                    {"value": 1, "arrow": 0, "heart": 0, "price": 0, "sound": collect2_sfx, "title": "-"},
  "diamonds":                   {"value": 5, "arrow": 0, "heart": 0, "price": 0, "sound": collect_sfx, "title": "-"},
  "bow":                        {"value": "bow", "arrow": 0, "heart": 0, "price": 20, "sound": "-", "title": "-"},
  "arrow":                      {"value": 0, "arrow": 3, "heart": 0, "price": 0, "sound": collect3_sfx, "title": "-"},
  "heart":                      {"value": 0, "arrow": 0, "heart": 1, "price": 0, "sound": one_up_sfx, "title": "-"},
  "heart with price":           {"value": 0, "arrow": 0, "heart": 1, "price": 5, "sound": one_up_sfx, "title": "-"},
  "grapple hook":               {"value": "grapple hook", "arrow": 0, "heart": 0, "price": 50, "sound": "-", "title": "-"},
  "healing capsule":            {"value": "healing capsule", "arrow": 0, "heart": 0, "price": 8, "sound": "-", "title": "-"},
  "healing potion":             {"value": "healing potion", "arrow": 0, "heart": 0, "price": 30, "sound": "-", "title": "-"},
  "healing potion priceless":   {"value": "healing potion", "arrow": 0, "heart": 0, "price": 0, "sound": collect3_sfx, "title": "-"},
  "adham sword":                {"value": "adham sword", "arrow": 0, "heart": 0, "price": 0, "sound": "Given", "title": "Sword of Adham Acquired!"},
  "renk 1":                     {"value": 0, "arrow": 0, "heart": 0, "price": 0, "sound": "Renk Gem", "title": "Renk Gem Acquired!"},
  "renk 2":                     {"value": 0, "arrow": 0, "heart": 0, "price": 0, "sound": "Renk Gem", "title": "Renk Gem Acquired!"},
  "renk 3":                     {"value": 0, "arrow": 0, "heart": 0, "price": 0, "sound": "Renk Gem", "title": "Renk Gem Acquired!"},
  "renk 4":                     {"value": 0, "arrow": 0, "heart": 0, "price": 0, "sound": "Renk Gem", "title": "Renk Gem Acquired!"},
}

npcs = {
  "naman": {
    "text 1": "Come have a bow!", "text 2": "It's SELECT to switch weapons", "content": "bow",
    "item x relative to npc": -40, "item y relative to npc": 0
  },
  "fidda": {
    "text 1": "In need of hearts?", "text 2": "Use it wisely!", "content": "healing potion",
    "item x relative to npc": -45, "item y relative to npc": 0
  },
  "arti": {
    "text 1": "What do ya say?", "text 2": "Try grapplin' stuff!", "content": "grapple hook",
    "item x relative to npc": 65, "item y relative to npc": 0
  },
  "polovo": {
    "text 1": "Don't tell anyone", "text 2": "-", "content": "heart with price",
    "item x relative to npc": 20, "item y relative to npc": -100
  },
  "kevser": {
    "text 1": ["Are you the boy named Tuff?", "I assume you know about...", "...the four Renk gems.",
               "You have 2 of them already!?", "That's splendid.",
               "Right beyond here is a man...", "...who had the other two.", "His name is Valmore", "Well, I just managed to...",
               "run off with one.", "He will tear the country apart...", "after he will unite the 4.", "So, take him down!"],
               "text 2": "-", "content": "-",
    "item x relative to npc": 20, "item y relative to npc": -100
  },
  "naman 2": {
    "text 1": "This sword was destined for you", "text 2": "Take down the bad guys!", "content": "adham sword",
    "item x relative to npc": -40, "item y relative to npc": 0
  },
  "ivan": {
    "text 1": "Take it as a gift", "text 2": "Don't tell anyone I'm here", "content": "healing capsule",
    "item x relative to npc": 20, "item y relative to npc": 90
  },
  "polovo 2": {
    "text 1": "Good luck out there", "text 2": "-", "content": "-",
    "item x relative to npc": 20, "item y relative to npc": -100
  },
  "valmore": {
    "text 1": ["Hm?", "..." "You must be the one", "...The one I've been waiting for.", "You took possession of ...", "3 worldly treasures",
               "One of them was once mine.", "That is baffling," ,"... for a tot like you.", "Perplexing..",
               "I will not make myself wait...", "...any longer.", "This is it!", "I tightly clench my fist",
               "and sow the seeds of chaos!", "I will take my wealth back.", "So squint your eyes!", " "],

    "text 2": ["  !", " Aargh!", "How did-", "HOW DID I LOSE!?", " ", "Impossible...!", " ",
               "There is still nothing to fear!", "I concealed the last Renk gem.", "You will never find it!!",
               "You'll remember this.", "No matter how much struggle,", "you're still not off the hook.", "You won't get any further!!!", " "],
    "content": "-",
    "item x relative to npc": 20, "item y relative to npc": -100
  },
  "naman 3": {
    "text 1": ["Tuff, you have all the gems?", "You also defeated Valmore.", "Thank you Tuff.",
               "Peace returns at last!", "You've proven yourself...", "... for the tree country",
               "Let's go see Polovo,", "the ship is waiting.", " "], "text 2": "-", "content": "-",
    "item x relative to npc": -40, "item y relative to npc": 0
  },
  "polovo 3": {
    "text 1": ["Did you find the last Renk gem?", "Good work", "Hero of the tree country!",
               "I didn't expect it to...", "...go so smoothly.",
               "We'll detain Valmore so he ...", "won't make another ruckus.",
               "Oh and about those gems,", "Leave them to me,", "I will keep them secure.",
               "Now let's go,", "I'll take you to where you live.", " "],
               "text 2": "-", "content": "-",
    "item x relative to npc": 20, "item y relative to npc": -100
  },
}

blit_text("Loading Classes...")
sleep(0.05)

class Main:
  def __init__(self):
    print("Running Game...")
    pygame.mixer.music.load("Sounds/tracks/Sound the Lost Page.mp3")
    pygame.mixer.music.play(-1, 0.0)
    self.started = False
    self.scrolly = 0
    self.gamestate = 0
    self.score = 0
    self.tiles = []
    self.actors = []
    self.past_actors = []
    self.scrolls = [0, 0]
    self.minimaps = [0, 0]
    self.projectiles = []
    self.items = [save for save in saves.values() if save["save"] != "savedefault"]
    self.keyboard = [["A", "B", "C", "D", "E", "F", "G"],
                     ["H", "I", "J", "K", "L", "M", "N"],
                     ["O", "P", "Q", "R", "S", "T", "U"],
                     ["V", "W", "X", "Y", "Z", "<", "_"]]
    self.selected_item_y = 0
    self.selected_item_x = 0
    self.timer = Timer()
    self.save = "save1"
    self.savename = "N E W   S A V E"
    self.letter = ""
    self.autosave_timer = Timer()
    self.renk_timer = Timer()
    self.gameover_timer = Timer()
    self.immobilize = False
    self.theme = "Legends of the Renk Gems"
    self.shake = [0, 0]
    self.saving_works = True
    #pygame.mixer.music.set_volume(0)
  
  def update(self):
    if self.gamestate == 0: self.scroll()
    if self.gamestate == 1: self.menu()
    if self.gamestate == 2: self.new_save()
    if self.gamestate == 3: self.are_you_sure()
    if self.gamestate == 4: self.gameplay()
    if self.gamestate == 5: self.ending()
    run()

  def scroll(self):
    global k_select, k_start, k_a
    maxnum = 784.5
    screen.blit(manzara3, (0, (HEIGHT - 0) - maxint(self.scrolly, maxnum)))
    screen.blit(manzara3, (0, ((HEIGHT * 2) - 0) - maxint(self.scrolly, maxnum)))
    screen.blit(manzara3, (0, ((HEIGHT * 3) - 0) - maxint(self.scrolly, maxnum)))
    screen.blit(manzara, (0, 0 - maxint(self.scrolly, maxnum)))
    screen.blit(manzara2, (0, (HEIGHT - 0) - maxint(self.scrolly, maxnum)))
    screen.blit(pygame.transform.flip(manzara2, True, True), (0, ((HEIGHT * 2.6) - 0) - maxint(self.scrolly, maxnum)))
    screen.blit(tuff, (287, ((HEIGHT - 63) - 0) - maxint(self.scrolly, maxnum)))
    if k_start:
      if not self.started: k_start = False
      self.started = True; k_select = False
    if self.started: self.scrolly += 1.4
    screen.blit(clouds, (0, (HEIGHT - 60) - maxint(self.scrolly, maxnum)))
    screen.blit(pygame.transform.flip(clouds, True, True), (0, ((HEIGHT * 2) - 100) - maxint(self.scrolly, maxnum)))
    #screen.blit(blue_line, (0, ((HEIGHT + 30) - 0) - maxint(self.scrolly, maxnum)))
    #screen.blit(logo, ((WIDTH / 2) - (logo.get_width() / 2), HEIGHT * 2.6 - maxint(self.scrolly, maxnum)))
    for index, text in enumerate(texts):
      if type(text) == str:
        dialogue = retrofontmedium.render(text, True, "White")
        if text[len(text) - 1] == "~": dialogue = retrofontmedium.render(text[:-1], True, "Black")
        if text[len(text) - 1] == "-": dialogue = retrofontsmall.render(text[:-1], True, "White")
        screen.blit(dialogue, ((WIDTH / 2) - (dialogue.get_width() / 2), ((index * 22.5) + (HEIGHT / 3.5)) - maxint(self.scrolly, maxnum)))
    if self.scrolly > maxnum + (FPS * 3) or (self.started and (k_select or k_start)): self.gamestate = 1; pygame.mixer.music.stop()
    k_select = False
    k_start = False
    k_a = False
  
  def menu(self):
    #screen.blit(logo, ((WIDTH / 2) - (logo.get_width() / 2), 40))
    screen.blit(retrofont.render("- S E L E C T   S A V E -", False, "White"), (35, 50))
    pygame.draw.rect(screen, "Blue", ((45, 100), (250, 155)), 5)
    for index, item in enumerate(self.items):
      if index == self.selected_item_y:
        screen.blit(retrofontmedium.render(item["name"], False, "White"), (110, 120 + (index * 40)))
        screen.blit(pygame.image.load(f"Assets/tuff/walkfront{self.timer.keep_count(FPS / 3, 3, 1)}.png").convert_alpha(), (75, 120 + (index * 40)))
        self.save = item["save"]; self.savename = item["name"]
      else:
        screen.blit(retrofontmedium.render(item["name"], False, "White"), (95, 120 + (index * 40)))
        screen.blit(pygame.image.load(f"Assets/tuff/walkfront0.png").convert_alpha(), (60, 120 + (index * 40)))
    screen.blit(retrofontsmall.render('Press SELECT to Delete a Save', True, 'White'), (3, HEIGHT-15))
    self.controls()

  def new_save(self):
    screen.blit(retrofont.render("- N E W   S A V E -", False, "White"), (60, 50))
    screen.blit(retrofont.render(self.savename + "_", False, "White"), (60, 110))
    pygame.draw.rect(screen, "Blue", ((45, 100), (250, 190)), 5)
    for indexy, itemsx in enumerate(self.keyboard):
      for indexx, letter in enumerate(itemsx):
        if indexy == self.selected_item_y and indexx == self.selected_item_x:
          if self.timer.wait(FPS / 3): screen.blit(retrofont.render(letter, False, "White"), (57 + (indexx * 35), 145 + (indexy * 35)))
          self.letter = letter
        else:
          screen.blit(retrofont.render(letter, False, "White"), (57 + (indexx * 35), 145 + (indexy * 35)))

    screen.blit(retrofontsmall.render('Press START to Continue', True, 'White'), (3, HEIGHT-30))
    screen.blit(retrofontsmall.render('Press SELECT to See Accents', True, 'White'), (3, HEIGHT-15))
    self.controls()

  def are_you_sure(self):
    screen.blit(retrofont.render("- A R E   Y O U   S U R E ? -", False, "White"), (16, 50))
    pygame.draw.rect(screen, "Blue", ((45, 120), (250, 120)), 5)
    for index, item in enumerate(["N o !", "Y e s"]):
      if index == self.selected_item_y:
        screen.blit(retrofontmedium.render(item, False, "White"), (110, 145 + (index * 40)))
      else:
        screen.blit(retrofontmedium.render(item, False, "White"), (95, 145 + (index * 40)))
    self.controls()
  
  def controls(self):
    global k_a
    if self.gamestate == 1:
      if k_up: self.selected_item_y -= 1; click_sfx.play()
      if k_down: self.selected_item_y += 1; click_sfx.play()
      if self.selected_item_y >= len(self.items): self.selected_item_y = 0
      if self.selected_item_y == -1: self.selected_item_y = len(self.items) - 1

      if k_a or k_start:
        if self.items[self.selected_item_y]["name"] == "N E W   S A V E": self.gamestate = 2; k_a = False; self.savename = ""; select2_sfx.play(); self.selected_item_x, self.selected_item_y = 0, 0
        else: self.load_game(); k_a = False; select_sfx.play()

      if k_select and self.items[self.selected_item_y]["name"] != "N E W   S A V E":
        self.gamestate = 3; self.selected_item_y = 0

    if self.gamestate == 2:
      if k_up: self.selected_item_y -= 1; click_sfx.play(); self.timer.reset()
      if k_down: self.selected_item_y += 1; click_sfx.play(); self.timer.reset()
      if self.selected_item_y >= len(self.keyboard): self.selected_item_y = 0; self.timer.reset()
      if self.selected_item_y == -1: self.selected_item_y = len(self.keyboard) - 1; self.timer.reset()
      if k_left: self.selected_item_x -= 1; click_sfx.play(); self.timer.reset()
      if k_right: self.selected_item_x += 1; click_sfx.play(); self.timer.reset()
      if self.selected_item_x >= 7: self.selected_item_x = 0; self.timer.reset()
      if self.selected_item_x == -1: self.selected_item_x = 7 - 1; self.timer.reset()
      if k_a:
        if self.letter == "<": self.savename = self.savename[:-1]; self.timer.reset(); select2_sfx.play()
        elif self.letter == "_":
          if len(self.savename) < 13: self.savename += " "; self.timer.reset(); select2_sfx.play()
        else:
          if len(self.savename) < 13: self.savename += self.letter; self.timer.reset(); select2_sfx.play()

      if k_start and len(self.savename) > 0: self.gamestate = 1; k_a = False; saves[self.save]["name"] = self.savename; self.timer.reset(); self.selected_item_x, self.selected_item_y = 0, 0

      if k_select:
        self.keyboard = [["Æ", "ß", "Ç", "Ð", "Ë", "F", "Ğ"],
                         ["H", "i", "J", "K", "Ł", "M", "Ñ"],
                         ["Ö", "P", "Q", "R", "Š", "T", "Ü"],
                         ["V", "W", "X", "Ÿ", "Ž", "<", "_"]]
      else:
        self.keyboard = [["A", "B", "C", "D", "E", "F", "G"],
                         ["H", "I", "J", "K", "L", "M", "N"],
                         ["O", "P", "Q", "R", "S", "T", "U"],
                         ["V", "W", "X", "Y", "Z", "<", "_"]]
        
    if self.gamestate == 3:
      if k_up: self.selected_item_y -= 1; click_sfx.play()
      if k_down: self.selected_item_y += 1; click_sfx.play()
      if self.selected_item_y >= 2: self.selected_item_y = 0
      if self.selected_item_y == -1: self.selected_item_y = 1

      if k_a and self.selected_item_y == 1:
        saves[self.save]["name"] = "N E W   S A V E"
        saves[self.save]["x"], saves[self.save]["y"] = WIDTH / 2, HEIGHT / 2
        saves[self.save]["position"] = [0, 0]
        saves[self.save]["minimaps"] = [0, 0]
        saves[self.save]["direction"] = "front"
        saves[self.save]["hearts"] = 5
        saves[self.save]["wealth"] = 0
        saves[self.save]["weapon"] = "sword"
        saves[self.save]["items"] = ["sword"]
        saves[self.save]["arrows"] = 3
        saves[self.save]["renks"] = {"renk 1": False, "renk 2": False, "renk 3": False, "renk 4": False}
        saves[self.save]["actors"] = []
        saves[self.save]["past actors"] = []
        saves[self.save]["theme"] = "Legends of the Renk Gems"
        saves[self.save]["Immobilize"] = False
        self.actors.clear()
        self.past_actors.clear()
        with open("Saves/memory_card/savefile.txt", "wb") as out_: pickle.dump(saves, out_)
        #saves[self.save]["actors"] = {"monster": [], "container": [], "npc": [], "collectible": []}
        #self.save_game(self.save)

        self.gamestate = 1
        self.selected_item_y = 0
      
      if k_a and self.selected_item_y == 0: self.gamestate = 1

  def ending(self):
    maxnum = 550; self.scrolly += 1.4 
    screen.blit(logo, (40, ((HEIGHT * 2) - 10) - maxint(self.scrolly, maxnum)))
    for index, text in enumerate(texts_end):
      if type(text) == str:
        dialogue = retrofontmedium.render(text, True, "White")
        if text[len(text) - 1] == "~": dialogue = retrofontmedium.render(text[:-1], True, "Black")
        if text[len(text) - 1] == "-": dialogue = retrofontsmall.render(text[:-1], True, "White")
        screen.blit(dialogue, ((WIDTH / 2) - (dialogue.get_width() / 2), ((index * 22.5) + (HEIGHT / 3.5)) - maxint(self.scrolly, maxnum)))
    if self.scrolly > maxnum and k_start:
      saves[self.save]["name"] = "N E W   S A V E"; saves[self.save]["x"], saves[self.save]["y"] = WIDTH / 2, HEIGHT / 2
      saves[self.save]["position"] = [0, 0]; saves[self.save]["minimaps"] = [0, 0]; saves[self.save]["direction"] = "front"
      saves[self.save]["hearts"] = 5; saves[self.save]["wealth"] = 0; saves[self.save]["weapon"] = "sword"; saves[self.save]["items"] = ["sword"]; saves[self.save]["arrows"] = 3
      saves[self.save]["renks"] = {"renk 1": False, "renk 2": False, "renk 3": False, "renk 4": False}; saves[self.save]["actors"] = []
      saves[self.save]["past actors"] = []; saves[self.save]["theme"] = "Legends of the Renk Gems"; saves[self.save]["Immobilize"] = False
      self.actors.clear()
      self.past_actors.clear()
      self.save_game(self.save); self.gamestate = 1; self.selected_item_y = 0; pygame.mixer.music.stop()
  
  def gameplay(self):
    if self.player.hearts > 0:
      self.timer.count(5, 4, 0)
      if self.timer.tally == 3 and self.timer.time == 1: beep_sfx.play(); pygame.mixer.music.play(-1, 0.0)
      if self.timer.tally >= 3:
        for tile in self.tiles: tile.update()
        for actor in self.actors:
          if not isinstance(actor, NPC):
            if actor.alive and actor.rect.x < WIDTH and actor.rect.x > 0 and actor.rect.y < HEIGHT and actor.rect.y > 0: actor.update()
        self.player.update()
        for actor in self.actors:
          if isinstance(actor, NPC):
            if actor.alive and actor.rect.x < WIDTH and actor.rect.x > 0 and actor.rect.y < HEIGHT and actor.rect.y > 0: actor.update()
        for proj in self.projectiles:
          proj.update()
          if not proj.alive: self.projectiles.remove(proj)

        if not self.immobilize and not self.theme == "Hollow Bones":
          if self.autosave_timer.timer(FPS * 30):
            try: self.save_game(self.save); self.saving_works = True
            except: self.saving_works = False
          if self.autosave_timer.time <= FPS * 3:
            if self.saving_works: screen.blit(retrofontsmall.render('Saving in memory card...', True, 'White'), (3, HEIGHT-25)); screen.blit(retrofontsmall.render('Don\'t power off the console', True, 'White'), (3, HEIGHT-15))
            else: screen.blit(retrofontsmall.render('The system had trouble saving...', True, 'White'), (3, HEIGHT-25)); screen.blit(retrofontsmall.render('No memory card inserted', True, 'White'), (3, HEIGHT-15))
      else: self.player.update()
    else:
      self.player.update()
      self.gameover_timer.count(FPS, 12, 0); self.projectiles.clear()
      if self.gameover_timer.tally == 0 and self.gameover_timer.time == 1: pygame.mixer.music.stop(); self.autosave_timer.reset()
      if self.gameover_timer.tally == 1 and self.gameover_timer.time == 1: pygame.mixer.music.load("Sounds/tracks/Defeat.mp3")
      if self.gameover_timer.tally == 1 and self.gameover_timer.time == 2: pygame.mixer.music.play(1, 0.0)
      if self.gameover_timer.tally >= 11: self.gamestate = 1; self.gameover_timer.reset(); self.end_game(False)
      screen.blit(retrofont.render("- Game Over -", False, "Yellow"), (30 + self.autosave_timer.oscillate(FPS / 4, 10, 0), 20))

    if not self.immobilize: self.player.controls()
    else: self.player.movement = [0, 0]

    if self.player.hearts <= 0: self.immobilize = True
    if not self.immobilize: self.render_ui()

  def render_ui(self):
    #pygame.draw.rect(screen, "Black", ((0, 0), (WIDTH, 50)))
    screen.blit(retrofont.render("Hearts", False, "White"), (3, 2))
    for index in range(math.ceil(main.player.hearts)):
      screen.blit(heart, (3 + (index * 19), 30))
    for index, weapon in enumerate(self.player.items):
      if self.player.equiped_item == index: screen.blit(pygame.image.load(f"Assets/{weapon}.png").convert_alpha(), (120 + (index * 16), 24))
      else: screen.blit(pygame.image.load(f"Assets/{weapon}.png").convert_alpha(), (120 + (index * 16), 28))
    screen.blit(retrofont.render("Items", False, "White"), (120, 2))
    screen.blit(pygame.image.load("Assets/diamond/1.png").convert_alpha(), (250, 9))
    screen.blit(pygame.image.load("Assets/tuff/arrowback.png").convert_alpha(), (250, 30))
    screen.blit(retrofont.render("× " + str(self.player.wealth), False, "White"), (270, 2))
    screen.blit(retrofont.render("× " + str(self.player.arrows), False, "White"), (270, 23))

    for index, renk in enumerate(["renk 1", "renk 2", "renk 3", "renk 4"]):
      if self.player.renks[renk] and self.timer.tally >= 4: screen.blit(pygame.transform.scale(pygame.image.load(f"Assets/{renk}/{int(self.timer.wait(FPS / 2)) + 1}.png").convert_alpha(), (16, 16)), (275 + (index * 18), HEIGHT - 18))

  def load_map(self):
    self.tiles.clear()
    for y, mapx in enumerate(map[self.minimaps[1]][self.minimaps[0]]):
      for x, tile in enumerate(mapx):
        self.tiles.append(Tile(tile, x, y))
        if not tile_types[tile]["entity"] == "-":
          instance = Monster(tile_types[tile]["entity"], x * 32, y * 32)
          if instance.origin not in self.past_actors:
            self.actors.append(instance)
            self.past_actors.append(instance.origin)
        if not tile_types[tile]["npc"] == "-":
          instance = NPC(tile_types[tile]["npc"], x * 32, y * 32)
          if instance.origin not in self.past_actors:
            self.actors.append(instance)
            self.past_actors.append(instance.origin)
        if not tile_types[tile]["item"] == "-":
          instance = Collectible(tile_types[tile]["item"], x * 32, y * 32)
          if instance.origin not in self.past_actors:
            self.actors.append(instance)
            self.past_actors.append(instance.origin)
        if not tile_types[tile]["asset"] == "-":
          instance = Chest(tile_types[tile]["asset"], x * 32, y * 32)
          if instance.origin not in self.past_actors:
            self.actors.append(instance)
            self.past_actors.append(instance.origin)
  
  def load_game(self):
    self.gamestate = 4
    self.player = Player()
    self.timer.reset()
    self.autosave_timer.reset()
    try:
      self.load_save(self.save)
      self.save_game(self.save)
    except: pass
    self.load_map()
    pygame.mixer.music.load(f"Sounds/tracks/{self.theme}.mp3")

  def load_save(self, save):
    with open("Saves/memory_card/savefile.txt", "rb") as savefile: saves = pickle.load(savefile)
    self.actors = []
    self.player.rect = pygame.Rect((saves[save]["x"], saves[save]["y"]), (26, 26))
    self.player.position = saves[save]["position"]
    self.minimaps = saves[save]["minimaps"]
    self.player.dir = saves[save]["direction"]
    self.player.hearts = saves[save]["hearts"]
    self.player.wealth = saves[save]["wealth"]
    self.player.item = saves[save]["weapon"]
    self.player.items = saves[save]["items"]
    self.player.arrows = saves[save]["arrows"]
    self.player.renks = saves[save]["renks"]
    self.actors = saves[save]["actors"]
    self.past_actors = saves[save]["past_actors"]
    self.theme = saves[save]["theme"]
    self.immobilize = saves[save]["Immobilize"]

  def save_game(self, save):
    global saves
    open("Saves/memory_card/savefile.txt", "rb")
    saves[save]["x"], saves[save]["y"] = self.player.rect.x, self.player.rect.y
    saves[save]["position"] = self.player.position
    saves[save]["minimaps"] = self.minimaps
    saves[save]["direction"] = self.player.dir
    saves[save]["hearts"] = self.player.hearts
    saves[save]["wealth"] = self.player.wealth
    saves[save]["weapon"] = self.player.item
    saves[save]["items"] = self.player.items
    saves[save]["arrows"] = self.player.arrows
    saves[save]["renks"] = self.player.renks
    saves[save]["actors"] = self.actors
    saves[save]["past_actors"] = self.past_actors
    saves[save]["theme"] = self.theme
    saves[save]["Immobilize"] = self.immobilize

    try:
      for actor in self.actors: 
        actor.image = pygame.surfarray.array3d(actor.image)
        #actor.sound = pygame.sndarray.array(actor.sound)
        if isinstance(actor, NPC):
          for content in actor.contents: content.image = pygame.surfarray.array3d(content.image)
      saves[save]["actors"] = self.actors
      with open("Saves/memory_card/savefile.txt", "wb") as out_: pickle.dump(saves, out_)
    except: pass
    for actor in saves[save]["actors"]:
      actor.image = pygame.surfarray.make_surface(actor.image)
      #actor.sound = pygame.sndarray.make_sound(actor.sound)
      if isinstance(actor, NPC):
        for content in actor.contents: content.image = pygame.surfarray.make_surface(content.image)
    #except: print("Saving Failed!")

    #for actor in self.actors: actor.image = None; actor.sound = decoy; actor.text = None
    #out_ = open("Saves/memory_card/savefile.txt", "wb"); pickle.dump(saves, out_); out_.close()

  def end_game(self, save_game=True):
    pygame.mixer.music.stop()
    if save_game: main.save_game(main.save)
    self.tiles = []
    self.timer.reset()
    
  def quit(self):
    global saves
    #try: self.save_game(self.save)
    #except: print("Loading failed.")
    try: self.save_game(self.save)
    except FileNotFoundError: print("Save file not found.")
    except EOFError: print("Save file is empty or invalid.")
    except Exception as e: print("An error occurred in saving:", str(e))
    pygame.quit()
    exit()
      

class Player:
  def __init__(self):
    self.rect = pygame.Rect((WIDTH / 2, HEIGHT / 2), (26, 13))
    self.speed = 5
    self.timer = Timer()
    self.hit_timer = Timer()
    self.dir = "front"
    self.state = "walk"
    self.frame = 1
    self.movement = [0, 0]
    self.collision = {'top': False, 'bottom': False, 'right': False, 'left': False}
    self.enemy_collision = {'top': False, 'bottom': False, 'right': False, 'left': False}
    self.image = pygame.image.load(f"Assets/tuff/{self.state}{self.dir}{self.frame}.png").convert_alpha()
    self.position = [self.rect.x + main.minimaps[0], self.rect.y + main.minimaps[1]]
    self.wealth = 0
    self.solid = True

    self.hearts = 5
    self.equiped_item = 0
    self.items = ["sword"]
    self.arrows = 3
    self.renks = {"renk 1": False, "renk 2": False, "renk 3": False, "renk 4": False}
    try: self.item = self.items[self.equiped_item]
    except: print("Player has no weapons!!")

  def update(self):
    try: self.image = pygame.image.load(f"Assets/tuff/{self.state}{self.dir}{self.frame}.png").convert_alpha()
    except: self.frame = 1
    if self.hit_timer.time:
      self.image.fill("White", special_flags=pygame.BLEND_RGB_MAX)
      self.hit_timer.wait(FPS / 8)
    screen.blit(self.image, (self.rect.x - 3, self.rect.y - 5))
    if k_select:
      self.equiped_item += 1
      if self.equiped_item >= len(self.items): self.equiped_item = 0
      self.item = self.items[self.equiped_item]
    #pygame.draw.rect(screen, "Blue", self.rect, 2)
    self.position = [self.rect.x + main.minimaps[0], self.rect.y + main.minimaps[1]]
    #self.rect.x -= main.scrolls[0]; self.rect.y -= main.scrolls[1]
    
    if self.rect.x > WIDTH - self.rect.width:
      for proj in main.projectiles: proj.rect.x -= WIDTH
      for entity in main.actors: entity.rect.x -= WIDTH
      scroll_sfx.play()
      #for entity in main.actors:
      #  if isinstance(entity, Monster) or isinstance(entity, NPC): main.actors.remove(entity)
      self.rect.x = 0; main.minimaps[0] += 1; main.load_map()
    if self.rect.x < 0:
      for proj in main.projectiles: proj.rect.x += WIDTH
      for entity in main.actors: entity.rect.x += WIDTH
      scroll_sfx.play()
      #for entity in main.actors:
      #  if isinstance(entity, Monster) or isinstance(entity, NPC): main.actors.remove(entity)
      self.rect.x = WIDTH - self.rect.width; main.minimaps[0] -= 1; main.load_map()
    if self.rect.y > HEIGHT - self.rect.height:
      for proj in main.projectiles: proj.rect.y -= HEIGHT
      for entity in main.actors: entity.rect.y -= HEIGHT
      scroll_sfx.play()
      #for entity in main.actors:
      #  if isinstance(entity, Monster) or isinstance(entity, NPC): main.actors.remove(entity)
      self.rect.y = 0; main.minimaps[1] += 1; main.load_map()
    if self.rect.y < 0:
      for proj in main.projectiles: proj.rect.y += HEIGHT
      for entity in main.actors: entity.rect.y += HEIGHT
      scroll_sfx.play()
      #for entity in main.actors:
      #  if isinstance(entity, Monster) or isinstance(entity, NPC): main.actors.remove(entity)
      self.rect.y = HEIGHT - self.rect.height; main.minimaps[1] -= 1; main.load_map()

    self.rect, self.collision = self.move(self.rect, self.movement, main.tiles + [actor for actor in main.actors if (not isinstance(actor, Monster) or (self.state != "grapple hook"))])

    for proj in main.projectiles:
      if self.rect.colliderect(proj.rect) and not isinstance(proj, Arrow) and not isinstance(proj, Grapple):
        proj.alive = False
        self.hearts -= proj.damage
        self.hit_timer.time = 1
        hurt_sfx.play()
        if self.hearts <= 0: main.timer.reset()

    if self.hearts > 5: self.hearts = 5
    self.speed = 5 + (int(k_debug) * 30)

    if main.player.renks["renk 1"] and main.player.renks["renk 2"]:
      for tile in main.tiles:
        if tile.type["name"] == "bale":
          tile.__init__("d ", tile.rect.x / 32, tile.rect.y / 32)

    if main.player.renks["renk 3"]:
      for tile in main.tiles:
        if tile.type["name"] == "dark grass solid":
          tile.__init__("h ", tile.rect.x / 32, tile.rect.y / 32)

    if main.theme == "The Gathering":
      for tile in main.tiles:
        if tile.type["name"] == "gate wall": tile.__init__("u ", tile.rect.x / 32, tile.rect.y / 32)

    if main.player.renks["renk 4"]:
      for tile in main.tiles:
        if tile.type["name"] == "dark grass tree":
          tile.__init__("h ", tile.rect.x / 32, tile.rect.y / 32)

  def controls(self):
    global k_a
    if self.state != self.item:
      if k_right:
        self.movement[0] = self.speed; main.scrolls[0] = self.speed
        self.state = "walk"; self.dir = "right"; self.frame = self.timer.keep_count(FPS / 4, 3, 1)
      elif k_left:
        self.movement[0] = -self.speed; main.scrolls[0] = self.speed
        self.state = "walk"; self.dir = "left"; self.frame = self.timer.keep_count(FPS / 4, 3, 1)
      else: main.scrolls[0] = 0; self.movement[0] = 0
      if k_up:
        self.movement[1] = -self.speed; main.scrolls[1] = self.speed
        self.state = "walk"; self.dir = "back"; self.frame = self.timer.keep_count(FPS / 4, 3, 1)
      elif k_down:
        self.movement[1] = self.speed; main.scrolls[1] = self.speed
        self.state = "walk"; self.dir = "front"; self.frame = self.timer.keep_count(FPS / 4, 3, 1)
      else: main.scrolls[1] = 0; self.movement[1] = 0
      if k_a and self.items != [] and ((self.item == "bow" and self.arrows > 0) or self.item != "bow") and (self.item != "healing potion" and self.item != "healing capsule" and self.item != "grapple hook"): self.state = self.item; self.frame = 1
      if k_a and self.item == "healing potion": collect4_sfx.play(); self.hearts += 2; self.items.remove(self.item); k_a = False; self.item = self.items[0]
      if k_a and self.item == "healing capsule": collect4_sfx.play(); self.hearts += 1; self.items.remove(self.item); k_a = False; self.item = self.items[0]
      if k_a and self.item == "grapple hook": grappling_sfx.play(); main.projectiles.append(Grapple(self.rect.x, self.rect.y, self.dir, self)); self.state = self.item
    if self.state == self.item:
      if self.state != "grapple hook":
        self.frame = self.timer.count(FPS / 15, 4, 0)
        self.movement = [0, 0]
        if self.timer.tally == 4:
          main.projectiles.append(Arrow(self.rect.x + 8, self.rect.y + 8, self.dir, self.item != "bow", self.item == "adham sword"))
          if self.item == "bow": self.arrows -= 1
          self.state = "walk"; self.frame = 1; self.timer.reset()
      else: self.frame = 1

  def move(self, rect, movement, tiles):
    collision_type = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]

    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
      if tile.solid and tile.type != "valmore" and not k_debug:
        if movement[0] > 0:
          rect.right = tile.rect.left
          collision_type['right'] = True
        elif movement[0] < 0:
          rect.left = tile.rect.right
          collision_type['left'] = True
    
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
      if tile.solid and tile.type != "valmore" and not k_debug:
        if movement[1] > 0:
          rect.bottom = tile.rect.top
          collision_type['bottom'] = True
        elif movement[1] < 0:
          rect.top = tile.rect.bottom
          collision_type['top'] = True

    return rect, collision_type
  
  def get_hit(self, rect, movement, tiles):
    collision_type = {'top': False, 'bottom': False, 'right': False, 'left': False}
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
      if movement[0] > 0: collision_type['right'] = True
      elif movement[0] < 0: collision_type['left'] = True
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
      if movement[1] > 0: collision_type['bottom'] = True
      elif movement[1] < 0: collision_type['top'] = True
    return rect, collision_type


class Tile:
  def __init__(self, tile, x, y):
    def load_img(tile):
      if not tile_types[tile]["sets"]: return pygame.image.load("Assets/tiles/" + tile_types[tile]["name"] + ".png").convert_alpha()
      else: return pygame.image.load("Assets/tiles/" + tile_types[tile]["name"] + "/" + tile_types[tile]["set"] + ".png").convert_alpha()
    self.type = tile_types[tile]
    self.image = load_img(tile)
    self.rect = pygame.Rect(x * 32, y * 32, 32, 32)
    self.solid = tile_types[tile]["solid"]

  def update(self):
    #self.rect.x += main.scrolls[0]; self.rect.y += main.scrolls[1]
    screen.blit(self.image, self.rect)
    #pygame.draw.rect(screen, "Red", self.rect, 2)


class Monster:
  def __init__(self, type, x, y):
    self.rect = pygame.Rect((x, y), (32 / (int(type == "madpuff weak") + 1), 32 / (int(type == "madpuff weak") + 1)))
    self.type = type
    self.speed = monster_types[self.type]["speed"]
    self.timer = Timer()
    self.dirx = "stay"
    self.diry = "stay"
    if self.type == "sharpy": self.diry = ["left", "right"][random.randrange(0, 2)]
    self.solid = True
    self.state = "walk"
    self.frame = 1
    self.movement = [0, 0]
    self.collision = {'top': False, 'bottom': False, 'right': False, 'left': False}
    self.enemy_collision = {'top': False, 'bottom': False, 'right': False, 'left': False}
    self.image = pygame.image.load(f"Assets/{self.type}/{self.state}{self.frame}.png").convert_alpha()
    self.position = [self.rect.x + main.minimaps[0], self.rect.y + main.minimaps[1]]
    self.flipped = False
    self.shoot_timer = Timer()
    self.hit_timer = Timer()
    self.hearts = monster_types[self.type]["hearts"]
    self.origin = [x, y, map_string_form[main.minimaps[1]][main.minimaps[0]]]
    self.object = "monster"
    self.alive = True
    self.hop_timer = Timer()
    self.hopping = 0
    if self.type == "regalios": self.flipped = bool(random.randrange(0, 2))
    if self.rect.x == 0: self.rect.x += 1
    if self.rect.y == 0: self.rect.y += 1

  def __str__(self):
    return f"{self.rect}, {self.alive}, {self.type}, {self.state}, {self.hearts}"

  def update(self):
    try:
      if self.type != "madpuff weak": self.image = pygame.transform.flip(pygame.image.load(f"Assets/{self.type}/{self.state}{self.frame}.png").convert_alpha(), self.flipped, False)
      elif self.type == "madpuff weak": self.image = pygame.transform.scale(pygame.transform.flip(pygame.image.load(f"Assets/{self.type}/{self.state}{self.frame}.png").convert_alpha(), self.flipped, False), (16, 16))
    except: self.frame = 1
    #screen.blit(retrofontsmall.render(str(self), False, "White"), (self.rect.x, self.rect.y - 10))
    if self.hit_timer.time:
      self.image.fill("White", special_flags=pygame.BLEND_RGB_MAX)
      self.hit_timer.wait(FPS / 8)
    screen.blit(self.image, (self.rect.x, self.rect.y - self.hopping))
    if self.hearts > 0:
      #pygame.draw.rect(screen, "Blue", self.rect, 2)
      #self.position = [self.rect.x + main.minimaps[0], self.rect.y + main.minimaps[1]]
      #self.rect.x -= main.scrolls[0]; self.rect.y -= main.scrolls[1]
      #if self.rect.x > WIDTH: self.rect.x = 0; main.minimaps[0] += 1; main.load_map()
      #if self.rect.x < -32: self.rect.x = WIDTH; main.minimaps[0] -= 1; main.load_map()
      #if self.rect.y > HEIGHT: self.rect.y = 0; main.minimaps[1] += 1; main.load_map()
      #if self.rect.y < -32: self.rect.y = HEIGHT; main.minimaps[1] -= 1; main.load_map()
      if self.hop_timer.tally <= 2:
        if self.type != "regalios":
          if self.dirx == "right": self.flipped = False
          if self.dirx == "left": self.flipped = True

        if self.type != "regall" and self.type != "yuma" and self.type != "regalios": self.rect, self.collision = self.move(self.rect, self.movement, main.tiles + main.actors + [main.player])

        if self.collision["bottom"]: self.diry = "back"
        if self.collision["top"]: self.diry = "front"
        if self.collision["left"]: self.dirx = "right"
        if self.collision["right"]: self.dirx = "left"

        if self.type != "sharpy":
          if self.rect.x > main.player.rect.x:
            self.dirx = "left"
            if self.rect.x - 45 < main.player.rect.x: self.dirx = "stay"
          if self.rect.x < main.player.rect.x:
            self.dirx = "right"
            if self.rect.x + 45 > main.player.rect.x: self.dirx = "stay"
          if self.rect.y > main.player.rect.y:
            self.diry = "back"
            if self.rect.y - 45 < main.player.rect.y: self.diry = "stay"
            else: self.stayy = False
          if self.rect.y < main.player.rect.y:
            self.diry = "front"
            if self.rect.y + 45 > main.player.rect.y: self.diry = "stay"
          
        if self.type != "regalios":
          if self.dirx == "right":
            self.movement[0] = self.speed; main.scrolls[0] = self.speed
            self.state = "walk"; self.frame = self.timer.keep_count(FPS / 8, 3, 1)
          elif self.dirx == "left":
            self.movement[0] = -self.speed; main.scrolls[0] = self.speed
            self.state = "walk"; self.frame = self.timer.keep_count(FPS / 8, 3, 1)
          else: main.scrolls[0] = 0; self.movement[0] = 0
          if self.diry == "back":
            self.movement[1] = -self.speed; main.scrolls[1] = self.speed
            self.state = "walk"; self.frame = self.timer.keep_count(FPS / 8, 3, 1)
          elif self.diry == "front":
            self.movement[1] = self.speed; main.scrolls[1] = self.speed
            self.state = "walk"; self.frame = self.timer.keep_count(FPS / 8, 3, 1)
          else: main.scrolls[1] = 0; self.movement[1] = 0

      if self.type == "croaker" or self.type == "xroaker":
        self.hop_timer.keep_count(FPS / 4, 5, 0)
        if self.hop_timer.tally == 1: self.hopping += self.hop_timer.time * 2
        if self.hop_timer.tally == 2: self.hopping -= self.hop_timer.time * 2
      else: self.hop_timer.tally = 1

      if self.type == "regalios":
        self.frame = self.timer.keep_count(2, 26, 1)
        if self.state == "attack": self.state = "walk"

      proj_angle = math.atan2(
        self.rect.centery - main.player.rect.centery,
        self.rect.centerx - main.player.rect.centerx,
      )

      if self.shoot_timer.timer(FPS * (3 - (int(self.type == "madpuff renk") * 2.2))): self.state = "attack"; self.frame = 1; main.projectiles.append(Projectile(self.rect.x, self.rect.y, proj_angle, monster_types[self.type]["can shoot"]))

      for proj in main.projectiles:
        if self.rect.colliderect(proj.rect) and not isinstance(proj, Projectile):
          if not isinstance(proj, Grapple):
            proj.alive = False
            self.hearts -= proj.damage
            self.hit_timer.time = 1
            hit_sfx.play()
            if proj.not_bow:
              if self.rect.y + 30 > main.player.rect.y and self.rect.y - 30 < main.player.rect.y:
                if self.rect.x >= main.player.rect.x: self.movement[0] = 30
                elif self.rect.x <= main.player.rect.x and self.rect.y + 30 > main.player.rect.y: self.movement[0] = -30
          if self.rect.x + 30 > main.player.rect.x and self.rect.x - 30 < main.player.rect.x:
            if self.rect.y >= main.player.rect.y: self.movement[1] = 30
            elif self.rect.y <= main.player.rect.y: self.movement[1] = -30
          if isinstance(proj, Grapple):
            if proj.retract:
              if proj.length > 40:
                self.hearts -= 1
                self.hit_timer.time = 1
                grapple_sfx.play()
              if proj.length > 15: self.rect.x, self.rect.y = proj.rect.x, proj.rect.y

    else:
      self.state = "defeat"
      self.frame = self.timer.tally
      self.alive = not self.timer.timer(4)
      if not self.alive and monster_types[self.type]["drop"] != "-": main.actors.append(Collectible(monster_types[self.type]["drop"], self.rect.x + 8, self.rect.y + 8))
      if self.timer.time == 1 and main.theme != "The Gathering": kill_sfx.play()
      self.solid = False

  def move(self, rect, movement, tiles):
    collision_type = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]

    if self.type != "sharpy":
      hit_list = collision_test(rect, tiles)
      for tile in hit_list:
        if tile.solid and tile is not self:
          if movement[0] > 0:
            rect.right = tile.rect.left
            collision_type['right'] = True
          elif movement[0] < 0:
            rect.left = tile.rect.right
            collision_type['left'] = True
    
      rect.y += movement[1]
      hit_list = collision_test(rect, tiles)
      for tile in hit_list:
        if tile.solid and tile is not self:
          if movement[1] > 0:
            rect.bottom = tile.rect.top
            collision_type['bottom'] = True
          elif movement[1] < 0:
            rect.top = tile.rect.bottom
            collision_type['top'] = True
    else:
      hit_list = collision_test(rect, tiles)
      for tile in hit_list:
        if not tile.solid and tile is not self:
          if movement[0] > 0:
            rect.right = tile.rect.left
            collision_type['right'] = True
          elif movement[0] < 0:
            rect.left = tile.rect.right
            collision_type['left'] = True
      if self.hop_timer.wait(FPS): self.dirx = "right"
      else: self.dirx = "left"

    return rect, collision_type
  

class Chest:
  def __init__(self, type, x, y):
    self.type = type
    self.state = "closed"
    self.rect = pygame.Rect((x, y), (32, 32))
    self.frame = 1
    self.image = pygame.image.load(f"Assets/{self.type}/{self.state}.png").convert_alpha()
    self.position = [self.rect.x + main.minimaps[0], self.rect.y + main.minimaps[1]]
    self.solid = True
    self.contents = container_types[self.type]["contents"]
    #self.sound = container_types[self.type]["sound"]
    self.origin = [x, y, map_string_form[main.minimaps[1]][main.minimaps[0]]]
    self.object = "container"
    self.bob_timer = Timer()
    self.alive = True
    if self.rect.x == 0: self.rect.x += 1
    if self.rect.y == 0: self.rect.y += 1
  
  def __str__(self): return f"{self.rect}, {self.alive}, {self.type}, {self.state}"
  
  def update(self):
    if self.type != "ship": self.image = pygame.image.load(f"Assets/{self.type}/{self.state}.png").convert_alpha()
    elif self.type == "ship": self.image = pygame.transform.scale2x(pygame.image.load(f"Assets/{self.type}/{self.state}.png").convert_alpha())
    screen.blit(self.image, (self.rect.x, self.rect.y + (self.bob_timer.oscillate(FPS / 3, 3, 0) * int(self.type == "ship"))))
    for proj in main.projectiles:
      if self.rect.colliderect(proj.rect) and isinstance(proj, Arrow) and self.state == "closed":
        proj.alive = False
        self.state = "open"
        self.solid = False
        container_types[self.type]["sound"].play()
        for prize in self.contents: main.actors.append(Collectible(prize, self.rect.x + 8, self.rect.y + 8))


class NPC:
  def __init__(self, type, x, y):
    self.type = type
    self.rect = pygame.Rect((x, y), (32, 32 * (int(self.type == "valmore") + 1)))
    self.frame = 1
    self.state = None
    self.flipped = False
    self.hearts = 1
    if self.type != "valmore": self.image = pygame.transform.flip(pygame.image.load(f"Assets/{self.type}/{self.frame}.png").convert_alpha(), self.flipped, False)
    elif self.type == "valmore": self.hearts = 30; self.state = "stand"; self.image = pygame.transform.scale2x(pygame.transform.flip(pygame.image.load(f"Assets/{self.type}/{self.state}{self.frame}.png").convert_alpha(), self.flipped, False))
    self.position = [self.rect.x + main.minimaps[0], self.rect.y + main.minimaps[1]]
    self.solid = True
    self.contents = []
    if npcs[self.type]["content"] != "-": self.contents = [Collectible(npcs[self.type]["content"], self.rect.x + npcs[self.type]["item x relative to npc"], self.rect.y + npcs[self.type]["item y relative to npc"])]
    self.full_dialogue = npcs[self.type]["text 1"]
    self.dialogue = ""
    self.text_timer = Timer()
    self.origin = [x, y, map_string_form[main.minimaps[1]][main.minimaps[0]]]
    self.object = "npc"
    self.alive = True
    self.timer = Timer()
    self.behavior_timer = Timer()
    if self.type != "valmore": self.image = pygame.image.load(f"Assets/{self.type}/{self.frame}.png").convert_alpha()
    self.text_index = 0
    if self.type == "kevser" and not main.player.renks["renk 3"]: self.rect.x = 1; main.player.rect.x = 250; main.player.rect.y = HEIGHT / 2; pygame.mixer.music.stop(); main.immobilize = True
    if self.type == "valmore" and main.theme == "Sword of Adham": self.flipped = True; main.player.rect.y = HEIGHT / 2; pygame.mixer.music.stop(); main.immobilize = True
    if self.type == "naman 3": self.rect.y = HEIGHT - 1
    if self.type == "polovo 3": main.player.rect.y = HEIGHT / 2; pygame.mixer.music.stop(); main.immobilize = True
    if self.rect.x == 0: self.rect.x += 1
    if self.rect.y == 0: self.rect.y += 1

  def __str__(self): return f"{self.rect}, {self.alive}, {self.type}"
  
  def update(self):
    global k_a, k_start, k_right
    if self.type != "valmore": screen.blit(pygame.transform.flip(pygame.image.load(f"Assets/{self.type}/{self.frame}.png").convert_alpha(), self.flipped, False), self.rect)
    elif self.type == "valmore": screen.blit(pygame.transform.scale2x(pygame.transform.flip(pygame.image.load(f"Assets/{self.type}/{self.state}{self.frame}.png").convert_alpha(), self.flipped, False)), self.rect)
    
    if self.type != "kevser" and self.type != "valmore" and self.type != "naman 3" and self.type != "polovo 3":
      try: self.dialogue += self.full_dialogue[self.text_timer.tally]; bow_sfx.play()
      except: pass
      self.text_timer.count(1, len(self.full_dialogue), 0)
      screen.blit(retrofontmedium.render(self.dialogue, False, "White"), (minint(self.rect.x - (retrofontmedium.render(self.full_dialogue, False, "White").get_width() / 1.6), 3), self.rect.y - 50))
    
    elif self.type == "kevser":
      if self.rect.x < 75: self.rect.x += 4; self.frame = self.timer.oscillate(2, 6, 2)
      else:
        self.frame = 1 + int(self.text_index >= 9 and self.text_index < len(self.full_dialogue) - 1)
        full_dialogue = self.full_dialogue[self.text_index]
        try: self.dialogue += full_dialogue[self.text_timer.tally]; bow_sfx.play()
        except: pass
        self.text_timer.count(1, len(full_dialogue), 0)
        screen.blit(retrofontmedium.render(self.dialogue, False, "White"), (5, self.rect.y - 50))
        if self.text_index < len(self.full_dialogue) - 1:
          if k_a or k_start: self.text_index += 1; self.dialogue = ""; self.text_timer.reset(); k_a = False; k_start = False
        else:
          if main.player.state != "holdgreen" and (main.player.state != "walk" or main.player.frame != 0): main.immobilize = not map_string_form[main.minimaps[1]][main.minimaps[0]] == self.origin[2]
          else: main.immobilize = True
        
    elif self.type == "valmore":
      if self.hearts > 0:
        if main.player.rect.x < 75 and main.theme == "Sword of Adham": main.player.rect.x += 2; main.player.state = "walk"; main.player.dir = "right"; main.player.frame = self.timer.keep_count(FPS / 4, 3, 1)
        else:
          if main.immobilize:
            k_right = False; main.theme = "Hollow Bones"
            self.frame = 1 + int(self.text_index >= 12)
            full_dialogue = self.full_dialogue[self.text_index]
            try: self.dialogue += full_dialogue[self.text_timer.tally]; bow_sfx.play()
            except: pass
            self.text_timer.count(1, len(full_dialogue), 0)
            screen.blit(retrofontmedium.render(self.dialogue, False, "White"), (5, self.rect.y - 50))
          else:
              screen.blit(retrofonttiny.render("Valmore HP", True, "White"), (2, HEIGHT - 30))
              for heart in range(math.ceil(self.hearts)): pygame.draw.rect(screen, "White", ((4 + (8 * heart), HEIGHT - 14), (6, 10)), border_radius=2)
              for proj in main.projectiles:
                if self.rect.colliderect(proj.rect) and not isinstance(proj, Projectile): self.hearts -= proj.damage / 8; hit_sfx.play()
              monster_count = 0
              for actor in main.actors:
                if actor.type == "madpuff weak" and actor.alive: monster_count += 1
              if self.behavior_timer.timer(FPS * (3.2 / (int(self.hearts <= 10) + 1))): self.state = "strike"
              if self.state == "strike":
                self.frame = self.timer.count(1, 15, 0)
                if self.frame >= 7:
                  if self.flipped: self.rect.x -= 20
                  elif not self.flipped: self.rect.x += 20
                  if self.rect.colliderect(main.player.rect): main.player.hearts -= 0.6; main.player.hit_timer.time = 1; hit_sfx.play()
                if self.frame == 14: self.state = "spawn"; self.frame = 1; self.flipped = not self.flipped; self.timer.reset()
              if self.state == "spawn":
                self.frame = self.timer.count(10 - (int(self.hearts <= 10) * 6), 4, 0)
                if self.frame == 2 and self.timer.time == 3 and monster_count < 8:
                  for y in range(1 + int(self.hearts < 25) + int(self.hearts < 4) + int(self.hearts < 2)): main.actors.append(Monster("madpuff weak", self.rect.x + (40 * (int(not self.flipped) - int(self.flipped))), (self.rect.y - 50) + (y * 50)))
                if self.frame == 3: self.state = "stand"; self.frame = 1; self.timer.reset()
      else:
        if main.theme == "Hollow Bones": main.immobilize = True
        if main.immobilize:
          if self.state != "defeat":
            main.shake[0] = 3
            for actor in main.actors:
              if isinstance(actor, Monster): actor.hearts = 0
            pygame.mixer.music.load("Sounds/tracks/Tumble.mp3"); pygame.mixer.music.play(0, 0.0)
            self.state = "defeat"
          if pygame.mixer.music.get_busy(): main.shake[0] *= -1; self.frame = 1; self.timer.reset(); self.behavior_timer.reset(); self.text_index = 0; self.full_dialogue = npcs[self.type]["text 2"]; main.theme = "The Gathering"
          elif not pygame.mixer.music.get_busy():
            main.shake[0] = 0
            self.frame = 1 + int(self.text_index >= 11 and self.text_index < len(self.full_dialogue) - 1)
            full_dialogue = self.full_dialogue[self.text_index]
            try: self.dialogue += full_dialogue[self.text_timer.tally]; bow_sfx.play()
            except: pass
            self.text_timer.count(1, len(full_dialogue), 0)
            screen.blit(retrofontmedium.render(self.dialogue, False, "White"), (10, self.rect.y - 50))
      if self.text_index < len(self.full_dialogue) - 1:
        if k_a or k_start: self.text_index += 1; self.dialogue = ""; self.text_timer.reset(); k_a = False; k_start = False
      else:
        if main.immobilize: pygame.mixer.music.load(f"Sounds/tracks/{main.theme}.mp3"); pygame.mixer.music.play(-1, 0.0)
        main.immobilize = not map_string_form[main.minimaps[1]][main.minimaps[0]] == self.origin[2]

    elif self.type == "naman 3":
      if main.theme == "Waves and Flutters" and not pygame.mixer.music.get_busy():
        if self.rect.y < 160: self.rect.y += 4; self.frame = self.timer.keep_count(4, 3, 1)
        else:
          self.frame = 3 + int(self.text_index >= 2 and self.text_index <= 4)
          full_dialogue = self.full_dialogue[self.text_index]
          try: self.dialogue += full_dialogue[self.text_timer.tally]; bow_sfx.play()
          except: pass
          self.text_timer.count(1, len(full_dialogue), 0)
          screen.blit(retrofontmedium.render(self.dialogue, False, "White"), (5, self.rect.y - 50))
          if self.text_index < len(self.full_dialogue) - 1:
            if k_a or k_start: self.text_index += 1; self.dialogue = ""; self.text_timer.reset(); k_a = False; k_start = False
            main.immobilize = True; pygame.mixer.music.stop()
          else:
            if main.immobilize: pygame.mixer.music.load(f"Sounds/tracks/{main.theme}.mp3"); pygame.mixer.music.play(-1, 0.0)
            main.immobilize = not map_string_form[main.minimaps[1]][main.minimaps[0]] == self.origin[2]
    
    elif self.type == "polovo 3":
      if main.player.rect.x > 275: main.player.rect.x -= 3; main.player.state = "walk"; main.player.dir = "left"; main.player.frame = self.timer.keep_count(FPS / 4, 3, 1)
      else:
        if main.immobilize:
          self.frame = 1 + int(self.text_index >= 5 and self.text_index <= 9)
          full_dialogue = self.full_dialogue[self.text_index]
          try: self.dialogue += full_dialogue[self.text_timer.tally]; bow_sfx.play()
          except: pass
          self.text_timer.count(1, len(full_dialogue), 0)
          screen.blit(retrofontmedium.render(self.dialogue, False, "White"), (5, self.rect.y - 50))
          if self.text_index < len(self.full_dialogue) - 1:
            if k_a or k_start: self.text_index += 1; self.dialogue = ""; self.text_timer.reset(); k_a = False; k_start = False
            main.immobilize = True; pygame.mixer.music.stop()
          else: pygame.mixer.music.load(f"Sounds/tracks/Ending.mp3"); pygame.mixer.music.play(-1, 0.0); main.gamestate = 5; main.timer.reset(); main.scrolly = -250

    for item in self.contents:
      if item.alive: item.update()
      else:
        self.contents.remove(item); self.frame = 3; self.contents = []
        if npcs[self.type]["text 2"] != "-": self.full_dialogue = npcs[self.type]["text 2"]; self.dialogue = ""; self.text_timer.reset()
    
    #if not "bow" in main.player.items: self.full_dialogue = "Have a bow, what do ya say?"; self.contents = [Collectible(self.rect.x - 40, self.rect.y, "bow")]
    #else: "Thank you, cool huh?"; self.contents = []; self.frame = 3


class Collectible:
  def __init__(self, type, x, y):
    self.type = type
    self.rect = pygame.Rect((x, y), (16, 16))
    self.frame = 1
    self.state = None
    self.image = pygame.image.load(f"Assets/{self.type}/{self.frame}.png")
    self.position = [self.rect.x + main.minimaps[0], self.rect.y + main.minimaps[1]]
    self.timer = Timer()
    self.value = collictible_types[self.type]["value"]
    self.arrow = collictible_types[self.type]["arrow"]
    self.heart = collictible_types[self.type]["heart"]
    self.price = collictible_types[self.type]["price"]
    self.title = collictible_types[self.type]["title"]
   #self.sound = collictible_types[self.type]["sound"]
    self.paid = 0
    self.bought = False
    self.solid = False
    self.origin = [x, y, map_string_form[main.minimaps[1]][main.minimaps[0]]]
    self.object = "collectible"
    self.held = False
    self.alive = type != ""
    if self.rect.x == 0: self.rect.x += 1
    if self.rect.y == 0: self.rect.y += 1

  def update(self):
    if not self.bought:
      self.image = pygame.image.load(f"Assets/{self.type}/{self.frame}.png")
      if not self.held: screen.blit(self.image, self.rect)
      if self.price > 0: screen.blit(retrofontsmall.render(str(self.price) + " Liras", False, "White"), (self.rect.x - 20, self.rect.y + 20))
      self.frame = int(self.timer.wait(FPS / (16 - (self.type == "arrow" * 15)))) + 1

      if self.rect.colliderect(main.player.rect) and main.player.wealth >= self.price:
        if type(self.value) == int: main.player.wealth += self.value
        elif not self.held: main.player.items.append(self.value)
        main.player.arrows += self.arrow
        main.player.hearts += self.heart
        if collictible_types[self.type]["sound"] != "-":
          if self.title == "-": collictible_types[self.type]["sound"].play(); self.bought = True
          else:
            if not self.held: pygame.mixer.music.load(f"Sounds/tracks/{collictible_types[self.type]['sound']}.mp3"); pygame.mixer.music.play(1, 0.0)
            self.held = True
            main.immobilize = True
            main.player.dir = "front"
            if self.frame - 1 or pygame.mixer.music.get_pos() / 1000 > 1.5: screen.blit(retrofont.render(self.title, False, "White"), (3, 2))
            if pygame.mixer.music.get_pos() / 1000 < 4.8:
              if   self.type == "renk 1": main.player.state = "holdred"; main.player.renks[self.type] = True
              elif self.type == "renk 2": main.player.state = "holdyellow"; main.player.renks[self.type] = True
              elif self.type == "renk 3": main.player.state = "holdgreen"; main.player.renks[self.type] = True; main.theme = "Sword of Adham"
              elif self.type == "renk 4": main.player.state = "holdblue"; main.player.renks[self.type] = True; main.theme = "Waves and Flutters"
              elif self.type == "adham sword": main.player.state = "holdsword"; main.player.renks[self.type] = True
            else: main.player.state = "walk"; main.player.frame = 0
            if not pygame.mixer.music.get_busy():
              self.bought = True
              if self.type != "renk 4": pygame.mixer.music.load(f"Sounds/tracks/{main.theme}.mp3"); pygame.mixer.music.play(-1, 0.0); main.immobilize = False; main.player.frame = 1
              else:
                for actor in [actor for actor in main.actors if actor.type == "naman 3"]: actor.rect.y = 1
        else: self.bought = True
          
      for proj in main.projectiles:
        if isinstance(proj, Grapple) and self.price <= 0:
          if proj.retract and self.rect.colliderect(proj.rect):
            if proj.length > 40: grapple_sfx.play()
            if proj.length > 15: self.rect.x, self.rect.y = proj.rect.x, proj.rect.y

    else:
      if self.price: self.pay()
      else: self.alive = False

  def pay(self):
    if not self.paid > self.price: main.player.wealth -= 1; self.paid += 1; change_by_sfx.play()
    if not self.paid > self.price - 15: main.player.wealth -= 10; self.paid += 10
    self.alive = not self.paid >= self.price
  

class Projectile:
  def __init__(self, x, y, angle, can_shoot, damage=0.5):
    self.rect = pygame.Rect((x, y), (16, 16))
    self.bool = True
    self.colors = ["Red", "Yellow"]
    self.speed = 5
    self.damage = damage
    self.dirx = self.speed * math.cos(angle)
    self.diry = self.speed * math.sin(angle)
    self.lifetime = 4 - ((not can_shoot) * 3.9)
    self.timer = Timer()
    self.can_shoot = can_shoot
    self.alive = True

  def update(self):
    if self.can_shoot: pygame.draw.rect(screen, self.colors[self.bool], self.rect, border_radius=8)
    self.bool = not self.bool
    self.rect.move_ip(-self.dirx, -self.diry)
    if not self.can_shoot: self.rect.move_ip(-self.dirx, -self.diry); self.rect.move_ip(-self.dirx, -self.diry); self.rect.move_ip(-self.dirx, -self.diry)
    if self.timer.timer(self.lifetime * FPS): self.alive = False


class Arrow:
  def __init__(self, x, y, dir, other_weapon=False, adham_sword=False):
    self.image = pygame.image.load(f"Assets/tuff/arrow{dir}.png").convert_alpha()
    self.rect = pygame.Rect((x, y), (16, 16))
    self.dir = dir
    self.lifetime = 0.7
    self.timer = Timer()
    self.alive = True
    self.damage = 1
    self.not_bow = other_weapon
    if other_weapon: self.lifetime = 0.2
    if adham_sword: self.lifetime = 0.4; self.damage = 2
    self.not_hook = True

  def update(self):
    if not self.not_bow: screen.blit(self.image, self.rect)
    if self.dir == "right": self.rect.x += 15
    if self.dir == "left": self.rect.x -= 15
    if self.dir == "front": self.rect.y += 15
    if self.dir == "back": self.rect.y -= 15
    if self.timer.timer(self.lifetime * FPS): self.alive = False


class Grapple:
  def __init__(self, x, y, dir, user):
    self.rect = pygame.Rect((x, y), (32, 32))
    self.dir = dir
    self.length = 0
    self.retract = False
    self.alive = True
    self.player = user
    self.not_bow = True
    self.not_hook = False
    self.damage = 1

  def update(self):
    pygame.draw.line(screen, "Grey", (self.player.rect.x + 15, self.player.rect.y + 15), (self.rect.x + 15, self.rect.y + 15), width=2)
    #pygame.draw.rect(screen, "White", self.rect)
    if self.dir == "right": self.rect.x = self.player.rect.x + self.length
    if self.dir == "left": self.rect.x = self.player.rect.x - self.length
    if self.dir == "front": self.rect.y = self.player.rect.y + self.length
    if self.dir == "back": self.rect.y = self.player.rect.y - self.length
    if self.retract: self.length -= 9
    else: self.length += 7
    if self.length > 50 and not self.retract: self.retract = True
    if self.length <= 2 and self.retract: self.alive = False; self.player.state = "walk"
    

def collision_test(rect, tiles):
  hit_list = []
  for tile in tiles:
    if rect.colliderect(tile):
      hit_list.append(tile)
  return hit_list

k_right, k_left, k_down, k_up, k_a, k_up2, k_select, k_start = False, False, False, False, False, False, False, False
k_debug = False

def run():
  global k_down, k_up, k_right, k_left, k_a, k_up2, k_select, k_start, k_debug
  if main.gamestate != 4: k_a, k_left, k_right, k_up, k_down, k_start = False, False, False, False, False, False
  if main.gamestate != 2: k_select = False
  k_start = False
  for event in pygame.event.get():
    if event.type == pygame.QUIT: main.quit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_RETURN: k_start = True
      if event.key == pygame.K_e or event.key == pygame.K_SPACE: k_a = True
      if event.key == pygame.K_RIGHT or event.key == pygame.K_d: k_right = True
      if event.key == pygame.K_LEFT or event.key == pygame.K_a: k_left = True
      if event.key == pygame.K_UP or event.key == pygame.K_w: k_up = True
      if event.key == pygame.K_DOWN or event.key == pygame.K_s: k_down = True
      if event.key == pygame.K_i: k_select = True
      #if event.key == pygame.K_z: k_debug = True
      if event.key == pygame.K_ESCAPE:
        if main.gamestate == 1: main.gamestate = 0; main.scrolly = 0; main.started = False; pygame.mixer.music.load("Sounds/tracks/Sound the Lost Page.mp3"); pygame.mixer.music.play(-1, 0.0)
        elif main.gamestate == 4: main.gamestate = 1; pygame.mixer.music.stop(); main.end_game()
        elif main.gamestate == 2: main.gamestate = 1
        else: main.quit()
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_RETURN: k_start = False
      if event.key == pygame.K_SPACE or event.key == pygame.K_e: k_a = False
      if event.key == pygame.K_RIGHT or event.key == pygame.K_d: k_right = False
      if event.key == pygame.K_LEFT or event.key == pygame.K_a: k_left = False
      if event.key == pygame.K_UP or event.key == pygame.K_w: k_up = False
      if event.key == pygame.K_DOWN or event.key == pygame.K_s: k_down = False
      if event.key == pygame.K_i: k_select = False
      #if event.key == pygame.K_z: k_debug = False
    if event.type == JOYBUTTONDOWN:
      if event.button == 0:
        if main.gamestate == 0: k_a = True
        else: k_a = True #x A
      if event.button == 1: k_select = True #menu
      if event.button == 2: k_a = True #□ X
      if event.button == 3: k_select = True #△ Y
      if event.button == 4: pygame.image.save(screen, "screenshot.png"); #share
      if event.button == 5: k_start = True #PS
      if event.button == 6:
        if main.gamestate == 0: k_select = True
        elif main.gamestate > 0: main.gamestate = 0; main.reset() #menu
      if event.button == 7:
        if main.gamestate == 0: k_start = True #L3
      if event.button == 8: k_start = True #R3
      if event.button == 9: k_start = True #L1 LB
      if event.button == 10: k_select = True #R1 RB
      if event.button == 11: k_up = True #up
      if event.button == 12: k_down = True #down
      if event.button == 13: k_left = True #left
      if event.button == 14: k_right = True #right
      if event.button == 15: pygame.image.save(screen, "screenshot.png"); #pad
    if event.type == JOYAXISMOTION:
      if abs(event.value) > 0.1:
        k_up, k_down = False, False
        if event.axis == 0:
          if event.value < -0.5: k_left = True #go left
          else: k_left = False
          if event.value > 0.5: k_right = True #go right
          else: k_right = False
        if event.axis == 1:
          if event.value < -0.5 + (main.gamestate == 0) / 5: k_up = True #go up
          else: k_up = False
          if event.value > 0.4 + (main.gamestate == 0) / 5: k_down = True #go down
          else: k_down = False
        if event.axis == 2:
          if event.value < -0.6: pass #look left
          if event.value > 0.6: pass #look right
        if event.axis == 3:
          if event.value < -0.6: pass #look up
          if event.value > 0.6: pass #look down
    if event.type == JOYBUTTONUP:
      if event.button == 0: k_a = False #x A
      if event.button == 1: k_select = False #o B
      if event.button == 2: k_a = False #□ X
      if event.button == 3: k_select = False #△ Y
      if event.button == 4: pass #share
      if event.button == 5: pass #PS
      if event.button == 6: pass #menu
      if event.button == 7: pass #L3
      if event.button == 8: pass #R3
      if event.button == 9: pass #L1 LB
      if event.button == 10: pass #R1 RB
      if event.button == 11: k_up = False #up
      if event.button == 12: k_down = False #down
      if event.button == 13: k_left = False #left
      if event.button == 14: k_right = False #right
      if event.button == 15: pass #pad
    if event.type == JOYDEVICEADDED:
      joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
      print("Current Controller Devices:", joysticks)
      for joystick in joysticks:
        print(joystick.get_name())
    if event.type == JOYDEVICEREMOVED:
      joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
      print("Current Controller Devices:", joysticks)
      for joystick in joysticks:
        print(joystick.get_name())
  if k_down and k_up and pygame.mouse.get_pressed(): pygame.image.save(screen, "screenshot.png")
  display.fill("Black")
  display.blit(screen, (0 + main.shake[0], 0 + main.shake[1]))
  pygame.display.update()
  screen.fill("Black")
  clock.tick(FPS)

#out_ = open("Saves/memory_card/savefile.txt", "wb"); pickle.dump(saves, out_); out_.close()
try:
  in_ = open("Saves/memory_card/savefile.txt", "rb"); saves = pickle.load(in_)

  print("JSON serializer", "Enabling ReadableBuffer"); print("SAVES FOUND!", open("Saves/memory_card/savefile.txt", "rb"))
except: print("No memory card inserted - if you want to keep saves, install the card in the itch.io page.")

class Decoy:
  def play(self): pass

decoy = Decoy()
main = Main()

main.player = Player()

while True:
  main.update()