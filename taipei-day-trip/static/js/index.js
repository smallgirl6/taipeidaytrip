//載入景點資料(一開始的頁面)
    let isLoading = false; //目前頁面是否正在載入API
    fetch("/api/attractions?page=0").then(function(response){
        return response.json();
    }).then(function(data){
        let attractions_names_Array=[];//建立一個Array等等用來放每筆資料的觀光景點(data.name)的資料
        let attractions_imgs_Array= []; //建立一個Array等等用來放每筆資料的觀光第一第一張圖片的資料
        let attractions_mrts_Array= []; //建立一個Array等等用來放每筆資料的觀光景點(data.mrt)的資料
        let attractions_cat_Array= []; //建立一個Array等等用來放每筆資料的觀光景點(data.category)的資料
        let count = data["data"].length; //看有幾筆資料
        
        for(let i=0; i< count; i++){ 
            attractions_names_Array.push((data["data"][i]).name); // 列表  
            attractions_imgs_Array.push((data["data"][i]).images[0]) ;//只取第一張圖
            attractions_mrts_Array.push((data["data"][i]).mrt);
            attractions_cat_Array.push((data["data"][i]).category) ;                                   
        };

        //獲取所有的 <標籤> 元素
        let Attraction_imgbox = document.querySelectorAll(".Attraction-imgbox");
        let Attraction_pic = document.querySelectorAll(".Attraction-pic"); 
        let Attraction_namebox = document.querySelectorAll(".Attraction-namebox"); 
        let Attraction_name = document.querySelectorAll(".Attraction-name");  
        let Attraction_detail = document.querySelectorAll(".Attraction-detail");
        let Attraction_mrt = document.querySelectorAll(".Attraction-mrt");
        let Attraction_cat = document.querySelectorAll(".Attraction-cat");

        for(let i=0; i<count; i++){ 
            //名稱
            let nextname = document.createElement("div"); //創建一個空的div元素節點  
            nextname.setAttribute("class", "Attraction-name"); //添加一個class屬性，值為Attraction_name   
            let nextnameTextNode = document.createTextNode(attractions_names_Array[i]);  //用attractions_names_Array[0-11]抓出的景點創造文字節點
            nextname.appendChild(nextnameTextNode); //將剛剛的文字節點(nextnameTextNode)添加到新建div元素
            Attraction_namebox[i].replaceChild(nextname, Attraction_name[i]);  //用新的元素nextname来替換Attraction_name[i]              
            
            //圖片
            let nextImg = document.createElement("img");
            nextImg.setAttribute("class", "Attraction-pic");
            nextImg.src = attractions_imgs_Array[i];
            Attraction_imgbox[i].replaceChild(nextImg,Attraction_pic[i]);

            //捷運
            let nextMrt = document.createElement("div");
            nextMrt.setAttribute("class", "Attraction-mrt");
            let nextmrtTextNode = document.createTextNode(attractions_mrts_Array[i]);
            nextMrt.appendChild(nextmrtTextNode);
            Attraction_detail[i].replaceChild(nextMrt,Attraction_mrt[i]); 

            //分類
            let nextCat = document.createElement("div");
            nextCat.setAttribute("class", "Attraction-cat");
            let nextcatTextNode = document.createTextNode(attractions_cat_Array[i]);
            nextCat.appendChild(nextcatTextNode);
            Attraction_detail[i].replaceChild(nextCat,Attraction_cat[i]);     
        };   
    });          
    
