var medianBar;

// Event listener for getting state details
d3.select('#get-states').on('click', function () {    
    fetchDataAndDisplay('/api/v1.0/states_details', '#states-json');
});

// Function to fetch and display JSON data from the API endpoints using d3.json
function fetchDataAndDisplay(endpoint, jsonElement) {
    d3.json(endpoint)
      .then(function (data) {
                
        // Clear existing content
        d3.select(jsonElement).html("");             
        
        // Create the dropdown for states
        let stateDrpdwn = d3.select(document.createElement('select'));      
        stateDrpdwn.attr("id", "states-list");

        // Get the number of items
        let scount = Object.keys(data.State).length;
        // Add the states to the dropdown
        for (let cnt =0; cnt < scount; cnt++)
        {
            let state = data.State[cnt]
            stateDrpdwn.append("option").text(state).attr("value",cnt);
        }
        d3.select(jsonElement).node().appendChild(stateDrpdwn.node());
        
        //Create Bar Chart using Chart.js
        createChart(data);
        
        // Function updateChart is called when the selection in state dropdown is changed
        d3.select("#states-list").on("change", updateChart);

        // // Updates the chart based on the selected State
        function updateChart()
        {
          let dropdownMenu = d3.select("select");
          // Assign the value of the dropdown menu option to a variable
          let selectedStateIndex = dropdownMenu.property("value");                   
          let selState = data.State[selectedStateIndex]
          let stateMedianIncome = data["Median Household Income"][selectedStateIndex];
          let stateMedianHousePrice = data["Median Home Price"][selectedStateIndex];
          //console.log(selState);
          // Update the values for the Chart based on the selected state
           medianBar.data.labels[1] = selState
           medianBar.data.datasets[0].data[1] = stateMedianIncome;
           medianBar.data.datasets[1].data[1] = stateMedianHousePrice;
           medianBar.update('none');
        }
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }
  
 
// Initial creation of the Bar chart
function createChart(fullData)
{
   //Calculate the National Median of the 3 columns
   let nationalMedianHousePrice = calculateMedian(fullData["Median Home Price"]);
   //let nationalMedianHouseSize = calculateMedian(fullData["Median Home Size (in square feet)"]);
   let nationalMedianHouseholdIncome = calculateMedian(fullData["Median Household Income"]);

   // Get the details of the first state for initial values of the Bar Chart
   let selState = fullData.State[0]
   let stateMedianIncome = fullData["Median Household Income"][0];
   let stateMedianHousePrice = fullData["Median Home Price"][0];
   
// Generate the Bar Chart        
   let barChartCanvas = document.getElementById('barChart');
   let xValues = ["National",selState,];
   let yIncome = [nationalMedianHouseholdIncome, stateMedianIncome];
   let yHousePrice = [nationalMedianHousePrice, stateMedianHousePrice];

   medianBar =  new Chart(barChartCanvas, {
       type: 'bar',
       data: {
       labels: xValues,
       datasets: [{
       backgroundColor: "green",
       data: yIncome,
       label: 'Median Income'        
       },
       {
       backgroundColor: "brown",
       data: yHousePrice,
       label: 'Median House Price'
       }]
       },
       options: {
       animation:{duration :0,loop :false},
       scales: { y: { beginAtZero: true } }
       }
   });
}

// Calculate Median of the input  
function calculateMedian(dataArray)
{
    if (Object.values(dataArray).length == 50)
    {
        let arrayForMedian = Object.values(dataArray);        
        sortedArray = arrayForMedian.sort((num1,num2)=> num1-num2);    
        nationalMedian = (sortedArray[24] + sortedArray[25])/2;
        return nationalMedian;   
    } 
    else
    {
        console.log("Check the array size to calculate Median.")
    }
}

 