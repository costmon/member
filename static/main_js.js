//마우스 이벤트 -
//마우스 올리기 - onmouseover, 마우스 내리기 - onmouseout
//addEventListener() - mouseover, mouseout 사용(on 생략)
let pic = document.getElementById("pic");
//pic.onmouseover = changePic;   //함수 호출시 괄호 생략
//pic.onmouseout = originPic;

pic.addEventListener('mouseover', changePic);
pic.addEventListener('mouseout', originPic);

function changePic(){
    pic.src = '../static/coffee-blue.jpg';
}
function originPic(){
    pic.src = '../static/coffee-gray.jpg';
}
