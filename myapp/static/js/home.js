let apiUrlViewlist = '/api/view_item_list';
let apiUrlCartData = '/api/get_cart_data';
console.log('test....', apiUrlViewlist, apiUrlCartData)

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
console.log(jsondata);
  if(jsondata.tog){
    $("#showmore").css("color","#dddddd")
  }
  if (jsondata.status==="success"){
    let jsonData=jsondata.data
    var tt=document.createElement("div")
    tt.id="connn"

    for (const i in jsonData) {
      let item=document.createElement("div")
      item.className="item card-body"
      item.id=jsonData[i].pk
      item.setAttribute('onclick', 'my_function(this.id)');
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

      name.append(jsonData[i].fields.name)
      item.append(name)

      price.append(jsonData[i].fields.price)
      item.append(price)
      
      description.append(jsonData[i].fields.description)
      item.append(description)

      tt.append(item)
    }
    $("#container").html(tt)
  }else{
    alert(jsondata.message)
  }


}

async function getCartData() {
  let jsonCartData = await getJson(apiUrlCartData)
  noOfItem=jsonCartData.data.no_of_item;
  $(".badge").html(noOfItem)
}
getCartData()







var type="default"
getData()

$("#searchform").submit((e)=>{
  e.preventDefault()
  $("#showmore").css("color","#0d6efd")
  type="query"
  array=[["query",$("#query").val()],["max_price",$("#max").val()],["min_price",$("#min").val()]]
  getData(array);
})

$("#sortsubmit").submit((e)=>{
  e.preventDefault()
  $("#showmore").css("color","#0d6efd")
  type="sort"
  array=[["query",$("#query").val()],["max_price",$("#max").val()],["min_price",$("#min").val()]]
  getData(array);
})

var defaultpage=1
var querypage=1
var sortpage=1
$("#showmore").click(()=>{
  if(type==="query"){
    array=[["query",$("#query").val()],["page",++querypage]]
    getData(array)
  }
  else if(type==="sort"){
    array=[["max_price",$("#max").val()],["min_price",$("#min").val()],["page",++sortpage]]
    getData(array)
  }else{
    getData([["page",++defaultpage]])
  }

})


function my_function(a){
  window.location.href="/viewitem/?id="+a
}


$("#cartbtn").click(()=>{
  window.location.href="/checkout"
})
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

