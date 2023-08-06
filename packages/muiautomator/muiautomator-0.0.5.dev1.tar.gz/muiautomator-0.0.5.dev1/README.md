# myuiautomator
根据uiautomator2 更改的自用版本

基本上没有做什么改动 只是修改了atx-agent源码并重新打包

修改点：    

    1.将atx-agent下载路径改为自己修改过后的安装包
    
    2.新增server文件以及atx.sh脚本文件 用于控制atx-agent服务的启动和关闭
    
    3.修改atx-agent中图像画质问题 将以前的默认值改为 画质为50%
    
    4.修改发送帧数频率 将以前的全部发送改为丢弃一半帧数
