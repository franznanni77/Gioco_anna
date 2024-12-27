import streamlit as st
import numpy as np
import sounddevice as sd

class PianoSynthesizer:
    def __init__(self):
        self.sample_rate = 44100
        self.base_frequencies = {
            'C': 261.63,  # Do
            'D': 293.66,  # Re
            'E': 329.63,  # Mi
            'F': 349.23,  # Fa
            'G': 392.00,  # Sol
            'A': 440.00,  # La
            'B': 493.88   # Si
        }

    def generate_note(self, frequency, duration=0.3, amplitude=0.3):
        """Genera una nota utilizzando una forma d'onda sinusoidale con envelope ADSR"""
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples, False)
        
        # Crea l'envelope ADSR
        attack = int(0.05 * samples)
        decay = int(0.1 * samples)
        sustain_level = 0.7
        release = int(0.2 * samples)
        
        envelope = np.ones(samples)
        # Attack
        envelope[:attack] = np.linspace(0, 1, attack)
        # Decay
        envelope[attack:attack+decay] = np.linspace(1, sustain_level, decay)
        # Sustain è già impostato a sustain_level
        # Release
        envelope[-release:] = np.linspace(sustain_level, 0, release)
        
        # Genera la nota base
        note = amplitude * np.sin(2 * np.pi * frequency * t)
        # Aggiungi alcune armoniche per un suono più ricco
        note += 0.5 * amplitude * np.sin(4 * np.pi * frequency * t)  # Prima armonica
        note += 0.25 * amplitude * np.sin(6 * np.pi * frequency * t)  # Seconda armonica
        
        # Applica l'envelope
        note = note * envelope
        
        return note.astype(np.float32)

    def play_note(self, note_name):
        """Riproduce una nota dato il suo nome"""
        if note_name in self.base_frequencies:
            frequency = self.base_frequencies[note_name]
            note_data = self.generate_note(frequency)
            sd.play(note_data, self.sample_rate)

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
    
    # Crea i tasti del piano con un layout migliorato
    cols = st.columns(7)
    
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