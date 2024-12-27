import streamlit as st
import pygame
import numpy as np
import time
from pygame import mixer

class PianoSynthesizer:
    def __init__(self):
        # Inizializza pygame e il mixer
        pygame.init()
        pygame.mixer.init()
        
        # Frequenze delle note
        self.frequencies = {
            'C': 261.63,  # Do
            'D': 293.66,  # Re
            'E': 329.63,  # Mi
            'F': 349.23,  # Fa
            'G': 392.00,  # Sol
            'A': 440.00,  # La
            'B': 493.88   # Si
        }
        
        # Genera e memorizza i suoni
        self.sounds = {}
        self.generate_sounds()
        
    def generate_sine_wave(self, frequency, duration=0.3, sample_rate=44100):
        """Genera una forma d'onda sinusoidale per una data frequenza"""
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        
        # Genera la nota base
        tone = np.sin(2 * np.pi * frequency * t)
        
        # Aggiungi armoniche per un suono più ricco
        tone += 0.5 * np.sin(4 * np.pi * frequency * t)
        tone += 0.25 * np.sin(6 * np.pi * frequency * t)
        
        # Normalizza
        tone = np.int16(tone * 32767)
        return tone
        
    def generate_sounds(self):
        """Genera i suoni per tutte le note"""
        for note, freq in self.frequencies.items():
            sound_array = self.generate_sine_wave(freq)
            sound = pygame.sndarray.make_sound(sound_array)
            self.sounds[note] = sound
            
    def play_note(self, note):
        """Riproduce una nota"""
        if note in self.sounds:
            self.sounds[note].play()
            time.sleep(0.1)  # Piccolo delay per evitare sovrapposizioni

def main():
    st.set_page_config(page_title="Piano Virtuale", page_icon="🎹")
    st.title("🎹 Piano Virtuale")
    
    # Inizializza il sintetizzatore
    if 'synth' not in st.session_state:
        st.session_state.synth = PianoSynthesizer()
    
    # Mappatura tasti-note
    key_bindings = {
        'A': 'C',
        'S': 'D',
        'D': 'E',
        'F': 'F',
        'G': 'G',
        'H': 'A',
        'J': 'B'
    }
    
    # Interfaccia utente
    st.markdown("""
    ### Istruzioni:
    - Usa il mouse per cliccare i tasti
    - Oppure usa i tasti della tastiera: A S D F G H J
    """)
    
    # Stile CSS per i tasti del piano
    st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        height: 120px;
        background-color: white;
        color: black;
        border: 1px solid black;
        border-radius: 0 0 5px 5px;
    }
    .stButton button:hover {
        background-color: #f0f0f0;
    }
    .stButton button:active {
        background-color: #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Crea i tasti del piano
    cols = st.columns(7)
    
    # Crea i tasti
    for i, (col, (key, note)) in enumerate(zip(cols, key_bindings.items())):
        with col:
            if st.button(f"{note}\n({key})", key=note):
                st.session_state.synth.play_note(note)
    
    # JavaScript per catturare gli eventi della tastiera
    st.markdown("""
    <script>
    document.addEventListener('keydown', function(e) {
        if (!e.repeat) {
            const key = e.key.toUpperCase();
            if ('ASDFGHJ'.includes(key)) {
                const buttons = document.querySelectorAll('button');
                for (let button of buttons) {
                    if (button.textContent.includes(key)) {
                        button.click();
                        break;
                    }
                }
            }
        }
    });
    </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()