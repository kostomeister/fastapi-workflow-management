import os

import networkx as nx


class FileStorage:
    def __init__(self):
        self.ensure_workflow_folder_exists()

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

    @staticmethod
    def ensure_workflow_folder_exists():
        folder_path = "workflows"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
