# bash launcher.sh
#!/bin/bash
# Projet personnel - Siyu WANG
# Install the dependencies and run the application

echo "******** Projet Personnel - Siyu WANG *********"
echo "--- Installation des dépendances ---"
pip3 install -r requirements.txt
echo "--- Scraping ---"
python3 projet_siyu.py
echo "--- Run the application ---"
streamlit run visualisation.py
