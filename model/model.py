import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.best_sol = None
        self.graph = nx.Graph()
        self.albums = DAO.get_all_albums()
        self.albums_map = {a.AlbumId: a for a in self.albums}

    def build_graph(self, durata):
        self.graph.clear()
        albums = DAO.get_nodes(durata, self.albums_map)
        self.graph.add_nodes_from(albums)
        for a1 in self.graph.nodes:
            for a2 in self.graph.nodes:
                if a1 != a2:
                    if DAO.get_edge(a1.AlbumId, a2.AlbumId) != "":
                        self.graph.add_edge(a1, a2)
        return self.graph

    def get_dimensione_connessa(self, album):
        return nx.node_connected_component(self.graph, album)

    def get_nBrani_connessa(self, connessa):
        album_brani = {}
        for album in connessa:
            album_brani[album] = DAO.get_n_brani(album.AlbumId)
        return album_brani

    def get_album_set(self, chosen_album, soglia):
        self.best_sol = []
        connessa = nx.node_connected_component(self.graph, chosen_album)
        self.ricorsione(set(), chosen_album, connessa, soglia)
        return self.best_sol

    def ricorsione(self, parziale, chosen_album, connessa, soglia):
        if len(parziale) > len(self.best_sol) and chosen_album in parziale:
            self.best_sol = copy.deepcopy(parziale)
            print(parziale)
        for album in connessa:
            if album.d_media <= soglia and album not in parziale:
                parziale.add(album)
                self.ricorsione(parziale, chosen_album, connessa, soglia)
                parziale.remove(album)
