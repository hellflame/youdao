# youdao

youdaodict

## Install
```bash
 $ sudo pip install youdaodict --upgrade

```

## Usage

How to Deploy

```bash
  $ youdao
  $ youdao -h
  $ youdao linux
  $ youdao how are you
  $ youdao hell -t
  $ youdao hell -wt
  $ youdao hell -tb
  $ youdao hell -a

```

## Detail

1. 主要面对linux系统使用过程中查阅单词，原理当然也很简单，所以是自己使用啦
2. 尽量保证使用过程中不会出现严重错误（当然还需要之后使用的时候再看啦）
3. 主函数在参数获取时支持 -tbw ... 方式和 --web -t -b ... 方式获取, 使用前一种方法时参数长度限制为两个,即需要查询的内容必须在前两个参数中,
并且不能以-开头
4. 翻译句子的时候请使用引号将句子引用起来
5. 添加彩色输出~~~自己才会需要的吧
6. 本地存储使用SQLIte3, 本想用MongoDB，但是考虑到不是所有人都用这个，暂时简单存储一下返回的json string，备更多离线功能的使用

## History

+ 1.1.4 ==> 添加新选项, -a --all 输出所有可选输出
+ 1.1.5 ==> 允许不使用引号查询空格隔开的句子
+ 1.1.6 ==> 修改json获取异常处理
+ 1.1.7 ==> 网络连接验证机制导致返回数据被强制重定向问题判断
+ 2.0.0 ==> 添加本地数据库缓存数据，离线可用
+ 2.0.1 ==> 放宽InstantDB版本限制
+ 2.0.2 ==> 修复mac os 中无法正确初始化数据库的错误
+ 3.1.0 ==> 使用SQLite3数据库进行本地存储，可离线查询
+ 3.1.2 ==> Bug修复，数据库清除可选
