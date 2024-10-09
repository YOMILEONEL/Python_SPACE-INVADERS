import pygame
import sys
import os
import random

#Initialisiere Pygame
pygame.init()



# Funktion zum Erstellen von feindlichen Schiffen
def create_enemy_ship(x, y, color, shape):
    enemy_img = pygame.Surface((50, 50))  # Beispielgröße, du kannst die Größe anpassen
    enemy_img.fill(color)

    #Zeichne die Form des feindlichen Schiffs basierend auf der ausgewählten Form
    if shape == 'rect':
        pygame.draw.rect(enemy_img, (0, 0, 0), enemy_img.get_rect(), 5)  # Beispiel: Rechteck
    elif shape == 'circle':
        pygame.draw.circle(enemy_img, (0, 0, 0), (25, 25), 25, 5)  # Beispiel: Kreis
    elif shape == 'triangle':
        # Beispiel: Dreieck (angepasst an deine Form)
        pygame.draw.polygon(enemy_img, (0, 0, 0), [(25, 5), (5, 45), (45, 45)], 5)
    elif shape == 'pentagon':
        #Beispiel: Pentagon (angepasst an deine Form)
        pygame.draw.polygon(enemy_img, (0, 0, 0), [(25, 5), (5, 20), (15, 45), (35, 45), (45, 20)], 5)

    screen.blit(enemy_img, (x, y))



#Definiere die Bildschirmbreite und -höhe
screen_width, screen_height = 1550, 800

#Erstelle das Fenster und definiere Fenstergröße
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption('Space Invaders')  # Setze den Fenstertitel

#Definiere Farben
black = (0, 0, 0)
yellow = (255, 255, 25)

