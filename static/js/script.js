$(document).ready(function() {

})



function addToList(id){
	$('#addBtn' + id).hide();
	// add to the cart
	$('#pill_products_container').append(`
			<div id="pill_product${id}" class="row pill_product">
				<div class="col-5" id="cartProName${id}">${ document.querySelector('#name'+id).textContent }</div>
				<div class="col-3">
					<input type=number" class="ids" id="cartProId${id}" value="${id}" hidden>
					<input type="number" id="cartProPrice${id}" value="${ document.querySelector('#price'+id).textContent }" min="0" name="">
				</div>
				<div class="col-2">
					<input type="number" id="cartProMount${id}" value="0" min="0" name="">
				</div>
				<div class="col-2">
					<button onclick="removeFromList(${id})" class="bill_button">X</button>
				</div>
			</div>
		`)
}

function removeFromList(id){
	$('#addBtn'+id).show()
	$('#pill_product'+id).remove()
}

function doTheDeal(){
	let arr =[];
	let data = [{name: document.querySelector("#orderOwner").value}]
	if (data[0].name == "") {
		$('#orderOwner').css({'border':"solid red 2px"})
		return;
	}
	// collect the ids
	idsInputs = document.querySelectorAll(".ids");
	for(i = 0; i < idsInputs.length; i++){
		data.push(convertToJson(Number(idsInputs[i].value)))
	}
	// console.log(data)
	var retData;
	$.ajax("/dothedeal",
		{
			type: "POST",
			data: JSON.stringify(data),
			contentType: 'application/json',
			dataType: 'json',
			success: function(data) {
				if (data.success == true) {
					location.href = '/waiting'
				}
			}
		}
	);

}

function convertToJson(id){
	temp =  {
		id: id,
		name: (document.querySelector("#cartProName"+id).textContent),
		price: Number(document.querySelector("#cartProPrice"+id).value) ,
		mount: Number(document.querySelector("#cartProMount"+id).value)
	}
	return temp
}

function deleteProduct(id){
	location.href = '/deleteproduct/' + id;
}

function deleteCut(id){
	location.href = '/deletecut/' + id;
}

function deletePill(id){
	location.href = '/deletepill/' + id;
}
function showpill(id){
	location.href = '/showpill/' + id;
}
function pillPaid(id){
	location.href = '/pillpaid/' + id;
}

function retValId(str, id){
	return Number(document.querySelector("#"+ str + id).value)
}
function updatePill(pillId){
	let idsInputs = document.querySelectorAll("#productid");
	let ids = []
	let data = [{pillid: pillId}]

	for(let i = 0; i < idsInputs.length; i++){
		// ids.push(Number(idsInputs[i].value));
		let id = Number(idsInputs[i].value);
		data.push({id: id, mount: retValId("productmount", id), price: retValId("productprice", id)})
	}

	var retData;
	$.ajax("/updatepill",
		{
			type: "POST",
			data: JSON.stringify(data),
			contentType: 'application/json',
			dataType: 'json',
			success: function(data) {
				if (data.success == true) {
					location.href = '/waiting'
				}
			}
		}
	);

}