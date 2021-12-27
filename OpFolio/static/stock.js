
var id = window.location.href.split("/");
id = id[id.length-1];
var stockData;
var month = ["Jan","Feb","Mär","Apr","Mai","Jun","Jul","Aug","Sep","Okt","Nov","Dez"]



//var stockData = response.data;
fetch("/stock/api/"+id,{headers: {'symbol': id}}).then(response => response.json()).then(data => useData(data)) 


function useData(stockJson){
    console.log(stockJson); 
    var para = document.createElement("p");
    var node = document.createTextNode(stockJson["informations"]["description"]);
    para.appendChild(node);
    var element = document.getElementById("mainDiv");
    element.appendChild(para);

    para = document.createElement("p");
    node = document.createTextNode(stockJson["informations"]["regularMarketLastPrice"]);
    para.appendChild(node);
    element = document.getElementById("mainDiv");
    element.appendChild(para);

    para = document.createElement("p");
    var gains = parseFloat(parseFloat(stockJson["informations"]["regularMarketLastPrice"]) - parseFloat(stockJson["lastMonth"]["candles"][stockJson["lastMonth"]["candles"].length-2]["close"])).toFixed(2)
    node = document.createTextNode(gains);
    para.appendChild(node);
    element = document.getElementById("mainDiv");
    element.appendChild(para);


    const labelsLastMonth = [];
    const labelsToday = []

    const stockTodayData = []
    stockJson["today"]["candles"].forEach(candles => {
        stockTodayData.push(candles["close"]);
        let date = new Date(candles["datetime"]);
        labelsToday.push(date.getHours()+":"+date.getMinutes());
    });

    const dataToday = {
        labels: labelsToday,
        datasets: [{
          backgroundColor: 'rgb(255, 150, 69)',
          borderColor: 'rgb(255, 150, 69)',
          data: stockTodayData,
        }]
    };
    
    const configToday = {
        type: 'line',
        data: dataToday,
        options:  {
            plugins: {
                legend: {
                    display: false
                }
            },
            radius : 0,
            interaction: {
                intersect: false,
                axis : 'x',
                mode : 'nearest',
              },
        }
    };

    const chart = new Chart(
    document.getElementById('todayChart'),
    configToday
    );

    var buttonToday = document.createElement("button");
    var buttonTodayText = document.createTextNode("Today");
    buttonToday.append(buttonTodayText);
    element = document.getElementById("chartDiv");
    element.appendChild(buttonToday);

    buttonToday.addEventListener("click", () => {
        chart.data = dataToday
        chart.update()
    });

    var buttonLastMonth = document.createElement("button");
    var buttonLastMonthText = document.createTextNode("Last Month");
    buttonLastMonth.append(buttonLastMonthText);
    element.appendChild(buttonLastMonth);

    buttonLastMonth.addEventListener("click", () => {
        chart.data = lastMonthData
        chart.update()
    });

    


    const stockLastMonthData = []
    stockJson["lastMonth"]["candles"].forEach(candles => {
        stockLastMonthData.push(candles["close"]);
        let date = new Date(candles["datetime"]);
        labelsLastMonth.push(date.getDate()+" "+month[date.getMonth()]);
    });

    const lastMonthData = {
        labels: labelsLastMonth,
        datasets: [{
          backgroundColor: 'rgb(255, 150, 69)',
          borderColor: 'rgb(255, 150, 69)',
          data: stockLastMonthData,
        }]
    };
}