#Definiere Schriftart und Schriftgröße für den Text
font = pygame.font.Font(None, 50)
text = font.render('Space Invaders', True, yellow)  #Erstelle den Text
text_position = text.get_rect(center=(screen_width // 2, screen_height // 2))  #Positioniere den Text



#Laden des Bildes der Laserkanone und Festlegen der Breite und Höhe
laser_img = pygame.image.load(os.path.join('images', 'laser.png'))
laser_width = laser_img.get_width()
laser_height = laser_img.get_height()

#Laden des Bildes der Laser-Projektile und Festlegen der Breite und Höhe
laser_projectile_img = pygame.Surface((10, 30))  # Beispielgröße, du kannst die Größe anpassen
laser_projectile_img.fill((255, 255, 255))  # Weiße Farbe für die Laser-Projektile


#Initialisieren der Position und Geschwindigkeit der Laserkanone
laser_pos = [screen_width // 2, screen_height - laser_height]
laser_speed = 7      #Geschwindigkeit

#Initialisieren der Liste der Laser-Projektile
laser_projectiles = []

#Geschwindigkeit der Laser-Projektile
laser_projectile_speed = 4

#Funktion zum Erstellen von Laser-Projektilen
def create_laser_projectile(x, y):
    screen.blit(laser_projectile_img, (x, y))


#Feindliche Schiffe
enemy_rows = 4  # Anzahl der Reihen
enemies_per_row = 24  # Anzahl der feindlichen Schiffe pro Reihe
enemy_gap = 100  # Abstand zwischen den feindlichen Schiffen



#Farben und Formen für verschiedene Arten von feindlichen Schiffen, Nutzung von Dictionaries + Python-Liste : https://www.youtube.com/watch?v=6x8oN6FtpLo
enemy_combinations = [
    {'color': (255, 0, 0), 'shape': 'rect', 'score': 2},      # Rotes Rechteck
    {'color': (0, 255, 0), 'shape': 'circle', 'score':3},    # Grüner Kreis
    {'color': (0, 0, 255), 'shape': 'triangle', 'score':5},  # Blaues Dreieck
    {'color': (128, 128, 0), 'shape': 'pentagon', 'score':10} # Gelbes Pentagon
] # Konfiguration von Farben bekam ich am Ende dieses Videos : https://www.youtube.com/watch?v=NCAxoWS7WRY

# Enemy movement variables
enemy_speed_x = 0.2     # Horizontale Geschwindigkeit der feindlichen Schiffe
enemy_speed_y = 5    # Vertikale Geschwindigkeit der feindlichen Schiffe, wenn sie den Bildschirmrand erreichen

# Erzeuge eine Liste von feindlichen Schiffen mit bestimmten Farben und Formen
enemies = []
for row in range(enemy_rows):
    for col in range(enemies_per_row):
        x = col * ((screen_width-3*enemy_gap) // enemies_per_row) + enemy_gap
        y = row * 70 + enemy_gap
        combination = random.choice(enemy_combinations)
        enemies.append({'x': x, 'y': y, 'color': combination['color'], 'shape': combination['shape'],'score': combination['score']})

# Initialisieren der Liste der feindlichen Projektile
enemy_projectiles = []

# Geschwindigkeit der feindlichen Projektile
enemy_projectile_speed = 1

# Füge eine neue Variable hinzu, um die Zeit seit dem letzten Projektil zu verfolgen
last_projectile_time = pygame.time.get_ticks()
#Funktion zum Überprüfen von Kollisionen zwischen zwei Rechtecken
def check_collision(recta, rectb):
    return recta.colliderect(rectb)            #https://www.youtube.com/watch?v=BHr9jxKithk gelernt

#Funktion zum Überprüfen von Kollisionen zwischen Laser-Projektilen und feindlichen Schiffen
def check_projectile_enemy_collision(projectiles, enemies, current_score):
    updated_score = current_score

    for projectile in projectiles:
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy['x'], enemy['y'], 50, 50)    #x: Hoirzontale Position von enemie, y: vertikale Position, 50: Grösse und Breite der Rect
            projectile_rect = pygame.Rect(projectile[0], projectile[1], 10, 30)
            if check_collision(enemy_rect, projectile_rect):      #Feindliches Shiff wurde getroffen
                updated_score += enemy['score']    #Erhöhe den Score entsprechend dem Punktwert des feindlichen Schiffs
                enemies.remove(enemy)              #die feindlichen Schiffen Verschwenden
                projectiles.remove(projectile)     #die Projektile verschwenden

    return updated_score

def display_score():
    score_text = font.render(f'Score: {score}', True, yellow)
    screen.blit(score_text, (screen_width - 200, 20))

# Funktion zum Zeichnen der Spieler-Leben
def draw_player_lives(player_lives):
    for i in range(player_lives):
        pygame.draw.rect(screen, (255, 255, 255), (10 + i * 40, 10, 30, 30))  # Beispielgröße, anpassen


# Funktion zum Erstellen von Schutzbunkern
def create_shield(x, y, lives):
    shield_color = yellow
    shield_width, shield_height = 150, 30
    # Zeichne den Shutzkannone nur, wenn er noch Leben hat
    if lives > 0:
        pygame.draw.rect(screen, shield_color, (x, y, shield_width, shield_height))


# Anzahl der Schutzbunker und deren Abstand
anzahl_shields = 4
shield_gap = (screen_width - anzahl_shields * 50) // (anzahl_shields + 1)

# Liste für die Positionen der Schutzbunker
shield_positions = [{'x': (i + 1) * shield_gap + i * 50, 'lives': 3} for i in range(anzahl_shields)]

#Funktion zum Überprüfen von Kollisionen mit Shield
def check_collision_with_shield(rect, shield, is_projectile):
    if rect.colliderect(pygame.Rect(shield['x'], screen_height - 170, 150, 30)):
        if is_projectile:
            shield['lives'] -= 1    #Reduziere die Leben
        if shield['lives'] == 0:
            shield_positions.remove(shield)  #Entferne den Schutzbunker
        return True
    return False

#  Variable für den Menüzustand
current_state = "menu"  # Initialer Zustand ist das Menü

#  Variable zum Verfolgen des ausgewählten Buttons im Menü
selected_button = 0

# Hauptspiel-Schleife
running = True
show_text = True  # Variable, um den Text "Space Invaders" zu zeigen
score = 0
player_lives = 3  # Start mit 3 Leben


while running:
    # Event-Schleife, um auf Benutzeraktionen zu reagieren
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Schließen des Fensters
            running = False  # Beende die Hauptschleife und das Spiel

        elif event.type == pygame.KEYDOWN:
            if current_state == "menu":
                if event.key == pygame.K_UP:  # Pfeiltaste nach oben wurde gedrückt
                    selected_button = (selected_button - 1) % 2
                elif event.key == pygame.K_DOWN:
                    selected_button = (selected_button + 1) % 2
                elif event.key == pygame.K_RETURN:
                    # Führe Aktion basierend auf ausgewähltem Button aus
                    if selected_button == 0:
                        current_state = "playing"
                    elif selected_button == 1:
                        running = False  # Beende das Spiel

            elif current_state == "playing":
                          # Behandle Tastatureingaben für das Spiel
                if event.key == pygame.K_LEFT and laser_pos[0] > 0:
                             laser_pos[0] -= laser_speed
                elif event.key == pygame.K_RIGHT and laser_pos[0] < screen_width - laser_width:
                             laser_pos[0] += laser_speed
                elif event.key == pygame.K_UP:
                     # Erstelle ein Laser-Projektil an der aktuellen Position der Laserkanone
                     laser_projectiles.append([laser_pos[0] + (laser_width - 10) // 2, laser_pos[1]])


            # Tastaturabfrage für gedrückte Tasten
    keys = pygame.key.get_pressed()

    # Bewegung der Laserkanone nach links
    if keys[pygame.K_LEFT] and laser_pos[0] > 0:
        laser_pos[0] -= laser_speed

    # Bewegung der Laserkanone nach rechts
    if keys[pygame.K_RIGHT] and laser_pos[0] < screen_width - laser_width:
        laser_pos[0] += laser_speed
    # Bewegung von feindlichen Schiffen
    for enemy in enemies:
        enemy['x'] += enemy_speed_x

        # Überprüfe, ob das feindliche Schiff den Bildschirmrand erreicht hat
        if enemy['x'] <= 0 or enemy['x'] >= screen_width - 50:
            # Bewege alle feindliche Schiffen nach unten
            for e in enemies:
                e['y'] += enemy_speed_y
            enemy_speed_x = -enemy_speed_x  # Ändere die Richtung um

        # Lassen Sie das feindliche Schiff in der ersten Reihe (am nächsten zur Laserkanone) schießen
        current_time = pygame.time.get_ticks()
        if current_time - last_projectile_time > 1000:  # 1000 Millisekunden = 1 Sekunde
            if enemy['y'] == max(e['y'] for e in enemies):
                # Zufällige Chance, ein Projektil abzufeuern
                if random.randint(0, 100) < 5:  # 5% Chance pro Frame
                    enemy_projectiles.append([enemy['x'], enemy['y']])
                    last_projectile_time = current_time  # Aktualisiere die Zeit des letzten Projektils

     # Bewegung der feindlichen Projektile
    for projectile in enemy_projectiles:
        projectile[1] += enemy_projectile_speed

        # Überprüfe Kollision zwischen Laser-Projektilen und feindlichen Schiffen
        updated_score = check_projectile_enemy_collision(laser_projectiles, enemies, score)

    # Bildschirmhintergrund füllen
    screen.fill(black)

    if show_text:  # Wenn show_text True ist, zeige den Text
        screen.blit(text, text_position)  # Zeige den Text auf dem Bildschirm
        pygame.display.flip()  # Aktualisiere den Bildschirm, um den Text anzuzeigen
        pygame.time.delay(2000)  # Warte 2 Sekunden, um den Text anzuzeigen
        show_text = False  # Setze show_text auf False, um den Text nicht mehr zu zeigen

    elif current_state == "menu":
        play_button_color = yellow if selected_button == 0 else (255, 255, 255)
        exit_button_color = yellow if selected_button == 1 else (255, 255, 255)

        play_button_text = font.render('Play', True, play_button_color)
        exit_button_text = font.render('Exit', True, exit_button_color)

        screen.blit(play_button_text, (screen_width // 2 - 50, screen_height // 2 - 50))
        screen.blit(exit_button_text, (screen_width // 2 - 50, screen_height // 2 + 50))
        # Ansonsten, wenn show_text False ist, zeige die Laserkanone

    elif current_state == "playing":  # Ansonsten, wenn show_text False ist, zeige die Laserkanone

        # Zeichnen der Spieler-Leben
        draw_player_lives(player_lives)

        # Zeichnen der Schutzbunker
        for shield in shield_positions:
            create_shield(shield['x'], screen_height - 170, shield['lives'])

        screen.blit(laser_img, (laser_pos[0], laser_pos[1]))  # Zeige die Laserkanone auf dem Bildschirm

        # Zeichnen der Laser-Projektile
        for projectile in laser_projectiles:
            create_laser_projectile(projectile[0], projectile[1])


        # Bewegung der Laser-Projektile , ich habe im folgendem Video gelernt : https://www.youtube.com/watch?v=5-WGGYLT8E8
        for projectile in laser_projectiles:
            projectile[1] -= laser_projectile_speed

        # Entferne Laser-Projektile, die den Bildschirm verlassen haben
        laser_projectiles = [projectile for projectile in laser_projectiles if projectile[1] > 0]

        # Überprüfe Kollision zwischen Laser-Projektilen und feindlichen Schiffen
        score = check_projectile_enemy_collision(laser_projectiles, enemies, score)

        # Zeige feindliche Schiffe
        for enemy in enemies:
            create_enemy_ship(enemy['x'], enemy['y'], enemy['color'], enemy['shape'])

        # Zeichnen der feindlichen Projektile
        for projectile in enemy_projectiles:
            pygame.draw.circle(screen, (255, 0, 0), (projectile[0], projectile[1]), 5)


        # Entferne Laser-Projektile, die den Bildschirm verlassen haben
        laser_projectiles = [projectile for projectile in laser_projectiles if projectile[1] > 0]

        # Zeige den aktuellen Gesamtscore oben rechts auf dem Spielfenster an
        display_score()

    for projectile in enemy_projectiles:
        projectile_rect = pygame.Rect(projectile[0], projectile[1], 5, 5)  # x,y Koordinaten, Grösse un Breite
        player_rect = pygame.Rect(laser_pos[0], laser_pos[1], laser_width, laser_height)

        if check_collision(player_rect, projectile_rect):
            # Der Spieler wurde von einem enemy Projektil getroffen
            player_lives -= 1
            laser_pos = [screen_width // 2, screen_height - laser_height]  # Spielerposition zurücksetzen

            # Überprüfe ob der Spieler noch Leben hat
            if player_lives == 0:
                current_state = "game_over"#####

            enemy_projectiles.remove(projectile)  #entferne den enemy Projektil
#Überprüfe Kollision mit Schutzbunker
    # Überprüfe Kollision mit enemy-Projectiles
    for projectile in enemy_projectiles:
        projectile_rect = pygame.Rect(projectile[0], projectile[1], 5, 5)

        for shield in shield_positions:
            if check_collision_with_shield(projectile_rect, shield, is_projectile=True):
                enemy_projectiles.remove(projectile)  # entferne den enemy Projektil

    #Überprüfe Kollision mit Laser-Projectiles
    for projectile in laser_projectiles:
        projectile_rect = pygame.Rect(projectile[0], projectile[1], 10, 30)

        for shield in shield_positions[:]:
            if check_collision_with_shield(projectile_rect, shield, is_projectile=False):
                laser_projectiles.remove(projectile)  # entferne den laser Projektil

    if len(enemies) == 0:
        current_state = "winner"

    if current_state == "game_over":
        game_over_text = font.render('Game Over', True, yellow)
        screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2 - 50))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False

    elif current_state == "winner":
        winner_text = font.render('Winner!', True, yellow)
        screen.blit(winner_text, (screen_width // 2 - 80, screen_height // 2 - 50))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False



    pygame.display.update()  # Aktualisiere den Bildschirm, um die Laserkanone und die feindlichen Schiffen anzuzeigen


# Beenden von Pygame und des Programms, wenn die Hauptschleife beendet ist
pygame.quit()
sys.exit()
