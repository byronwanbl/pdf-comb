work_path = "./work"  # 存放中间文件和输出文件的地址

src_path = "/home/you/your/source/path"  # 源地址, 为 cover 以及 files 的根目录

cover = "cover.pdf"  # 封面
files = (
    "markdown1.md",  # 支持 Markdown
    "pdf1.pdf",  # 支持 PDF
    "html1.html",  # 支持 html
    # "docx1.docx" # 理论上支持 docx, 但测试失败
    ("img1", "jpg1.jpg", "jpg2.jpg")  # 图片, 先将若干张图片组合成单独的一个文档, img1 为文档名称
)

pdf_engine = "weasyprint"  # Pandoc 用来导出成 PDF 的引擎, 具体参见 Pandoc 官网
