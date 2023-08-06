1、下载配置
在用户根目录下添加.pip文件夹，创建pip.conf文件，添加如下配置：
[global]
index-url = http://username:password@localhost:8081/repository/jiayundata/simple
[install]
trusted-host = localhost

2、上传配置
在用户根目录下添加.pypirc文件，添加如下配置：
[distutils]
index-servers =
    pypi
    pypitest
    nexus
    nexustest

[pypi]
repository:https://pypi.python.org/pypi
username:your_username
password:your_password

[pypitest]
repository:https://testpypi.python.org/pypi
username:your_username
password:your_password

[nexus]
repository:http://ip:port/repository/jiayun_host/
username:your_username
password:your_password

[nexustest]
repository:http://ip:port/repository/jiayun_host/
username:your_username
password:your_password

安装python的twine包
pip install twine

twine upload --repository-url https://test.pypi.org/legacy/ dist/*
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*