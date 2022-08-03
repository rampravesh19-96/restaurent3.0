  
  let url= "/api/order_history_for_admin"
  
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
    
    con=document.createElement("div");
    con.className="container"
    for (let i = 0; i < data.length; i++) {
      let item=document.createElement("div")
      item.className="item card-body"
            
      let name=document.createElement("div")
      let description=document.createElement("div")
      let orderId=document.createElement("div")
      let price=document.createElement("div")
      let quantity=document.createElement("div")
      let time=document.createElement("div")
  
      item.append("orderid : "+data[i].order_id,orderId)
      item.append(data[i].time,time)
      item.append(data[i].name,name)
      item.append("Qty : "+data[i].product_quantity,quantity)
      item.append("Price : "+data[i].product_price,price)
      item.append(data[i].description,description)
      con.append(item)
    }
    $("#maincon").html(con)
  }
  
  var page=1

  getData([["page",page]])
 
  
  $("#showmore").click(()=>{
      getData([["page",++page]])
  
  })
  
  


  
  