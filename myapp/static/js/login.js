const login=(email,password)=>{

    let headersList = {}
    
    let bodyContent = new FormData();
    bodyContent.append("email", email);
    bodyContent.append("password", password);
    fetch("/api/login", { 
      method: "POST",
      body: bodyContent,
      headers: headersList
    }).then((response)=> {
      return response.text();
    }).then((data)=> {
        let jsonData=JSON.parse(data)
        console.log(jsonData);
      if(jsonData.status==='success'){
        document.location.href=jsonData.data.url
      }else{
        alert(jsonData.message)
      }
    })
    }

    $("#loginform").submit((e)=> {
    e.preventDefault()
    regexp = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    var email = $("#email").val();
    var password = $("#password").val();
    if(!email || !password)
    {
        alert("All fields are required")
    }
    else if(!regexp.test(email))
    {
        alert("Invalid email")
    }
    else
    {
        login(email,password)
    }

})


