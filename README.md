Questa repository contiene il codice e le fonti per il progetto dell'esame "Visualizzazione delle informazioni" 2024/2025.
Il progetto è stato portato avanti da:
- Alice Cecot
- Francesca Delli Carpini
- Lorenzo Battisti
- Sofia Lapi

il progetto propone una visualizzazione interattiva di eventi e connessioni ispirata all'universo della serie Dark, che permette di esplorare i legami tra personaggi, viaggi nel tempo e mondi paralleli.

## Funzionalità principali

### Visualizzazione Grafica
- Timeline cronologica degli eventi disposti sull'asse X (tempo) e Y (mondi: Jonas, Martha, Origin).
- Eventi rappresentati come *nodi*, con connessioni tra di essi rappresentate da *archi* (viaggi nel tempo, scambi di mondo, ecc.).
- Colori, forme e linee permettono una chiara distinzione tra tipologie di eventi e connessioni.

### Navigazione
- Zoom e pan tramite mouse.
- Tooltip e evidenziazione dinamica di nodi e archi con informazioni dettagliate.

### Filtri Interattivi
- Filtra eventi per:
  - *Mondo* (Jonas, Martha, Origin).
  - *Morte*: mostra solo eventi con decessi.
  - *Eventi chiave*: mostra solo trigger importanti.
  - *Intervallo temporale* (anno da / a).
  - *Personaggi coinvolti*, con modalità:
    - OR (almeno uno)
    - AND (tutti presenti)
  - *Tipologia di arco* (viaggio riuscito, fallito, entanglement, ecc.)

### Raggruppamento ed Espansione
- Eventi dello stesso giorno e mondo sono *raggruppati* in nodi aggregati.
- Clic su un nodo aggregato espande tutti i nodi interni
- Clic su una data espande quella data permettendo una visione più chiara degli eventi.

### Dettaglio Personaggi
- Pannello laterale con immagini e nomi dei personaggi coinvolti in ogni evento.


