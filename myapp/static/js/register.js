const dateIsValid=(dateStr)=> {
    const regex = /^\d{4}-\d{2}-\d{2}$/;
  
    if (dateStr.match(regex) === null) {
      return false;
    }
  
    const date = new Date(dateStr);
  
    const timestamp = date.getTime();
  
    if (typeof timestamp !== 'number' || Number.isNaN(timestamp)) {
      return false;
    }
  
    return date.toISOString().startsWith(dateStr);
  }






const register=(email,password,confirmPassword,name,dob,phone,address)=>{

    let headersList = {}
    
    let bodyContent = new FormData();
    bodyContent.append("email", email);
    bodyContent.append("password", password);
    bodyContent.append("confirmPassword", confirmPassword);
    bodyContent.append("name", name);
    bodyContent.append("dob", dob);
    bodyContent.append("phone", phone);
    bodyContent.append("address", address);
    
    fetch("/api/register", { 
      method: "POST",
      body: bodyContent,
      headers: headersList
    }).then((response)=> {
      return response.text();
    }).then((data)=> {
        let jsonData=JSON.parse(data)
        console.log(jsonData);
      if(jsonData.status==='success'){
        alert(jsonData.message)
        document.location.href=jsonData.data.url
      }else{
        alert(jsonData.message)
      }
    })
    }






$('#registerform').submit((e)=> {
    e.preventDefault()
    emailRegexp = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    var email = $("#email").val();
    var password = $("#password").val();
    var confirmPassword = $("#confirmPassword").val();
    var name = $("#name").val();
    var dob = $("#dob").val();
    var phone = $("#phone").val();
    var address = $("#address").val();

    if(!email || !password || !confirmPassword || !name || !dob || !phone || !address)
    {
        alert("All fields are required")
    }
    else if(!emailRegexp.test(email))
    {
        alert("Invalid email")
    }
    else if(!phone.length===10 && !/^\d+$/.test(phone)){
        alert("Invalid phone number")
    }
    else if(!dateIsValid(dob)){
        alert("Enter date of birth")
    }
    else if(address.length<25 || address.length>500){
        alert("Address must be between 15 to 500 characters")
    }
    else if(password !==confirmPassword){
        console.log("Pasword did not match");
    }
    else
    {
        register(email,password,confirmPassword,name,dob,phone,address)
    }

})


