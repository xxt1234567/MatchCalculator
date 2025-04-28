# 电子竞技和传统体育比赛出线形势计算系统

## 系统简介

本系统是一个基于 **Laravel + Vue.js + Python** 的赛事出线形势分析工具，主要用于计算电子竞技/传统体育赛事中各队伍的 **实时排名** 和 **出线概率**。系统的功能包括：
- 支持单循环/双循环、自由得分/BO系列赛、2-10支队伍参赛的多种赛制，适配大部分主流赛事
- 通过输入框、下拉框、复选框等基础表单组件，便捷地完成输入
- 提供蒙特卡洛模拟和全量枚举两种计算模式，根据赛事复杂程度动态平衡计算速度与精度
- 通过表格、饼图、流程图等多种可视化形式，直观地呈现结果
- 自由指定输出形式，支持展示排名前列/末尾概率、特定队伍排名范围筛选等功能
- 支持将输入作为JSON文件持久化保存，便于后续加载分析

## 运行环境要求

| 组件       | 版本要求          | 
|------------|-------------------|
| PHP        | 8.2.12+           |
| Node.js    | v22.11.0+         |
| Python     | 3.9.7+            |
| numpy      | 1.24.2+           |
| Composer   | 2.8.3+            |
| npm        | 10.9.0+           |
| Laravel    | v10.3.3           |

## 环境配置指南

### 1.安装numpy库

```bash
pip install numpy
```

### 2.修改php.ini配置文件

如果php文件夹中没有php.ini文件，将php.ini-development文件复制一份并重命名为php.ini

打开php.ini文件，取消以下配置项的注释符号";"以启用扩展包：

- extension=curl
- extension=fileinfo
- extension=gettext
- extension=mbstring
- extension=zip

如果disable_functions配置项中包含shell_exec函数，将其删去

### 3.配置文件设置

将项目文件夹中的.env.example文件复制一份并重命名为.env

### 4.安装依赖

命令行进入项目文件夹，执行以下命令：

```bash
npm i @vitejs/plugin-vue 
npm i dhx-suite 
npm i mermaid
npm install 
composer install
php artisan key:generate
```

### 5.启动服务

打开两个命令行窗口，进入项目文件夹，分别执行：

```bash
npm run dev
```

```bash
php artisan serve
```

浏览器访问``http://127.0.0.1:8000``即可运行，推荐使用Chrome/Firefox最新版

## 核心代码

- ``.\app\Http\Controllers\CalculationController.php``
- ``.\app\Http\Controllers\matchcalculator.py``
- ``.\resources\js\app.js``
- ``.\resources\js\app.vue``
- ``.\resources\views\welcome.blade.php``
- ``.\routes\web.php``

欢迎各位学习交流
