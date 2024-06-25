import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self.page = page
        self.page.title = "Template application using MVC and DAO"
        self.page.horizontal_alignment = 'CENTER'
        self.page.theme_mode = ft.ThemeMode.DARK
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_durata = None
        self.btn_grafo = None
        self.dd_a1 = None
        self.btn_analisi = None
        self.txt_soglia = None
        self.btn_set = None
        self.txt_result = None

    def load_interface(self):
        # title
        self._title = ft.Text("Hello World", color="blue", size=24)
        self.page.controls.append(self._title)

        self.txt_durata = ft.TextField(label="Durata")
        self.btn_grafo = ft.ElevatedButton(text="Crea grafo", on_click=self.controller.handle_crea_grafo)
        row1 = ft.Row([self.txt_durata, self.btn_grafo], alignment=ft.MainAxisAlignment.CENTER)
        self.page.controls.append(row1)

        self.dd_a1 = ft.Dropdown(label="Album", disabled=True)
        self.btn_analisi = ft.ElevatedButton(text="Analisi componente",
                                             disabled=True,
                                             on_click=self.controller.handle_connessa)
        row2 = ft.Row([self.dd_a1, self.btn_analisi], alignment=ft.MainAxisAlignment.CENTER)
        self.page.controls.append(row2)

        self.txt_soglia = ft.TextField(label="Soglia", disabled=True)
        self.btn_set = ft.ElevatedButton(text="Set di album",
                                         disabled=True,
                                         on_click=self.controller.handle_set_album)
        row3 = ft.Row([self.txt_soglia, self.btn_set], alignment=ft.MainAxisAlignment.CENTER)
        self.page.controls.append(row3)

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self.page.controls.append(self.txt_result)
        self.page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def update_page(self):
        self.page.update()
