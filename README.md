**说明**

谷歌地图在国内无法愉快的使用，大家都知道的，但是可以通过反代的方式，把部分被kill的请求通过一台Server中转下，还是能凑合使用以下的。

这里主要使用了python去自动生成nginx使用的配置文件，包括location段和replace的配置，把原始js中的地址替换成自己服务器的地址，然后通过location去定义路径，用proxy_pass实现反代。

**博客文章**

https://www.coderecord.cn/google-map-proxy.html

**案例**

https://www.nicebing.com

