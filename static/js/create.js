/*添加食材*/
function show() {
  var newing = document.getElementById("a1").value
  var show = document.getElementById("show")
  var content = show.value
  if(content == null || content.length == 0)  
  {  
      show.value = newing
      show.innerHTML =  show.value;
  }
  else {
      show.value = show.value +","+ newing
      show.innerHTML = show.value;
  }
  document.getElementById("a1").value = ""
}

/*下拉菜单*/

var  myselect=document.getElementById("test");
var index=myselect.selectedIndex ; 
myselect.options[index].value;
myselect.options[index].text;


/*上传图片*/
function getImgsByFileReader(el, files) {
  for (var i = 0; i < files.length; i++) {
    let img = document.createElement('img')
    img.setAttribute('style', 'width: 40px; height: 40px; vertical-align: middle; margin-right: 5px;')
    el.appendChild(img)
    var reader = new FileReader()
    reader.onload = function (e) {
      img.src = e.target.result
    }
    reader.readAsDataURL(files[i])
  }
}
function showImg(obj) {
  var files = obj.files
  // document.getElementById("imgContainer").innerHTML = getImgsByUrl(files)
  getImgsByFileReader(document.getElementById("imgContainer"), files)
}
// 使用window.URL.createObjectURL(file)读取file实例并显示图片
function getImgsByUrl(files) {
  var elements = ''
  for (var i = 0; i < files.length; i++) {
    var url = window.URL.createObjectURL(files[i])
    elements += "<img src='" + url + "' style='width: 40px; height: 40px; vertical-align: middle; margin-right: 5px;' />"
  }
  return elements
}