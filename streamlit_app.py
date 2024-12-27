import streamlit as st
from mingus.containers import Note
from mingus.midi import fluidsynth
import time
import os

def init_fluidsynth():
    # Inizializza FluidSynth
    sf2 = os.path.join(os.path.dirname(os.path.realpath(__file__)), "soundfont.sf2")
    if not os.path.exists(sf2):
        st.error("Soundfont file not found. Please download a .sf2 file and place it in the project directory.")
        return False
    fluidsynth.init(sf2)
    return True

def play_note(note_name):
    note = Note(note_name)
    fluidsynth.play_Note(note)
    time.sleep(0.3)
    fluidsynth.stop_Note(note)

def main():
    st.title("🎹 Piano Virtuale")
    
    # Verifica che FluidSynth sia inizializzato correttamente
    if not init_fluidsynth():
        return
    
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
    
    st.write("Usa il mouse per cliccare i tasti o premi le lettere corrispondenti sulla tastiera")
    
    # Crea i tasti del piano
    cols = st.columns(7)
    
    for i, (col, (key, note)) in enumerate(zip(cols, key_bindings.items())):
        with col:
            if st.button(f"{note} ({key})", key=note):
                play_note(note)
    
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