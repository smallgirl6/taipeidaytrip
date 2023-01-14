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
            let member_name= document.querySelector(".member-name");
            let member_account= document.querySelector(".member-account");
            member_name.textContent = result["data"].name;
            member_account.textContent = result["data"].email  
            fetch("/api/member",
                {method:"GET",headers: {"Content-Type":"application/json"}
                }).then(function(response){
                    return response.json();
                }).then(function(data){
                    if (data["data"] !=null){ //歷史訂單
                        for(let i=0; i< data["data"].length; i++){
                                //歷史訂單
                            //外框 
                            let order_history = document.getElementById("order-history");
                            //每筆歷史訂單
                            let Nextorder_history_box = document.createElement("div"); 
                            Nextorder_history_box.setAttribute("class", "order-history-box");
                            //加到父div
                            order_history.appendChild(Nextorder_history_box);        
                                //照片盒
                            let Nextorder_history_pic = document.createElement("div");   
                            Nextorder_history_pic.setAttribute("class", "order-history-pic");
                                    //照片
                            let Nextorder_history_img = document.createElement("img");   
                            Nextorder_history_img.setAttribute("class", "order-history-img");
                            Nextorder_history_img.src =(data["data"][i]).trip.attraction.image;
                            //加到父div        
                            Nextorder_history_pic.appendChild(Nextorder_history_img);
                            Nextorder_history_box.appendChild(Nextorder_history_pic);
                                //訂單內容格子
                            let Nextorder_history_info = document.createElement("div");   
                            Nextorder_history_info.setAttribute("class", "order-history-info");
                            //加到父div        
                            Nextorder_history_box.appendChild(Nextorder_history_info);          
                                    //title
                            let Nextorder_history_orderid_title = document.createElement("div");   
                            Nextorder_history_orderid_title.setAttribute("class", "order-history-orderid-title");
                            Nextorder_history_orderid_title.textContent = "訂單編號："
                            let Nextorder_history_neme_title = document.createElement("div");   
                            Nextorder_history_neme_title.setAttribute("class", "order-history-name-title");
                            Nextorder_history_neme_title.textContent = "台北一日遊："
                            let Nextorder_history_date_title = document.createElement("div");   
                            Nextorder_history_date_title.setAttribute("class", "order-history-date-title");
                            Nextorder_history_date_title.textContent = "日期："
                            let Nextorder_history_time_title = document.createElement("div");   
                            Nextorder_history_time_title.setAttribute("class", "order-history-time-title");
                            Nextorder_history_time_title.textContent = "時間："
                            let Nextorder_history_fee_title = document.createElement("div");   
                            Nextorder_history_fee_title.setAttribute("class", "order-history-fee-title");
                            Nextorder_history_fee_title.textContent = "費用："
                            let Nextorder_history_address_title = document.createElement("div");   
                            Nextorder_history_address_title.setAttribute("class", "order-history-address-title");
                            Nextorder_history_address_title.textContent = "地點："
                            let Nextcontact_name_title = document.createElement("div");   
                            Nextcontact_name_title.setAttribute("class", "contact-name-title");
                            Nextcontact_name_title.textContent = "聯絡人姓名："
                            let Nextcontact_phone_title = document.createElement("div");   
                            Nextcontact_phone_title.setAttribute("class", "contact-phone-title");
                            Nextcontact_phone_title.textContent = "連絡電話："
                            let Nextcontact_email_title = document.createElement("div");   
                            Nextcontact_email_title.setAttribute("class", "contact-email-title");
                            Nextcontact_email_title.textContent = "連絡信箱："
                                        //content
                            let Nextorder_history_orderid = document.createElement("div");   
                            Nextorder_history_orderid.setAttribute("class", "order-history-orderid");
                            Nextorder_history_orderid.textContent = (data["data"][i]).number;
                            let Nextorder_history_neme = document.createElement("div");   
                            Nextorder_history_neme.setAttribute("class", "order-history-name");
                            Nextorder_history_neme.textContent = (data["data"][i]).trip.attraction.name;
                            let Nextorder_history_date = document.createElement("div");   
                            Nextorder_history_date.setAttribute("class", "order-history-date");
                            Nextorder_history_date.textContent = (data["data"][i]).trip.date;
                            let Nextorder_history_time = document.createElement("div");   
                            Nextorder_history_time.setAttribute("class", "order-history-time");
                            if ((data["data"][i]).trip.time=="morning"){
                                Nextorder_history_time.textContent="早上 9 點到下午 12 點";
                                }
                                else{
                                    Nextorder_history_time.textContent="下午 1 點到下午 4 點";
                                }
                            let Nextorder_history_fee = document.createElement("div");   
                            Nextorder_history_fee.setAttribute("class", "order-history-fee");
                            Nextorder_history_fee.textContent = "新台幣" + (data["data"][i]).price + "元";
                            let Nextorder_history_address = document.createElement("div");   
                            Nextorder_history_address.setAttribute("class", "order-history-address");
                            Nextorder_history_address.textContent = (data["data"][i]).trip.attraction.address;
                            let Nextcontact_name = document.createElement("div");   
                            Nextcontact_name.setAttribute("class", "contact-name");
                            Nextcontact_name.textContent = (data["data"][i]).contact.name;
                            let Nextcontact_phone = document.createElement("div");   
                            Nextcontact_phone.setAttribute("class", "contact-phone");
                            Nextcontact_phone.textContent = (data["data"][i]).contact.phone;
                            let Nextcontact_email = document.createElement("div");   
                            Nextcontact_email.setAttribute("class", "contact-email");
                            Nextcontact_email.textContent = (data["data"][i]).contact.email;                      
                            //加到父div        
                            Nextorder_history_info.appendChild(Nextorder_history_orderid_title);
                            Nextorder_history_orderid_title.appendChild(Nextorder_history_orderid);
                            Nextorder_history_info.appendChild(Nextorder_history_neme_title);
                            Nextorder_history_neme_title.appendChild(Nextorder_history_neme);
                            Nextorder_history_info.appendChild(Nextorder_history_date_title);
                            Nextorder_history_date_title.appendChild(Nextorder_history_date);
                            Nextorder_history_info.appendChild(Nextorder_history_time_title);
                            Nextorder_history_time_title.appendChild(Nextorder_history_time);
                            Nextorder_history_info.appendChild(Nextorder_history_fee_title);
                            Nextorder_history_fee_title.appendChild(Nextorder_history_fee);
                            Nextorder_history_info.appendChild(Nextorder_history_address_title);
                            Nextorder_history_address_title.appendChild(Nextorder_history_address);
                            Nextorder_history_info.appendChild(Nextcontact_name_title);
                            Nextcontact_name_title.appendChild(Nextcontact_name);
                            Nextorder_history_info.appendChild(Nextcontact_email_title);
                            Nextcontact_email_title.appendChild(Nextcontact_email);
                            Nextorder_history_info.appendChild(Nextcontact_phone_title); 
                            Nextcontact_phone_title.appendChild(Nextcontact_phone);                                   
                        }
                    }
                    else{ //沒有歷史訂單
                        let no_order_data = document.querySelector(".no-order-data");
                        let hr2 = document.querySelector(".hr2");
                        let footer = document.querySelector(".footer");
                        no_order_data.style.display = "block";
                        no_order_data.textContent="您沒有歷史訂單"
                        hr2.style.top= "95px";
                        footer.style.height= "265px";
                    }    
                });                   
        }
        else{
            document.location.href="/" //沒有登入(沒有cookie)的話回到首頁
        } 
    });
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
//上傳照片的function
//     function uploaddata(){
//     const userimage= document.querySelector('#uploader-user-pic').files[0];  
//     const usermessage = document.getElementById('text-content-input').value; 
//     const errormessage= document.querySelector('.error')
//     if ((userimage !=null) && (usermessage.length!=0)){
//         let formData = new FormData();  //創建了一個新的 FormData 對象(表單數據)
//         formData.append('usermessage', usermessage);
//         formData.append('userimage', userimage); 
//         fetch("/api/image-uploade",{
//             method:"POST",
//             body:formData,
//         }).then(function(response){
//                 return response.json();//將資料用JSON的格式詮釋成:物件和陣列的組合
//         }).then(function(result){ 
//             if (result["ok"] ==true){
//                 document.querySelector('#uploader-user-pic').value = "";
//                 document.querySelector('#text-content-input').value = "";
//                 location.reload();
//             }
//             if (result["error"] ==true){
//                 errormessage.textContent="圖片上傳失敗"
//                 document.querySelector('#uploader-user-pic').value = "";
//                 location.reload();     
//             }
//         });
//     }
//     else{
//         errormessage.textContent="請輸入訊息以及選擇要上傳圖片"
//     }
// };

            
