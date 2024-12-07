#!/usr/bin/env python3

import yaml

PATH = './tree.yaml'

if __name__ == '__main__':
    with open(PATH, 'r') as f:
        data = yaml.load(f, Loader=yaml.CLoader)

    print(data)
