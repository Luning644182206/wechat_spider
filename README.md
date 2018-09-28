# wechat_spider
------

用搜狗搜索按照关键词搜索爬取公众号文章

------

## 目录结构

    ├── README.md
    
    ├── main.py                     程序主入口
    
    └── src
        ├── class_files             所有的class文件都存在这里
        │   ├── constant.py         静态变量都存在这里
        │   ├── driver_common.py    无头浏览器通用配置项
        │   └── search.py           爬虫主程序
        ├── data
        │   └── news.csv            爬取后的存储文件
        └── third_party             第三方依赖

## 代码思路

1. 首先通过访问weixin.sogou.com根据关键词搜索文章
2. 逐页抓取文章链接
3. 访问文章链接抓取内容
4. 存储文章内容
5. 查看抓取结果

## 备注

1. 请在使用本程序前安装最新版本的firefox浏览器
2. 请根据不同系统版本替换本程序中的驱动(src/third_party/geckodriver)程序中的版本为mac版
3. 驱动下载链接 https://github.com/mozilla/geckodriver/releases
4. 浏览器对应驱动版本，请参考博客 https://blog.csdn.net/u013250071/article/details/78803230
5. 由于搜狗对非登录情况下有条数限制，请用浏览器登录搜狗，将cookie拷贝到(src/class_files/constant里面的COOKIE_LIST下，直接替换即可)
