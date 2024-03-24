import os
import glob
import sys

sys.path.append(os.getcwd())


class PromptLibrarian:
    def __init__(self, root_path, endswith='.pmt'):
        self.endswith = endswith
        self.root = self._create_node(root_path)

    def _create_node(self, path):
        entries = glob.glob(os.path.join(path, '*'))
        node = {}
        for entry in entries:
            if os.path.isdir(entry):
                node[os.path.basename(entry)] = self._create_node(entry)
            elif entry.endswith(self.endswith):
                with open(entry, 'r', encoding='utf-8') as f:
                    node[os.path.basename(entry).rstrip(self.endswith)] = f.read()
        return node

    def print_tree(self, tree=None, parent_key='', level=0):
        """
        递归打印树结构
        :param tree:
        :param parent_key:
        :param level:
        :return:
        """
        tree = self.root if tree is None else tree
        space = '  '
        indent = space * level
        for key, value in tree.items():
            if isinstance(value, dict):
                print(f"{indent}|--- {key}")
                self.print_tree(value, f"{parent_key}.{key}", level + 1)
            else:
                print(f"{indent}|--- {key}")

    def read(self, path: str) -> str:
        """
        根据路径获取prompt内容
        :param path: "formatted.in_json.v1"
        :return:
        """
        # 通过路径获取节点内容
        path_list = path.split('.')
        node = self.root
        for p in path_list:
            node = node.get(p, None)
            if node is None:
                raise Exception(f"路径{path}中{p}不存在")
        return node

    def __str__(self):
        return str(self.root)


PromptLibrarian = PromptLibrarian(os.path.join(os.getcwd(), r"./utils/prompter/library"))
