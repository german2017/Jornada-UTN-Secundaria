import pygame
import json
import sqlite3
from os import walk

# Volumen
class Volume():
    def __init__(self):
        self.music_volume = 0.5
        self.sfx_volume = 0.5

volume = Volume()
tile_size = 32

# Level layout
#╔  ╗  ╚  ╝ ^

level_1 = {
    'bg':"resources/graphics/bg/1.png",
    'level_layout':[
    '                                        ',
    '                                        ',
    '777776                                  ',
    ' cKc           c                        ',
    '                                        ',
    '3333333333333334                        ',
    '╔77777777777╗╔76   c     c              ',
    '5           15                          ',
    '5   c      c15 H   0     0    c         ',
    '5          c15        S                 ',
    '5c  2334    1╚334^^^^^^^^^^^234         ',
    '5   87╗╚34  1999╚33333333333╝╔6    c    ',
    '╚4    87╗5  877777777777777776          ',
    '95  c   15c                      234    ',
    '9╚4     15c                      876   c',
    '99╚34   15c             c               ',
    '77776   15c         cc                 2',
    'E      2╝5c   cc        24            2╝',
    'E      195c     c   00  15   B     B  19',
    'ED  P 2╝95         ^^^^^1╚333333333333╝9',
    '333333╝99╚3334  23333333╝999999999999999'
    ],'limits':[
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '           ¡                            ',
    '                                        ',
    '            }                           ',
    '          ¡ }                           ',
    '         }  }                           ',
    '         }  }                           ',
    '         }                              ',
    '         } ¡                            ',
    '         }                              ',
    '         }               !            ! ',
    '         }                              ',
    '         }                              ',
    '          ¡                             ',
    '                                        '
    ],'song':'resources/music/level_1.ogg',
    'time':120, 'best_time_score':9000
}

level_2 = {
    'bg':"resources/graphics/bg/2.png",
    'level_layout':[
    '                                        ',
    '                                        ',
    '76                       15  86         ',
    '     H                   15             ',
    '           c             15  cc         ',
    '4000000   234            15  DD         ',
    '5   cc    195            15  24c        ',
    '5         195g           15  15   cccc  ',
    '5  2333333╝9╚33333334   c15  15         ',
    '5  1╔77777╗99╔7777776    15  15  233334 ',
    '5  15     19╔6   c c    015  15 c1╔7776 ',
    '5  15  cc 195            15  15  15     ',
    '5  86 c  c195            15  15  15cKc  ',
    '5      00c195         G  15  15  15 S  2',
    '5  c      195c   23333333╝5  15c 1╚3333╝',
    '5         195    8777777776  15  8777777',
    '╚3333334  1950     c    c    15         ',
    '77777776  195                15         ',
    'E c       195                15       P ',
    'E         195g              ^15  2333333',
    '3333333333╝9╚3333333333333333╝5  1999999'
    ],'limits':[
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                               ¡        ',
    '                              }         ',
    '                              }         ',
    '                              }         ',
    '                              } ¡       ',
    '                              }  }      ',
    '                              }  }      ',
    '                                 }      ',
    '                               ¡ }      ',
    '                              }  }      ',
    '                              }  }      ',
    '                              }         ',
    '                              } ¡       ',
    '                              }         ',
    '                              }         ',
    '                               ¡        '
    ],'song':'resources/music/level_2.mp3',
    'time':120, 'best_time_score':7500
}

level_3 = {
    'bg':"resources/graphics/bg/3.png",
    'level_layout':[
    '                                        ',
    '                                        ',
    '9999999995K         0   0        15     ',
    '9999999995                       15     ',
    '╔77777777600 c  c   c   c   c   O15    P',
    '5                   L   l        15  233',
    '5   c        0^^0^^^0^^^0^^^0  c 15  877',
    '5     L      8777777777777776    15     ',
    '5   233334                     0 15  c  ',
    '5 23╝╔77╗5                       15^    ',
    '5 8776cO15                       1╚334  ',
    '5       15            c          1╔876  ',
    '5       15 S                  G  15     ',
    '5 c     1╚333333334  233333333333╝5 c   ',
    '5    G  199999╔7776  8777╗999999995    ^',
    '5 233333╝99╔776          877╗999995 2333',
    '5 8777777776     c    c     8777776 877╗',
    '5             c          c             1',
    '5 c   c   c     234  234       c    c O1',
    '5 B   B   B  233╝95EE19╚334  l   L     1',
    '╚333333333333╝99995DD19999╚333333333333╝'
    ],'limits':[
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    ' ¡                              ¡       ',
    '                                 }      ',
    '}                                }      ',
    '}                                }      ',
    '}                                }      ',
    '}                                }      ',
    '}                                }      ',
    '}                               ¡       ',
    '}                                       ',
    '}                                       ',
    '}                                       ',
    '}                                       ',
    '}                                       ',
    '!            !                          ',
    ' ¡                                      ',
    '                                        '
    ],'song':'resources/music/level_3.mp3',
    'time':120, 'best_time_score':8500
}

