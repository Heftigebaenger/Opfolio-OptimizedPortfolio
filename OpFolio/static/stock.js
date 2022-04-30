
var id = window.location.href.split("/");
id = id[id.length-1];
var stockData;
var month = ["Jan","Feb","Mär","Apr","Mai","Jun","Jul","Aug","Sep","Okt","Nov","Dez"]



//var stockData = response.data;
fetch("/stock/api/"+id,{headers: {'symbol': id}}).then(response => response.json()).then(data => useData(data)) 


function useData(stockJson){
    
    console.log(stockJson); 
    // Add textual content to Html
    
    // Add name
    addContent("h2",stockJson["informations"]["description"]+" ("+id+")","stockNameDiv");
    // Add exchange eame
    addContent("p",stockJson["informations"]["exchangeName"],"stockNameDiv",null,"smallP");
    // Add last price
    addContent("span",stockJson["informations"]["regularMarketLastPrice"],"stockPriceDiv","stockPrice");
    // Add total difference 
    var gains = parseFloat(stockJson["informations"]["regularMarketNetChange"]);
    var percentGains = parseFloat(stockJson["informations"]["regularMarketPercentChangeInDouble"]).toFixed(2);
    // Add diff in %
    addContent("span",gains+" ("+percentGains+"%)","stockPriceDiv","stockGains");
    // Styles color difference grenn if > 0 else red

    if (gains < 0){
        document.getElementById("stockGains").style.color = "red"
    } else document.getElementById("stockGains").style.color = "greenyellow"

    // Add last update
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

    placeHolderDiv = document.createElement("div");

    // Add volume
    addInfoContent("Volumen",stockJson["informations"]["totalVolume"]);
    // Add bid price
    let bidPrice = stockJson["informations"]["bidPrice"];
    addInfoContent("Gebot",bidPrice);
    // Add ask price
    let askPrice = stockJson["informations"]["askPrice"];
    addInfoContent("Briefkurs",askPrice);
    // Add spread (Spread = ask-bid ?)
    let spread = parseFloat(askPrice - bidPrice).toFixed(2);
    addInfoContent("Spread",spread);
    // Add Yesterday close
    let yesterdayClose = stockJson["lastMonth"]["candles"][stockJson["lastMonth"]["candles"].length-2]["close"];
    console.log(yesterdayClose);
    addInfoContent("Schluss Vortag", yesterdayClose);
    // Add today open
    let todayOpen = stockJson["informations"]["openPrice"]
    addInfoContent("Eröffnung", todayOpen);
    // Add today high / low
    let todaySpan = "" + stockJson["informations"]["lowPrice"]+ " - " + stockJson["informations"]["highPrice"];
    addInfoContent("Tagesspanne",todaySpan);

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

    var buttonLastYear = document.createElement("button");
    var buttonLastYearText = document.createTextNode("Last Year");
    buttonLastYear.append(buttonLastYearText);
    element.appendChild(buttonLastYear);

    buttonLastYear.addEventListener("click", () => {
        chart.data = lastYearData;
        chart.update();
    });

    var buttonLast5Years = document.createElement("button");
    var buttonLast5YearsText = document.createTextNode("Last 5 Year");
    buttonLast5Years.append(buttonLast5YearsText);
    element.appendChild(buttonLast5Years);

    buttonLast5Years.addEventListener("click", () => {
        chart.data = last5YearsData;
        chart.update();
    });
    

    ////////////////////////////
    //Last Month Chart settings
    ////////////////////////////

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

    ////////////////////////////
    //Last 6 Month Chart settings
    ////////////////////////////

    //Create variables for settings
    const labelsLast6Month = [];
    const stockLast6MonthData = [];

    //Add Data from stockJson to the Labes / Data array
    stockJson["last6Month"]["candles"].forEach(candles => {
        stockLast6MonthData.push(candles["close"]);
        let date = new Date(candles["datetime"]);
        labelsLast6Month.push(date.getDate()+" "+month[date.getMonth()]);
    });
    
    //Finished settings
    const last6MonthData = {
        labels: labelsLast6Month,
        datasets: [{
            backgroundColor: 'rgb(255, 150, 69)',
            borderColor: 'rgb(255,150,69)',
            data: stockLast6MonthData,
        }]
    }
    
    ////////////////////////////
    //Last Year Chart settings
    ////////////////////////////

    //Create variables for settings
    const labelsLastYear = [];
    const stockLastYearData = [];

    //Add Data from stockJson to the Labes / Data array
    stockJson["lastYear"]["candles"].forEach(candles => {
        stockLastYearData.push(candles["close"]);
        let date = new Date(candles["datetime"]);
        labelsLastYear.push(date.getDate()+" "+month[date.getMonth()]);
    });
    
    //Finished settings
    const lastYearData = {
        labels: labelsLastYear,
        datasets: [{
            backgroundColor: 'rgb(255, 150, 69)',
            borderColor: 'rgb(255,150,69)',
            data: stockLastYearData,
        }]
    }
    
    ////////////////////////////
    //Last 5 Years Chart settings
    ////////////////////////////

    //Create variables for settings
    const labelsLast5Years = [];
    const stockLast5YearsData = [];

    //Add Data from stockJson to the Labes / Data array
    stockJson["last5Years"]["candles"].forEach(candles => {
        stockLast5YearsData.push(candles["close"]);
        let date = new Date(candles["datetime"]);
        labelsLast5Years.push(date.getDate()+" "+month[date.getMonth()]);
    });
    
    //Finished settings
    const last5YearsData = {
        labels: labelsLast5Years,
        datasets: [{
            backgroundColor: 'rgb(255, 150, 69)',
            borderColor: 'rgb(255,150,69)',
            data: stockLast5YearsData,
        }]
    }
    
}

//Creats a html element of tpye "elementType" with the text "elementText" and binds it to "parentElement"
function addContent(elementType,elementText = null ,parentElement = null,idName = null,className = null){
    var para = document.createElement(elementType);
    if(elementText != null){
        var node = document.createTextNode(elementText);
        para.appendChild(node);
    }
    if(idName != null){
       para.id = idName;
    }
    if(className != null){
        para.classList.add(className);
    }
    if(parentElement != null){
        var element;
        if(typeof parentElement === "string" || parentElement instanceof String){
            element = document.getElementById(parentElement);
        } else element = parentElement;
        
        element.appendChild(para);
    }
    return para;
}

function addInfoContent(infoName,infoValue){
    let newDiv = addContent("div",null,"stockInfoDiv");
    addContent("p",infoName,newDiv,null,"left");
    addContent("p", infoValue,newDiv,null,"right");
}



