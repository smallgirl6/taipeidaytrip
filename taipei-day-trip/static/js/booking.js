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
        if (result["data"] !=null){//如果使用者是在登入狀態(有TOKEN的話)，連線到/api/booking取資料
            let booking_attraction= document.querySelector(".booking-attraction");
            booking_attraction.textContent = "您好，"+result["data"].name +"，待預訂的行程如下："  
            fetch("/api/booking",
                {method:"GET",headers: {"Content-Type":"application/json"}
                }).then(function(response){
                    return response.json();
                }).then(function(data){
                    if (data["data"] !=null){ //有預約行程
                        let attraction_name = document.querySelector(".attraction-name");
                        let attraction_date = document.querySelector(".attraction-date");
                        let attraction_time = document.querySelector(".attraction-time");
                        let attraction_fee = document.querySelector(".attraction-fee");
                        let attraction_address = document.querySelector(".attraction-address");
                        let attraction_img = document.querySelector(".attraction-img");
                        let booking_total = document.querySelector(".booking-total");
                        
                        attraction_name.textContent = data["data"].attraction.name;
                        attraction_date.textContent = data["data"].date;
                        if (data["data"].time=="morning"){
                            attraction_time.textContent="早上 9 點到下午 12 點";
                        }
                        else{
                            attraction_time.textContent="下午 1 點到下午 4 點";
                        }
                        attraction_fee.textContent = "新台幣" + data["data"].price + "元";
                        booking_total.textContent= "總價:" + "新台幣" + data["data"].price + "元";
                        attraction_address.textContent = data["data"].attraction.address;
                        attraction_img.src= data["data"].attraction.image;
                    }
                    else{ //沒有預約行程
                        let Booking_box = document.querySelector(".Booking-box");
                        let no_booking_data = document.querySelector(".no-booking-data");
                        let footer = document.querySelector(".footer");
                        Booking_box.style.display = "none";
                        no_booking_data.style.display = "block";
                        no_booking_data.textContent="目前沒有任何待預訂的行程，若要查詢歷史訂單，請點擊右上角的會員中心"
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
    };
    
//串接金流    
    // 把 TapPay 內建輸入卡號的表單給植入到 div 中
    let fields = {
        number: {
            element: '#card-number',
            placeholder: '**** **** **** ****'
        },
        expirationDate: {
            element: document.getElementById('card-expiration-date'),
            placeholder: 'MM / YY'
        },
        ccv: {
            element: '#card-ccv',
            placeholder: 'ccv'
        }
    };
    TPDirect.card.setup({
        fields: fields,
        isMaskCreditCardNumber: true,
        maskCreditCardNumberRange: {
        beginIndex: 6,
        endIndex: 11
        }
    });
    // 讓 button click 之後觸發 getPrime 方法
    let isclick=true; // 防止多次點擊
    function confirm_order() {
        if (isclick == false){
            return
        };
        isclick = false;
        let order_faild_message = document.querySelector(".order_faild_message");
        const tappayStatus = TPDirect.card.getTappayFieldsStatus()
        if (tappayStatus.canGetPrime === false) {
            order_faild_message.style.display = "block";
            order_faild_message.textContent="信用卡資訊錯誤";
            isclick = true;
            return
        };
        TPDirect.card.getPrime((result) => {
            if (result.status !== 0) {
                order_faild_message.style.display = "block";
                order_faild_message.textContent="信用卡資訊錯誤";//result.msg;
                isclick = true;
                return
            };
            //console.log("prime is"+result.card.prime)
            //建立訂單編號和資料，透過AJAX fetch API連線到/api/booking取得頁面資料
            //取得聯絡資訊輸入值
            let contact_name_input = document.getElementById('contact-name-input');
            let contact_email_input = document.getElementById('contact-email-input');
            let contact_phone_input = document.getElementById('contact-phone-input');
            fetch("/api/booking",
            {method:"GET",headers: {"Content-Type":"application/json"}
            }).then(function(response){
                return response.json();
            }).then(function(data){
            //給fetch/api/orders內body:的request body的資料型態
            let req_body = {
                    "prime":result.card.prime,
                    "order": {
                        "price": data["data"].price,
                        "trip": {
                            "attraction": {
                            "id": data["data"].attraction.id,
                            "name":  data["data"].attraction.name,
                            "address":  data["data"].attraction.address,
                            "image": data["data"].attraction.image
                            },
                            "date": data["data"].date,
                            "time": data["data"].time
                        },
                        "contact": {
                            "name": contact_name_input.value,
                            "email": contact_email_input.value,
                            "phone": contact_phone_input.value
                        }
                    }
            };
            //給fetch內header:的Content-type的資料型態
            let header = {
                "Content-type": "application/json",
            };
                fetch("/api/orders",{ //連線到後端API
                method:"POST",
                body:JSON.stringify(req_body),
                headers:header,
                }).then(function(response){
                        return response.json();//將資料用JSON的格式詮釋成:物件和陣列的組合
                }).then(function(result){
                    if (result["error"]==undefined){ //收到的不是錯誤訊息，只有付款成功和付款失敗的兩種回應(有訂購編號)
                        if (result["data"]["payment"].status==0){  //付款成功
                            document.location.href="/thankyou?number="+result["data"].number 
                            isclick = true;
                        }
                        else//付款失敗(後端TapPay 提供的付款 API那邊收到錯誤的回應導致失敗)(有訂購編號)
                            order_faild_message.style.display = "block";
                            order_faild_message.textContent=result["data"]["payment"].message;
                            isclick = true;
                    }
                    if  (result["data"]==undefined){  //收到的都是錯誤訊息，沒有順利成立訂單
                        if (result["error"]==true){ 
                            if(result["message"]=="未登入" || result["message"]=="伺服器內部錯誤，請重新訂購"){ 
                                document.location.href="/";
                                isclick = true;
                            }
                            else
                                order_faild_message.style.display = "block";
                                order_faild_message.textContent=result["message"];
                                isclick = true;
                        }
                    }  
                });
            });
        });
    };
    
    
    
