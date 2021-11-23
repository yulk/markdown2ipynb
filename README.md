# markdown2ipynb #

Very simple markdown to IPython notebook converter.
_markdown2ipynb_ 用于将markdown 文件转变为 _IPython notebooks_ 的 .ipynb 格式文件

This script will take code blocks that look like
这个脚本将会处理markdown中如下的代码块

    ```[python/py]
    ...
    ```

把他们用IPython的code单元格包裹起来. 其他的部分则用markdown单元格包裹.
And wrap them in an IPython code cell. All other parts are wrapped in markdown
cells.

To create an **ipynb** just type:
要创建一个 **ipynb** 文件,请使用以下命令:

    python markdown2ipynb.py --out python100tips.ipynb python100tips.md


origin from https://github.com/ap--/md2ipynb
rebuild for modern python book (v4.2) by dreamrise: https://github.com/yulk/markdown2ipynb