//載入第二頁後的資料+生成HTML的標籤
    //用Intersection Observer API，必須觀察1.page是否為null  2.觀察有關鍵字的第二頁或沒有關鍵字的第二頁
    let page = 1 
    let options = { //Intersection Observer API的選項
        root:null,
        rootMargin:"0px 0px 0px 0px",//窗口的縮放，CSS的margin
        threshold:0.0, //當目標退出視口時將會觸發
    };
    const observer = new IntersectionObserver((entries) => { //用瀏覽器構造函數建構一個建構式函數observer
        entries.forEach((entry) => {  //entries 的清單，包含了各個物件中的資訊。
            //isLoading是true代表正在載入其他API，就先不要動作。若是 false 才動作。
            if (isLoading==true) {
                return;
            }
            if (page==null){
                return;
            }             
            if (entry.isIntersecting ==true && isLoading==false) {
                //判斷是否有關鍵字以及頁數
                isLoading = true;//使用 fetch() 之前，將 isLoading 設定為 true，表示現在開始要呼叫 API 了
                fetch( "/api/attractions?page="+ page+"&"+"keyword="+ inputkeyword.value).then(function(response){
                    return response.json();
                }).then(function(data){
                    let nextpage= data.nextPage;     //下一page
                    let count = data["data"].length; //看有幾筆資料
                    for(let i=0; i< data["data"].length; i++){ 
                    //做下一頁新的HTML框
                        //外框 每個景點
                        let Attractions = document.getElementById("Attractions");
                            //每個景點 Attraction(NextAttraction)
                        let NextAttraction = document.createElement("div"); 
                        NextAttraction.setAttribute("class", "Attraction");
                                //照片盒Attraction-imgbox(NextAttraction-imgbox)
                        let NextAttraction_imgbox = document.createElement("div");   
                        NextAttraction_imgbox.setAttribute("class", "Attraction-imgbox"); 
                                    //照片Attraction-pic(NextAttraction-pic)
                        let NextAttraction_pic = document.createElement("img");   
                        NextAttraction_pic.setAttribute("class", "Attraction-pic");
                        NextAttraction_pic.src = (data["data"][i]).images[0];
                        //加到父div        
                        NextAttraction_imgbox.appendChild(NextAttraction_pic);
                                    //景點名盒Attraction-namebox(NextAttraction-namebox)
                        let NextAttraction_namebox = document.createElement("div");   
                        NextAttraction_namebox.setAttribute("class", "Attraction-namebox"); 
                                        //景點名Attraction-name(NextAttraction-name)
                        let NextAttraction_name = document.createElement("div");   
                        NextAttraction_name.setAttribute("class", "Attraction-name");
                        NextAttraction_name.textContent = (data["data"][i]).name; 
                        //加到父div        
                        NextAttraction_namebox.appendChild(NextAttraction_name);
                                //詳細Attraction-detail(NextAttraction-detail)
                        let NextAttraction_detail = document.createElement("div");   
                        NextAttraction_detail.setAttribute("class", "Attraction-detail"); 
                                    //捷運Attraction-mrt(NextAttraction-mrt)
                        let NextAttraction_mrt = document.createElement("div");   
                        NextAttraction_mrt.setAttribute("class", "Attraction-mrt");
                        NextAttraction_mrt.textContent = (data["data"][i]).mrt;
                        //加到父div        
                        NextAttraction_detail.appendChild(NextAttraction_mrt); 
                                    //分類Attraction-cat(NextAttraction-cat)
                        let NextAttraction_cat = document.createElement("div");   
                        NextAttraction_cat.setAttribute("class", "Attraction-cat"); 
                        NextAttraction_cat.textContent = (data["data"][i]).category;
                        //加到父div        
                        NextAttraction_detail.appendChild(NextAttraction_cat);     
                        //加到父div        
                        NextAttraction.appendChild(NextAttraction_imgbox);
                        NextAttraction.appendChild(NextAttraction_namebox);       
                        NextAttraction.appendChild(NextAttraction_detail);
                        Attractions.appendChild(NextAttraction);                                               
                    };
                    if (nextpage != null){
                        page = nextpage;
                    }
                    else{
                        observer.unobserve(footer);//不查了
                    }
                    isLoading = false;   //當 fetch() 載入完畢，取得後端回應後，將 isLoading 設定為 false，表示現在沒有在載入 API 了。                                             
                });
            }
        }); 
    }, options); 
    const footer = document.querySelector(".footer");
    observer.observe(footer); // 指定觀察footer
    
