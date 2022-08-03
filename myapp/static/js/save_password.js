const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const token = urlParams.get('token')
// function parseJwt (token) {
//   var base64Url = token.split('.')[1];
//   var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
//   var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
//       return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
//   }).join(''));

//   return JSON.parse(jsonPayload);
// }
// id=parseJwt(token).id

const savePassword=(otp,password,confirmPassword)=>{

    let headersList = {}
    
    let bodyContent = new FormData();
    bodyContent.append("otp", otp);
    bodyContent.append("password", password);
    bodyContent.append("confirmPassword", confirmPassword);
    bodyContent.append("token", token);
    fetch("/api/save_password",{ 
      method: "POST",
      body: bodyContent,
      headers: headersList
    }).then((response)=> {
      return response.text();
    }).then((data)=> {
        let jsonData=JSON.parse(data)
      if(jsonData.status==='success'){
        alert("Password reset sucessfully")
        document.location.href=jsonData.data.url
      }else{
        alert(jsonData.message)
      }
    })
    }

    $("#savepassform").submit((e)=> {
    e.preventDefault()
    regexp = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    var otp = $("#otp").val();
    var password = $("#password").val();
    var confirmPassword = $("#confirmPassword").val();
    if(password!==confirmPassword)
    {
        alert("Password didn't match")
    }
    else
    {
        savePassword(otp,password,confirmPassword)
    }

})


