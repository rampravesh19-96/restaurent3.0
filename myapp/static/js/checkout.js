async function getJson(url) {
 
    body= { 
      method: "POST",
    }
      let response = await fetch(url,body);
      let data = await response.json()
      return data;
  }

  async function getData() {
    let jsondata = await getJson("/api/checkout")
    console.log(jsondata);

    if (jsondata.status==="success"){
      if(jsondata.data.length===0){
        $("#placeOrder").css("display","none")
        $("#totalamt").css("display","none")
        $(".emptyCart").css("display","flex")
      }
      $("#totalamt").html("Total amount : "+jsondata.total)
        noOfPage=jsondata.no_of_page
        let jsonData=jsondata.data
        var tt=document.createElement("div")
        tt.id="connn"
        for (const i in jsonData) {
          let item=document.createElement("div")
          item.className="item card-body"
          
          let image=document.createElement("img")
          image.src="https://img.freepik.com/free-photo/indian-chicken-biryani-served-terracotta-bowl-with-yogurt-white-background-selective-focus_466689-72554.jpg?w=1380&t=st=1657178102~exp=1657178702~hmac=eee7e590a1a70249bf6c36e8a3e6730261dc173c7646ecb66031fb4947bfea5f"
          image.className="itemimage"
          item.append(image)
    
          let name=document.createElement("div")
          name.className="name card-title"
    
          let description=document.createElement("div")
          description.className="description card-text"
    
          let price=document.createElement("div")
          price.className="price"

          let quantity=document.createElement("div")
          quantity.className="quantity"

          let removebtn=document.createElement("button")
          removebtn.id=jsonData[i].pk
          removebtn.className="btn btn-sm btn-danger"
          removebtn.setAttribute('onclick', 'removeFromcart(this.id)');
          

          name.append(jsonData[i].fields.name)
          item.append(name)
    
          price.append(jsonData[i].fields.price)
          item.append(price)
          
          description.append(jsonData[i].fields.description)
          item.append(description)
          quantity.append(" Quantity : "+jsonData[i].fields.quantity)

          item.append(quantity)

          removebtn.append("Remove")
          item.append(removebtn)
          tt.append(item)
        }
        $("#container").html(tt)

      }else{
        alert(jsondata.message)
      }
  }
  getData()

  const removeFromcart=(a)=>{
    let bodyContent = new FormData();
    bodyContent.append("product_id", a);

fetch("/api/remove_from_cart", { 
  method: "POST",
  body: bodyContent,
}).then(function(response) {
  return response.text();
}).then(function(data) {
  data=JSON.parse(data)
  console.log(data);
  if(data.data===null){
    $("#placeOrder").css("display","none")
    $("#totalamt").css("display","none")
    $(".emptyCart").css("display","flex")
  }
})
location.reload()
  }

$("#placeOrder").click(()=>{
  
  let bodyContent = new FormData();
  bodyContent.append("a", "");
  
  fetch("/api/create_order", { 
    method: "POST",
    body: bodyContent,
  }).then(function(response) {
    return response.text();
  }).then(function(data) {
    data=JSON.parse(data)
    console.log(data);
    if(data.status!=="success"){
      alert(data.message)
    }else{
      alert("Order placed successfully")
    }

  })
})