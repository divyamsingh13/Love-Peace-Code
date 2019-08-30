var margin = { left:100, right:10, top:10, bottom:150 };

var width = 800 - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom;

var g = d3.select("#chart-area")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform", "translate(" + margin.left
            + ", " + margin.top + ")");

var xAxisGroup = g.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height +")");

var yAxisGroup = g.append("g")
    .attr("class", "y axis");

// X Scale
var x = d3.scaleBand()
    .range([0, width])
    .padding(0.2);

// Y Scale
var y = d3.scaleLinear()
    .range([height, 0]);

// X Label
g.append("text")
    .attr("y", height + 80)
    .attr("x", width / 2)
    .attr("font-size", "20px")
    .attr("text-anchor", "middle")
    .text("Area");

// Y Label
g.append("text")
    .attr("y", -60)
    .attr("x", -(height / 2))
    .attr("font-size", "20px")
    .attr("text-anchor", "middle")
    .attr("transform", "rotate(-90)")
    .text("Air Quality Index");

d3.csv(csvdata).then(function(data){
    // Clean data
    data.forEach(function(d) {
        d.AQI = +d.AQI;
    });
});
d3.interval(function(){
    update()
}, 1000);
// Run the vis for the first time
update();


function update(){
    d3.csv(csvdata).then(function(data){
    // Clean data
    data.forEach(function(d) {
        d.AQI = +d.AQI;
    });

    console.log(data);

    x.domain(data.map(function(d){ return d.country }));
    y.domain([0, d3.max(data, function(d) { return d.AQI })])

    // X Axis
    var xAxisCall = d3.axisBottom(x);
    xAxisGroup.call(xAxisCall)
        .selectAll("text")
        .attr("y", "10")
        .attr("x", "-30")
        .attr("font-size", "15px")
        .attr("text-anchor", "middle")
        .attr("transform", "rotate(-40)");

    // Y Axis
    var yAxisCall = d3.axisLeft(y)
        .tickFormat(function(d){ return d; });
    yAxisGroup.call(yAxisCall);

    // JOIN new data with old elements.
    var rects = g.selectAll("rect")
        .data(data);

    // EXIT old elements not present in new data.
    rects.exit().remove();

    // UPDATE old elements present in new data.
    rects
        .attr("y", function(d){ return y(d.AQI);})
        .attr("x", function(d){ return x(d.country);})
        .attr("height", function(d){ return height - y(d.AQI); })
        .attr("width", x.bandwidth)
        .attr("fill", function(d){
            if(d.AQI>=0 && d.AQI<=50){
                return "green";
            } else if(d.AQI>50 && d.AQI<=100){
                return "yellow";
            } else if(d.AQI>100 && d.AQI<=150){
                return "orange";
            } else if(d.AQI>151 && d.AQI<=200){
                return "red";
            } else if(d.AQI>200 && d.AQI<=300){
                return "purple";
            } else if(d.AQI>300 && d.AQI<=500){
                return "orange";
            }
        });

    rects.enter()
    .append("rect")
        .attr("y", function(d){ return y(d.AQI);})
        .attr("x", function(d){ return x(d.country);})
        .attr("width", x.bandwidth)
        .attr("height", function(d){
            return height - y(d.AQI);
        })
        .attr("fill", function(d){
            if(d.AQI>=0 && d.AQI<=50){
                return "green";
            } else if(d.AQI>50 && d.AQI<=100){
                return "yellow";
            } else if(d.AQI>100 && d.AQI<=150){
                return "orange";
            } else if(d.AQI>151 && d.AQI<=200){
                return "red";
            } else if(d.AQI>200 && d.AQI<=300){
                return "purple";
            } else if(d.AQI>300 && d.AQI<=500){
                return "orange";
            }
        });
    });
}