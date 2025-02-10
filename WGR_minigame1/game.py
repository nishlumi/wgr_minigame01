import pyxel
# title: Warship-Girls mini game
# author: ISHII Eiju
# desc: Mini shooting game for Warship-Girls R
# license: MIT
# version: 1.0

AUTHOR = "@lumidina"
SCREEN_WIDTH = 8 * 15
SCREEN_HEIGHT = 8 * 20
STONE_INTERVAL = 30
START_SCENE = "start"
PLAY_SCENE = "play"
CONFIG_SCENE = "config"
GAME_OVER_DISPLAY_TIME = 60
PLAYER_IMAGE_W = 16
IMGPLT_1 = 0
IMGPLT_2 = 1
IMGPLT_3 = 2
IMGPLT_4 = 3
SHOT_IMAGEINDEX_X = 0
SHOT_IMAGEINDEX_Y = 8
SHOT_IMAGEINDEX_W = 8
SHOT_IMAGEINDEX_H = 8
SINGLE_FONTSIZE = 8
DOUBLE_FONTSIZE = 16
IMG_CONFIG_CHECK_X = 8
IMG_CONFIG_CHECK_Y = 64
IMG_CONFIG_UNCHECK_X = 0
DASH_COOLTIME = 10
ENEMY_MOTION_FPS = 15
MODE_TIME_LIST = (30, 45, 60)
MODE_RESULT_S = (30, 40, 50)
MODE_RESULT_A = (20, 30, 35)

class SoundManager:
    def __init__(self):
        self.bgm_ch0 = 0
        self.bgm_ch1 = 1
        self.defeat_enemy = 2
        self.shoot_ch2 = 3
        self.shoot_ch3 = 4
        self.healing = 5
        self.player_damage = 6
        self.bgm_gameover = 7
        self.bgm_finish_ch0 = 8
        self.bgm_finish_ch1 = 9
        self.show_rank = 10
        
    def play_shoot(self):
        pyxel.play(2, self.shoot_ch2)
        pyxel.play(3, self.shoot_ch3)
    
    def play_gameclear(self):
        pyxel.playm(1,loop=False)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bkx = x
        self.bky = y
        self.w = 16
        self.h = 16
        self.hp = 2
        self.maxhp = 2
        self.img_page = 0
        self.health_img_x = 0
        self.health_img_y = 80
    
    def draw(self):
        pyxel.blt(self.x, self.y, self.img_page, self.health_img_x, self.health_img_y, self.w, self.h, pyxel.COLOR_BLACK)
    
    def update(self, start_dash: bool, dir: int):
        self.x += dir
        if start_dash:
            self.x += dir
        if self.x > self.bkx:
            self.health_img_y = 96
        elif self.x < self.bkx:
            self.health_img_y = 112
        else:
            self.health_img_y = 80
                
        
        self.bkx = self.x
    
    def damage(self):
        self.hp -= 1
        if self.hp < 2:
            self.health_img_x = 16
    
    def recovery(self):
        self.hp += 1
        if self.hp > 1:
            self.health_img_x = 0
    
    def death(self):
        if self.hp <= 0:
            self.health_img_x = 16
            self.health_img_y = 64
        
class Shot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 8
        self.h = 8
        
        self.img_page = 0
        self.speed = 7
        
    def update(self, start_dash: bool):
        if pyxel.frame_count % self.speed:
            if self.y >= 0:
                self.y -= 1
                if start_dash:
                    self.y -= 1
    
    def draw(self):
        pyxel.blt(self.x, self.y, self.img_page, SHOT_IMAGEINDEX_X, SHOT_IMAGEINDEX_Y, SHOT_IMAGEINDEX_W, SHOT_IMAGEINDEX_H, pyxel.COLOR_BLACK)