boss_level = {
    'bg':"resources/graphics/bg/boss.png",
    'level_layout':[
    '                                        ',
    '                                        ',
    '                                        ',
    '          77777777777777777777          ',
    '         5                    1         ',
    '         5                    1         ',
    '         5                   H1         ',
    '         5 R                  1         ',
    '         5                    1         ',
    '         5                    1         ',
    '         5                    1         ',
    '         5                    1         ',
    '         5                    1         ',
    '         5                    1         ',
    '         5                    1         ',
    '         5          P         1         ',
    '         5                    1         ',
    '         5                    1         ',
    '         5                    1         ',
    '          33333333333333333333          ',
    '                                        '
    ],'limits':[
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '                                        ',
    '          ¡                  ¡          ',
    '                                        ',
    '         }                    }         ',
    '         }                    }         ',
    '         }                    }         ',
    '         }                    }         ',
    '         }                    }         ',
    '         }                    }         ',
    '         }                    }         ',
    '         }                    }         ',
    '         }                    }         ',
    '         }                    }         ',
    '         }                    }         ',
    '                                        ',
    '          ¡                  ¡          ',
    '                                        '
    ],'song':'resources/music/boss.ogg',
    'time':120, 'best_time_score':8600
}

levels = {
    '1':level_1,
    '2':level_2,
    '3':level_3,
    'boss':boss_level
}

# # Functions
def import_folder(path:str, size:tuple):
    surfaces_list = []
    
    for _,_,img_files in walk(path):
        for img in img_files:
            full_path = path + '/' + img
            img_surface = pygame.image.load(full_path)
            img_surface = pygame.transform.scale(img_surface,(size)).convert_alpha()
            surfaces_list.append(img_surface)

    return surfaces_list

def time_format(number):
    mins = int(number / 60)
    mins_zeros = ''
    secs = number % 60
    secs_zeros = ''

    if mins < 10:
        mins_zeros = '0'
    if secs < 10:
        secs_zeros = '0'

    time = f"{mins_zeros}{mins}:{secs_zeros}{secs}"
    return time

# Levels ranks and scores
def calculate_rank(best_score, player_score, hits):
    if player_score >= best_score and hits == 0:
        rank = 'S+'
    elif player_score >= int(best_score*0.9) and hits <= 1:
        rank = 'S'
    elif player_score >= int(best_score*0.8) and hits <= 1:
        rank = 'A'
    elif player_score >= int(best_score*0.7) and hits <= 2:
        rank = 'B'
    elif player_score >= int(best_score*0.6) and hits <= 2:
        rank = 'C'
    else:
        rank = 'D'
            
    return rank

def calculate_higher_rank(rank_1, rank_2):
    rtn = ''
    if rank_2:
        if rank_1 == 'S' or rank_1 == 'S+':
            if rank_2 == 'S' or rank_2 == 'S+':
                if rank_1 > rank_2:
                    rtn = 1
                elif rank_1 < rank_2:
                    rtn = 2
                else:
                    rtn = 0
            else:
                rtn = 1
        elif rank_2 == 'S' or rank_2 == 'S+':
            rtn = 2
        else:
            if rank_1 < rank_2:
                rtn = 1
            elif rank_1 > rank_2:
                rtn = 2
            else:
                rtn = 0
    else:
        rtn = 1
    
    return rtn

