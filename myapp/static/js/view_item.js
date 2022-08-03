const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const productId = urlParams.get('id')


let baseUrl = "/api/"
// const bodyData=[["product_id",productId]]
async function hitApi(endpoint,bodyData=[]) {
  let bodyContent = new FormData();
  for (const i of bodyData) {
    bodyContent.append(i[0], i[1]);
  }
  body= { 
    method: "POST",
    body: bodyContent,
  }
    const url=baseUrl+endpoint
    let response = await fetch(url,body);
    let data = await response.json()
    return data;
}

async function getData() {
    let jsondata = await hitApi("view_item",[["product_id",productId]])
    let jsonData=jsondata.data[0].fields
    if (jsondata.status==="success"){
    $(".name").html(jsonData.name)
    $(".price").html(jsonData.price)
    $(".avlqty").html(jsonData.available_quantity)
    $(".description").html(jsonData.description)
    $(".selectQty").attr("max",jsonData.available_quantity)
    $("#availableQty").val(jsonData.available_quantity)    
    return jsonData.available_quantity 
    }else{
      alert(jsondata.message)
    }

}
getData()



$("#addToCart").click(()=>{
  let availableQty=$("#availableQty").val()
  let productQty=$(".selectQty").val()
  if(!/^\d+$/.test(productQty)){
    alert("Product quantity must be number")
  }
  else if(parseInt(productQty)>parseInt(availableQty)){
    alert("Quantity can't be more than available quantity")
  }else{
    let bodyContent = new FormData();
    bodyContent.append("product_id", productId);
    bodyContent.append("product_quantity", productQty);
  
  fetch(baseUrl+"add_to_cart", { 
    method: "POST",
    body: bodyContent,
  }).then(function(response) {
    return response.text();
  }).then(function(data) {
    data=JSON.parse(data)
    if(data.status==="success"){
      alert(data.message)
      window.location.href="/"
    }else{
      alert(data.message)
    }
  })
  }
})

