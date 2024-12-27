import streamlit as st
from playsound import playsound
import os

class Piano:
    def __init__(self):
        # Crea una cartella per i suoni se non esiste
        if not os.path.exists('sounds'):
            os.makedirs('sounds')
            
        # Dizionario che mappa le note ai file audio
        self.notes = {
            'C': 'sounds/C.mp3',
            'D': 'sounds/D.mp3',
            'E': 'sounds/E.mp3',
            'F': 'sounds/F.mp3',
            'G': 'sounds/G.mp3',
            'A': 'sounds/A.mp3',
            'B': 'sounds/B.mp3'
        }
    
    def play_note(self, note):
        """Riproduce il suono della nota"""
        if note in self.notes and os.path.exists(self.notes[note]):
            playsound(self.notes[note], False)  # False per riproduzione asincrona

def main():
    st.set_page_config(page_title="Piano Virtuale", page_icon="🎹")
    st.title("🎹 Piano Virtuale")
    
    # Inizializza il piano
    if 'piano' not in st.session_state:
        st.session_state.piano = Piano()
    
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
    
    # Controlla se i file audio esistono
    missing_files = [note for note, file in st.session_state.piano.notes.items() 
                    if not os.path.exists(file)]
    
    if missing_files:
        st.warning(f"""
        ⚠️ File audio mancanti per le note: {', '.join(missing_files)}
        Per favore, scarica i file audio MP3 per ogni nota e inseriscili nella cartella 'sounds'.
        I file devono essere nominati: C.mp3, D.mp3, E.mp3, F.mp3, G.mp3, A.mp3, B.mp3
        """)
    
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
                st.session_state.piano.play_note(note)
    
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