# Json
def create_stats_json():
    # Json existence check
    try:
        with open("player stats.json", "r"):
            pass
    except Exception:
        level = {
            "score":0,
            "hits":0,
            "rank":''
        }
        data = {
            '1':level,
            '2':level,
            '3':level,
            'boss':level
        }
        with open("player stats.json", 'w') as file:
            json.dump(data, file, indent=4)

def level_stats_dict(player):
    lvl_stats = {
        'score':player.score,
        'hits':player.hits,
        'rank':player.rank
    }
    return lvl_stats

def save_level_stats(player, level):
    with open("player stats.json") as file:
        data = json.load(file)
    level_stats = level_stats_dict(player)
    save_data = False
    higher_rank = calculate_higher_rank(level_stats['rank'],
                                        data[level]['rank'])
    
    if higher_rank == 1:
        save_data = True
    elif higher_rank == 0 and\
        level_stats['score'] > data[level]['score']:
        save_data = True
    
    if save_data:
        data[level]['score'] = level_stats['score']
        data[level]['hits'] = level_stats['hits']
        data[level]['rank'] = level_stats['rank']
        with open("player stats.json", 'w') as file:
            json.dump(data, file, indent=4)
    
    return save_data

def total_score():
    with open("player stats.json") as file:
        data = json.load(file)
    
    total = 0

    for level in data:
        total += data[level]['score']

    return total

def delete_data_json():
    level = {
            "score":0,
            "hits":0,
            "rank":''
        }

    data = {
        '1':level,
        '2':level,
        '3':level,
        'boss':level
    }
    with open("player stats.json", 'w') as file:
        json.dump(data, file, indent=4)

def get_level_permissions():
    with open("player stats.json") as file:
        data = json.load(file)
    
    permissions = {
        '1':True,
        '2':False,
        '3':False,
        'boss':False,
    }

    permission = True
    for level in data:
        permissions[level] = permission
        if data[level]['rank'] == 'S+' or\
            data[level]['rank'] == 'S' or\
            data[level]['rank'] == 'A':
            permission = True
        else:
            permission = False

    return permissions

# SQL data base
def create_scores_db():
    with sqlite3.connect("scores database.db") as connection:
        try:
            sentence = '''
                        CREATE TABLE Scores
                        (
                            id integer PRIMARY KEY AUTOINCREMENT,
                            username text,
                            lvl1 integer,
                            lvl2 integer,
                            lvl3 integer,
                            lvlboss integer,
                            total integer
                        )
                        '''
            connection.execute(sentence)
            sentence = '''INSERT INTO Scores (username,lvl1,lvl2,lvl3,lvlboss,total)
                        VALUES("User",0,0,0,0,0)'''
            connection.execute(sentence)
            sentence = '''INSERT INTO Scores (username,lvl1,lvl2,lvl3,lvlboss,total)
                        VALUES("Doomer",13200,14800,14400,18500,60900)'''
            connection.execute(sentence)
            sentence = '''INSERT INTO Scores (username,lvl1,lvl2,lvl3,lvlboss,total)
                        VALUES("Mark",13000,14600,13900,18200,59800)'''
            connection.execute(sentence)
            sentence = '''INSERT INTO Scores (username,lvl1,lvl2,lvl3,lvlboss,total)
                        VALUES("Melody",12900,14400,13700,18100,59100)'''
            connection.execute(sentence)
            sentence = '''INSERT INTO Scores (username,lvl1,lvl2,lvl3,lvlboss,total)
                        VALUES("ARandomGuy",12700,14300,13500,17600,58100)'''
            connection.execute(sentence)
            sentence = '''INSERT INTO Scores (username,lvl1,lvl2,lvl3,lvlboss,total)
                        VALUES("TheWorst",12000,13900,13100,16400,55400)'''
            connection.execute(sentence)
        except Exception as e:
            pass

def update_scores_db(level, score):
    with sqlite3.connect("scores database.db") as connection:
        try:
            total = total_score()
            sentence = f'''UPDATE Scores
                        SET lvl{level} = ?,
                            total = ?
                        WHERE id = 1''' 
            connection.execute(sentence,(score,total))
        except Exception as e:
            print(f"Update scores db: {e}")

