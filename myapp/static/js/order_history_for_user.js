  
  let url= "/api/order_history_for_user"
  
  async function getJson(bodyData) {
    let bodyContent = new FormData();
    for (const i of bodyData) {
      bodyContent.append(i[0], i[1]);
    }
    
    body= { 
      method: "POST",
      body: bodyContent,
    }
      let response = await fetch(url,body);
      let data = await response.json()
      return data;
  }


async function getData(array) {
      let data = await getJson(array)
      let tog=data.tog
      if(tog){
        $("#showmore").css("color","#dddddd")
      }
      data=data.data
      console.log(data);
    
    con=document.createElement("div");
    con.className="container"
    for (let i = 0; i < data.length; i++) {
      let item=document.createElement("div")
      item.className="item card-body"
            
      let image=document.createElement("img")
      image.src="https://img.freepik.com/free-photo/indian-chicken-biryani-served-terracotta-bowl-with-yogurt-white-background-selective-focus_466689-72554.jpg?w=1380&t=st=1657178102~exp=1657178702~hmac=eee7e590a1a70249bf6c36e8a3e6730261dc173c7646ecb66031fb4947bfea5f"
      image.className="itemimage"
      item.append(image)
      let name=document.createElement("div")
      let description=document.createElement("div")
      let orderId=document.createElement("div")
      let price=document.createElement("div")
      let quantity=document.createElement("div")
      let time=document.createElement("div")
  
      item.append(image)
      item.append(data[i].name,name)
      item.append(data[i].description,description)
      item.append("orderid : "+data[i].order_id,orderId)
      item.append("Price : "+data[i].product_price,price)
      item.append("Qty : "+data[i].product_quantity,quantity)
      item.append(data[i].time,time)
      con.append(item)
    }
    $("#maincon").html(con)
  }
  
  var page=1

  getData([["page",page]])
 
  
  $("#showmore").click(()=>{
      getData([["page",++page]])
  
  })
  
  


  
  