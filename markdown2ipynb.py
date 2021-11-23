# =*= coding: utf-8 -*-

"""Very simple markdown to IPython notebook converter.
_markdown2ipynb_ 用于将markdown 文件转变为 _IPython notebooks_ 的 .ipynb 格式文件

这个脚本将会处理markdown中如下的代码块

    ```[python/py]
    ...
    ```
"""
import json
import re


class NBStructure(dict):

    def __init__(self, name):
        """returns and empty ipynb notebook structure"""
        super(NBStructure, self).__init__()
        self.update((("metadata", {}),
                     ("nbformat", 4),
                     ("nbformat_minor", 2),
                     ("cells", [])))
        self["metadata"].update({
                "language_info": {
                "name": "python"
                },
                "orig_nbformat": 4
                })

    def addcell(self, cell):
        """Add a cell to the notebook"""
        self["cells"].append(cell)


class NBCodeCell(dict):

    def __init__(self):
        """returns an empty ipynb code cell"""
        super(NBCodeCell, self).__init__()
        self.update((("cell_type", "code"),
                     ("execution_count", None),
                     ("metadata", {}),
                     ("source", []),
                     ("outputs", [])))

    def load(self, string):
        """load code string into cell"""
        for line in string.split("\n"):
            self["source"].append(line + "\n")
        return self


class NBMarkdownCell(dict):

    def __init__(self):
        """returns an empty ipynb markdown cell"""
        super(NBMarkdownCell, self).__init__()
        self.update((("cell_type", "markdown"),
                     ("metadata", {}),
                     ("source", [])))

    def load(self, string):
        """load markdown string into cell"""
        for line in string.split("\n"):
            self["source"].append(line + "\n")
        return self


class IPyNB(object):

    def __init__(self, mdfile, name):
        """Ipython notebook abstraction"""
        self.base = NBStructure(name)
        data = mdfile.read()
        self.load(data)

    def load(self, string):
        """loads markdown and python from string data"""
        segments = re.split("(```.*?```)", string.replace("```python","```").replace("```py","```"), flags=re.DOTALL)
        for segment in segments:
            if segment.startswith('```') and segment.endswith('```'):
                newcell = NBCodeCell().load(segment[3:-3].strip())
            else:
                newcell = NBMarkdownCell().load(segment.strip('\n'))
            self.base.addcell(newcell)

    def write(self, outfile):
        """write ipynb file"""
        # print(self.base)
        outfile.write(json.dumps(self.base, indent=1, sort_keys=True))

if __name__ == "__main__":

    import argparse
    import sys

    parser = argparse.ArgumentParser(description="converts markdown to ipynb")
    parser.add_argument("mdfile", nargs='?', type=argparse.FileType('r',encoding='utf-8'), help="md input file")
    parser.add_argument('--out', type=argparse.FileType('w',encoding='utf-8'),
                        help="ipynb output file", default=sys.stdout)
    parser.add_argument('--name', type=str, help="ipynb name")
    args = parser.parse_args()

    name = args.out.name if args.name is None else args.name
    
    nb = IPyNB(args.mdfile, name)
    nb.write(args.out)
    print("view this output file: " + args.out.name)

"""
To create an **ipynb** just type:
要创建一个 **ipynb** 文件,请使用以下命令:  python markdown2ipynb.py --out sample\python100tips.ipynb sample\python100tips.md
"""