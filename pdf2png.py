import fitz  # PyMuPDF
import os
from PIL import Image

def convert_single_page_pdfs_to_png(pdf_folder, output_folder, dpi=300):
    """
    将指定文件夹内的所有单页PDF文件（如matplotlib图）转换为PNG图片。

    Args:
        pdf_folder (str): 包含PDF文件的文件夹路径。
        output_folder (str): 输出PNG图片的文件夹路径。
        dpi (int): 输出图片的DPI (每英寸点数)，DPI越高图片越清晰但文件越大。
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            base_name = os.path.splitext(filename)[0] # 获取不带扩展名的文件名
            try:
                doc = fitz.open(pdf_path)
                # 检查PDF是否确实只有一页
                if doc.page_count != 1:
                    print(f"警告: 文件 '{filename}' 包含多页 ({doc.page_count} 页)。只会转换第一页。")

                page = doc[0] # 总是取第一页
                pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))

                # 创建PIL图像对象
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                # 输出PNG文件名直接使用原PDF文件名，只改变扩展名
                output_png_path = os.path.join(output_folder, f"{base_name}.png")
                img.save(output_png_path)
                print(f"已转换: {filename} -> {os.path.basename(output_png_path)}")
                doc.close()
            except Exception as e:
                print(f"处理文件 {filename} 时发生错误: {e}")

if __name__ == "__main__":
    # >>> 请替换为你的实际文件夹路径 <<<
    pdf_directory = "/Users/bytedance/Desktop/lxf/projects/alphapuzzle/alphapuzzle/assets/puzzles"
    output_directory = "/Users/bytedance/Desktop/lxf/projects/alphapuzzle/alphapuzzle/assets/puzzles"
    convert_single_page_pdfs_to_png(pdf_directory, output_directory, dpi=300)