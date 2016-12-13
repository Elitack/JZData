# JZData

## 安装环境

#### Windows 系统

#### python 2.7

#### scrapy
+ 若在无网机器上，可先在有网机器上安装好相关库，再将python27复制粘贴到C盘下。

## 使用方法

### html解析：

1. 在input.txt 中输入文件读取路径
2. 在output.txt中输入爬取文件存储路径
3. 运行run.py程序

##### 注：假设需爬取文件存储在 C:// aaa/.../bbb下， 且bbb下有XXX,YYY,ZZZ文件夹
1. 文件读取路径格式如下:    C:// aaa/.../bbb
+ 假设bbb文件夹下有XXX, YYY, ZZZ三个文件夹，则爬取的内容为XXX, YYY, ZZZ 底下的html文件。即：XXX,YYY,ZZZ底下应有Contents0.html, Contents1.html等文件

2. 文件存储
+ 格式为csv
+ 存储命名为：XXX-adressBook.csv, XXX-message.csv, XXX-callLog.csv. （类似地，也有YYY和ZZZ的文件）


### BCP以及xml文件解析：
1. 将所有压缩包解压到某文件夹,假设为 C://aaa/.../bbb下，即bbb下有XXX，YYY，ZZZ文件夹，且XXX，YYY，ZZZ底下应有xml和bcp文件。
2. 在input.txt中输入文件读取路径
3. 在ouput.txt中输入爬取文件路径
4. 运行run.py程序

##### 注：
1. 文件读取路径格式如下:    C:// aaa/.../bbb
2. 文件存储
+ 在输入存储文件夹路径底下输出格式为XXX_change, YYY_change, ZZZ_change三个文件夹
+ XXX_change, YYY_change, ZZZ_change底下均含有相关csv文件
