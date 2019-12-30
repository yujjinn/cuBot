var keyword_num = 0;
var genres='';
 function genre_get(gnr){

       // initializing
       genres = '';
       genre_cnt = 0;
       if( gnr[0].checked == true)
       {
         genres += '드라마, ';
         genre_cnt+=1;
       }
       if( gnr[1].checked == true)
       {
         genres += '영화, ';
         genre_cnt+=1;
       }
       if( gnr[2].checked == true)
       {
         genres += '책, ';
         genre_cnt+=1;
       }
       if(genre_cnt ==0)
       {
         alert('장르를 최소 1가지 선택해 주세요');
       }
       else
       {
         genres = genres.substring(0,genres.length-2);
         $("#chatbox").append('<p class="botText"><img src="/static/qbicc.png" alt="My Image" width="200" height="200"><span><b>'+genres+'</b>을(를) 선택하셨군요! <br>원하시는 <b>키워드</b>를 입력하시거나<br><b>추천 버튼</b>을 눌러주세요.</span></p>'+'<button id="genre_rcm" onclick="rcm_click();" type="button">&nbsp;&nbsp;&nbsp;추천&nbsp;&nbsp;&nbsp;</button><hr>');
       }
 }



function genre_checked(){
 genre_click = 0;
 genre_click+=1;
 genres = '';
 genre_cnt  = 0;
//  alert(genre_click+"! & choice ");
 if (my_form.mycheck[0].checked ){
   genres += '드라마 ';
   genre_cnt+=1;
 }
 if (my_form.mycheck[1].checked ){
   genres += '영화 ';
   genre_cnt+=1;
 }
 if (my_form.mycheck[2].checked ){
   genres += '책 ';
   genre_cnt+=1;
 }

 if(genre_click && genre_cnt > 0){
   document.getElementById("init_click").disabled = true;
 }

 if(genre_cnt ==0)
 {
   alert('장르를 최소 1가지 선택해 주세요');
 }
 else
 {
   $("#chatbox").append('<p class="botText"><img src="/static/qbicc.png" alt="My Image" width="200" height="200"><span><b>'+genres+'</b>을(를) 선택하셨군요! <br><b>키워드</b>를 입력하시겠어요<br><b>아님 추천</b>해드릴까요?'+

   '<button id="genre_rcm" onclick="rcm_click();" type="button">&nbsp;&nbsp;&nbsp;추천&nbsp;&nbsp;&nbsp;</button></span></p>');
 }

}




function check_all() {
 //  alert("check_all "+ my_form.mycheck.length + "!")
   for(i=0; i < my_form.mycheck.length; i++) {
     my_form.mycheck[i].checked = true;
   }
}





var kwd_name = "";
function getBotResponse(str, rawText) {
//alert("!" +str);

var userHtml = '<p class="userText"><span>' + rawText + "</span></p>";
$("#textInput").val("");
$("#chatbox").append(userHtml);
//영화 포함한다면

function getDrama(str){
 // alert('drama');
   document
    .getElementById("userInput")
    .scrollIntoView({ block: "start", behavior: "smooth" });
  $.ajax({
    url:'/drama',
    type:'GET',
    data : {msg:rawText},
    async: false,
    success:function(data){
      var botHtml = '<p class="botText"><span>드라마</span></p>'+data;
      $("#chatbox").append(botHtml);
    }
  });

}
function getMovie(str){
 //alert('movie');

   document
    .getElementById("userInput")
    .scrollIntoView({ block: "start", behavior: "smooth" });
  $.ajax({
    url:'/movie',
    type:'GET',
    data : {msg:rawText},
    async: false,
    success:function(data){
      var botHtml = '<p class="botText"><span>영화</span></p>'+data;
      $("#chatbox").append(botHtml);
    }
  });

}
 function getBook(str){
   //alert('book');
  document
   .getElementById("userInput")
   .scrollIntoView({ block: "start", behavior: "smooth" });
   $.ajax({
   url:'/book',
   type:'GET',
   data : {msg:rawText},
   async: false,
   success:function(data){
     var botHtml = '<p class="botText"><span>책</span></p>'+data;
     $("#chatbox").append(botHtml);
   }
 });

 }

   if(str.indexOf('드라마')>=0)
   {
     getDrama(str);
   }
   if(str.indexOf('영화')>=0)
   {
     getMovie(str);
   }
   if(str.indexOf('책')>=0)
   {
     getBook(str);
   }
   $("#chatbox").append('<p class="botText"><span>장르를 다시 선택하고 싶다면 <b>처음으로</b> 버튼을, <br> 키워드를 다시 입력 혹은 선택하고 싶다면 <b>뒤로가기</b> 버튼을 입력해 주세요.</span></p>');
   $("#chatbox").append('<br><button id ="back_to_first" onclick="go_back()">처음으로</button>&nbsp;&nbsp;&nbsp;<button id ="back_button" onclick="backTo()">뒤로가기</button>');
 }





