<!DOCTYPE html>
<html>
    <head lang="{{ str_replace('_','-',app()->getLocale())}}">
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="csrf-token" content="{{ csrf_token() }}">
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        @vite(['resources/css/app.css','resources/js/app.js'])
        <title>电子竞技和传统体育比赛出线形势计算系统</title>
        <style>html,body,#app {
            width: 100%;height:100%;
            margin: @px;padding:0px;
            overflow: hidden;
        }</style>
    </head>
    <body><div id="app"></div></body>
</html>
