# 安装ifconfig
yum list | grep net-tool*
yum install -y net-tools.x86_64

# cpu个数
cat /proc/cpuinfo | grep "core id"

# 单机不卸载数据库，重新初始化实例办法：

# 1.创建实例存放路径
su - gbase
mkdir -p /opt/gbase8c/install/data/dn2

# 2.初始化实例
gs_initdb -D /opt/gbase8c/install/data/dn2 -w "gbase;123" --nodename='dn2'

# 3.修改配置文件，端口号等信息

# 4.启动数据库
gs_ctl start -D /opt/gbase8c/install/data/dn2 -Z single_node -l logfile

# django
django-admin startproject mysite
python manage.py runserver
python manage.py migrate
python manage.py makemigrations polls
python manage.py sqlmigrate polls 0001
python manage.py migrate


certutil -hashfile C:\\Users\\zero4\\Desktop\  MD5
C:\\Users\\zero4\\Desktop

# 修改python软连接
update-alternatives --install /usr/bin/python python /usr/bin/python3 1
