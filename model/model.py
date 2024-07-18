import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._allAirports = DAO.getAllAirports()
        self._idMap = {}
        for a in self._allAirports:
            self._idMap[a.ID] = a

        self._grafo = nx.Graph()

    def buildGraph(self, nMin):
        self._nodi = DAO.getAllNodes(nMin, self._idMap)
        self._grafo.add_nodes_from(self._nodi)
        self.addEdgesV2()


    def addEdgesV2(self):
        allConnessioni = DAO.getAllEdgesV2(self._idMap)
        for c in allConnessioni:
            # devo controllare SEMPRE che gli oggetti siano nodi del grafo
            if c.V0 in self._grafo and c.V1 in self._grafo:
                self._grafo.add_edge(c.V0, c.V1, weight=c.N)

    def esistePercorso(self, v0, v1):
        # questo metodo restituisce la componente connessa che contiene v0
        connessa = nx.node_connected_component(self._grafo, v0)
        if v1 in connessa:
            return True
        return False

    #trovaCamminoV1 si riferisce a versione 1, non a v1 parametro passato
    def trovaCamminoV1(self, v0, v1):
        #Questo ci restituisce il cammino ottimo
        return nx.dijkstra_path(self._grafo,
                         v0,
                         v1)
    def trovaCamminoV2(self, v0, v1):
        #Questo ci restituisce un grafo orientato
        #albero di visita
        tree = nx.bfs_tree(self._grafo, v0)
        if v1 in tree:
            print(f"{v1} è presente nell'albero di vistia BFS")

        #Come recupero il cammino (path)?
        path = [v1]
        while path[-1] != v0:
            #da rivedere bene
            path.append(list(tree.predecessors(path[-1]))[0])

        path.reverse()
        return path

    def trovaCamminoV3(self, v0, v1):
        tree = nx.dfs_tree(self._grafo, v0)
        if v1 in tree:
            print(f"{v1} è presente nell'albero di vistia DFS")

        # Come recupero il cammino (path)?
        path = [v1]
        while path[-1] != v0:
            # da rivedere bene
            path.append(list(tree.predecessors(path[-1]))[0])

        path.reverse()
        return path


    def printGRaphDetails(self):
        print(f"Il grafo ha {len(self._grafo.nodes)} nodi ")
        print(f"Il grafo ha {len(self._grafo.edges)} archi ")

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    # def getSortedVicini(self, v0):
    #     # per ottenere i vicini self._grafo.neighbors(v0)
    #     vicini = self._grafo.neighbors(v0)
    #     viciniTuple = []
    #     for v in vicini:
    #         viciniTuple.append((v, self._grafo[v0][v]["weight"]))
    #     #questa funzione sort ordina gli elementi della lista di tuple
    #     #in base al parametro lambda, cioè in base al secondo elemento inserito
    #     #negli elementi della tupla viciniTuples -----> il peso dell'arco tra
    #     # v0 e v
    #     viciniTuple.sort(key=lambda x: x[1], reverse=True)
    #     return viciniTuple

    def getSortedVicini(self, v0):
        vicini = self._grafo.neighbors(v0)
        viciniTuple = []
        for v in vicini:
            viciniTuple.append((v, self._grafo[v0][v]["weight"]))
        viciniTuple.sort(key=lambda x: x[1], reverse=True)

        return viciniTuple

    def getAllNodes(self):
        return self._nodi