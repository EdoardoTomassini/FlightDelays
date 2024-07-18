import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceAeroportoP = None
        self._choiceAeroportoA = None

    def handleAnalizza(self, e):
        self._view._txt_result.controls.clear()
        nMin = self._view._txt_InNumCompagnie.value
        if nMin == "":
            self._view._txt_result.controls.append(
                ft.Text("Inserire un valore"))
            self._view.update_page()
            return
        try:
            nMinInt = int(nMin)
        except ValueError:
            self._view._txt_result.controls.append(
                ft.Text("Valore inserito non intero"))
            self._view.update_page()
            return

        self._model.buildGraph(nMinInt)
        nN, nE = self._model.getGraphDetails()
        self._view._txt_result.controls.append(
            ft.Text(f"Il grafo ha {nN} nodi e {nE} archi"))
        self._view.update_page()
        self._view._ddAeroportoP.disabled = False
        self._view._ddAeroportoA.disabled = False
        self._view._btnConnessi.disabled = False
        self._view._btnCercaItinerario.disabled = False
        self.fillDD()
        self._view.update_page()

    # def handleConnessi(self, e):
    #     if self._choiceAeroportoP is None:
    #         self._view._txt_result.controls.append(
    #             ft.Text("Selezionare un aeroporto di partenza"))
    #         self._view.update_page()
    #         return
    #     v0 = self._choiceAeroportoP
    #     vicini = self._model.getSortedVicini(v0)
    #
    #     self._view._txt_result.controls.append(ft.Text(f"Ecco i vicini di {v0}"))
    #     for v in vicini:
    #         self._view._txt_result.controls.append(
    #             ft.Text(f"{v[1]} - {v0}"))
    #
    #     self._view.update_page()

    def handleConnessi(self, e):
        if self._choiceAeroportoP is None:
            self._view._txt_result.controls.append(ft.Text(f"Selezionare un aeroporto di partenza"))
            return
        v0 = self._choiceAeroportoP
        vicini = self._model.getSortedVicini(v0)

        self._view._txt_result.controls.append(ft.Text(f"Ecco i vicini di {v0}"))
        for v in vicini:
            self._view._txt_result.controls.append(ft.Text(f"{v[1]} - {v[0]}"))

        self._view.update_page()

    def handleTestConnessione(self, e):
        if self._choiceAeroportoP is None:
            self._view._txt_result.controls.append(ft.Text(f"Selezionare un aeroporto di partenza"))
            self._view.update_page()
            return
        v0 = self._choiceAeroportoP

        if self._choiceAeroportoA is None:
            self._view._txt_result.controls.append(ft.Text(f"Selezionare un aeroporto di arrivo"))
            self._view.update_page()
            return

        v1 = self._choiceAeroportoA

        #Verificare che ci sia un percorso
        if(not self._model.esistePercorso(v0, v1)):
            self._view._txt_result.controls.append(
                ft.Text(f"Non esiste un percorso tra {v0} e {v1}"))
            self._view.update_page()
            return
        else:
            self._view._txt_result.controls.append(
                ft.Text(f"Trovato un percorso tra {v0} e {v1}"))

        #Trovare un percorso possibile
        path = self._model.trovaCamminoV2(v0, v1)
        self._view._txt_result.controls.append(
            ft.Text(f"il cammino con minor numero "
                    f"di archi (BFS) tra {v0} e {v1} è:"))
        for p in path:
            self._view._txt_result.controls.append(
                ft.Text(f"{p}"))

        self._view.update_page()


        self._view.update_page()

    def handleCercaItinerario(self, e):
        pass

    def fillDD(self):
        allNodes = self._model.getAllNodes()
        for nodo in allNodes:
            # devo appendere alle options del dropdown un oggetto di tipo Option
            # per questo ft.dropdown.Option()
            self._view._ddAeroportoP.options.append(
                ft.dropdown.Option(data=nodo,
                                   on_click=self.readDDAeroportoP,
                                   text=nodo.AIRPORT
                                   ))
            self._view._ddAeroportoA.options.append(
                ft.dropdown.Option(data=nodo,
                                   on_click=self.readDDAeroportoA,
                                   text=nodo.AIRPORT
                                   ))

    #metodo che cattura un evento e
    def readDDAeroportoP(self, e):
        self._view._txt_result.controls.clear()
        scelta = e.control.data
        if scelta is None:
            self._view._txt_result.controls.append("Non è stata effettuata nessuna scelta")
            self._view.update_page()
        else:
          self._choiceAeroportoP = scelta

    def readDDAeroportoA(self, e):
        self._view._txt_result.controls.clear()
        scelta = e.control.data
        if scelta is None:
            self._view._txt_result.controls.append("Non è stata effettuata nessuna scelta")
            self._view.update_page()
        else:
          self._choiceAeroportoA = scelta

