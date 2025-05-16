import copy

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []
        self._color = None
        self._year = None
        self._massimoCammino=[]

        self._choiceProduct = None

    def fillDDyear(self):
        self._listYear = self._model.get_anni()

        for a in self._listYear:
            self._view._ddyear.options.append(ft.dropdown.Option(text=a,
                                                                 data=a))

    def fillDDColors(self):
        self._listColor = self._model.get_corlors()

        for a in self._listColor:
            self._view._ddcolor.options.append(ft.dropdown.Option(text=a,
                                                                  data=a))

    def handle_graph(self, e):
        year = self._view._ddyear.value
        color = self._view._ddcolor.value

        if year is None or color is None:
            self._view.txtOut.controls.clear()
            self._view.txtOut.controls.append(
                ft.Text("Attenzione, selezionare anno e/o colore .", color="red"))
            self._view.update_page()
            return
        yearInt = int(year)
        self._model.buildGraph(color, yearInt)
        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append(ft.Text("Grafo correttamente creato!"))
        self._view.txtOut.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumNodi()} nodi."))
        self._view.txtOut.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumArchi()} archi."))
        self._view.update_page()

        sorted_edges = sorted(self._model._grafo.edges(data=True), key=lambda x: x[2].get('weight', 0), reverse=True)

        top_nodi = []
        top_nodi_rip = []
        # Print sorted edges
        for i, (u, v, data) in enumerate(sorted_edges):
            if i >= 3:
                break
            self._view.txtOut.controls.append(
                ft.Text(f"{u.Product_number} - {v.Product_number}: weight = {data['weight']}"))

            for nodo in (u.Product_number, v.Product_number):
                (top_nodi_rip if nodo in top_nodi else top_nodi).append(nodo)

        self.fillDDProduct()
        self._view.txtOut.controls.append(
            ft.Text(f" I nodi ripetuti sono {top_nodi_rip} "))
        self._view.update_page()

    def fillDDProduct(self):
        allP = self._model.getAllNodes()
        for n in allP:
            self._view._ddnode.options.append(
                ft.dropdown.Option(
                    data=n,
                    on_click=self.readDDProduct,
                    text=n.Product_number
                ))

    def readDDProduct(self, e):
        if e.control.data is None:
            self._choiceProduct = None
        else:
            self._choiceProduct = e.control.data
        print(f"readDDProduct called -- {self._choiceProduct}")

    #massimoCammino=[]
    def handle_search(self, e):
        nodoPartenza = self._choiceProduct

        camminoBest = self._model.ricorsione(nodoPartenza, [])

        for passo in camminoBest:
            self._view.txtOut2.controls.clear()
            self._view.txtOut2.controls.append(ft.Text(f"Numero di archi percorso più lungo: {len(camminoBest)}"))
            self._view.update_page()


