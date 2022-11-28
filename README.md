代码主要用于处理从巨潮网抓取下来的年报（PDF文件），转换成txt文件，并进行分词、词频统计分析

### 代码模块

* pdf2txt.py 用于将年报pdf文件转为txt文件
* sample2txt.py 基于产业类型，进行分层抽样
* texSmartPart 利用腾讯texsmart API进行分词，并统计词频

### 结果

* json_result文件夹将API分词返回的结果进行存储（每100句）
* xls_result文件夹将每次词频统计后的结果进行存储
