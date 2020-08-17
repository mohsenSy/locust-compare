axios({
  url: "/dirs",
  method: 'GET',
  responseType: "json"
}).then(function(response) {
  data_list = document.getElementById("results");
  dirs = response.data.dirs
  var options = "";
  for (var dir in response.data.dirs) {
    dir = dirs[dir].split("/")[1]
    options += "<option value='" + dir + "' />";
  }
  data_list.innerHTML = options;
})

function display_chart(result) {
  file = "/results/" + result + "/data.csv"
  d3.csv(file).then(makeChart);
  function makeChart(data) {
    var rps = data.map(function(d) { return d.rps;})
    var avg = data.map(function(d) { return d.avg;})
    var failures = data.map(function(d) { return d.failures;})
    var myChart = new Chart("chart", {
      type: "bar",
      data: {
        labels: rps,
        datasets: [
          {
            label: "avg",
            data: avg,
            backgroundColor: Array(avg.length).fill('rgba(255,120,50,1.0)')
          },
          {
            label: "failures",
            data: failures
          }
        ]
      },
      options: {
        title: {
          display: true,
          text: result
        },
        legend: {
          display: true
        },
        scales: {
              yAxes: [{
                  ticks: {
                      beginAtZero: true
                  }
              }]
          }
      }
    })
  }
}

function go(event) {
  event.preventDefault();
  var result = document.getElementById("result").value;
  display_chart(result)
}