class Damecon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img_page = 0
        self.speed = 1
        
    def update(self):
        if self.y < SCREEN_HEIGHT:
            self.y += self.speed
    
    def draw(self):
        pyxel.blt(self.x, self.y, self.img_page, 8, 8, 8, 8, pyxel.COLOR_BLACK)
    

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img_page = 1
        self.speed = 1
        self.lv = 1
        self.w = 8
        self.h = 8
        self.motionlst = [(8,0),(8,8)]
        self.motioninx = 0
        
        # LV2 enemy by 1/5 
        if pyxel.rndi(1, 5) == 1:
            self.lv = 2
            self.speed = 2
            self.w = 16
            self.h = 16
            self.motionlst = [(16,0),(16,16)]
        
        self.hp = self.lv
    
    def is_defeat(self):
        if self.hp <= 0:
            return True
        else:
            return False
    
    def update(self):
        if self.y < SCREEN_HEIGHT:
            self.y += self.speed
            
    def draw(self):        
        motpage = self.motionlst[self.motioninx]
        pyxel.blt(self.x, self.y, self.img_page, motpage[0], motpage[1], self.w, self.h, pyxel.COLOR_NAVY)
        if pyxel.frame_count % ENEMY_MOTION_FPS == 0:
            self.motioninx += 1
            if self.motioninx > 1:
                self.motioninx = 0
            
                
    
    def check_player_collision(self, player: Player):
        return (
            player.x < self.x + self.w
            and
            player.x + player.w > self.x
            and
            player.y < self.y + self.h
            and
            player.y + player.h > self.y
        )
    
    def check_shooting(self, shot: Shot):
        #print(self.x, self.y, shot.x, shot.y)
        """if  (
            shot.x - 4 <= self.x <= shot.x + 8
            and
            self.y + self.h > shot.y
            and
            shot.y + SHOT_IMAGEINDEX_H > self.y
        ):
            return True
        else:
            return False"""
        return (
            shot.x < self.x + self.w
            and
            shot.x + shot.w > self.x
            and
            shot.y < self.y + self.h
            and
            shot.y + shot.h > self.y
        )
            


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Warship-Girls R MINI Game")
        pyxel.mouse(True)
        pyxel.load("my_resource.pyxres")
        self.jp_font = pyxel.Font("umplus_j10r.bdf")
        self.jp_font12 = pyxel.Font("umplus_j12r.bdf")
        self.se = SoundManager()
        self.setup_config()
        self.current_scene = START_SCENE
        if self.config["use_sound"]:
            pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)
        
    def posx(self,val):
        #return SCREEN_WIDTH // 20 * val
        return 8 * val
    def posy(self,val):
        #return SCREEN_HEIGHT // 20 * val
        return 8 * val

    def setup_config(self):
        self.config = {
            "use_sound": False,
            "mode_time" : 30,
        }
    def reset_play_scene(self):
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT * 4 // 5
        self.player_hp = 2
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 4 // 5)
        self.enemies = []
        self.shots = []
        self.damecons = []
        self.is_collision = False
        self.game_over_display_timer = GAME_OVER_DISPLAY_TIME
        self.points = 0
        self.timeup_dash = 10
        self.start_dash = False
        self.play_time = self.config["mode_time"]
        self.play_result_s = MODE_RESULT_S[0]
        self.play_result_a = MODE_RESULT_A[0]
        self.is_gameclear = False
        self.is_showrank = False
        self.gameclear_inverval = 0
        self.clearrank_posy = 192
    
    def check_anykey(self):
        ishit = False
        for key in range(256):
            if pyxel.btnp(key):
                print(f"key={key}")
                ishit = True
                break
        
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            ishit = True
        
        if (
            pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)
            or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)
            or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)
            or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y)
            or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START)
        ):
            ishit = True
        return ishit
    
    def check_mouse_playscreen(self):
        return (0 <= pyxel.mouse_x <= SCREEN_WIDTH) and (0 <= pyxel.mouse_y <= SCREEN_HEIGHT - 16)            
        
    
    def update_start_scene(self):
        #if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
        #    self.reset_play_scene()
        #    self.current_scene = PLAY_SCENE
        
        #---to play
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if (
                (self.posx(1) <= pyxel.mouse_x <= self.posx(1) + SINGLE_FONTSIZE * 5)
                and
                (self.posy(17) <= pyxel.mouse_y <= self.posy(17) + SINGLE_FONTSIZE)
            ):
                self.reset_play_scene()
                self.current_scene = PLAY_SCENE
        
        #---to option
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if (
                (self.posx(10) <= pyxel.mouse_x <= self.posx(10) + SINGLE_FONTSIZE * 6)
                and
                (self.posy(17) <= pyxel.mouse_y <= self.posy(17) + SINGLE_FONTSIZE)
            ):
                self.current_scene = CONFIG_SCENE
            
    
    def update_play_scene(self):
        # game over 
        if self.is_collision:
            if self.game_over_display_timer > 0:
                self.game_over_display_timer -= 1
            else:
                ishit = self.check_anykey()
                
                if ishit:
                    self.current_scene = START_SCENE
                    if self.config["use_sound"]:
                        pyxel.playm(0, loop=True)
            return

        # count play time
        if pyxel.frame_count % 30 == 0 and self.play_time > 0:
            self.play_time -= 1
            
        #---prepare game clear
        if self.play_time <= 0 and not self.is_gameclear:
            #pyxel.play(0, self.se.bgm_finish_ch0)
            #pyxel.play(1, self.se.bgm_finish_ch1)
            if self.config["use_sound"]:
                self.se.play_gameclear()
            
            if pyxel.frame_count % 30 == 0:
                self.gameclear_inverval += 1
                
            if self.gameclear_inverval > 1:
                self.is_gameclear = True
            
            return
        
        #---complete game clear, prepare show rank
        if self.is_gameclear and not self.is_showrank:
            if pyxel.frame_count % 30 == 0:
                self.gameclear_inverval += 1
                
            if self.gameclear_inverval > 4 and not self.is_showrank:
                self.is_showrank = True
                if self.config["use_sound"]:
                    pyxel.stop(0)
                    pyxel.stop(1)
                    pyxel.play(2, self.se.show_rank,loop=False)
            return

        #---complete show rank
        if self.is_showrank:
            ishit = self.check_anykey()
                
            if ishit:
                self.current_scene = START_SCENE
                if self.config["use_sound"]:
                    pyxel.playm(0, loop=True)
            return

        #--- prepare boost
        if not self.start_dash and self.timeup_dash >= DASH_COOLTIME:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                if (
                    (self.posx(0) <= pyxel.mouse_x <= self.posx(0) + DOUBLE_FONTSIZE)
                    and
                    (self.posy(19) <= pyxel.mouse_y <= self.posy(19) + DOUBLE_FONTSIZE)
                ):
                    self.start_dash = True
            elif pyxel.btnp(pyxel.KEY_SHIFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                self.start_dash = True
        
        #--- count boost remain time
        if self.start_dash:
            if pyxel.frame_count % 30 == 0:
                self.timeup_dash -= 1
                if self.timeup_dash <= 0:
                    self.start_dash = False
        else:
            if pyxel.frame_count % 30 == 0:
                self.timeup_dash += 1
                if self.timeup_dash  > 10:
                    self.timeup_dash = 10

        # player move
        if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)) and self.player.x < SCREEN_WIDTH - 14:
            self.player.update(self.start_dash, 1)
            #self.player.x += 1
            #if self.start_dash:
            #    self.player.x += 1
        elif (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)) and self.player.x > -2:
            self.player.update(self.start_dash, -1)
            #self.player.x -= 1
            #if self.start_dash:
            #    self.player.x -= 1
        else:
            self.player.update(self.start_dash, 0)
        
        # shoot gun
        if (pyxel.btnp(pyxel.KEY_SPACE) or (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.check_mouse_playscreen()) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)) and len(self.shots) < 3:
            if self.config["use_sound"]:
                self.se.play_shoot()
                
            self.shots.append(Shot(self.player.x + (self.player.w // 2) - (SHOT_IMAGEINDEX_W // 2), self.player.y))
            
        # generate Enemy
        if pyxel.frame_count % STONE_INTERVAL == 0:
            if pyxel.rndi(0, 9) > 3:
                self.enemies.append(Enemy(pyxel.rndi(0, SCREEN_WIDTH - 8), 0))
            else:
                self.enemies.append(Enemy(pyxel.rndi(0, SCREEN_WIDTH - 8), pyxel.rndi(0,3) * SINGLE_FONTSIZE))
                self.enemies.append(Enemy(pyxel.rndi(0, SCREEN_WIDTH - 8), pyxel.rndi(0,3) * SINGLE_FONTSIZE))

        # generate damecon (max == 1)
        if self.player.hp < 2 and pyxel.rndi(1, 50) == 1 and len(self.damecons) < 1:
            self.damecons.append(Damecon(pyxel.rndi(0, SCREEN_WIDTH - 8), 0))
        
        # loop check damecon
        for damecon in self.damecons.copy():
            damecon.update()
            
            # check player
            if (self.player.x <= damecon.x <= self.player.x + 8 and
                self.player.y <= damecon.y <= self.player.y + 8):
                self.player.recovery()
                if self.config["use_sound"]:
                    pyxel.play(2, self.se.healing)
                self.damecons.remove(damecon)
            
            if damecon.y >= (SCREEN_HEIGHT // 20 * 17):
                self.damecons.remove(damecon)
                    
        # loop check shot
        for shot in self.shots.copy():
            shot.update(self.start_dash)
            if shot.y <= 0:
                self.shots.remove(shot)

        # loop check enemy
        for enemy in self.enemies.copy():
            enemy.update()
            
            # check player
            #if (self.player.x <= enemy.x <= self.player.x + 8 and
            #    self.player.y <= enemy.y <= self.player.y + 8):
            if enemy.check_player_collision(self.player):
                self.player.damage()
                self.enemies.remove(enemy)
                if self.config["use_sound"]:
                    pyxel.play(2, self.se.player_damage)
                if self.player.hp <= 0:
                    self.is_collision = True
                    if self.config["use_sound"]:
                        pyxel.play(0, self.se.bgm_gameover)
                    pyxel.stop(1)
                    self.player.death()
                
            if enemy.y >= (SCREEN_HEIGHT // 20 * 17):
                try:
                    self.enemies.remove(enemy)
                except Exception as e:
                    print(e)
            
            # check shooting
            for shot in self.shots.copy():
                if enemy.check_shooting(shot):
                    if self.config["use_sound"]:
                        pyxel.play(2, self.se.defeat_enemy)
                    enemy.hp -= 1
                    if enemy.is_defeat():
                        self.points += enemy.lv
                        try:
                            self.enemies.remove(enemy)
                        except Exception as e:
                            print(e)
                    self.shots.remove(shot)

    def update_config_scene(self):
        
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            #---return button
            if (
                (self.posx(1) <= pyxel.mouse_x <= self.posx(1) + SINGLE_FONTSIZE)
                and
                (self.posy(1) <= pyxel.mouse_y <= self.posy(1) + SINGLE_FONTSIZE)
            ):
                self.current_scene = START_SCENE
        
            #---use sound
            if (
                (self.posx(1) <= pyxel.mouse_x <= self.posx(1) + SINGLE_FONTSIZE)
                and
                (self.posy(3) <= pyxel.mouse_y <= self.posy(3) + SINGLE_FONTSIZE)
            ):
                self.config["use_sound"] = not self.config["use_sound"]
                if self.config["use_sound"]:
                    pyxel.playm(0, loop=True)
                else:
                    pyxel.stop(0)
                    pyxel.stop(1)
            
            #---mode time
            for tm in enumerate(MODE_TIME_LIST):
                if (
                    (self.posx(2 + tm[0] * 3) <= pyxel.mouse_x <= self.posx(2 + tm[0] * 3) + SINGLE_FONTSIZE)
                    and
                    (self.posy(6) <= pyxel.mouse_y <= self.posy(6) + SINGLE_FONTSIZE)
                ):
                    self.config["mode_time"] = tm[1]
                    self.play_result_s = MODE_RESULT_S[tm[0]]
                    self.play_result_a = MODE_RESULT_A[tm[0]]
                    print(f"S rank={self.play_result_s}")
                    print(f"A rank={self.play_result_a}")
            
        
        
    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
            
        
        if self.current_scene == START_SCENE:
            self.update_start_scene()        
        elif self.current_scene == PLAY_SCENE:
            self.update_play_scene()
        elif self.current_scene == CONFIG_SCENE:
            self.update_config_scene()
    
    def draw_start_scene(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        pyxel.blt(0, 0, IMGPLT_1, 32, 0, 120, 120)
        
        pyxel.text(self.posx(1)+1, self.posy(1),"Warship-Girls R", pyxel.COLOR_BLACK, self.jp_font12)
        pyxel.text(self.posx(1), self.posy(1),"Warship-Girls R", pyxel.COLOR_RED, self.jp_font12)
        pyxel.text(self.posx(4)+1, self.posy(3),"MINI Game", pyxel.COLOR_BLACK, self.jp_font)
        pyxel.text(self.posx(4), self.posy(3),"MINI Game", pyxel.COLOR_RED, self.jp_font)
        #pyxel.text(self.screen_posx(3), self.screen_posy(6), "Start: ", pyxel.COLOR_RED)
        #pyxel.text(self.screen_posx(5), self.screen_posy(7), "Left click / SPACE", pyxel.COLOR_RED)
        #pyxel.text(self.screen_posx(1), self.screen_posy(16), "<-: A key / Left",pyxel.COLOR_WHITE)
        #pyxel.text(self.screen_posx(1), self.screen_posy(17), "->: D key / Right",pyxel.COLOR_WHITE)
        pyxel.text(self.posx(8), self.posy(13) + 4,f"{AUTHOR}", pyxel.COLOR_RED, self.jp_font)
        
        #---new menu
        pyxel.text(self.posx(2), self.posy(17), "Start", pyxel.COLOR_WHITE, self.jp_font)
        pyxel.text(self.posx(9), self.posy(17), "Option", pyxel.COLOR_WHITE, self.jp_font)
    
    def draw_play_scene(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        pyxel.bltm(0, 0, 0, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 20 * 18)
        # enemites
        for enemy in self.enemies:
            enemy.draw()
        
        # shot
        for shot in self.shots:
            shot.draw()
        
        # damecon
        for damecon in self.damecons:
            damecon.draw()
        
        # player
        self.player.draw()        
        
        # game over
        if self.is_collision:
            pyxel.rect(self.posx(0), self.posy(9),SCREEN_WIDTH, SINGLE_FONTSIZE * 3, pyxel.COLOR_BLACK)
            pyxel.text(self.posx(4), self.posy(9)+4, "Game Over", pyxel.COLOR_ORANGE, self.jp_font12)
        
        # game clear
        if self.is_gameclear:
            
            self.clearrank_posy = 224
            #---illust
            if self.points > self.play_result_s:
                pyxel.rect(self.posx(0), self.posy(2),SCREEN_WIDTH, 120, pyxel.COLOR_BLACK)
                pyxel.blt(self.posx(0), self.posy(2),IMGPLT_1,32,120,120,120)
                self.clearrank_posy = 160
            elif self.points > self.play_result_a:
                pyxel.rect(self.posx(0), self.posy(2),SCREEN_WIDTH, 120, pyxel.COLOR_BLACK)
                pyxel.blt(self.posx(1), self.posy(2),IMGPLT_1,152,120,120,120)
                self.clearrank_posy = 192
            else:
                pyxel.rect(self.posx(0), self.posy(7),SCREEN_WIDTH, 16+32+16, pyxel.COLOR_BLACK)    
            #---string: victory
            pyxel.blt(self.posx(0), self.posy(8),IMGPLT_1,32,240,120,16,pyxel.COLOR_BLACK)
        
        if self.is_showrank:
            #---string: rank
            pyxel.blt(self.posx(5), self.posy(11),IMGPLT_1,0,self.clearrank_posy,32,32,pyxel.COLOR_BLACK)
            #pyxel.text(self.screen_posx(3), self.screen_posy(10), "Game Clear", pyxel.COLOR_RED,self.jp_font)
            
        # top UI
        ###---point
        pyxel.text(self.posx(1)+1, self.posy(1), f"Point: {self.points}", pyxel.COLOR_BLACK)
        pyxel.text(self.posx(1), self.posy(1), f"Point: {self.points}", pyxel.COLOR_WHITE)
        ###---timer
        pyxel.text(self.posx(10)+1, self.posy(1), f"Limit: {self.play_time}", pyxel.COLOR_BLACK)
        pyxel.text(self.posx(10), self.posy(1), f"Limit: {self.play_time}", pyxel.COLOR_WHITE)
        #--debug
        #pyxel.text(self.posx(7), self.posy(3), f"Mouse: {pyxel.mouse_x}:{pyxel.mouse_y}", pyxel.COLOR_PINK)
        
        
        # bottom UI
        
        ###----Speed up 
        if self.timeup_dash >= 10:
            pyxel.blt(self.posx(0), self.posy(18), IMGPLT_1, 0, 32, 16, 16, pyxel.COLOR_BLACK)
        else:
            pyxel.blt(self.posx(0), self.posy(18), IMGPLT_1, 0, 48, 16, 16, pyxel.COLOR_BLACK)
        pyxel.text(self.posx(4), self.posy(19), f"{self.timeup_dash}", pyxel.COLOR_WHITE)
        
        ###---player HP
        pyxel.text(self.posx(9), self.posy(19), f"HP: {self.player.hp} / {self.player.maxhp}", pyxel.COLOR_WHITE)

    def draw_config_scene(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        
        # return button
        pyxel.blt(self.posx(1), self.posy(1), IMGPLT_1, 0, 72, 8, 8, pyxel.COLOR_BLACK)
        
        # use BGM/SE
        if self.config["use_sound"]:
            pyxel.blt(self.posx(1), self.posy(3),IMGPLT_1, IMG_CONFIG_CHECK_X, IMG_CONFIG_CHECK_Y, SINGLE_FONTSIZE, SINGLE_FONTSIZE, pyxel.COLOR_BLACK)
        else:
            pyxel.blt(self.posx(1), self.posy(3),IMGPLT_1, IMG_CONFIG_UNCHECK_X, IMG_CONFIG_CHECK_Y, SINGLE_FONTSIZE, SINGLE_FONTSIZE, pyxel.COLOR_BLACK)
        pyxel.text(self.posx(1) + SINGLE_FONTSIZE + 4,self.posy(3), "BGM/SE",pyxel.COLOR_WHITE)
        
        # Mode time
        pyxel.text(self.posx(1), self.posy(5), "Time:",pyxel.COLOR_WHITE)
        
        for tm in enumerate(MODE_TIME_LIST):
            if self.config["mode_time"] == tm[1]:
                pyxel.blt(self.posx(2 + tm[0] * 3) , self.posy(6),IMGPLT_1, IMG_CONFIG_CHECK_X, IMG_CONFIG_CHECK_Y, SINGLE_FONTSIZE, SINGLE_FONTSIZE, pyxel.COLOR_BLACK)
            else:
                pyxel.blt(self.posx(2 + tm[0] * 3), self.posy(6),IMGPLT_1, IMG_CONFIG_UNCHECK_X, IMG_CONFIG_CHECK_Y, SINGLE_FONTSIZE, SINGLE_FONTSIZE, pyxel.COLOR_BLACK)
            pyxel.text(self.posx(3 + tm[0] * 3) + 2, self.posy(6), f"{tm[1]}",pyxel.COLOR_WHITE)
        
        
        
        
        #---help
        pyxel.text(self.posx(1), self.posy(12), "---Help---",pyxel.COLOR_WHITE)
        pyxel.text(self.posx(1), self.posy(13), "<-: A-key, Left-key",pyxel.COLOR_WHITE)
        pyxel.text(self.posx(1), self.posy(14), "->: D-key, Right-key",pyxel.COLOR_WHITE)
        pyxel.text(self.posx(1), self.posy(15), "Shot: SPACE, Mouse left,",pyxel.COLOR_WHITE)
        pyxel.text(self.posx(5), self.posy(16), "Gamepad A-button",pyxel.COLOR_WHITE)
        pyxel.text(self.posx(1), self.posy(17), "Boost:  Shift-key",pyxel.COLOR_WHITE)        
        pyxel.text(self.posx(5), self.posy(18), "Gamepad B-button",pyxel.COLOR_WHITE)
        pyxel.blt(self.posx(2),  self.posy(18), IMGPLT_1, 0, 32, 16, 16, pyxel.COLOR_BLACK)
        pyxel.text(self.posx(5), self.posy(19), "- button",pyxel.COLOR_WHITE)
        
    def draw(self):
        if self.current_scene == START_SCENE:
            self.draw_start_scene()
        elif self.current_scene == PLAY_SCENE:
            self.draw_play_scene()
        elif self.current_scene == CONFIG_SCENE:
            self.draw_config_scene()
        
App()

