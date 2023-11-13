# TODO

## server
* capire perchè il sistema non si accorge quando un sensore è morto (sembra che non funzioni lo status = dead) => pare che dopo il riavvio riesca ad accorgersene
* mettere il node['status'] dead anche al keep_alive della classe Protocols
* fare in modo che il keep_alive_tread esegua il protocollo di Protocols
* fare un logging su file disabilitabile da linea di comando e da telegram bot, il file di log deve essere stampabile su richiesta da telegram bot, e CLI (definendo numero di righe)
* capire perchè il sistema non funzoiona in background

## sensor node

