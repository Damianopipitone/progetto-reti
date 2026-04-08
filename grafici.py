import pandas as pd
import matplotlib.pyplot as plt


# FASE DI CARICAMENTO E PREPARAZIONE DATI

print("Caricamento dati in corso...")

# Definiamo i nomi delle colonne manualmente per essere sicuri al 100%
colonne = ['timestamp', 'id_device', 'sensor_type', 'flow', 'volume']

# Leggiamo il file forzando i nomi delle colonne
data = pd.read_csv('sensor_log.csv', names=colonne, header=0)

# Convertiamo la colonna timestamp
data['timestamp'] = pd.to_datetime(data['timestamp'], format='mixed')

# Creiamo una "tela" con due grafici (uno sopra, uno sotto)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

print('Elenco sensori disponibili: ' \
'      1. Arch_sens1' \
'      2. Arch_sens2' \
'      3. Eng_sens1' \
'      4. Eng_sens2' \
'      5. Lit_sens1' \
'      6. Lit_sens2')
sensore_scelto = input('Inserisci il nome del sensore...')
grandezza = input('Inserisci la grandezza (flow/volume)...')

dati_sensore = data[data['id_device'] == sensore_scelto]

ax1.plot(dati_sensore['timestamp'], dati_sensore[grandezza], marker='o', color='b', linestyle='-')
ax1.set_title(f'Andamento {grandezza.capitalize()} nel tempo per {sensore_scelto}')
ax1.set_xlabel('Orario')
ax1.set_ylabel(f'{grandezza.capitalize()} (Litri)')
ax1.grid(True)

# Andamento temporale per un dipartimento

# Funzione per riconoscere il dipartimento dal nome del sensore
def assegna_dipartimento(nome_sensore):
    if 'Eng' in str(nome_sensore):
        return 'Ingegneria'
    elif 'Arch' in str(nome_sensore):
        return 'Architettura'
    elif 'Lit' in str(nome_sensore):
        return 'Lettere'
    return 'Altro'

# Creo la colonna 'dipartimento' direttamente nel dataframe principale
data['dipartimento'] = data['id_device'].apply(assegna_dipartimento)

# Raggruppo per Orario e Dipartimento, sommando i volumi!
volumi_temporali = data.groupby(['timestamp', 'dipartimento'])['volume'].sum().unstack()

# Rappresentazione grafica
volumi_temporali.plot(ax=ax2, marker='s', linewidth=2)
ax2.set_title('Andamento Temporale del Volume Totale per Dipartimento')
ax2.set_xlabel('Orario')
ax2.set_ylabel('Volume Totale (Litri)')
ax2.grid(True)
ax2.legend(title='Dipartimenti')

plt.tight_layout()
plt.show()