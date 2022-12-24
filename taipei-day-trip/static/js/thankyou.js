//按上一頁會強制刷新
window.onpageshow = function(event) {
    if (event.persisted) {
        window.location.reload();
    }
};
//登出的function，透過AJAX fetch API連線到/api/user/auth送資料
function signout(){
    fetch("/api/user/auth",{
        method:"DELETE",//啟動後端刪除使用者TOKEN的API
    }).then(function(response){
            return response.json();
    }).then(function(result){
        if (result["ok"] ==true){//如果順利刪除後(沒有cookie)會回到首頁
            document.location.href="/" ;
        };          
    });
} ;
//取得Query String的訂單編號
let urlParams = new URLSearchParams(window.location.search);
orderid = urlParams.get('number');


//先檢查會員登入狀態，透過AJAX fetch API連線到/api/user/auth送資料
fetch("/api/user/auth",{
    method:"GET",
}).then(function(response){
        return response.json();//將資料用JSON的格式詮釋成:物件和陣列的組合
}).then(function(result){
//如果使用者是在登入狀態(有TOKEN的話)就連線到/api/order取資料
    if (result["data"] !=null){
        let order_title= document.querySelector(".order_title")
        order_title.textContent = "您好，"+result["data"].name +"，以下是您的訂單編號："
        fetch("/api/order/"+orderid,{
            method:"GET",
        }).then(function(response){
                return response.json();
        }).then(function(result){
            if (result["data"]!=null){ //如果有付款成功的訂單資料就顯示在頁面中
                console.log(result["data"])
                let order_id= document.querySelector(".order_id")
                order_id.textContent = result["data"].number;
                }
            else//若是沒有符合的訂單資料就回到首頁
                document.location.href="/";    
        })
    }
    else{//沒有登入(沒有cookie)的話回到首頁
        document.location.href="/";   
    } 
})

