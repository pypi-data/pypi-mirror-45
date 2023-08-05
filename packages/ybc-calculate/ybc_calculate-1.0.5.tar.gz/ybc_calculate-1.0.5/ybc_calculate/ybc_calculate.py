import ybc_config
import sys
import os
import requests
from PIL import Image, ImageDraw
import time

from ybc_exception import *

__PREFIX = ybc_config.config['prefix']
__MENTAL_MATH_URL = __PREFIX + ybc_config.uri + '/mental-math'
__MAX_OUTLINE_THICKNESS = 5
__MIN_OUTLINE_THICKNESS = 2
__ICON_WIDTH = 40
__MAX_ICON_MARGIN = 10
__MIN_ICON_MARGIN = 2
__MARK_CONFIG = {
    1: {
        'outline': '#45DBA6',
        'icon': 'icon_correct.png'
    },
    2: {
        'outline': '#FF4F48',
        'icon': 'icon_error.png'
    },
    3: {
        'outline': '#FFAF02',
        'icon': 'icon_warning.png'
    }
}


def check(image=''):
    """
    批改图片中出现的算式

    :param image:   包含待批改算式的图片
    :return:        返回标注了批改结果的图片的名字，如果未检测到算式，返回 -1;
    """
    error_flag = 1
    # 参数类型正确性判断
    error_msg = ""
    if not (isinstance(image, str)):
        error_flag = -1
        error_msg = "'image'"
    if error_flag == -1:
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)

    try:
        try:
            ybc_config.resize_if_too_large(image)
        except Exception:
            return -1
        file_path = os.path.abspath(image)
        files = {'file': open(file_path, 'rb')}
        url = __MENTAL_MATH_URL

        for i in range(3):
            r = requests.post(url, files=files)
            if r.status_code == 200:
                res = r.json()
                if len(res) <= 0:
                    return -1
                original_image = Image.open(image)
                __mark_image(image=original_image, search_results=res)
                processed_image_name = os.path.splitext(image)[0] + '_' + str(int(time.time())) + '_result.png'
                original_image.save(processed_image_name)
                files['file'].close()
                return processed_image_name

        raise ConnectionError("check 方法调用失败: 请稍后再试")
    except Exception as e:
        raise InternalError(e, 'ybc_calculate')


def __mark_image(image, search_results):
    min_region_height = sys.maxsize
    for search_result in search_results:
        if search_result['result_type'] != 1:
            # 不是口算批改结果
            continue
        region = search_result['region']
        width, height = region['width'], region['height']
        min_region_height = min(min_region_height, height)

    '''
    识别出来的算式的区域的高度有可能会比图标小，
    此时为了把图标放入框内，需要对图标进行缩放，
    同时图标周围的空白也要缩小，
    框的线条粗度也要相应减小
    '''
    if min_region_height >= __ICON_WIDTH + __MAX_ICON_MARGIN * 2:
        icon_margin = __MAX_ICON_MARGIN
    else:
        icon_margin = int(max(min_region_height / 6, __MIN_ICON_MARGIN))

    icon_width = min(min_region_height - icon_margin * 2, __ICON_WIDTH)
    if icon_width <= 0:
        icon_width = min_region_height
        icon_margin = 0
    outline_thickness = max((min_region_height - icon_width) / icon_margin, __MIN_OUTLINE_THICKNESS)
    outline_thickness = min(outline_thickness, __MAX_OUTLINE_THICKNESS)

    for search_result in search_results:
        if search_result['result_type'] != 1:
            # 不是口算批改结果
            continue
        region = search_result['region']
        search_result_type = search_result['type']
        draw = ImageDraw.Draw(image)
        x0, y0 = region['x'], region['y']
        x1, y1 = region['x'] + region['width'] + icon_width + icon_margin * 2, region['y'] + region['height']
        points = (x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)
        current_module_file_path = os.path.abspath(__file__)
        current_pkg_path = os.path.split(current_module_file_path)[0]
        if search_result_type > 1:
            draw.line(points, fill=__MARK_CONFIG[search_result_type]['outline'], width=int(outline_thickness))
        icon = Image.open(current_pkg_path + '/' + __MARK_CONFIG[search_result_type]['icon'])
        icon.thumbnail((icon_width, icon_width), Image.ANTIALIAS)
        icon_pos = (x1 - icon_width - icon_margin, int((y0 + y1 - icon_width) / 2))
        image.paste(icon, icon_pos, icon)


def main():
    result = check('test.jpg')
    print(result)
    result = check('test.txt')
    print(result)


if __name__ == '__main__':
    main()
