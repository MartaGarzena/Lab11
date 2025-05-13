import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []
        self._color=None
        self._year=None


    def fillDDyear(self):
        self._listYear  = self._model.get_anni()

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

        # Print sorted edges

        for u, v, data in sorted_edges:
            self._view.txtOut.controls.append(ft.Text(f"{u} - {v}: weight = {data['weight']}"))

        self._view.update_page()



    def fillDDProduct(self):
        pass


    def handle_search(self, e):
        pass
