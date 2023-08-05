# PySetup
Pypi 上传工具, 使用流程: 进入项目目录 -> 创建 `setup.py` 文件 -> 修改 `setup.py` 文件信息 -> 上传

## 安装
```
pip3 install pysetup --upgrade
```

## 使用
查看命令列表
```
>>> pysetup help
```
创建 setup.py 文件
```
>>> pysetup create_setup
```
打包项目上传到 https://upload.pypi.org/legacy/
```
>>> pysetup upload <username> <password>
```
打包项目上传到 https://test.pypi.org/legacy/ (测试发布平台)
```
>>> pysetup upload_test <username> <password>
```
- TestPyPI 和 PyPI 是两个不同的账号

打包项目
```
>>> pysetup package
```
删除打包文件
```
>>> pysetup remove_packaged
```
