
var id = window.location.href.split("/");
id = id[id.length-1];
var stockData;



//var stockData = response.data;
fetch("/stock/api/"+id,{headers: {'symbol': id}}).then(response => response.json()).then(data => useData(data)) 


function useData(stockJson){
    console.log(stockJson); 
    var para = document.createElement("p");
    var node = document.createTextNode(stockJson["info"]["description"]);
    para.appendChild(node);
    var element = document.getElementById("mainDiv");
    element.appendChild(para);

    para = document.createElement("p");
    node = document.createTextNode(stockJson["quotes"]["regularMarketLastPrice"]);
    para.appendChild(node);
    element = document.getElementById("mainDiv");
    element.appendChild(para);

    para = document.createElement("p");
    var gains = parseFloat(parseFloat(stockJson["quotes"]["regularMarketLastPrice"]) - parseFloat(stockJson["lastMonth"]["candles"][stockJson["lastMonth"]["candles"].length-2]["close"])).toFixed(2)
    node = document.createTextNode(gains);
    para.appendChild(node);
    element = document.getElementById("mainDiv");
    element.appendChild(para);


    const labels = [];

    const stockLastMonthData = []
    stockJson["lastMonth"]["candles"].forEach(candles => {
        stockLastMonthData.push(candles["close"]);
        let date = new Date(candles["datetime"]);
        labels.push(date.toDateString());
    })
    
    console.log(stockLastMonthData)
    
    
    
    const data = {
        labels: labels,
        datasets: [{
          backgroundColor: 'rgb(255, 150, 69)',
          borderColor: 'rgb(255, 150, 69)',
          data: stockLastMonthData,
        }]
    };
    
    const config = {
        type: 'line',
        data: data,
        options:  {
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    };

    const myChart = new Chart(
    document.getElementById('myChart'),
    config
  );
}




