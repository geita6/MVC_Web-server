# MVC_Web-server
=====================
## 简介
- 测试账号 用户名：admin  密码：123
- 底层使用socket实现数据通信，解析 HTTP 协议，进行多线程处理
- 通过MVC架构，实现数据和视图解耦。View部分通过jinja2模板实现，渲染各个路由函数对应html页面；
Contrl部分由自制web框架实现，主要涉及路由分发，模板函数，响应函数，数据处理，读取文件等内容；
Model部分通过ORM实现，基类对不同类型数据进行实例化，抽象出评论，微博，用户，session等model子类接口。
- 实现登录注册，权限验证，发表微博和评论，session管理，基于AJAX的留言板等功能

## 功能演示
### 注册/登录
- 默认为游客
![注册/登录](https://github.com/geita6/MVC_Web-server/blob/master/static/login.gif)

### 简易weibo
- 已登录用户可以发表weibo和评论
- 用户可以修改删除自己的weibo和评论
- weibo主可以删除自己微博下的评论
![简易weibo]

## 运行环境
- Python 3.6.5



