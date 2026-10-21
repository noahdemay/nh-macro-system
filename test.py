import matplotlib.pyplot as plt
import yfinance as yf

# Récupération de l'EUR/USD sur 1 mois
print("Téléchargement des données...")
data = yf.download("EURUSD=X", period="1mo", interval="1d")

# Affichage des 5 dernières lignes dans le terminal
print("\nDernières cotations :")
print(data.tail())

# Affichage du graphique
data["Close"].plot(title="EUR/USD - 1 mois", figsize=(9, 5))
plt.xlabel("Date")
plt.ylabel("Taux de change")
plt.grid(True)
plt.tight_layout()
plt.show()
