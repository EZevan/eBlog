# eBlog
Personal blog project which developed by django and vue.js

1. python继承的三种用法
2. uuid.uuid1, uuid4用法
3. django model中 DatetimeField 的auto_now, auto_now_add 用法区别
4. django model中 verbose_name，verbose_name_plural用法区别
5. django MEDIA_ROOT 和 MEDIA_URL配置用法
6. 正则表达式中的?P<name>命名组用法
7. receiver装饰器用法
8. django路由分发配置
9. flex布局
10. django中直接引入 vue.js
11. django中使用 vue.js 语法，直接在 html 中无法使用{{variable}} 方式填充数据（替代方案：delimiters: ["[[","]]"])
12. vue 冒号":"的作用 - 冒号即 v-bind，动态绑定；如\<a :href="..."> 等价于 \<a v-bind:href="..."> 
13. vue 显示隐藏 v-show 和 v-if 的用法
14. css 中&符号的作用 - sass 语法，标识嵌套的上一层
15. css 中>符号的作用 - 子元素选择器，用法：> div{...}
16. django 自定义过滤器
17. django 模板标签（simple_tag; inclusion_tag）
18. django 路由
19. django 模板继承
20. css @keyframes动画用法
21. css : 伪类
    ```
    :first-child，:link，:hover，:active,:focus，:nth-child
    ```
22. css :: 伪元素
    ```
    :first-line，:first-letter，:before，:after
    ```
23. css [] 属性选择器
       ```
       span[class='test']    匹配所有带有class类名test的span标签
       span[class *='test']  匹配所有包含了test字符串的class类名的span标签
       span[active]          匹配所有带有active属性的span标签
       [class='all']         匹配页面上所有带有class='all'的标签
       [class *='as']        匹配页面上所有class类且类名带有as字符串的类的标签
       ```
24. css ’~‘ 子代选择器
    ```css
    div ~ ul    表示选择 div 后的所有ul标签，不管多少层级
    ```
25. css ’>‘ 子代选择器
    ```css
    div > ul    表示选择该 div 标签内紧跟着的所有的ul标签
    ```
26. css ’+‘ 相邻兄弟选择器（）
     ```css
     div + ul    表示选择紧接在 div 标签后出现的ul标签，且div和ul拥有相同的父元素
     ```
27. 单行文本截断
    ```
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    ```
28. 多行文本截断
    ```
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 4;
    overflow: hidden;
    text-overflow: ellipsis;
    ```    
29. axios 进行接口请求
    ```
    <script></script>
    ```
30. django 中间件  
    ```
    from django.utils.deprecation import middlemareMixin
    ```
31. axios 中间件
32. 浏览器CSRF攻击
33. django CSRF 拦截，配合使用在对应前端页面添加{% csrf_token %}

