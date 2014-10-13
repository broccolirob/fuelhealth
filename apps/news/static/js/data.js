$(document).ready(function(){

    var build_sleep_graph = function(asleep, awake){
        var data = asleep;

        var m = [80, 80, 80, 80]; // margins
        var w = 700; // width
        var h = 500; // height


        // X scale will fit all values from data[] within pixels 0-w
        var x = d3.scale.linear().domain([0, data.length]).range([0, w]);
        // Y scale will fit values from 0-10 within pixels h-0 (Note the inverted domain for the y-scale: bigger is up!)
        var y = d3.scale.linear().domain([Math.min.apply(Math, data), Math.max.apply(Math, data)]).range([h, 0]);
            // automatically determining max range can work something like this
            // var y = d3.scale.linear().domain([0, d3.max(data)]).range([h, 0]);

        // create a line function that can convert data[] into x and y points
        var line = d3.svg.line()
            // assign the X function to plot our line as we wish
            .x(function(d,i) {
                // verbose logging to show what's actually being done
                // return the X coordinate where we want to plot this datapoint
                return x(i);
            })
            .y(function(d) {
                // verbose logging to show what's actually being done
                // return the Y coordinate where we want to plot this datapoint
                return y(d);
            });

            // Add an SVG element with the desired dimensions and margin.
            var graph = d3.select("#graph").append("svg:svg")
                  .attr("width", w + m[1] + m[3])
                  .attr("height", h + m[0] + m[2])
                .append("svg:g")
                  .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

            // create yAxis
            var xAxis = d3.svg.axis().scale(x).tickSize(-h).tickSubdivide(true);
            // Add the x-axis.
            graph.append("svg:g")
                  .attr("class", "x axis")
                  .attr("transform", "translate(0," + h + ")")
                  .call(xAxis);


            // create left yAxis
            var yAxisLeft = d3.svg.axis().scale(y).ticks(4).orient("left");
            // Add the y-axis to the left
            graph.append("svg:g")
                  .attr("class", "y axis")
                  .attr("transform", "translate(-25,0)")
                  .call(yAxisLeft);

            // Add the line by appending an svg:path element with the data line we created above
            // do this AFTER the axes above so that the line is above the tick-lines
            graph.append("svg:path").attr("d", line(data));

            graph.append("svg:text")
                .attr("text-anchor", "right")
                .style("font-size", "16px")
                .style("font-weight", "bold")
                .text("Time Asleep");
    };
    var build_graph = function(healthArray, title){
        var data = healthArray;
        var title = title.replace("_", " ");

        var m = [80, 80, 80, 80]; // margins
        var w = 700; // width
        var h = 500; // height


        // X scale will fit all values from data[] within pixels 0-w
        var x = d3.scale.linear().domain([0, data.length]).range([0, w]);
        // Y scale will fit values from 0-10 within pixels h-0 (Note the inverted domain for the y-scale: bigger is up!)
        var y = d3.scale.linear().domain([Math.min.apply(Math, data), Math.max.apply(Math, data)]).range([h, 0]);
            // automatically determining max range can work something like this
            // var y = d3.scale.linear().domain([0, d3.max(data)]).range([h, 0]);

        // create a line function that can convert data[] into x and y points
        var line = d3.svg.line()
            // assign the X function to plot our line as we wish
            .x(function(d,i) {
                // verbose logging to show what's actually being done
                // return the X coordinate where we want to plot this datapoint
                return x(i);
            })
            .y(function(d) {
                // verbose logging to show what's actually being done
                // return the Y coordinate where we want to plot this datapoint
                return y(d);
            });

            // Add an SVG element with the desired dimensions and margin.
            var graph = d3.select("#graph").append("svg:svg")
                  .attr("width", w + m[1] + m[3])
                  .attr("height", h + m[0] + m[2])
                .append("svg:g")
                  .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

            // create yAxis
            var xAxis = d3.svg.axis().scale(x).tickSize(-h).tickSubdivide(true);
            // Add the x-axis.
            graph.append("svg:g")
                  .attr("class", "x axis")
                  .attr("transform", "translate(0," + h + ")")
                  .call(xAxis);


            // create left yAxis
            var yAxisLeft = d3.svg.axis().scale(y).ticks(4).orient("left");
            // Add the y-axis to the left
            graph.append("svg:g")
                  .attr("class", "y axis")
                  .attr("transform", "translate(-25,0)")
                  .call(yAxisLeft);

            // Add the line by appending an svg:path element with the data line we created above
            // do this AFTER the axes above so that the line is above the tick-lines
            graph.append("svg:path").attr("d", line(data));

            graph.append("svg:text")
                .attr("text-anchor", "right")
                .style("font-size", "16px")
                .style("font-weight", "bold")
                .text(title.charAt(0).toUpperCase() + title.slice(1));
    };
    var endpoints = ['blood_glucose', 'blood_oxygen', 'bmi', 'body_fat', 'height', 'heart_rate', 'weight'];
    var glucose_data = function(endpoint){
        var values = [];
        $.ajax({
            url: 'https://api.humanapi.co/v1/human/' + endpoint + '/readings/?access_token=demo',
            type: 'GET',
            dataType: 'json',
            success: function(data){
                for (var i=0; i< data.length; i++){
                    values.push(data[i].value);
                }
                build_graph(values, endpoint);
            }
        });
    };
    var sleep_data = function(){
        var timeAsleep = [];
        var timeAwake = [];
        $.ajax({
            url: 'https://api.humanapi.co/v1/human/sleeps/summaries/?access_token=demo',
            type: 'GET',
            dataType: 'json',
            success: function(data){
                for (var i=0; i<data.length; i++){
                    timeAsleep.push(data[i].timeAsleep);
                    timeAwake.push(data[i].timeAwake);
                }
                build_sleep_graph(timeAsleep, timeAwake);
            }
        });
    };


    for (var i=0; i<endpoints.length; i++){
        glucose_data(endpoints[i]);
    }
    sleep_data();
});