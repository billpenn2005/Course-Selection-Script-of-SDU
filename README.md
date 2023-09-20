# Course-Selection-Script-of-SDU
使用方法：
程序需使用三个文件:pwd.txt(用于登录),config.txt(计时器配置),course.txt(选课设置)

pwd.txt:
第一行:用户名
第二行:密码

config.txt:
第一行:小时
第二行:分钟

course_select.txt:
    标记(四个,后面必须加冒号):
        BX:                 必选
        XX:                 限选
        RX:                 任选
        QT:                 其他
    每个标记下面填写若干课程,格式为课程编号加空格加任课教师(也可选择不填任课教师)
    示例:
    BX:
    sd30210010
    sd02810460 陈家付
    XX:
    RX:
    QT:
