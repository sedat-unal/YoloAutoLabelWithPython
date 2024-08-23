import os


def rename_images(folder_path, format_string):
    files = os.listdir(folder_path)

    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    for i, image_file in enumerate(image_files, start=1):
        old_path = os.path.join(folder_path, image_file)

        new_name = format_string.format(index=i)
        new_path = os.path.join(folder_path, new_name)

        os.rename(old_path, new_path)

        # rename with .txt file
        # if you dont need comment out this block

        root_old, extension_old = os.path.splitext(old_path)
        root, extension = os.path.splitext(new_path)

        old_txt = f"{root_old}.txt"
        new_txt = f"{root}.txt"
        if os.path.exists(old_txt):
            os.rename(old_txt, new_txt)
            print(f"Renamed TXT : {old_txt} -> {new_txt}")
        else:
            print(f"cant find file => {old_txt}")

        print(f"Renamed Image : {old_path} -> {new_path}")


if __name__ == "__main__":
    klasor_yolu = "C:\\Users\\sedat.unal\\Desktop\\TRAIN_PHOTOS\\all_label\\front"
    yeni_isim_formati = "tr_id_front_with_label_{index}.png"

    rename_images(klasor_yolu, yeni_isim_formati)
