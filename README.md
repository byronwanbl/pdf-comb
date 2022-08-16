# Pdf-Comb

生成简单的 PDF 书籍。

支持自动转换文件，生成目录，添加页码，添加封面。

需要根据 `config.example.py` 自行配置 `config.py`。

依赖:

- [Pandoc](https://pandoc.org/index.html) ， 需要在 `PATH` 中有 Pandoc 可执行文件。

- [weasyprint](https://pypi.org/project/WEasyPrint) ，Pandoc 的 PDF 引擎，可以更换。

- [PyMuPdf](https://pymupdf.readthedocs.io/en/latest/#) ，操纵 PDF 的 Python 库。

## 安装和使用

```bash
git clone https://github.com/byronwanbl/pdf-comb
cd pdf-comb

python -m venv ./venv
source ./venv/bin/active

pip install weasyprint
pip install pymupdf

# 可以提前安装 pandoc
# 或者用如下命令下载 pandoc 可执行文件 (linux amd64)
curl -L https://github.com/jgm/pandoc/releases/download/2.19/pandoc-2.19-linux-amd64.tar.gz -o pandoc.tar.gz
tar -xzf pandoc.tar.gz pandoc-2.19/bin/pandoc 
export PATH=$PATH:./pandoc-2.19/bin

cp config.example.py config.py
# 参照注释, 编辑 config.py

python pdf_comb.py
```

## 已知问题

1. 使用 Pandoc 转换的页面会上添加的文字会上下翻转，
   猜测可能是 PyMuPdf 和 Pandoc 的 PDF 引擎的兼容性问题。
