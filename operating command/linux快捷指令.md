- 查看当前目录下的文件占用内存

    `du -sh`

- 查看文件系统磁盘占用情况
  
    `df -h $home`

- 计算文件数
  
    `ls | wc -l`

- 查看当前文件夹下每个文件的大小
  
    `ls -lh`


- 暂停进程18000秒
  
    `sh -c | sleep 18000`

> ## tar

- **解压** tar.gz file
  
    `tar -zxvf folder.tar.gz folder`

- **解压** tar file
  
    `tar -xvf folder.tar`

> ## unrar
- 解压rar file
  
    `unrar x example.rar`

> ## unzip

- **解压** zip file
  
  `unzip -l example.zip`

远程发送文件
scp folder_path root@ip:folder_path
远程链接服务器
ssh username@remote_server_ip

手动挂载U盘
mkdir /mnt/usb 			#新建文件夹
fdisk -l			#查看u盘名称
mount /dev/sdb1 /mnt/usb	#将u盘挂载到文件夹
umount /mnt/usb			#使用完，退出挂载

批量安装rpm包
rpm -ivh *.rpm

 


