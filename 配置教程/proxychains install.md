# proxychains安装
- 解压源码 ` tar zxvf proxychains-ng-x.xx.tar.gz `

- 进入解压后的目录，执行 `./configure`

- 安装软件执行 `make`,`make intsall `

- 修改代理服务器(xxx为你的代理服务器地址)
  
>  cd /usr/local/etc/proxychains.conf

>  最后一行处修改 <b> socks5 xxxxxx </b>
