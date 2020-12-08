function add() {
    var post = document.createElement("form");
    var task = document.getElementById("addtask");
    var func = "add";

    post.style.display = "none";
    post.methods = "post";
    post.setAttribute("contnet", task);
    post.setAttribute("func", func);

    document.body.appendChild(post);

    post.submit()
}
