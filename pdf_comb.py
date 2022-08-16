import os
import fitz  # PyMuPdf 操作 PDF 的库
import subprocess
import time

import fix_quotes
from config import *
# 相关配置, 需要自行完善, 参见 config.example.py


def main():
    if not os.path.exists(work_path):
        os.mkdir(work_path)

    out_list = process_files(files)
    cover_out = process_file(cover)
    index = calc_and_add_page_number(out_list)
    index_file = generate_index(out_list, index)
    metadata_file = generate_metadata(files)

    out = join_all_pdf([cover_out, index_file] +
                       out_list + [metadata_file])
    print(f"Generated file {out}")


def process_files(sources) -> list[str]:
    out_list = []
    for src in sources:
        out_list.append(process_file(src))
    return out_list


def process_file(src: tuple | list | str) -> str:
    """
    处理文件, 返回处理后文件名.
    """
    if isinstance(src, tuple | list):
        out_filename = src[0]
        images = map(lambda f: os.path.join(src_path, f), src[1:])
        print(f"Process {out_filename}, covert images to PDF.")
        out = image_to_pdf(out_filename, images)
    elif src.endswith(".PDF"):
        print(f"Copy {src}.")
        copy_file(os.path.join(src_path, src),
                  os.path.join(work_path, src))
        out = os.path.join(work_path, src)
    else:
        print(f"Processing {src}, using Pandoc.")
        fix_quotes.fix_quotes_file_inplace(os.path.join(src_path, src))
        out = to_pdf(os.path.join(src_path, src))
    return out


def calc_and_add_page_number(out_list: tuple[str]) -> map:
    """
    计算并直接在页面上加上页码.
    BUG: 使用 Pandoc 转换的页面会上添加的文字会上下翻转,
         猜测可能是 PyMuPdf 和 Pandoc 的 PDF 引擎的兼容性问题.
    """
    print("Calculating page number and add to PDF files.")
    num = 0
    page_num_map = {}
    for out in out_list:
        doc = fitz.open(out)
        page_num_map[out] = num + 1
        for page in doc:
            num += 1
            page.insert_text(
                fitz.Point(page.rect.x0 + 20, page.rect.y0 + 20),
                f"{num}", fontsize=16)
        doc.saveIncr()
    return page_num_map


def generate_index(out_list: tuple[str], index: map):
    """
    生成目录。
    文件名中的下划线会被替换成空格。
    """
    print("Generating index.")
    index_filename = os.path.join(work_path, "index.md")
    with open(index_filename, "w") as f:
        f.write("# 目录\n")

        for out in out_list:
            name = os.path.basename(out).split(".")[0].replace("_", " ")
            f.write(f"#### {name} —— {index[out]}\n")

        f.write("\n")

    return to_pdf(index_filename)


def generate_metadata(files: tuple[str]):
    """
    生成源数据。
    包括：CopyRight，时间，源文件。
    """
    print("Generating extra metadata.")
    metadata_filename = os.path.join(work_path, "metadata.md")
    with open(metadata_filename, "w") as f:
        f.write("# Extra Metadata\n")
        f.write("Generate by `pdf_comb`. \n\n")
        f.write(
            f"Copyright ByronWan here (c) 2022-{time.localtime(time.time()).tm_year}. All rights reserved.\n\n")
        f.write("---\n\n")
        f.write(
            f"Generate time: {time.asctime(time.localtime(time.time()))}\n\n")
        f.write(f"Source files: \n\n")
        f.write(f"```\n")
        f.write(str(files))
        f.write(f"\n```\n")
        f.write(f"\n")
    return to_pdf(metadata_filename)


def to_pdf(filename: str) -> str:
    """
    使用 Pandoc 转换至 PDF.
    """
    new_filename = os.path.join(
        work_path, os.path.basename(filename) + ".PDF")
    run(
        f"./pandoc -f markdown -t PDF --PDF-engine {pdf_engine} {filename} -o {new_filename}")
    return new_filename


def image_to_pdf(out: str, images: tuple[str]) -> str:
    """
    将图片转换成 pdf。
    每页一张图片，自动居中。
    """
    out = os.path.join(work_path, out + ".PDF")
    doc = fitz.Document()

    for image in images:
        page = doc.new_page()
        page.insert_image(page.rect, filename=image)

    doc.save(out)

    return out


def join_all_pdf(filenames: tuple[str]):
    """
    拼接所有 PDF 文件。
    """
    print("Joining all PDF files.")
    out = fitz.Document()

    for filename in filenames:
        file = fitz.open(filename)
        out.insert_pdf(file)

    name = os.path.join(work_path, "out.PDF")
    out.save(name)
    return name


def run(cmd: str | tuple[str]):
    """
    调用 shell 命令。
    运行失败时会终止程序。
    """
    subprocess.run(cmd if isinstance(cmd, str) else " ".join(
        map(lambda s: f"\"{s}\"", cmd)), shell=True, check=True, text=True)


def copy_file(src: str, dst: str):
    """
    使用系统命令复制文件。
    (不使用 Shutil 是因为 Shutil 比较慢。)
    """
    if os.name == "nt":
        run(("copy", src, dst))
    else:
        run(("cp", src, dst))


if __name__ == "__main__":
    main()
