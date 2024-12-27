import streamlit as st
import pygame
import numpy as np
from PIL import Image
import io

class Cat:
    def __init__(self):
        self.x = 300  # posizione iniziale x
        self.y = 500  # posizione iniziale y
        self.velocity_y = 0
        self.is_jumping = False
        self.lives = 3
        self.width = 40
        self.height = 40
        
    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -15
            self.is_jumping = True
    
    def update(self):
        # Gravità
        self.velocity_y += 0.8
        self.y += self.velocity_y
        
        # Impedisce al gatto di uscire dallo schermo in basso
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
    
    def update(self):
        self.y += self.speed
        
    def collide_with_cat(self, cat):
        return (cat.x < self.x + self.width and
                cat.x + cat.width > self.x and
                cat.y < self.y + self.height and
                cat.y + cat.height > self.y)

class Game:
    def __init__(self):
        self.cat = Cat()
        self.platforms = [Platform(300, 100)]
        self.score = 0
        self.game_over = False
        
    def update(self):
        if not self.game_over:
            self.cat.update()
            
            # Aggiorna piattaforme
            for platform in self.platforms:
                platform.update()
                
                # Collisione con il gatto
                if platform.collide_with_cat(self.cat):
                    self.cat.y = platform.y - self.cat.height
                    self.cat.velocity_y = 0
                    self.cat.is_jumping = False
                    self.score += platform.points
            
            # Rimuovi piattaforme fuori schermo e aggiungi nuove
            self.platforms = [p for p in self.platforms if p.y < 600]
            if len(self.platforms) < 3:
                self.platforms.append(
                    Platform(
                        np.random.randint(100, 500),
                        self.platforms[-1].y - 200
                    )
                )
            
            # Controllo game over
            if self.cat.y > 550:
                self.cat.lives -= 1
                if self.cat.lives <= 0:
                    self.game_over = True
                else:
                    self.cat.y = 500
                    self.cat.velocity_y = 0

def draw_game(game):
    # Crea superficie pygame
    surface = pygame.Surface((600, 600))
    surface.fill((255, 255, 255))
    
    # Disegna il gatto
    pygame.draw.rect(
        surface,
        (0, 0, 0),
        (game.cat.x, game.cat.y, game.cat.width, game.cat.height)
    )
    
    # Disegna le piattaforme
    for platform in game.platforms:
        pygame.draw.rect(
            surface,
            (100, 100, 100),
            (platform.x, platform.y, platform.width, platform.height)
        )
    
    # Converti la superficie pygame in un'immagine per Streamlit
    return Image.frombytes('RGB', surface.get_size(),
                         pygame.image.tostring(surface, 'RGB'))

def main():
    st.set_page_config(page_title="Cat Platform Game")
    
    if 'game' not in st.session_state:
        st.session_state.game = Game()
        
    # Titolo e istruzioni
    st.title("🐱 Cat Platform Game")
    st.write("Usa la barra spaziatrice per saltare!")
    
    # Display score e vite
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Score: {st.session_state.game.score}")
    with col2:
        st.write(f"Lives: {st.session_state.game.cat.lives}")
    
    # Area di gioco
    game_placeholder = st.empty()
    
    # Game over message
    if st.session_state.game.game_over:
        st.write("Game Over! Premi R per ricominciare")
        if st.button("Restart"):
            st.session_state.game = Game()
    
    # Game loop
    def update():
        if not st.session_state.game.game_over:
            st.session_state.game.update()
            game_image = draw_game(st.session_state.game)
            game_placeholder.image(game_image)
    
    # Gestione input
    if st.button("Jump"):
        st.session_state.game.cat.jump()
    
    update()

if __name__ == "__main__":
    main()