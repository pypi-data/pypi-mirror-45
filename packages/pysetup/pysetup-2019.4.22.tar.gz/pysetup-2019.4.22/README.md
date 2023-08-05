# PySetup
Pypi 上传工具

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
打包/上传 项目
```
>>> pysetup upload <username> <password>
```
打包/上传 test 项目
```
>>> pysetup upload_test <username> <password>
```
打包项目
```
>>> pysetup package
```
删除打包文件
```
>>> pysetup remove_packaged
```
