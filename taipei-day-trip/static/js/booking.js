//按上一頁會強制刷新
    window.onpageshow = function(event) {
        if (event.persisted) {
            window.location.reload();
        }
    };
//檢查會員登入狀態，透過AJAX fetch API連線到/api/user/auth送資料
    fetch("/api/user/auth",{
        method:"GET",
    }).then(function(response){
            return response.json();//將資料用JSON的格式詮釋成:物件和陣列的組合
    }).then(function(result){
        if (result["data"] !=null){//如果使用者是在登入狀態(有TOKEN的話)的話顯示預約的行程或沒有預約
            let booking_attraction= document.querySelector(".booking-attraction");
            booking_attraction.textContent = "您好，"+result["data"].name +"，待預訂的行程如下："
            
            fetch("/api/booking",
                {method:"GET",headers: {"Content-Type":"application/json"}
                }).then(function(response){
                    return response.json();
                }).then(function(data){
                    if (data["data"] !=null){
                        let attraction_name = document.querySelector(".attraction-name");
                        let attraction_date = document.querySelector(".attraction-date");
                        let attraction_time = document.querySelector(".attraction-time");
                        let attraction_fee = document.querySelector(".attraction-fee");
                        let attraction_address = document.querySelector(".attraction-address");
                        let attraction_img = document.querySelector(".attraction-img");
                        
                        attraction_name.textContent = data["data"].attraction.name
                        attraction_date.textContent = data["data"].date
                        if (data["data"].time=="morning"){
                            attraction_time.textContent="早上 9 點到下午 12 點"
                        }
                        else{
                            attraction_time.textContent="下午 1 點到下午 4 點"
                        }
                        attraction_fee.textContent = "新台幣" + data["data"].price + "元"
                        attraction_address.textContent = data["data"].attraction.address
                        attraction_img.src= data["data"].attraction.image
                    }
                if (data["data"] ==null){
                    let Booking_box = document.querySelector(".Booking-box");
                    let no_booking_data = document.querySelector(".no-booking-data");
                    let footer = document.querySelector(".footer");
                    Booking_box.style.display = "none";
                    no_booking_data.style.display = "block";
                    no_booking_data.textContent="目前沒有任何待預訂的行程"
                    footer.style.height= "865px";
                }    
                });                   
        }
        else{
            document.location.href="/" //沒有登入(沒有cookie)的話回到首頁
        } 
    });
//刪除目前預定行程
    function deleteattraction(){
        fetch("/api/booking",{
            method:"DELETE",//連線後端，後端會消除存在資料庫中的資料
            cache: "no-cache",
        }).then(function(response){
                return response.json();
        }).then(function(result){
            if (result["ok"] ==true){//如果順利刪除後會收到OK重新整理⾴⾯。
                window.location.reload();   
                  
            };          
        });
    }
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

    } 
        