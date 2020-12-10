function check() {
    var password = document.getElementById("password")
    var password_feedback = document.getElementById("password-feedback");
    var confirmpassword = document.getElementById("confirmpassword");
    var confirmpassword_feedback = document.getElementById("confirmpassword-feedback");

    password.classList.remove("is-invalid");
    password_feedback.innerHTML="";
    confirmpassword.classList.remove("is-invalid");
    confirmpassword_feedback.innerHTML=""

    //密码检查
    if(password.value==""){
        password_feedback.innerHTML = "密码不能为空";
        password.classList.remove("is-valid");
        password.classList.add("is-invalid");
        confirmpassword.classList.remove("is-valid");
        confirmpassword.classList.add("is-invalid");
        return false;
    }
    if(password.value.length>20){
        password_feedback.innerHTML = "密码长度需小于20个字符";
        password.classList.remove("is-valid");
        password.classList.add("is-invalid");
        confirmpassword.classList.remove("is-valid");
        confirmpassword.classList.add("is-invalid");
        return false;
    }

    //确认密码检查
    if(confirmpassword.value==""){
        confirmpassword_feedback.innerHTML = "请确认密码";
        confirmpassword.classList.remove("is-valid");
        confirmpassword.classList.add("is-invalid");
        return false;
    }
    if(password.value != confirmpassword.value){
        confirmpassword_feedback.innerHTML = "密码不一致";
        password.classList.remove("is-valid");
        password.classList.add("is-invalid");
        confirmpassword.classList.remove("is-valid");
        confirmpassword.classList.add("is-invalid");
        return false;
    }

    //清除错误提示，改成成功提示
    password.classList.remove("is-invalid");
    password_feedback.innerHTML="";
    confirmpassword.classList.remove("is-invalid");
    confirmpassword_feedback.innerHTML=""
    return true;
}
