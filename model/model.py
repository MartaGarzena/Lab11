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

