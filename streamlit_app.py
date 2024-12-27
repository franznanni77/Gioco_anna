import streamlit as st
import pygame
import numpy as np
from PIL import Image
import time

class Cat:
    def __init__(self):
        self.x = 300
        self.y = 500
        self.velocity_y = 0
        self.is_jumping = False
        self.lives = 3
        self.width = 40
        self.height = 40
        self.direction = 1
        
    def draw(self, surface):
        # Corpo principale (ovale)
        pygame.draw.ellipse(surface, (255, 255, 255), 
                          (self.x, self.y, self.width, self.height))
        
        # Orecchie triangolari
        pygame.draw.polygon(surface, (255, 255, 255), [
            (self.x + 5, self.y - 5),
            (self.x + 15, self.y - 15),
            (self.x + 25, self.y - 5)
        ])
        pygame.draw.polygon(surface, (255, 255, 255), [
            (self.x + 25, self.y - 5),
            (self.x + 35, self.y - 15),
            (self.x + 45, self.y - 5)
        ])
        
        # Occhi
        pygame.draw.circle(surface, (0, 0, 0), 
                         (self.x + 15, self.y + 15), 3)
        pygame.draw.circle(surface, (0, 0, 0), 
                         (self.x + 35, self.y + 15), 3)
        
        # Naso
        pygame.draw.circle(surface, (255, 192, 203), 
                         (self.x + 25, self.y + 20), 2)
        
        # Baffi
        for i in [-1, 1]:
            pygame.draw.line(surface, (0, 0, 0),
                           (self.x + 25, self.y + 20),
                           (self.x + 25 + (15 * i), self.y + 18), 1)
            pygame.draw.line(surface, (0, 0, 0),
                           (self.x + 25, self.y + 20),
                           (self.x + 25 + (15 * i), self.y + 22), 1)
    
    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -15
            self.is_jumping = True
    
    def update(self):
        # Gravità
        self.velocity_y += 0.8
        self.y += self.velocity_y
        
        # Limite inferiore
        if self.y > 500:
            self.y = 500
            self.velocity_y = 0
            self.is_jumping = False

class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 20
        self.speed = 2
        self.points = 10
        self.color = (100, 100, 100)
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color,
                        (self.x, self.y, self.width, self.height))
        # Effetto 3D
        pygame.draw.rect(surface, (50, 50, 50),
                        (self.x, self.y + self.height - 5, self.width, 5))
    
    def update(self):
        self.y += self.speed
        
    def collide_with_cat(self, cat):
        return (cat.x < self.x + self.width and
                cat.x + cat.width > self.x and
                cat.y < self.y + self.height and
                cat.y + cat.height > self.y)

class Game:
    def __init__(self):
        pygame.init()
        self.cat = Cat()
        self.platforms = [Platform(300, 100)]
        self.score = 0
        self.game_over = False
        self.last_platform_y = 100
        
    def update(self):
        if not self.game_over:
            self.cat.update()
            
            # Aggiorna piattaforme
            for platform in self.platforms:
                platform.update()
                
                # Collisione con il gatto
                if platform.collide_with_cat(self.cat):
                    if self.cat.velocity_y > 0:  # Solo quando sta scendendo
                        self.cat.y = platform.y - self.cat.height
                        self.cat.velocity_y = 0
                        self.cat.is_jumping = False
                        self.score += platform.points
            
            # Gestione piattaforme
            self.platforms = [p for p in self.platforms if p.y < 600]
            while len(self.platforms) < 3:
                self.last_platform_y -= 200
                new_x = np.random.randint(100, 500)
                self.platforms.append(Platform(new_x, self.last_platform_y))
            
            # Game over
            if self.cat.y > 550:
                self.cat.lives -= 1
                if self.cat.lives <= 0:
                    self.game_over = True
                else:
                    self.reset_position()

    def reset_position(self):
        self.cat.y = 500
        self.cat.velocity_y = 0
        self.cat.is_jumping = False

def draw_game(game):
    surface = pygame.Surface((600, 600))
    surface.fill((30, 30, 50))  # Sfondo più scuro
    
    # Disegna le piattaforme
    for platform in game.platforms:
        platform.draw(surface)
    
    # Disegna il gatto
    game.cat.draw(surface)
    
    return Image.frombytes('RGB', surface.get_size(),
                         pygame.image.tostring(surface, 'RGB'))

def main():
    st.set_page_config(page_title="Cat Platform Game")
    
    # Inizializzazione del gioco nella session_state
    if 'game' not in st.session_state:
        st.session_state.game = Game()
    
    st.title("🐱 Cat Platform Game")
    st.markdown("""
    ### Controlli:
    - Premi il pulsante **Salta** per far saltare il gatto
    - Raggiungi le piattaforme per ottenere punti
    - Non cadere!
    """)
    
    # Display score e vite in colonne
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"Score: {st.session_state.game.score}")
    with col2:
        st.write(f"Lives: {st.session_state.game.cat.lives}")
    with col3:
        # Pulsante di salto con chiave univoca
        jump_button = st.button("Salta!", key="jump_button")
        if jump_button:
            st.session_state.game.cat.jump()
    
    # Container per l'area di gioco
    game_container = st.empty()
    
    # Game over check
    if st.session_state.game.game_over:
        st.error("Game Over!")
        if st.button("Ricomincia", key="restart_button"):
            st.session_state.game = Game()
    else:
        # Aggiorna stato del gioco
        st.session_state.game.update()
    
    # Aggiorna il display
    game_image = draw_game(st.session_state.game)
    game_container.image(game_image)

    # Aggiungi un pulsante per aggiornare manualmente
    st.button("Aggiorna Frame", key="update_frame")

if __name__ == "__main__":
    main()