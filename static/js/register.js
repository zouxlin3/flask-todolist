function check() {
    var username = document.getElementById("username");//获取username那个div
    var username_feedback = document.getElementById("username-feedback");
    var password = document.getElementById("password")
    var password_feedback = document.getElementById("password-feedback");
    var confirmpassword = document.getElementById("confirmpassword");
    var confirmpassword_feedback = document.getElementById("confirmpassword-feedback");
    var agree = document.getElementById("agree");
    var agree_feedback = document.getElementById("agree-feedback");

    username.classList.remove("is-invalid");
    username_feedback.innerHTML="";
    password.classList.remove("is-invalid");
    password_feedback.innerHTML="";
    confirmpassword.classList.remove("is-invalid");
    confirmpassword_feedback.innerHTML=""
    agree.classList.remove("is-invalid");
    //agree_feedback.innerHTML = "";

    //用户名检查
    if(username.value==""){
        username_feedback.innerHTML = "用户名不能为空";//修改username-feedback div中的内容
        username.classList.remove("is-valid");//清除合法状态
        username.classList.add("is-invalid");//添加非法状态
        return false;//onsubmit  return false阻止表单提交
    }
    if(username.value.length>20){
        username_feedback.innerHTML = "用户名长度需小于20个字符";
        username.classList.remove("is-valid");
        username.classList.add("is-invalid");
        return false;
    }

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

    //同意检查
    if(agree.checked == false){
        //agree_feedback.innerHTML = "您必须先勾选此项";//todo
        agree.classList.remove("is-valid");
        agree.classList.add("is-invalid");
        return false;
    }

    //清除错误提示，改成成功提示
    username.classList.remove("is-invalid");
    username_feedback.innerHTML="";
    password.classList.remove("is-invalid");
    password_feedback.innerHTML="";
    confirmpassword.classList.remove("is-invalid");
    confirmpassword_feedback.innerHTML=""
    agree.classList.remove("is-invalid");
    agree_feedback.innerHTML = "";
    return true;
}

function needtoknow() {
    alert("《用户须知》\n1.本网站仅为演示版本，不定期删除数据库，本站不负责因此造成的任何损失。\n2.必须在遵守国家法律、法规、政策及本协议的前提下，使用本网站。");
}
