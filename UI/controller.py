import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.chosen_album = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_crea_grafo(self, e):
        try:
            durata = sec_to_milliseconds(int(self.view.txt_durata.value))
        except ValueError:
            self.view.create_alert("Inserire una durata in secondi")
            return
        graph = self.model.build_graph(durata)
        self.fill_dd_a1(graph)
        self.view.txt_soglia.disabled = False
        self.view.btn_analisi.disabled = False
        self.view.btn_set.disabled = False
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"Grafo con {len(graph.nodes)} nodi e {len(graph.edges)} archi"))
        self.view.update_page()

    def fill_dd_a1(self, graph):
        for album in graph.nodes:
            self.view.dd_a1.options.append(ft.dropdown.Option(data=album,
                                                              text=album,
                                                              on_click=self.read_album))
        self.view.dd_a1.disabled = False

    def read_album(self, e):
        if e.control.data is None:
            self.chosen_album = None
        self.chosen_album = e.control.data

    def handle_connessa(self, e):
        if self.chosen_album is None:
            self.view.create_alert("Selezionare un album")
            return
        connessa = self.model.get_dimensione_connessa(self.chosen_album)
        album_brani = self.model.get_nBrani_connessa(connessa)
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(
            ft.Text(f"La dimensione della componente connessa a cui appartiene '{self.chosen_album}' è {len(connessa)}"))
        self.view.txt_result.controls.append(ft.Text(f"Gli album di questa componente e il numero di brani:"))
        for a in album_brani:
            self.view.txt_result.controls.append(ft.Text(f"{a}, {album_brani[a]}"))
        self.view.update_page()

    def handle_set_album(self, e):
        if self.chosen_album is None:
            self.view.create_alert("Selezionare un album")
            return
        try:
            soglia = min_to_milliseconds(float(self.view.txt_soglia.value))
        except ValueError:
            self.view.create_alert("Inserire una soglia in minuti")
            return
        album_set = self.model.get_album_set(self.chosen_album, soglia)
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"Il set di album trovato è il seguente:"))
        for a in album_set:
            self.view.txt_result.controls.append(ft.Text(a))
        self.view.update_page()

    @property
    def view(self):
        return self._view

    @property
    def model(self):
        return self._model


def sec_to_milliseconds(durata):
    return durata * 1000


def min_to_milliseconds(durata):
    return durata * 3600 * 1000
