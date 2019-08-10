function getCurrentISOtime(){
  Date.prototype.toIsoString = function() {
    var tzo = -this.getTimezoneOffset(),
        dif = tzo >= 0 ? '+' : '-',
        pad = function(num) {
            var norm = Math.floor(Math.abs(num));
            return (norm < 10 ? '0' : '') + norm;
        };
    return this.getFullYear() +
        '-' + pad(this.getMonth() + 1) +
        '-' + pad(this.getDate()) +
        'T' + pad(this.getHours()) +
        ':' + pad(this.getMinutes()) +
        ':' + pad(this.getSeconds()) +
        dif + pad(tzo / 60) +
        ':' + pad(tzo % 60);
  }

  var dt = new Date();
  return dt.toIsoString()

}

function showRadius(){
    const value = document.getElementById("radius").value;
    document.getElementById("show-radius").innerText = value;
}

function addZero(i) {
    if (i < 10) {
      i = "0" + i;
    }
    return i;
  }
function like(event,user_id,restaurant_id,recommendation_time){

  const local_time = getCurrentISOtime()
  var url = `http://localhost:8000/feedback:senior+${user_id}+${local_time}+${restaurant_id}+${recommendation_time}+1`

  fetch(url,{mode: 'cors',headers:{'Access-Control-Allow-Origin':'*' }})
    .then(function(response){
    })
    .catch(error => console.log('Error:', error));
}
function disLike(event,user_id,restaurant_id,recommendation_time){
  const local_time = getCurrentISOtime()
  var url = `http://localhost:8000/feedback:senior+${user_id}+${local_time}+${restaurant_id}+${recommendation_time}+-0.1`

  fetch(url,{method:"GET",mode:'cors',headers:{'Access-Control-Allow-Origin':'*' }})
    .then(function(response){
    })
    .catch(error => console.log('Error:', error));
}

function updateElement(node,index,info){
  const user_id = document.getElementById("user_id").value;

  node.setAttribute("value",info.id)
  node.setAttribute("class","recommendation-result");
  node.setAttribute("id","recommendation_num_"+index);
  node.setAttribute("recommendation_time",info.recommendation_time);
  
  category = info.categories.map(x=>x["title"]).join("・");
  distance = Math.round(info.distance)
  text = `<span style='font-size:1.025em'>${info.name}&nbsp</span><span style='font-size:0.75em'>(${distance} m)</span><br>\
          <span style='font-size:1em'>${info.rating}🌟・${info.review_count} reviews・${info.price}</span><br>\
          <span style='font-size:0.75em'>${category}</span><br>\
          <span style='font-size:1em'>${info.location}</span><br>\
          <span style='margin-left:12%'><button name="call">Call</button><button name="go">Go</button><button name="dislike">No interest</button></span>`
  node.innerHTML = text;
  const call = document.querySelector(`#recommendation_num_${index} button[name="call"] `);
  const go = document.querySelector(`#recommendation_num_${index} button[name="go"] `);
  const dislike = document.querySelector(`#recommendation_num_${index} button[name="dislike"]`);
  call.addEventListener("click",(event)=>{like(event,user_id,info.id,info.recommendation_time)})
  go.addEventListener("click",(event)=>{like(event,user_id,info.id,info.recommendation_time)})
  dislike.addEventListener("click",(event)=>{disLike(event,user_id,info.id,info.recommendation_time)})
  
  return node
  
}


function getRecommendation(){
    const user_id = document.getElementById("user_id").value;
    const longitude = document.getElementById("longitude").value;
    const latitude = document.getElementById("latitude").value;
    const radius = document.getElementById("radius").value;
    const price = document.getElementById("price").value;

    const local_time = getCurrentISOtime()

    var url = `http://localhost:8000/getRecommendation:senior+${user_id}+${local_time}+${longitude}+${latitude}+${radius}+${price}`

    fetch(url,{method:"GET"})
      .then(function(response){
        console.log(response)
        if(response.status >= 200 && response.status < 300) {
          return response.json();
        }
        else{
          throw new Error('Fail to post questions');
        }
      })
      .then(function(data){
        console.log(data)
        data = data["success"]
        const root = document.getElementById("recommendation-box");
        for (let i=0;i<3;i++){
          node = document.getElementById("recommendation_num_"+i);
          if (!node){
            node = document.createElement("div")
            root.appendChild(node);
            // node.addEventListener("click",)
          }
          updateElement(node,i,data[i]);
        }

      })
      .catch(error => console.log('Error:', error));

}

function main() {
    showRadius();
    const radiusInput = document.getElementById("radius");
    radiusInput.addEventListener("click",showRadius);
    const recommendation = document.getElementById("recommend");
    recommendation.addEventListener("click",getRecommendation);
  }
  
  document.addEventListener("DOMContentLoaded", main);