function CheckAll(chk){
 for (i = 0; i < chk.length; i++){
     if( !chk[i].checked){chk[i].checked = true ;}
 }
}




////////////////////////키워드 입력////////////////////////////////

function send_keyword(){
   keyword_num += 1;
   if ( keyword_num > 0) {
     var rawText = $("#textInput").val();
     kwd_name = rawText;
     if (genres.length < 1){
       alert("장르를 먼저 선택해 주세요. ");
       $("#textInput").val("");
     }
     else{

       if ( rawText.length <= 1 ){
         alert("두글자 이상을 입력해 주세요.");
       }
       else{

         getBotResponse(genres, rawText);
         keyword_num =0;
       }
     }
   }
}

function kwd_click(){
 keyword_num += 1;
 alert("키워드를 입력해주세요");

}


function backTo(){

 $("#chatbox").append('<p class="botText"><img src="/static/qbicc.png" alt="My Image" width="200" height="200"><span><b>'+genres+'</b>을(를) 선택하셨군요! <br>원하시는 <b>키워드</b>를 입력하시거나 <b>추천 버튼</b>을 눌러주세요.</span></p>'+

 '<button id="genre_rcm" onclick="rcm_click();" type="button">&nbsp;&nbsp;&nbsp;추천&nbsp;&nbsp;&nbsp; </button><hr>');
}


//////////////////////// 추천 /////////////////////////////



var rcm_cnt = 0;
function rcm_click(){
  rcm_cnt+=1;

 $.ajax({
     type: 'GET',
     url: '/process',
     data : {num:rcm_cnt},
     success: function(data){
       var bothtml = data;
       //var bothtml = '<p class="botText">'+data+'</p>';
       $("#chatbox").append('<p class="botText"><span><b>키워드 입니다</span></p>'+bothtml);
     }
   });


}


function rcm_f5(){

  $.ajax({
      type: 'POST',
      url: '/rcmF5',
      success: function(data){
        var bothtml = data;
        var newRandArray = [];
        newRandArray = bothtml.split(',');

        $('#'+rcm_cnt+'rcm_genre1').replaceWith('<button id ="'+rcm_cnt+'rcm_genre1" onclick="get_inform(\''+newRandArray[0]+'\');">'+newRandArray[0]+'</button>');
        $('#'+rcm_cnt+'rcm_genre2').replaceWith('<button id ="'+rcm_cnt+'rcm_genre2" onclick="get_inform(\''+newRandArray[1]+'\');">'+newRandArray[1]+'</button>');
        $('#'+rcm_cnt+'rcm_genre3').replaceWith('<button id ="'+rcm_cnt+'rcm_genre3" onclick="get_inform(\''+newRandArray[2]+'\');">'+newRandArray[2]+'</button>');
        //$("#chatbox").append('<p class="botText"><span><b>키워드 입니다</span></p>'+bothtml);
      }
    });


  //$('#원본').replaceWith(새객체);
}