def delete_data_db():
    with sqlite3.connect("scores database.db") as connection:
        try:
            sentence = '''UPDATE Scores 
                        SET lvl1 = 0,
                            lvl2 = 0,
                            lvl3 = 0,
                            lvlboss = 0,
                            total = 0
                        WHERE id = 1'''
            connection.execute(sentence)
        except Exception as e:
            print(e)

def get_all_scores():
    with sqlite3.connect("scores database.db") as connection:
        try:
            sentence = '''SELECT lvl1, lvl2, lvl3, lvlboss, total
                        FROM Scores
                        WHERE id = 1'''
            data = connection.execute(sentence)
            for fila in data:
                scores = list(fila)
        except Exception as e:
            print(f"Get all scores: {e}")
    
    return scores

def save_username(new_username):
    try:
        with sqlite3.connect("scores database.db") as connection:
            sentence = '''UPDATE Scores
                        SET username = ?
                        WHERE id = 1'''
            connection.execute(sentence,(new_username,))
    except Exception as e:
        print(f"Save username: {e}")

def obtain_top_5_players_data():
    top_5_players = {
        '1':None,
        '2':None,
        '3':None,
        '4':None,
        '5':None,
    }

    try:
        with sqlite3.connect("scores database.db") as connection:
            sentence = '''SELECT username,total FROM Scores
                        ORDER BY total DESC LIMIT 5'''
            data = connection.execute(sentence)
            counter = 0
            for file in data:
                player = {}
                counter += 1

                player['username'] = file[0]
                player['total'] = file[1]

                top_5_players[str(counter)] = player
    except Exception as e:
        print(f"Obtain leaderboard data: {e}")
    
    return top_5_players

# # Data collections

# Font
fonts = {
    '0':'','1':'','2':'','3':'','4':'','5':'','6':'','7':'','8':'','9':'',
    'a':'','b':'','c':'','d':'','e':'','f':'','g':'','h':'','i':'','j':'',
    'k':'','l':'','m':'','n':'','o':'','p':'','q':'','r':'','s':'','t':'',
    'u':'','v':'','w':'','x':'','y':'','z':'','!':'','?':'',',':'','.':'',
    '"':'',':':'','#':'','$':'','-':'','+':'','*':'','/':'','%':'','=':'',
    '(':'',')':'','[':'',']':'', ' ':''
}

list_of_fonts = import_folder("resources/graphics/font", (32,24))

for font_index,font in enumerate(fonts):
    fonts[font] = list_of_fonts[font_index]

# Health
health_bar_img = pygame.image.load("resources/graphics/characters/health/bar.png")
width = health_bar_img.get_width() * 3
height = health_bar_img.get_height() * 3
health_bar_img = pygame.transform.scale(health_bar_img, (width, height))

lives = {
    '1':{'img':'', 'pos':(1152, 22)},
    '2':{'img':'', 'pos':(1122, 22)},
    '3':{'img':'', 'pos':(1092, 22)}
}
live_img = pygame.image.load("resources/graphics/characters/health/live.png")
width = live_img.get_width() * 3
height = live_img.get_height() * 3
live_img = pygame.transform.scale(live_img, (width, height))
for live in lives.keys():
    lives[live]['img'] = live_img

names_initial = {
    'x':'',
    'bill':''
}

name_initial_img = pygame.image.load("resources/graphics/characters/health/x.png")
width = name_initial_img.get_width() * 3
height = name_initial_img.get_height() * 3
names_initial['x'] = pygame.transform.scale(name_initial_img, (width, height))

name_initial_img = pygame.image.load("resources/graphics/characters/health/b.png")
width = name_initial_img.get_width() * 3
height = name_initial_img.get_height() * 3
names_initial['bill'] = pygame.transform.scale(name_initial_img, (width, height))


# Characters

x_dict = {
    'bullet_path':"resources/graphics/characters/x/bullet",
    'bullet_size':(16,12),
    'bullet_spawn_xright':24,
    'bullet_spawn_xleft':10,
    'bullet_spawn_y':27
}

bill_dict = {
    'bullet_path':"resources/graphics/characters/bill/bullet",
    'bullet_size':(12,12),
    'bullet_spawn_xright':12,
    'bullet_spawn_xleft':0,
    'bullet_spawn_y':27,
    'bullet_spawn_ycrouch':67
}

characters = {
    'x':x_dict,
    'bill':bill_dict
}