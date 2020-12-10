function add() {
    var post = document.createElement("form");  // 创建一个表单
    var task = document.getElementById("addtask").value;
    var func = "add";

    post.style.display = "none";  // 不在html中显示出来
    post.method = "POST";
    var post_task = document.createElement("input");
    var post_func = document.createElement("input");
    post_task.name = "content";
    post_task.value = task;
    post_func.name = "func";
    post_func.value = func;
    post.appendChild(post_task);
    post.appendChild(post_func);

    document.body.appendChild(post);

    post.submit();
}
