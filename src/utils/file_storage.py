import os

import networkx as nx


class FileStorage:
    @staticmethod
    async def save_workflow_file(file_path: str, name: str, G=None):
        if G is None:
            G = nx.DiGraph(name=name)
        nx.write_graphml(G, file_path)

    @staticmethod
    async def delete_workflow_file(file_path: str):
        os.remove(file_path)

    @staticmethod
    def read_workflow_file(file_path: str) -> nx.DiGraph:
        return nx.read_graphml(file_path)
