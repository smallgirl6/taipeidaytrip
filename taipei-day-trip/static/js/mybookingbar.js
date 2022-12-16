//導覽列上的預定⾏程文字連結處理
    const my_booking = document.getElementById("my-booking");
    my_booking.addEventListener("click",function(){
        //有登入(有cookie)的話導向預定⾏程的⾴⾯  ( /booking )
        if(document.cookie){
            document.location.href="/booking"    
        }
        //沒有登入(沒有cookie)的話顯示登入popup
        if(!document.cookie){
            signinsignup()
         }
    });
   