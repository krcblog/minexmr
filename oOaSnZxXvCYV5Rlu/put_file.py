from default import base64, gen_name, requests, settings, time


def path_unify(file_path: str):
    return file_path.replace('\\', '/')


def get_time():
    return time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())


def cdn_get(account_name=settings.account_name, repo_name=settings.repo_name, full_path="$"):
    try:
        cdn_address = "https://cdn.jsdelivr.net/gh/" + \
            account_name + "/" + repo_name + "/" + full_path
        cdn_result = requests.get(url=cdn_address, stream=True)
        if cdn_result.status_code == 200:
            print("CDN Available. Address: \n{}".format(
                cdn_address))
        else:
            print(
                "CDN Unavailable. Alternative address: \nhttps://github.com/{}/{}/raw/master/{}".format(settings.account_name, repo_name, full_path))
    except:
        print("CDN test failed. File address: \nhttps://github.com/{}/{}/raw/master/{}".format(
            settings.account_name, repo_name, full_path))


def get_file(file_path: str):
    try:
        with open(file_path, "rb") as File:
            file = File.read()
            return file
    except:
        print("========== File {} not found. ==========".format(file_path))
        return False


def put_file(file_path: str, account_name=settings.account_name, repo_name=settings.repo_name, remote_path_setting="-1", remote_name_setting=0, cdn_test=True, proxy=False, proxies=settings.proxies):
    # remote_path_setting
    # -1: 直接放在根目录下
    # 其它数字: 生成 remote_path_setting(0,62] 个随机字符作为目录名
    # 字符串: 以该字符串为目录名

    # remote_name_setting
    # -1: 保留源文件名
    # 0: 使用文件 hash 值作为文件名
    # 其它数字: 生成 remote_name_setting(0,62] 个随机字符作为文件名

    # 传入file_path之前需要先对其进行path_unify操作

    file = get_file(file_path)
    if file != False:
        remote_file_name = file_path.split('/')[-1] if remote_name_setting == -1 else ((gen_name.gen(str(file).encode()) if remote_name_setting == 0 else gen_name.simple_gen(
            remote_name_setting)) + '.' + file_path.split('.')[-1])

        remote_full_path = ("" if remote_path_setting == "-1" else ((remote_path_setting if
                                                                     remote_path_setting.isdigit() == False
                                                                     else gen_name.simple_gen(int(remote_path_setting)))
                                                                    + '/')) + remote_file_name

        request_url = settings.base_url + "repos/" + account_name + \
            "/" + repo_name + "/contents/" + remote_full_path

        file_content = base64.b64encode(file)

        content = {"message": "@MinecraftFuns: Original file: {}".format(file_path), "committer": {
            "name": settings.user_name, "email": settings.user_mail}, "content": str(file_content)[2:-1]}

        request_headers = {
            "Accept": "application/vnd.github.v3+json", "Authorization": "token " + settings.u_token}

        is_passed = False

        while is_passed != True:
            try:
                result = requests.put(
                    url=request_url, json=content, headers=request_headers) if proxy == False else requests.put(
                    url=request_url, json=content, headers=request_headers, proxies=proxies)

                if result.status_code == 201:
                    if cdn_test == True:
                        cdn_get(account_name=account_name,
                                repo_name=repo_name, full_path=remote_full_path)
                    print("========== File {} has successfully been uploaded @{}. ==========".format(
                        file_path, get_time()))
                    is_passed = True
                elif result.text.find("sha") != -1:
                    print("========== File {} has already existed. ==========".format(
                        file_path))
                    is_passed = True
                elif result.text.find("Server") != -1:
                    print("========== File {} is too large to be uploaded. ==========".format(
                        file_path))
                    is_passed = True
                elif result.status_code == 401:
                    print("Error u-token. 401 Unauthorized.")
                    is_passed = True
                else:
                    print(
                        "An unknown error occuerd while uploading file {}. The server returned the following info: {} \nRetrying ...".format(file_path, result.text))
            except:
                print(
                    "An unknown error occuerd while processing file {}. \nRetrying ...".format(file_path))
