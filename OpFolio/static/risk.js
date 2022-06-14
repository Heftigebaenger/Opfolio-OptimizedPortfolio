
function compareStocks() {
    let firstStockSymbol = document.getElementById("stockOne").value
    let secondStockSymbol = document.getElementById("stockTwo").value
    console.log(firstStockSymbol)
    console.log(secondStockSymbol)
    fetch("/risk/api/"+firstStockSymbol+"/"+secondStockSymbol).then(response => response.json()).then(data => useData(data))
    
    
}

function useData(data){
    console.log(data)
    Highcharts.chart('container', {
        chart: {
            type: 'spline',
            inverted: true
        },
        title: {
            text: 'Yield by Risk'
        },
        subtitle: {
            text: 'According to OPFolio'
        },
        xAxis: {
            reversed: false,
            title: {
                enabled: true,
                text: 'Yield'
            },
            labels: {
                format: '{value}'
            },
            accessibility: {
                rangeDescription: ''
            },
            showLastLabel: true,
            beginAtZero: true
        },

        yAxis: {
            title: {
                text: 'Risk'
            },
            labels: {
                format: '{value}%'
            },
            accessibility: {
                rangeDescription: ''
            },
            lineWidth: 2,
            maxPadding: 1
        },
        legend: {
            enabled: false
        },
        tooltip: {
            headerFormat: '<b>{series.name}</b><br/>',
            pointFormat: '{point.x}: {point.y}%'
        },
        plotOptions: {
            spline: {
                marker: {
                    enable: false
                }
            }
        },
        series: [{
            name: 'Risk',
            data: data.effCurveArray
        }]
    });
    alert(data.corr)
}