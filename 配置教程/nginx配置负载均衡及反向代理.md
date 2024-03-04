nginx是著名的


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
