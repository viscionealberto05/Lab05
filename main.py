import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    """-------------------------------------------------"""

    """          --- HANDLER DEL COUNTER ---            """

    def handleAdd(e):
        currentVal = txtOut.value

        txtOut.value = currentVal + 1
        txtOut.update()

    def handleRemove(e):
        currentVal = txtOut.value

        txtOut.value = currentVal - 1
        txtOut.update()

    """------------------------------------------------"""

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata, scrollabile
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)

    marcaAuto = ft.TextField(value="",label="Marca")    #Value="" codice superfluo, value può essere modificato senza inizializzarlo in textfield
    modelloAuto = ft.TextField(value="",label="Modello")
    annoAuto = ft.TextField(value="",label="Anno")

    btnMinus = ft.IconButton(icon=ft.Icons.REMOVE,
                             icon_color="red",
                             icon_size=24, on_click=handleRemove)

    btnAdd = ft.IconButton(icon=ft.Icons.ADD,
                           icon_color="green",
                           icon_size=24, on_click=handleAdd)

    txtOut = ft.TextField(width=100, disabled=True,
                          value=0, border_color="green",
                          text_align=ft.TextAlign.CENTER)


    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # --- HANDLER AGGIUNTA NUOVA AUTO ---

    # La funzione viene chiamata quando si clicca sul bottone "Aggiungi", definito sotto la funzione
    # che viene chiamata in caso di click

    def nuova_auto(e):

        #INIZIALIZZO I PARAMETRI CHE PASSERO' COME ARGOMENTI AL METODO aggiungi_automobile
        #DELLA CLASSE autonoleggio

        marca = marcaAuto.value
        modello = modelloAuto.value
        anno = annoAuto.value
        posti = txtOut.value

        #VERIFICA DELLA VALIDITA' DEI DATI IMMESSI DALL'UTENTE
        #   Controllo prima di tutto che il valore inserito per l'anno sia un numero,
        #   dopodichè verifico che quest'ultimo e il numero di posti siano entrambi positivi

        try:
            anno = int(anno)
            if anno >= 0 and int(posti) > 0:

                #Chiamo il metodo per inserire la nuova auto nella lista

                autonoleggio.aggiungi_automobile(marca,modello,anno,posti)

                #Pulisco dunque i campi di tutti i textfield che ho precedentemente introdotto

                marcaAuto.value = ""
                modelloAuto.value = ""
                annoAuto.value = ""
                txtOut.value = 0

                #Concludo aggiornando la lista e mostrandola a schermo

                aggiorna_lista_auto()
                page.update()
            else:

                alert.show_alert("Errore: Valori non validi inseriti per il numero di posti o l'anno!")
        except Exception as ValueError:
            alert.show_alert("Errore: Inserisci un valore numerico per l'anno di immatricolazione.")


    # --- BOTTONI ---

    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)
    pulsante_aggiunta_auto = ft.ElevatedButton("Aggiungi", on_click=nuova_auto)


    # --- LAYOUT ---

    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(),

        ft.Text(value="Aggiungi Automobile", size=25, weight=ft.FontWeight.BOLD),


        ft.Row(spacing=8,
               controls=[marcaAuto, modelloAuto, annoAuto, btnMinus, txtOut, btnAdd],
               alignment=ft.MainAxisAlignment.CENTER),

        pulsante_aggiunta_auto,

        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
