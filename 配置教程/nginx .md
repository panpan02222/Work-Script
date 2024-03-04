## Nginx的设计理念注重性能、并发性和可扩展性，使其成为处理高并发、大规模访问的理想服务器和代理工具。<br>

-------------------------

### 基础命令

- 启动命令 `sudo nginx`</br>
- 关闭命令 `sudo nginx -s stop`</br>
- 重启加载 `sudo ngingx -s reload`</br>
- 查看进程 `ps aux | grep nginx`</br>
- 查看状态 `sudo nginx -t`</br>



```
#user  nobody;

events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    sendfile        on;
    
    keepalive_timeout  65;
    
    server {
    	listen  18080;
    	server_name		localhost;


​		
		location /chat/knowledge_base_chat/ {
			proxy_pass      http://127.0.0.1:17861/chat/knowledge_base_chat;
		}
		location /chat/chat/ {
			proxy_pass      http://127.0.0.1:17861/chat/chat;
		}
		
		location /knowledge_base/list_knowledge_bases/
		{
			proxy_pass      http://127.0.0.1:17861/knowledge_base/list_knowledge_bases;
		}
		
	}

}
```