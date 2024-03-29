//按上一頁會強制刷新
window.onpageshow = function(event) {
    if (event.persisted) {
        window.location.reload();
    }
};
//除了登入註冊的DIV以外透明
function set_opacity_index(){
    let navigation_bar_frame = document.getElementById("navigation-bar-frame");
    let welcome_img = document.getElementById("welcome-img");
    let Attractions = document.getElementById("Attractions");
    let footer = document.getElementById("footer");
    navigation_bar_frame.style.opacity="0.25";
    welcome_img.style.opacity="0.25";
    Attractions.style.opacity="0.25";
    footer.style.opacity="0.25";
}

function turnback_opacity_index(){
    let navigation_bar_frame = document.getElementById("navigation-bar-frame");
    let welcome_img = document.getElementById("welcome-img");
    let Attractionsele = document.getElementById("Attractions");
    let footer = document.getElementById("footer");
    navigation_bar_frame.style.opacity="1";
    welcome_img.style.opacity="1";
    Attractionsele.style.opacity="1";
    footer.style.opacity="1";
}

//按下登入註冊的按鈕function，點擊右上⾓【登入 / 註冊】，顯⽰會員登入表單
    const signin = document.querySelector(".signin");
    const signup = document.querySelector(".signup");
    const body = document.getElementById("navigation-bar-frame")
    function signinsignup(){
        set_opacity_index();
        signin.style.display = "block"; 
    }
//會員登入表單，按右上角的叉關閉視窗，
    //1)按最下方文字可以開啟註冊視窗並關起現在的視窗
    //2)按右上角的叉關閉視窗
    const goto_signup = document.querySelector(".goto-signup");
    const signup_message_class = document.querySelector(".signup-message");
    goto_signup.addEventListener("click",function(){
        signin.style.display = "none";
        signup_message_class.style.display = "none";//若剛剛有其他訊息的話必須先消除
        signup.style.display = "block";
    });
    const signin_close = document.querySelector(".signin-close");
    signin_close.addEventListener("click",function(){
        signin.style.display = "none";
        turnback_opacity_index();
    });
//會員註冊表單，按右上角的叉關閉視窗，
    //1)按最下方文字可以開啟登入視窗並關起現在的視窗
    //2)按右上角的叉關閉視窗
    const goto_signin = document.querySelector(".goto-signin");
    const signin_message_class = document.querySelector(".signin-message");
    goto_signin.addEventListener("click",function(){
        signup.style.display = "none";
        signin_message_class.style.display = "none";
        signin.style.display = "block";
    });
    const signup_close = document.querySelector(".signup-close");
    signup_close.addEventListener("click",function(){
        signup.style.display = "none";
        turnback_opacity_index();
    });
//註冊的function，透過AJAX fetch API連線到/api/user送資料
    function signupsubmit(){  
        //抓取使用者輸入資料
        let get_signup_name = signup_form.signup_name.value;
        let get_signup_email = signup_form.signup_email.value;
        let get_signup_password = signup_form.signup_password.value;
        //給fetch內body:的request body的資料型態
        let req_body = {
            "name": get_signup_name,
            "email": get_signup_email,
            "password": get_signup_password
        };
        //給fetch內header:的Content-type的資料型態
        let header = {
            "Content-type": "application/json",
        };
        fetch("/api/user",{
            method:"POST",
            body:JSON.stringify(req_body),
            headers:header,
        }).then(function(response){
                return response.json();//將資料用JSON的格式詮釋成:物件和陣列的組合
        }).then(function(result){  
            // 把結果縣示在頁面
            let signup_message_id = document.getElementById("signup-message");
            let signup_message_class = document.querySelector(".signup-message");
            if (result["ok"] ==true){
                signup_message_id.innerHTML = "註冊成功";
                signup_message_class.style.display = "block";
            }
            if (result["error"] ==true){
                errormessage=result["message"] 
                signup_message_id.innerHTML = errormessage;
                signup_message_class.style.display = "block";
            }
        })
        // 清空輸入框數據
        signup_form.signup_name.value= "";
        signup_form.signup_email.value= "";
        signup_form.signup_password.value= "";
    }
//登入的function，透過AJAX fetch API連線到/api/user/auth送資料
    function signinsubmit(){  
    //抓取使用者輸入資料
    let get_signin_email = signin_form.signin_email.value;
    let get_signin_password = signin_form.signin_password.value;
    //給fetch內body:的request body的資料型態
    let req_body = {
        "email": get_signin_email,
        "password": get_signin_password
    };
    //給fetch內header:的Content-type的資料型態
    let header = {
        "Content-type": "application/json",
    };
    fetch("/api/user/auth",{
        method:"PUT",
        body:JSON.stringify(req_body),
        headers:header,
    }).then(function(response){
            return response.json();//將資料用JSON的格式詮釋成:物件和陣列的組合
    }).then(function(result){  
        // 把結果縣示在頁面
        let signin_message_id = document.getElementById("signin-message");
        let signin_message_class = document.querySelector(".signin-message");
        if (result["ok"] ==true){
            window.location.reload(); // 登入成功後重新載載入
        }
        if (result["error"] ==true){
            errormessage=result["message"] 
            signin_message_id.innerHTML = errormessage;
            signin_message_class.style.display = "block";
        }
    })
    // 清空輸入框數據
    signin_form.signin_email.value= "";
    signin_form.signin_password.value= "";
    }
//檢查會員登入狀態，透過AJAX fetch API連線到/api/user/auth送資料
    fetch("/api/user/auth",{
        method:"GET",
    }).then(function(response){
            return response.json();//將資料用JSON的格式詮釋成:物件和陣列的組合
    }).then(function(result){
        console.log(result)
        const signin_signup = document.getElementById("signin-signup")
        if (result["data"] !=null){//如果使用者是在登入狀態(有TOKEN的話)
            document.getElementById("signin-signup").setAttribute("onclick", "member()");
            signin_signup.textContent="會員中心"//右上將顯示會員中心
        }
        else{
            document.getElementById("signin-signup").setAttribute("onclick", "signinsignup()");
            signin_signup.textContent="登入/註冊"
        } 
    });
//會員中心的function，如果按下會員中心會先檢查有沒有TOEKN，有TOEKN會連到登入頁面
    function member(){
        //有登入(有cookie)的話導向預定⾏程的⾴⾯  ( /booking )
        if(document.cookie){
            document.location.href="/member"    
        }
        //沒有登入(沒有cookie)的話顯示登入popup
        if(!document.cookie){
            signinsignup()
        }
    } 
  