//搜尋欄位
    //抓取使用者輸入資料
    const inputkeyword = document.getElementById("keyword");
    function searchbar(){
        let src = "/api/attractions?page=0&keyword="+ inputkeyword.value; 
        if (isLoading==true) {
            return;
        }
        isLoading = true;
        fetch(src,{methods:"GET",}).then(function(response){
            return response.json();
        }).then(function(data){
            console.log(data)
            if (data["error"]==true){ //如果沒有對應資料的話API會給["error"]==true
                Attractions.innerHTML = "查無相關景點";//把原本圖片給洗掉顯示"查無相關景點"
            }
            else{
                Attractions.innerHTML = " ";//把原本圖片給洗掉
            }
            let nextpage= data.nextPage;     //下一page
            let count = data["data"].length; //看有幾筆資料
            for(let i=0; i< count; i++){ 
            //做新的HTML框
                //外框 每個景點
                let Attractions = document.getElementById("Attractions");
                    //每個景點 Attraction(NextAttraction)
                let NextAttraction = document.createElement("div"); 
                NextAttraction.setAttribute("class", "Attraction");
                        //照片盒Attraction-imgbox(NextAttraction-imgbox)
                let NextAttraction_imgbox = document.createElement("div");   
                NextAttraction_imgbox.setAttribute("class", "Attraction-imgbox"); 
                            //照片Attraction-pic(NextAttraction-pic)
                let NextAttraction_pic = document.createElement("img");   
                NextAttraction_pic.setAttribute("class", "Attraction-pic");
                NextAttraction_pic.src = (data["data"][i]).images[0];
                //加到父div        
                NextAttraction_imgbox.appendChild(NextAttraction_pic);
                            //景點名盒Attraction-namebox(NextAttraction-namebox)
                let NextAttraction_namebox = document.createElement("div");   
                NextAttraction_namebox.setAttribute("class", "Attraction-namebox"); 
                                //景點名Attraction-name(NextAttraction-name)
                let NextAttraction_name = document.createElement("div");   
                NextAttraction_name.setAttribute("class", "Attraction-name");
                NextAttraction_name.textContent = (data["data"][i]).name; 
                //加到父div        
                NextAttraction_namebox.appendChild(NextAttraction_name);
                        //詳細Attraction-detail(NextAttraction-detail)
                let NextAttraction_detail = document.createElement("div");   
                NextAttraction_detail.setAttribute("class", "Attraction-detail"); 
                            //捷運Attraction-mrt(NextAttraction-mrt)
                let NextAttraction_mrt = document.createElement("div");   
                NextAttraction_mrt.setAttribute("class", "Attraction-mrt");
                NextAttraction_mrt.textContent = (data["data"][i]).mrt;
                //加到父div        
                NextAttraction_detail.appendChild(NextAttraction_mrt); 
                            //分類Attraction-cat(NextAttraction-cat)
                let NextAttraction_cat = document.createElement("div");   
                NextAttraction_cat.setAttribute("class", "Attraction-cat"); 
                NextAttraction_cat.textContent = (data["data"][i]).category;
                //加到父div        
                NextAttraction_detail.appendChild(NextAttraction_cat);     
                //加到父div        
                NextAttraction.appendChild(NextAttraction_imgbox);
                NextAttraction.appendChild(NextAttraction_namebox);       
                NextAttraction.appendChild(NextAttraction_detail);
                Attractions.appendChild(NextAttraction);
            };
            isLoading = false;
        });
    };

// 點選搜尋框顯示的分類
    fetch("/api/categories").then(function(response){
        return response.json();
    }).then(function(data){
        let categorydata = data["data"]
        let count = data["data"].length; //看有幾筆資料
        categorymenu = document.querySelector(".categoryMenu");
        const categorybox = document.createElement("div");
        categorybox.setAttribute("class", "categoryBox");

        for (let i = 0; i <count; i++) {
            //做分類的內容物item
            const categoryitem = document.createElement("div");
            categoryitem.setAttribute("class", "categoryItem");
            categoryitem.textContent = categorydata[i];
            //加到父div (categorybox)
            categorybox.appendChild(categoryitem);    
        }
        //加到父div (categorybox)
        categorymenu.appendChild(categorybox);
    
        //監聽使用者的行動
        //點選到搜尋區塊就顯示categorymenu
        const inputkeyword = document.getElementById("keyword");
        inputkeyword.addEventListener("click",function(event){
            categorymenu.style.display = "block";
            event.stopPropagation();
        });
        //點選畫⾯的其他位置，隱藏跳出式分類區塊
        document.addEventListener("click",function(event){
            categorymenu.style.display = "none";
        });
        //點選分類，將景點分類名稱填入搜尋框，隱藏跳出式分類區塊
        //let cat = document.getElementsByClassName("categoryItem");//剛剛生成的categoryItem
        let catitem = document.getElementsByClassName("categoryItem");
        for(let i = 0; i<catitem.length; i++){//監聽全部分類選項
            catitem[i].addEventListener("click",function(event){ //若點其中一個選項的話，把選項的文字傳到輸入框的值
                inputkeyword.value = catitem[i].textContent;
                categorymenu.style.display = "none";    //隱藏跳出式分類區塊
            }); 
        }; 
    });

          
