import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._choiceProdStart = None
        self._choiceProdEnd = None

    def handleCreaGrafo(self, e):
        category_id = self._view._ddcategory.value
        if category_id is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Seleziona una categoria dal menu", color = "red")
            )
            self._view.update_page()
            return

        date1 = self._view._dp1.value
        date2 = self._view._dp2.value
        if date1 is None or date2 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Seleziona una data di partenza e di fine", color = "red")
            )
            self._view.update_page()
            return

        self._model.buildGraph(category_id, date1, date2)
        self._fillDDProducts()

        numNodes, numEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text("Grafo correttamente creato", color="green")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo ha {numNodes} nodi e {numEdges} archi")
        )
        self._view.update_page()


    def handleBestProdotti(self, e):
        topProdotti = self._model.getTopProdotti()
        for p in topProdotti:
            self._view.txt_result.controls.append(
                ft.Text(f"{p} with score: {p.peso_archi_uscenti-p.peso_archi_entranti}")
            )
        self._view.update_page()

    def handleCercaCammino(self, e):
        if self._choiceProdStart is None or self._choiceProdEnd is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Scegli un prodotto di partenza e di arrivo", color ="red")
            )
            self._view.update_page()
            return
        lun = self._view._txtInLun.value
        if lun == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserisci un valore di lunghezza", color="red")
            )
            self._view.update_page()
            return
        try:
            lunInt = int(lun)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserisci un valore numerico intero", color="red")
            )
            self._view.update_page()
            return
        if lunInt<= 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserisci un valore positivo", color="red")
            )
            self._view.update_page()
            return

        self._model.getPath(self._choiceProdStart, self._choiceProdEnd, lunInt)

        path = self._model._solBest
        score = self._model._costoBest
        if len(path) == 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Non è stato trovato nessun cammino")
            )
            self._view.update_page()
            return
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Segue il cammino con peso massimo tra i nodi {self._choiceProdStart} e {self._choiceProdEnd} con peso {score}")
        )
        for p in path:
            self._view.txt_result.controls.append(
                ft.Text(p)
            )
        self._view.update_page()





    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)


    def fillDDCategories(self):
        categories = self._model.getAllCategories()
        for category in categories:
            self._view._ddcategory.options.append(
                ft.dropdown.Option(
                    key = category[0],
                    text = category[1]
                )
            )
        self._view.update_page()

    def _fillDDProducts(self):
        nodes = self._model._graph.nodes

        for n in nodes:
            self._view._ddProdStart.options.append(
                ft.dropdown.Option(
                    data = n,
                    key = n.product_id,
                    text = n.product_name,
                    on_click=self._readChoiceProdStart
                )
            )
            self._view._ddProdEnd.options.append(
                ft.dropdown.Option(
                    data=n,
                    key=n.product_id,
                    text=n.product_name,
                    on_click=self._readChoiceProdEnd
                )
            )
        self._view.update_page()

    def _readChoiceProdStart(self, e):
        if e.control.data is None:
            self._choiceProdStart = None
        self._choiceProdStart = e.control.data

    def _readChoiceProdEnd(self, e):
        if e.control.data is None:
            self._choiceProdEnd = None
        self._choiceProdEnd = e.control.data
