#!/usr/bin/env python3

import yaml
import networkx as nx

PATH = './tree.yaml'

if __name__ == '__main__':
    with open(PATH, 'r') as f:
        data = yaml.load(f, Loader=yaml.CLoader)

    G = nx.from_dict_of_lists(data)
    print(G)
