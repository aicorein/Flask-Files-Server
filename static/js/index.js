window.addEventListener('DOMContentLoaded', function () {
  // 两个浮动面板
  var flashTablet = document.querySelector('.flash-tablet');
  var body = document.body;
  var tableHeight = document.querySelector('.files-table').offsetTop;
  var toTopBtn = document.querySelector('#to-top');

  window.addEventListener('scroll', function () {
    if (window.pageYOffset > tableHeight) {
      flashTablet.style.display = 'block';
    }
    else {
      flashTablet.style.display = 'none';
    }
  })

  toTopBtn.addEventListener('click', function () {
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    })
  })

  // 点击驱动器标号或点击文件夹触发更新
  var driverLinks = document.querySelectorAll('.drivers-container a');
  var pathCon = document.querySelector('#pathForm input[type="text"]');
  var SubmitBtn = document.querySelector('#pathForm input[type="submit"]')

  for (let i = 0; i < driverLinks.length; i++) {
    driverLinks[i].addEventListener('click', function (e) {
      e.preventDefault();
      pathCon.value = driverLinks[i].getAttribute('location');
      SubmitBtn.click();
    })
  }

  var dirLinks = document.querySelectorAll('.dir a');
  var curPathCons = document.querySelectorAll('.currentPath span');

  for (let i = 0; i < dirLinks.length; i++) {
    dirLinks[i].addEventListener('click', function (e) {
      e.preventDefault();
      var pathText = curPathCons[0].innerHTML;

      if (pathText[pathText.length - 1] == '/') { }
      else {
        pathText += '/';
      }
      pathCon.value = pathText + this.getAttribute('dirname');
      SubmitBtn.click();
    })
  }

  // 判断当前路径，根目录下“返回上级”按钮要禁用
  var tolastBtns = document.querySelectorAll('.to-lastPath');

  if (curPathCons[0].innerHTML.length <= 3) {
    for (let i = 0; i < tolastBtns.length; i++) {
      tolastBtns[i].style.cssText = 'background-color: gray;' +
        'background-image: linear-gradient(135deg, rgb(198 207 212) 0%, rgb(172, 173, 195) 100%);' +
        'color: #747474;';
      tolastBtns[i].disabled = 'disabled';
    }
  }
  else { }
})
