function check() {
    var username = document.getElementById("username");//获取username那个div
    var username_feedback = document.getElementById("username-feedback");
    var password = document.getElementById("password");
    var password_feedback = document.getElementById("password-feedback");

    username.classList.remove("is-invalid");
    username_feedback.innerHTML="";
    password.classList.remove("is-invalid");
    password_feedback.innerHTML="";

    //用户名检查
    if(username.value==""){
        username_feedback.innerHTML = "用户名不能为空";//修改username-feedback div中的内容
        username.classList.remove("is-valid");//清除合法状态
        username.classList.add("is-invalid");//添加非法状态
        return false;//onsubmit  return false阻止表单提交
    }

    //密码检查
    if(password.value==""){
        password_feedback.innerHTML = "密码不能为空";
        password.classList.remove("is-valid");
        password.classList.add("is-invalid");
        return false;
    }

    //清除错误提示，改成成功提示
    username.classList.remove("is-invalid");
    username_feedback.innerHTML="";
    password.classList.remove("is-invalid");
    password_feedback.innerHTML="";
    return true;
}
