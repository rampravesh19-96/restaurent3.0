$("#save").click((e)=>{
    e.preventDefault()
    let name=$("#name").val()
    let phone=$("#phone").val()
    let dob=$("#dob").val()
    let address=$("#address").val()
    let bodyContent = new FormData();
    bodyContent.append("name", name);
    bodyContent.append("phone", phone);
    bodyContent.append("dob", dob);
    bodyContent.append("address", address);
    
    fetch("/api/edit_user_profile", { 
      method: "POST",
      body: bodyContent,
    }).then(function(response) {
      return response.text();
    }).then(function(data) {
    data=JSON.parse(data)
    alert(data.message)
    })
})