def download_wallpapers():
    import os
    import re
    from urllib.parse import urljoin
    import requests
    from .os import USER_HOME_PATH, save_file

    BING_WALLPAPERS_SAVE_PATH = os.path.join(USER_HOME_PATH, 'Pictures', 'BingWallpapers')
    wallpapers = []
    for url in ('https://cn.bing.com/HPImageArchive.aspx?format=js&idx=-1&n=8',
                'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=7&n=8'):
        try:
            response = requests.get(url, timeout=30)
            images = response.json().get('images', [])
            for image in images:
                date = image['enddate']  # 图片日期, 格式 YYYmmdd
                title = re.sub(r'(\s*\(©.*?\)\s*$|[【】])', '', image['copyright']).replace('，', '_').strip()  # 去除版权信息等
                url = urljoin('https://cn.bing.com', image['url'])  # 图片下载地址
                path = os.path.join(BING_WALLPAPERS_SAVE_PATH, f'{date}-{title}.jpg')  # 图片保存路径
                wallpapers.append((path, url))
        except BaseException:
            pass

    wallpapers.reverse()
    for path, url in wallpapers:
        try:
            print(os.path.basename(path), end=' ')
            save_error = save_file(path, url=url, timeout=30)
            assert not save_error, f'\033[1;31m{save_error}\033[0m'
            print('\033[1;32mdownload done\033[0m')
        except BaseException as error:
            print(error)
