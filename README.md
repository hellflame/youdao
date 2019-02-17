# youdao

> 曾经通过[有道翻译API](http://fanyi.youdao.com/openapi)进行终端单词，翻译查询，由于这个接口将于2017年年底关闭，故采用网页爬虫的形式进行

> 在连续写了很多公司代码之后，重新审视了一下项目代码，发现很多面向对象开发的范式要求都没有被很好的遵守，导致后期维护变的比较麻烦而难以理解，这种心情就像第一次发现测试开发有多重要的时候感觉一样。

__该项目代码应该在较长时间内不会有大的更新__ (如果有小的bug修复应该会及时更新，毕竟这也是自己常用的小工具)，之后如果有较多时间，可能会考虑整体的重构，主要是

1. python3 的兼容(这可能是一个漫长的过程)
2. 终端命令行解析
3. 测试用例

### 安装

```bash
$ sudo pip install youdaodict --upgrade
```

MacOS 中如果出现权限问题的话

```bash
$ pip install youdaodict --upgrade --user

# 仅为当前用户安装
```

可执行脚本将被安装在`/Users/<username>/Library/Python/2.7/bin/`，将此路径添加进环境变量`PATH`中即可，或者

```bash
$ echo export PATH=$PATH:/Users/<username>/Library/Python/2.7/bin/ > ~/.bash_profile
```

### 使用

终端调用：

#### 帮助菜单

```bash
$ youdao
$ youdao -h
```

```bash
有道翻译终端程序

Usage:
  youdao <word | phrase | sentence> [args...] 参数后置，查询翻译或解释
  youdao [args...] <word | phrase | sentence> 参数前置，查询翻译或解释

  --basic,-b  基本释义
  --debug,-d  调试模式
  --trans,-t  直接翻译
  --comp,-cp  自动补全
  --all,-a  翻译+基本释义
  --version,-v  版本信息
  --web,-w  网络翻译
  --clean,-c  清除数据库
  --help,-h 显示帮助信息

输入youdao + 想要查询的内容即可

更多帮助信息
https://github.com/hellflame/youdao/blob/v4.2.0/README.md
```

#### 基本查询

```bash
$ youdao whatever
```

终端输入`youdao` + 想要查询的`单词`或`句子`即可进行三重查询，`本地查询`/`个人服务器查询`/`有道网页查询`，从三种查询中获取最快的响应。

```bash
基本释义 >>>
  [wɒt'evə]
  us. [wət'ɛvɚ]
  uk. [wɒt'evə]
  conj. 无论什么
  adj. 不管什么样的
  pron. 无论什么；诸如此类
```

#### 网络释义

```bash
$ youdao whatever -w
$ youdao -w whatever
```

```bash
网络释义 >>>
  Whatever
    WHATEVER,  Whatever,  诸如此类,
  Whatever Works
    怎样都行,  总之得就得,  纽约遇到爱,
  Whatever Things
    MTV搞什麽,
```

在查询单词或前或后添加`-w`参数，即可获得网络释义结果

#### 翻译查询

1.

```bash
$ youdao whatever -t
$ youdao -t whatever
```

在目标单词或前或后添加`-t`参数，即可获取该单词的对应翻译

2.

```bash
$ youdao linux is fine
```

```bash
翻译     >>>
  linux是好
```

如果直接跟句子的话，一般也只会得到翻译结果

> 由于有道翻译的结果基本不能接受，所以还是考虑更靠谱的Google翻译好了，在v4.0.0之后，爬虫抓取结果不会再涉及翻译结果，最多采用有道的相似结果

#### 所有查询结果

```bash
$ youdao whatever -a
$ youdao -a whatever
```

```bash
基本释义 >>>
  [wɒt'evə]
  us. [wət'ɛvɚ]
  uk. [wɒt'evə]
  conj. 无论什么
  adj. 不管什么样的
  pron. 无论什么；诸如此类

网络释义 >>>
  Whatever
    WHATEVER,  Whatever,  诸如此类,
  Whatever Works
    怎样都行,  总之得就得,  纽约遇到爱,
  Whatever Things
    MTV搞什麽,

翻译     >>>
  无论
```

当有对应查询结果时，才会有对应显示，并不是所有查询都会有全部返回结果

当找不到查询的单词或句子时，将会提示没有这个单词或句子的结果

```bash
$ youdao hellflame

 (╯▔皿▔ )╯ hellflame ㄟ(▔皿▔ ㄟ)
```

> v4.0.0之后可能会有相似结果出现

```bash
相关词语     >>>
  hotflame
  hotflame

  hellfire
  n.地狱之火；严酷的苦难
```

#### 清除用户数据库

```bash
$ youdao -c
```

用户数据库所在位置`~/.youdao.sqlite3.db`，sqlite3

> v4.0.7.2 之后支持删除给定数据库中单词的数据，通过以下命令删除：

```bash
$ youdao -c <query>
```

删除用户数据库并不会影响在线状态下的继续使用

> API相关的功能在v4.0.0之后不存在

用户数据库中主要存储着用户给定的API key信息以及缓存的查询结果，缓存查询结果，可以加速下一次相同的查询，也可以在离线情况下使用

#### 调试状态

```bash
$ youdao whatever -d
$ youdao -d whatever
```

```json
{
  "errorCode": 0,
  "query": "whatever",
  "translation": [
    "\u65e0\u8bba"
  ],
  "basic": {
    "phonetic": "w\u0252t'ev\u0259",
    "us-phonetic": "w\u0259t'\u025bv\u025a",
    "explains": [
      "conj. \u65e0\u8bba\u4ec0\u4e48",
      "adj. \u4e0d\u7ba1\u4ec0\u4e48\u6837\u7684",
      "pron. \u65e0\u8bba\u4ec0\u4e48\uff1b\u8bf8\u5982\u6b64\u7c7b"
    ],
    "uk-phonetic": "w\u0252t'ev\u0259"
  },
  "web": [
    {
      "value": [
        "WHATEVER",
        "Whatever",
        "\u8bf8\u5982\u6b64\u7c7b"
      ],
      "key": "Whatever"
    },
    {
      "value": [
        "\u600e\u6837\u90fd\u884c",
        "\u603b\u4e4b\u5f97\u5c31\u5f97",
        "\u7ebd\u7ea6\u9047\u5230\u7231"
      ],
      "key": "Whatever Works"
    },
    {
      "value": [
        "MTV\u641e\u4ec0\u9ebd"
      ],
      "key": "Whatever Things"
    }
  ]
}
```

由于版本兼容问题考虑欠佳，在 `v4.0.0` 以后的版本调试信息会类似如下:

```json
{
  "translate": [
    "adj. \u4e0d\u7ba1\u4ec0\u4e48\u6837\u7684",
    "pron. \u65e0\u8bba\u4ec0\u4e48\uff1b\u8bf8\u5982\u6b64\u7c7b",
    "conj. \u65e0\u8bba\u4ec0\u4e48"
  ],
  "web_translate": [
    "\u65e0\u8bba\u4ec0\u4e48",
    "\u8bf8\u5982\u6b64\u7c7b",
    "\u65e0\u6240\u8c13",
    "\u529b\u6240\u80fd\u53ca"
  ],
  "pronounces": [
    "\u82f1[w\u0252t'ev\u0259]",
    "\u7f8e[w\u0259t'\u025bv\u025a]"
  ]
}
```



如果出现怀疑查询结果与实际看到的输出不一致的情况的话，使用调试选项，输出从API获取的返回json输出，json未经过更易读的编码调整，如果真的需要的话，需要其他工具进行进一步转换

#### 个人服务器

> 非必需

个人服务器的存在只是为了(可能的)进一步加速查询过程，如果没有这个服务器的话，程序依然可以正常运行，只是数据来源就只有本地存储和实时网页爬虫了。

服务器中的查询结果当然也是来自于爬虫，预想中是如果有很多人查询的话，相同的结果就会更快的得到响应，从而加速查询。所以如果某一个单词是第一次被请求的话，服务器就要先使用爬虫，然后再返回结果，如果没有网络原因的话，应该比本地的爬虫要慢一点。

```bash
$ service.youdao
```

该命令默认会在本地3697端口开启TCP服务

> 测试

```bash
$ telnet localhost 3697
Trying ::1...
telnet: connect to address ::1: Connection refused
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
linux
{"insert_time": 1499742022, "pronounces": ["\u82f1[\u02c8la\u026an\u028cks;\u02c8l\u026an\u028cks]", "\u7f8e[\u02c8l\u026an\u0259ks]"], "used": 6, "web_translate": ["\u64cd\u4f5c\u7cfb\u7edf", "\u6b63\u7248", "\u5e38\u7528\u547d\u4ee4", "\u9884\u88c5"], "translate": ["n. Linux\u64cd\u4f5c\u7cfb\u7edf\uff08\u4e00\u79cd\u7c7b\u4f3c\u4e8eUNIX\u7684\u8ba1\u7b97\u673a\u64cd\u4f5c\u7cfb\u7edf\uff09"]}
windows
{"insert_time": 1499742054, "pronounces": ["['w\u026andoz]"], "used": 1, "web_translate": ["\u7a97\u53e3\u64cd\u4f5c\u7cfb\u7edf", "\u8981\u6c42", "\u9700\u6c42", "\u7a97\u53e3"], "translate": ["n. \u5fae\u8f6f\u516c\u53f8\u751f\u4ea7\u7684\u201c\u89c6\u7a97\u201d\u64cd\u4f5c\u7cfb\u7edf"]}
```

服务不会主动断开连接，并且直接响应每一行输入，返回目标json

服务默认最高支持1024个连接，更多连接数会abort(实际最高连接数量可以自行修改)

作者可能在自己的服务器上开启这个端口访问，也可能不会！(现在看来是不会了=。=)

#### 版本信息

```bash
$ youdao -v
$ youdao --version
```

### bash自动补全

> 添加于v3.3.0版本

可以将输出的bash脚本输出到用户目录的 *.bash_profile* 、*.bashrc* 等文件

```bash
# 自动补全代码:
$ youdao -cp

# 输出到resource文件
# on Mac OS
$ youdao -cp >> ~/.bash_profile
# on Linux
$ youdao -cp >> ~/.bashrc
```

若要立即生效，执行如下命令:

```bash 
$ source ~/.bash_profile

# or on Linux 
$ source ~/.bashrc
```

> 由于对bash补全不是很熟悉，不排除会出现补全过程出现问题=。=，并且只有bash补全，对于zsh等其他shell，支持情况不明。

![](https://static.hellflame.net/resource/c26b182ef30500ffa3bc7373d5207036)

### 开发历程

- 1.1.4 ==> 添加新选项, -a --all 输出所有可选输出
- 1.1.5 ==> 允许不使用引号查询空格隔开的句子
- 1.1.6 ==> 修改json获取异常处理
- 1.1.7 ==> 网络连接验证机制导致返回数据被强制重定向问题判断
- 2.0.0 ==> 添加本地数据库缓存数据，离线可用
- 2.0.1 ==> 放宽InstantDB版本限制
- 2.0.2 ==> 修复mac os 中无法正确初始化数据库的错误
- 3.1.0 ==> 使用SQLite3数据库进行本地存储，可离线查询
- 3.1.2 ==> Bug修复，数据库清除可选
- 3.2.0 ==> 手动处理参数获取
- 3.2.1 ==> 精细错误码识别
- 3.2.2 ==> 单词默认小写
- 3.3.0 ==> bash自动补全
- 4.0.0 ==> 取消API调用
- 4.0.1 ==> 修复在无基本释义情况下的显示策略问题
- 4.0.2 ==> 修复无效翻译的无效输出问题以及其他小问题
- 4.0.3 ==> 修复爬虫翻译结果空格过多的问题
- 4.0.4 ==> 捕获超时异常
- 4.0.5 ==> 捕获强行终止异常
- 4.0.6 ==> bug fix
- 4.0.7 ==> 搞了好几个版本的异常捕获=。=真的是醉了，这应该算是最终版本了才对
- 4.2.0 ==> 代码整理，终端入口不受影响，程序API发生变更，sqlite 防注入

项目主要目的在于简单方便的终端查询，虽然功能在越来越多，但是一般能够用到的还是只有查询这一个功能。主要也在于linux系统中没有找到方便的单词查询工具，而且本身只要调用接口的话，就什么都出来了，这使得整个项目变的很简单。项目的所有功能依据也都是来自于个人的需求

关于本地存储，使用SQLite3作为本地数据库，本想使用MongoDB或者MySQL的，但是并不是所有人都会安装这些数据库的样子，而且这样也会使得使用配置过程变得很麻烦，因为曾经还想着异步更新来着，后来发现这样的需求并不是很重要的样子，并且现在可以手动更新本地数据库，所以使用SQLite也可以满足实际需要

> v4.0.0

从4.0.0版本开始，不再调用有道提供的API。

虽然官方给了另一个API，但是只有专为移动客户端准备的SDK，然而我也不想深入底层查看验证机制(用python来实现一套SDK)，所以就用最简单的爬虫来完成了.

对于本地翻译工具的话，Mac自带的词典工具其实可以满足部分需求，至于词汇量嘛，，，

在线翻译工具的话, [Google翻译](https://translate.google.com.hk/?hl=zh-CN&tab=wT) 翻译结果还好吧。

> PS. 由于对之前版本的兼容性考虑不是很多，之前版本的数据库中的查询结果可能会导致一些问题=。=，可能需要删除一下原始的数据库，执行 `youdao -c` 删除之前版本的数据库或者手动删除`rm ~/.youdao.sqlite3.db`

以上