// 각각 키워드 입력했을 때의 결과값 장르마다 도출할 수 있도록
function get_inform(word){

 var str = genres;
//  alert(str+ " hi "+ word);
 var rawText = word;
 kwd_name = word;
 var userHtml = '<p class="userText"><span>' + rawText + "</span></p>";
 $("#chatbox").append(userHtml);

 function getDrama(){
   //alert('drama');

   document
     .getElementById("userInput")
     .scrollIntoView({ block: "start", behavior: "smooth" });
   $.ajax({
     url:'/drama',
     type:'GET',
     data : {msg:rawText},
     async: false,
     success:function(data){
       var botHtml = '<p class="botText"><span>드라마</span></p>'+data;
       $("#chatbox").append(botHtml);
     }
   });

 }
 function getMovie(){
 //  alert('movie');

   document
     .getElementById("userInput")
     .scrollIntoView({ block: "start", behavior: "smooth" });
   $.ajax({
     url:'/movie',
     type:'GET',
     data : {msg:rawText},
     async: false,
     success:function(data){
       var botHtml = '<p class="botText"><span>영화</span></p>'+data;
       $("#chatbox").append(botHtml);
     }
   });

 }
 function getBook(){
//    alert('book');

   document
       .getElementById("userInput")
       .scrollIntoView({ block: "start", behavior: "smooth" });
     $.ajax({
       url:'/book',
       type:'GET',
       data : {msg:rawText},
       async: false,
       success:function(data){
         var botHtml = '<p class="botText"><span>책</span></p>'+data;
         $("#chatbox").append(botHtml);
       }
     });

 }

   if(str.indexOf('드라마')>=0)
   {
     getDrama();
   }
   if(str.indexOf('영화')>=0)
   {
     getMovie();
   }
   if(str.indexOf('책')>=0)
   {
     getBook();
   }

   $("#chatbox").append('<p class="botText"><span>장르를 다시 선택하고 싶다면 <b>처음으로</b> 버튼을, <br> 키워드를 다시 입력 혹은 선택하고 싶다면 <b>뒤로가기</b> 버튼을 입력해 주세요.</span></p>');
   $("#chatbox").append('<br><button id ="back_to_first" onclick="go_back()">처음으로</button>&nbsp;&nbsp;&nbsp;<button id ="back_button" onclick="backTo()">뒤로가기</button>');
}



////////////////////// 처음으로 ///////////////////////////

goBack_cnt=0;
function go_back(){
 goBack_cnt+=1;
 genre_click = 0;
 genres = '';
 $("#chatbox").append('<p class="botText"><img src="/static/qbicc.png" alt="My Image" width="200" height="200"><span> 안녕 난 큐봇이야! 원하는 장르를 선택하고 <b>확인</b>을 눌러줘!</span><br>'+
  '<form method="POST" id="R'+goBack_cnt+'check_form" name="R'+goBack_cnt+'my_form">'+
 '<input type="checkbox" name="R'+goBack_cnt+'mycheck" value="drama_check" id = "ch1"><label for = "ch1">드라마</label>'+
 '<input type="checkbox" name="R'+goBack_cnt+'mycheck" value="movie_check" id = "ch2"><label for = "ch2">영화</label>'+
 '<input type="checkbox" name="R'+goBack_cnt+'mycheck" value="book_check" id = "ch3"><label for = "ch3">책    </label>&nbsp;'+
 '<input type="button" id="init_click" value="전체 선택" onclick="CheckAll(document.R'+goBack_cnt+'my_form.R'+goBack_cnt+'mycheck)"/>&nbsp;&nbsp;&nbsp;'+
 '<input type="button" id="init_click" value="확인" onclick="genre_get(document.R'+goBack_cnt+'my_form.R'+goBack_cnt+'mycheck)"/></form><hr></p>');

}
