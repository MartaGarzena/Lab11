import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._anni = DAO.getAnni()
        self._colors = DAO.getColors()
        self._listAnni = []
        self._listColors = []

        self._grafo = nx.Graph()
        self._prodotti= DAO.getAllProdotti()
        self._massimoCammino = []

        self._idMapProdotti = {}
        for p in self._prodotti:
            self._idMapProdotti[p.Product_number] = p

        self._nodes = self._grafo.nodes

    def get_anni(self):
        for e in self._anni:
            for anno in list(e.values()):
                self._listAnni.append(anno)
        return self._listAnni

    def get_corlors(self):
        for e in self._colors:
            for c in list(e.values()):
                self._listColors.append(c)
        return self._listColors

    def buildGraph(self,color, anno):
        # Aggiungiamo i nodi
        self._listProductsColor=DAO.getProductsFromColor(color)
        self._grafo.add_nodes_from(self._listProductsColor)
        self.addAllEdges(anno)

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    def addAllEdges(self,anno):
        for n1 in self._nodes:
            for n2 in self._nodes:
                if n1 != n2:
                    count = DAO.getPeso(n1.Product_number, n2.Product_number, anno)
                    if count[0] > 0:
                        self._grafo.add_edge(n1, n2, weight=count[0])

    def getAllNodes(self):
        return list(self._grafo.nodes)

    def ricorsione(self, nodoCorrente, camminoAttuale):
        if len(camminoAttuale) > len(self._massimoCammino):
            self._massimoCammino = copy.deepcopy(camminoAttuale)

        # camminoAttuale.append(NodoPartenza)
        # ricorisione(camminoAttuale,nodiGiaVisitati,pesoUtilmoArco  :
        # for nodo in vicini(camminoAttulae[-1])
        # if nodo not in nodiGiaVisitati and grafo[nodo][NodoPartenza] > pesoUltimoArco:
        # camminoAttuale.append(arco)
        # else:

        for u, v, data in self._grafo.edges(nodoCorrente, data=True):
            # In un grafo non orientato, v può essere nodoCorrente o il vicino
            nodoSuccessivo = v if u == nodoCorrente else u
            pesoArco = data['weight']

            if not self.arcoUsato(u,v,camminoAttuale) and self.pesoCrescente(pesoArco,camminoAttuale):
                camminoAttuale.append((u, v, pesoArco))

                self.ricorsione(nodoSuccessivo, camminoAttuale)

                camminoAttuale.pop()

        return self._massimoCammino

    def arcoUsato(self, u, v, camminoAttuale):
        for a in camminoAttuale:
            if (a[0] == u and a[1] == v) or (a[0] == v and a[1] == u):
                return True
        return False

    def pesoCrescente(self, pesoNuovo, camminoAttuale):
        return len(camminoAttuale) == 0 or pesoNuovo >= camminoAttuale[-1][2]

