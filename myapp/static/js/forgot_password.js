const forgotPassword=(email)=>{

    let headersList = {}
    
    let bodyContent = new FormData();
    bodyContent.append("email", email);
    fetch("/api/forgot_password", { 
      method: "POST",
      body: bodyContent,
      headers: headersList
    }).then((response)=> {
      return response.text();
    }).then((data)=> {
        let jsonData=JSON.parse(data)
      if(jsonData.status=='success'){
        alert("otp sent")
        document.location.href=jsonData.data.url
        
      }else{
        alert(jsonData.message)
      }
    })
    }

    $("#forgotpassform").submit((e)=> {
        e.preventDefault();
    regexp = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    var email = $("#email").val();
    if(!email)
    {
        alert("Email is required")
    }
    else if(!regexp.test(email))
    {
        alert("Invalid email")
    }
    else
    {
        forgotPassword(email)
    }

})


