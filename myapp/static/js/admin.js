let apiUrlViewlist = "/api/view_item_list"
let apiUrlCartData = "/api/get_cart_data"

async function getJson(url,bodyData=[]) {
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
async function getData(array=[]) {
  let jsondata = await getJson(apiUrlViewlist,array)
if(jsondata.tog){
  $("#showmore").css("color","#dddddd")
}
  if(jsondata.tog){
    $("#showmore").css("color","#dddddd")
  }
  if (jsondata.status==="success"){
    let jsonData=jsondata.data
    var tt=document.createElement("div")
    tt.id="connn"

    for (const i in jsonData) {
      let item=document.createElement("div")
      item.className="item"
      
      
      let name=document.createElement("input")
      name.className="name"
      name.id="name"+jsonData[i].pk

      let description=document.createElement("input")
      description.className="description"
      description.id="description"+jsonData[i].pk

      let price=document.createElement("input")
      price.className="price"
      price.id="price"+jsonData[i].pk
      

      let availableQty=document.createElement("input")
      availableQty.className="availableQty"
      availableQty.id="availableQty"+jsonData[i].pk

      saveBtn=document.createElement("button")
      saveBtn.append("Save")
      saveBtn.className="btn btn-sm btn-success m-3 mb-0 mt-0"
      saveBtn.id=jsonData[i].pk
      saveBtn.setAttribute('onclick', 'Save(this.id)');

      deleteBtn=document.createElement("button")
      deleteBtn.append("Delete")
      deleteBtn.className="btn btn-sm btn-danger"

      deleteBtn.id=jsonData[i].pk
      deleteBtn.setAttribute('onclick', 'Delete(this.id)')

      name.value=jsonData[i].fields.name
      item.append(name)

      price.value=jsonData[i].fields.price
      item.append(price)
      
      description.value=jsonData[i].fields.description
      item.append(description)

      availableQty.value=jsonData[i].fields.available_quantity
      item.append(availableQty)

      btncon=document.createElement("div")
      btncon.append(saveBtn)

      item.append(btncon)
      tt.append(item)
    }
    $("#container").html(tt)
  }else{
    alert(jsondata.message)
  }


}
var noOfProductPerPage=14
var type="default"
getData([["no_of_product_per_page", noOfProductPerPage]])

$("#searchform").submit((e)=>{
  e.preventDefault()
  $("#showmore").css("color","#0d6efd")
  type="query"
  array=[["query",$("#query").val()],["max_price",$("#max").val()],["min_price",$("#min").val()],["no_of_product_per_page", noOfProductPerPage]]
  getData(array);
})

$("#sortsubmit").submit((e)=>{
  e.preventDefault()
  $("#showmore").css("color","#0d6efd")
  type="sort"
  array=[["query",$("#query").val()],["max_price",$("#max").val()],["min_price",$("#min").val()],["no_of_product_per_page", noOfProductPerPage]]
  getData(array);
})

var defaultpage=1
var querypage=1
var sortpage=1
$("#showmore").click(()=>{
  if(type==="query"){
    array=[["query",$("#query").val()],["page",++querypage],["no_of_product_per_page", noOfProductPerPage]]
    getData(array)
  }
  else if(type==="sort"){
    array=[["max_price",$("#max").val()],["min_price",$("#min").val()],["page",++sortpage],["no_of_product_per_page", noOfProductPerPage]]
    getData(array)
  }else{
    getData([["page",++defaultpage],["no_of_product_per_page", noOfProductPerPage]])
  }

})


function Save(a){
  let bodyContent = new FormData();
bodyContent.append("product_id", a);
bodyContent.append("name", $("#name"+a).val());
bodyContent.append("price", $("#price"+a).val());
bodyContent.append("description", $("#description"+a).val());
bodyContent.append("available_quantity",$("#availableQty"+a).val());

fetch("/api/edit_item", { 
  method: "POST",
  body: bodyContent,
}).then(function(response) {
  return response.text();
}).then(function(data) {
  data=JSON.parse(data)
  alert(data.message)
})
}

$("#logoutbtn").click(()=>{
  fetch("/api/logout", { 
  method: "POST",
}).then(function(response) {
  return response.text();
}).then(function(data) {
  data=JSON.parse(data)
  if(data.status==="success"){
    window.location.href="/login"
  }else{
    alert(data.message)
  }
})
})


$("#createItemform").submit((e)=>{
  e.preventDefault()
  
  let name=$("#name").val()
  let price=$("#price").val()
  let description=$("#description").val()
  let availableQty=$("#availableQty").val()
 

  let bodyContent = new FormData();
bodyContent.append("name", name);
bodyContent.append("description", description);
bodyContent.append("price", price);
bodyContent.append("available_quantity", availableQty);


fetch("/api/create_item", { 
  method: "POST",
  body: bodyContent,
}).then(function(response) {
  return response.text();
}).then(function(data) {
  data=JSON.parse(data)
  console.log(data);
  alert(data.message)
})
})