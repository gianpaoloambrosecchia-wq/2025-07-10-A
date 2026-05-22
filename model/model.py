import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapP = {}
        self._solBest = []
        self._costoBest = 0


    def getPath(self, start, end, lun):
        self._solBest = []
        self._costoBest = 0
        parziale = [start]
        self._ricorsione(parziale, end, lun)


    def _ricorsione(self, parziale, end, lun):
        # CASO BASE: Abbiamo raggiunto il numero di ARCHI richiesto (lunghezza del cammino)
        # uso len(parziale) -1 poichè lun è il numero di archi, parziale contiene i nodi
        # e il numero di achi è pari al numero di nodi meno 1
        if len(parziale) - 1 == lun:
            # Se siamo anche arrivati al nodo finale corretto, valutiamo la soluzione
            if parziale[-1] == end:
                if self._getScore(parziale) > self._costoBest:
                    self._solBest = copy.deepcopy(parziale)  # Va benissimo anche list(parziale) che è più veloce
                    self._costoBest = self._getScore(parziale)
            return  # BLOCCA SEMPRE la ricorsione qui, anche se non siamo nel nodo 'end'

        # RICORDA!!! In questo caso chiede che il cammino attraversi gli archi rispettando i versi,
        # quindi devo usare successors e non neighbors (dove può anche non rispettarli)
        for v in self._graph.successors(parziale[-1]):
            if v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale, end, lun)
                parziale.pop()


    def _getScore(self, parziale):
        score = 0
        for i in range(len(parziale)-1):
            score += self._graph[parziale[i]][parziale[i+1]]["weight"]
        return score



    def buildGraph(self, category_id, date1, date2):
        self._graph.clear()
        self._idMapP = {}
        nodes = DAO.getAllNodes(category_id)
        self._graph.add_nodes_from(nodes)
        for node in nodes:
            self._idMapP[node.product_id] = node

        DAO.getNumVendite(category_id, self._idMapP, date1, date2)
        archi = DAO.getArchi(category_id, self._idMapP, date1, date2)
        self._addEdges(archi)


    def _addEdges(self, archi):
        for a in archi:
            if a[0].num_vendite > a[1].num_vendite:
                self._graph.add_edge(a[0], a[1], weight = a[0].num_vendite+a[1].num_vendite)
                a[0].peso_archi_uscenti += a[0].num_vendite+a[1].num_vendite
                a[1].peso_archi_entranti += a[0].num_vendite+a[1].num_vendite
            elif a[1].num_vendite > a[0].num_vendite:
                self._graph.add_edge(a[1], a[0], weight = a[0].num_vendite+a[1].num_vendite)
                a[1].peso_archi_uscenti += a[0].num_vendite+a[1].num_vendite
                a[0].peso_archi_entranti += a[0].num_vendite+a[1].num_vendite
            else:
                self._graph.add_edge(a[0], a[1], weight=a[0].num_vendite + a[1].num_vendite)
                self._graph.add_edge(a[1], a[0], weight=a[0].num_vendite + a[1].num_vendite)
                a[0].peso_archi_uscenti += a[0].num_vendite + a[1].num_vendite
                a[1].peso_archi_entranti += a[0].num_vendite + a[1].num_vendite
                a[1].peso_archi_uscenti += a[0].num_vendite + a[1].num_vendite
                a[0].peso_archi_entranti += a[0].num_vendite + a[1].num_vendite




    def getDateRange(self):
        return DAO.getDateRange()

    def getAllCategories(self):
        return DAO.getAllCategories()

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getTopProdotti(self):
        top = sorted(self._graph.nodes, key=lambda x: x.peso_archi_uscenti-x.peso_archi_entranti, reverse=True)
        return top[0:5]