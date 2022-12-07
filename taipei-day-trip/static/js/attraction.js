//根據使用者點擊的導覽時間切換價錢
    const booking_TWD = document.querySelector(".booking-TWD");
    const morning = document.getElementById("morning");
    const afternoon = document.getElementById("afternoon");

    morning.addEventListener("click",function(){
        booking_TWD.textContent="新台幣:2000元"
    });
    afternoon.addEventListener("click",function(){
        booking_TWD.textContent="新台幣:2500元"
    });

//串接景點 API，取得並展⽰特定景點資訊
    const attraction_pic_box = document.querySelector(".attraction-pic-box")
    const dotsbox = document.querySelector(".dotsbox")
    const left_arrow = document.querySelector(".left-arrow")
    const right_arrow = document.querySelector(".right-arrow")
    const attraction_name = document.querySelector(".attraction-name");
    const attraction_cat_mrt = document.querySelector(".attraction-cat-mrt");
    const attraction_introduce = document.querySelector(".attraction-introduce");
    const attraction_addres = document.querySelector(".attraction-addres");
    const attraction_transport = document.querySelector(".attraction-transport");
 
    let url=window.location.pathname
    fetch("/api"+url,{method:"Get",headers: {"Content-Type":"application/json"}
    }).then(function(response){
        return response.json();
    }).then(function(data){
        let attractionData = data["data"];
        let attractionimages = attractionData["images"];
        for(let i=0; i<attractionimages.length; i++){
            // 把每個景點的每張圖都加入屬性
            let next_img = document.createElement("img");
            next_img.setAttribute("class", "attraction-pic");
            next_img.src = attractionimages[i];
            attraction_pic_box.appendChild(next_img);
            // 有幾張圖就有幾個點，把每個點都加入屬性
            let next_dot = document.createElement("span");
            next_dot.setAttribute("class", "dot");
            next_dot.setAttribute("onclick",`currentdot(${i})`);
            dotsbox.appendChild(next_dot);
        };
        let attraction_pic = document.querySelectorAll(".attraction-pic")
        attraction_pic[0].style.display = "block"
  
        let alldots = document.querySelectorAll(".dot")
        alldots[0].className += " active";

        attraction_name.textContent = attractionData["name"];
        attraction_cat_mrt.textContent  = attractionData["category"]+"at "+attractionData["mrt"]
        attraction_introduce.textContent = attractionData["description"];
        attraction_addres.textContent = attractionData["address"];
        attraction_transport.textContent = attractionData["transport"];
        attraction_introduce.textContent = attractionData["description"];
        attraction_addres.textContent = attractionData["address"];
        attraction_transport.textContent = attractionData["transport"];
    });

// 照片輪播 https://www.w3schools.com/howto/howto_js_slideshow.asp
    let index =0;
    showpic(index);
    // 箭頭 
    function arrow(n){
        showpic(index += n);
    }
    // 點點
    function currentdot(n){
        showpic(index = n);
    }

    function showpic(n) {
        let attraction_pic = document.getElementsByClassName("attraction-pic");
        let dots = document.getElementsByClassName("dot");
        // 箭頭 按左-1 加到最後一位返回第一張
        if (n > attraction_pic.length-1){
            index = 0
        }
        // 箭頭 按左-1 減到最後一位返回最後張
        if (n < 0) {
            index = attraction_pic.length-1
        };
        for (i = 0; i < attraction_pic.length; i++) {
            attraction_pic[i].style.display = "none";
        }
        for (i = 0; i < dots.length; i++) {
          dots[i].className = dots[i].className.replace(" active", "");
        }
        attraction_pic[index].style.display = "block";
        dots[index].className += " active";
      }
   
    