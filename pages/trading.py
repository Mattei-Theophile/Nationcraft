import streamlit as st
import os
from nationsglory.bots.server.number_detector import NumberDetector

# Main page content
st.markdown("# Trading 🏦")
st.sidebar.markdown("# Trading 🏦")

# Initialize session state variables
if 'TraderMachineNumber' not in st.session_state:
    st.session_state.TraderMachineNumber = []

# Create tabs for different trading functionalities
manual_tab, auto_tab, history_tab = st.tabs(["Manuel", "Automatique", "Historique"])

with manual_tab:
    st.title("Numéro de la machine serveur")
    st.write("Entrez manuellement les numéros de la machine de trading")

    # Create 4 columns for number input
    tradingNumber = st.columns(4)

    # Clear the list before appending new values
    st.session_state.TraderMachineNumber = []

    for col in tradingNumber:
        Num = col.container(height=120, border=False)
        st.session_state.TraderMachineNumber.append(
            Num.number_input("Choisissez un nombre", min_value=0, max_value=9, value=0, key=f"manual_{col}")
        )

    if st.button("Enregistrer les numéros"):
        st.success(f"Numéros enregistrés: {st.session_state.TraderMachineNumber}")

    tradingRoom = st.file_uploader("Enregistrer le schematic de votre salle de trading")

    if st.button("Lancer le changement de numéro"):
        st.info("Changement de numéro en cours...")
        st.write(f"Numéros à configurer: {st.session_state.TraderMachineNumber}")
        # Here you would implement the actual number changing logic

with auto_tab:
    st.title("Détection automatique des numéros")
    st.write("Utilisez la détection automatique pour lire les numéros de la machine de trading")

    # Initialize the NumberDetector
    detector = NumberDetector()

    # File uploader for screenshots
    screenshot = st.file_uploader("Télécharger une capture d'écran de la machine", type=["jpg", "jpeg", "png"])

    if screenshot:
        # Create a temporary directory for the uploaded file if it doesn't exist
        os.makedirs("temp", exist_ok=True)

        # Save the uploaded file
        with open(os.path.join("temp", screenshot.name), "wb") as f:
            f.write(screenshot.getbuffer())

        # Display the uploaded image
        st.image(screenshot, caption="Capture d'écran téléchargée", use_column_width=True)

        # Process the image
        confidence_threshold = st.slider("Seuil de confiance", min_value=0, max_value=100, value=30)

        if st.button("Détecter les numéros"):
            st.info("Détection des numéros en cours...")

            try:
                # Process the image file
                numbers, _ = detector.extract_numbers(os.path.join("temp", screenshot.name), confidence_threshold)

                if numbers:
                    st.success(f"Numéros détectés: {[num['text'] for num in numbers]}")

                    # Update the machine numbers
                    detected_numbers = [int(num['text']) for num in numbers if num['text'].isdigit()][:4]

                    # Pad with zeros if less than 4 numbers detected
                    while len(detected_numbers) < 4:
                        detected_numbers.append(0)

                    # Truncate if more than 4 numbers detected
                    detected_numbers = detected_numbers[:4]

                    st.session_state.TraderMachineNumber = detected_numbers
                    st.write(f"Numéros à configurer: {st.session_state.TraderMachineNumber}")
                else:
                    st.warning("Aucun numéro détecté. Essayez d'ajuster le seuil de confiance.")
            except Exception as e:
                st.error(f"Erreur lors de la détection: {str(e)}")



# Sidebar options
st.sidebar.title("Options")
st.sidebar.checkbox("Mode automatique", value=False)
st.sidebar.checkbox("Notifications", value=True)
st.sidebar.slider("Intervalle de vérification (min)", min_value=1, max_value=60, value=5)
