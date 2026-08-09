import os
import re

from tqdm import tqdm

from epub_chapter import Chapter, is_volume, is_chapter, fit_space


def main():
    data_path = r'H:\Download\庆余年\data'
    atc = [os.path.abspath(os.path.join(data_path, i)) for i in os.listdir(data_path) if i.startswith('index_split')]
    cpt = Chapter(atc[0])
    for index, file in tqdm(enumerate(atc[1:])):
        cpt.body += Chapter().load_from_file(file).body
    new_chapter = cpt.clone()
    volume_name = ""
    previous_index = 0
    total_index = 0
    title = "引言"
    paragraph = list(cpt.body.paragraphs())
    for index, para in paragraph:
        if is_volume(para.text):
            if is_chapter(para.text):
                new_chapter.body.set_para(cpt[previous_index:index])
                new_chapter.set_title(title)
                previous_index = index
                title = f"{fit_space(para.text.replace("卷", "卷 "))}"
            else:
                volume_name = para.text
        elif is_chapter(para.text):
            if volume_name:
                new_chapter.body.set_para(cpt[previous_index:index - 1])
                new_chapter.set_title(title)
                previous_index = index - 1
                title = f"{volume_name} {para.text}"
                volume_name = ""
        elif volume_name:
            print(f"Error Occured in {index} - {para.text}\nvolume_name = {volume_name}")
            ipt = input("(Y/N)")
            if ipt.lower() == "y":
                new_chapter.body.set_para(cpt[previous_index:index - 1])
                new_chapter.set_title(title)
                previous_index = index - 1
                title = f"{fit_space(volume_name.replace("卷", "卷 "))}"
                volume_name = ""
            else:
                print(ipt)
        if not new_chapter.is_empty():
            for indexx, paraa in new_chapter.body.paragraphs():
                paraa.text = re.sub(r'\s+', '', paraa.text).strip()
            new_chapter.save_to_file(f"out/{total_index:03}.html")
            print(f"已保存文件 {total_index} in para{index} 《{new_chapter.title}》")
            total_index += 1
            new_chapter = cpt.clone()


main()
