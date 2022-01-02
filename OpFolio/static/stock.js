
var id = window.location.href.split("/");
id = id[id.length-1];
var stockData;
var month = ["Jan","Feb","Mär","Apr","Mai","Jun","Jul","Aug","Sep","Okt","Nov","Dez"]



//var stockData = response.data;
fetch("/stock/api/"+id,{headers: {'symbol': id}}).then(response => response.json()).then(data => useData(data)) 


function useData(stockJson){
    
    console.log(stockJson); 

    addContent("h2",stockJson["informations"]["description"]+" ("+id+")","stockNameDiv");
    addContent("p",stockJson["informations"]["exchangeName"],"stockNameDiv",null,"smallP");
    addContent("span",stockJson["informations"]["regularMarketLastPrice"],"stockPriceDiv","stockPrice");

    var gains = parseFloat(stockJson["informations"]["regularMarketNetChange"]);
    var percentGains = parseFloat(stockJson["informations"]["regularMarketPercentChangeInDouble"]).toFixed(2);
    addContent("span",gains+" ("+percentGains+"%)","stockPriceDiv","stockGains");
    if (gains < 0){
        document.getElementById("stockGains").style.color = "red"
    } else document.getElementById("stockGains").style.color = "greenyellow"

    let stockDate = new Date(parseInt(stockJson["informations"]["regularMarketTradeTimeInLong"]))
    let stockMinutes = stockDate.getMinutes();
    let stockHours = stockDate.getHours();
    if(stockDate.getMinutes() <= 9){
        stockMinutes = "0"+stockMinutes;
    }
    if(stockDate.getHours() <= 9){
        stockHours = "0"+stockHours;
    }
    
    addContent("p","Last updated "+stockHours+":"+stockMinutes+", "+stockDate.getDate()+"."+month[stockDate.getMonth()],"stockPriceDiv",null,"smallP");

    addContent("p","Volumen: "+stockJson["informations"]["totalVolume"],"stockInfoDiv");
    

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
        chart.data = dataToday;
        chart.update();
    });

    var buttonLastMonth = document.createElement("button");
    var buttonLastMonthText = document.createTextNode("Last Month");
    buttonLastMonth.append(buttonLastMonthText);
    element.appendChild(buttonLastMonth);

    buttonLastMonth.addEventListener("click", () => {
        chart.data = lastMonthData;
        chart.update();
    });

    var buttonLast6Month = document.createElement("button");
    var buttonLast6MonthText = document.createTextNode("Last 6 Month");
    buttonLast6Month.append(buttonLast6MonthText);
    element.appendChild(buttonLast6Month);

    buttonLast6Month.addEventListener("click", () => {
        chart.data = last6MonthData;
        chart.update();
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

    const labelsLast6Month = [];
    const stockLast6MonthData = [];

    stockJson["last6Month"]["candles"].forEach(candles => {
        stockLast6MonthData.push(candles["close"]);
        let date = new Date(candles["datetime"]);
        labelsLast6Month.push(date.getDate()+" "+month[date.getMonth()]);
    });
    
    const last6MonthData = {
        labels: labelsLast6Month,
        datasets: [{
            backgroundColor: 'rgb(255, 150, 69)',
            borderColor: 'rgb(255,150,69)',
            data: stockLast6MonthData,
        }]
    }
}

//Creats a html element of tpye "elementType" with the text "elementText" and binds it to "parentElement"
function addContent(elementType,elementText,parentElement,idName = null,className = null){
    var para = document.createElement(elementType);
    var node = document.createTextNode(elementText);
    para.appendChild(node);
    
    if(idName != null){
       para.id = idName;
    }
    if(className != null){
        para.classList.add("smallP");
    }

    var element = document.getElementById(parentElement);
    element.appendChild(para);
}




