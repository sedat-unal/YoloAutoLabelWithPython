from app.app.core import core, get_input_data


def start_process(input_image_path, output_path, max_angle, rotate_angle):
    input_datas = get_input_data(input_folder=input_image_path)
    for input in input_datas:
        core(
            input_img_path=input,
            output_path=output_path,
            max_angle=max_angle,
            rotate_angle=rotate_angle
        )
    return True