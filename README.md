# youdao

通过[有道翻译API](http://fanyi.youdao.com/openapi)进行终端单词，翻译查询

### 安装

```bash
$ sudo pip install youdaodict --upgrade
```

### 使用

终端调用：

#### 帮助菜单

```bash
$ youdao
$ youdao -h
```

```
有道翻译终端程序

Usage:
  youdao <word | phrase | sentence> [args...]	参数后置，查询翻译或解释
  youdao [args...] <word | phrase | sentence>	参数前置，查询翻译或解释

  --a-key,-k	添加API key
  --version,-v	版本信息
  --web,-w	网络翻译
  --r-key,-r	删除API key
  --basic,-b	基本释义
  --update,-u	更新数据库
  --debug,-d	调试模式
  --trans,-t	直接翻译
  --comp,-cp	自动补全
  --all,-a	翻译+基本释义
  --help,-h	显示帮助信息
  --clean,-c	清除数据库

程序一开始应该便可用，输入youdao + 想要查询的内容即可

更多帮助信息
https://github.com/hellflame/youdao/blob/v3.3.0/README.md
```


#### 基本查询

```bash
$ youdao whatever
```

终端输入`youdao` + 想要查询的`单词`或`句子`即可进行查询，如果该单词存在词库，则默认输出基本解释，API接口可以进行英汉双向翻译或解释

```
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

```
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

```
翻译     >>>
	linux是好
```

如果直接跟句子的话，一般也只会得到翻译结果

#### 所有查询结果

```bash
$ youdao whatever -a
$ youdao -a whatever
```

```
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

#### 添加API key

```bash
$ youdao -k (查看用户自己添加的key)
$ youdao -k <key> <keyfrom>
```

一般情况下，并不需要手动添加自己的key还有keyfrom，如果添加，程序将只会使用用户提供的API key，如果提示这是无效key的话，删除这对key或者索性删除数据库文件也可以

#### 删除API key

```bash
$ youdao -r <key>
```

当在需要时，删除用户手动添加的API key

#### 清除用户数据库

```bash
$ youdao -c
```

用户数据库所在位置`~/.youdao.sqlite3.db`，sqlite3

删除用户数据库并不会影响在线状态下的继续使用

用户数据库中主要存储着用户给定的API key信息以及缓存的查询结果，缓存查询结果，可以加速下一次相同的查询，也可以在离线情况下使用

#### 更新数据库

```bash
$ youdao -u
```

由于缓存在本地的查询结果在不删除的情况下，就不会请求API，然而查询结果有时会稍微有一点变动，执行更新操作之后，会将本地数据库中的所有查询重新查询一次并缓存，通常不需要更新也可以满足正常使用

#### 调试状态

```bash
$ youdao whatever -d
$ youdao -d whatever
```

```
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

如果出现怀疑查询结果与实际看到的输出不一致的情况的话，使用调试选项，输出从API获取的返回json输出，json未经过更易读的编码调整，如果真的需要的话，需要其他工具进行进一步转换

#### 版本信息

```bash
$ youdao -v
$ youdao --version
```

作为Py Library调用

```
from youdao import Youdao
instant = Youdao()

```

### bash自动补全

> 添加于v3.3.0版本

自动补全代码:

```bash
$ youdao -cp
```

可以将输出的bash脚本输出到用户目录的 *.bash_profile* 、*.bash_profile*等目录，若要立即生效，执行如下命令:

```bash 
$ source ~/.bash_profile

# or in Linux 
$ source ~/.bashrc
```

> 由于对bash补全不是很熟悉，不排除会出现补全过程出现问题=。=

![](https://static.hellflame.net/resource/c26b182ef30500ffa3bc7373d5207036)

### 开发历程

+ 1.1.4 ==> 添加新选项, -a --all 输出所有可选输出
+ 1.1.5 ==> 允许不使用引号查询空格隔开的句子
+ 1.1.6 ==> 修改json获取异常处理
+ 1.1.7 ==> 网络连接验证机制导致返回数据被强制重定向问题判断
+ 2.0.0 ==> 添加本地数据库缓存数据，离线可用
+ 2.0.1 ==> 放宽InstantDB版本限制
+ 2.0.2 ==> 修复mac os 中无法正确初始化数据库的错误
+ 3.1.0 ==> 使用SQLite3数据库进行本地存储，可离线查询
+ 3.1.2 ==> Bug修复，数据库清除可选
+ 3.2.0 ==> 手动处理参数获取
+ 3.2.1 ==> 精细错误码识别
+ 3.2.2 ==> 单词默认小写
+ 3.3.0 ==> bash自动补全

项目主要目的在于简单方便的终端查询，虽然功能在越来越多，但是一般能够用到的还是只有查询这一个功能。主要也在于linux系统中没有找到方便的单词查询工具，而且本身只要调用接口的话，就什么都出来了，这使得整个项目变的很简单。项目的所有功能依据也都是来自于个人的需求

关于本地存储，使用SQLite3作为本地数据库，本想使用MongoDB或者MySQL的，但是并不是所有人都会安装这些数据库的样子，而且这样也会使得使用配置过程变得很麻烦，因为曾经还想着异步更新来着，后来发现这样的需求并不是很重要的样子，并且现在可以手动更新本地数据库，所以使用SQLite也可以满足实际需要
