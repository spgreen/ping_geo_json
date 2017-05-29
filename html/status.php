<!DOCTYPE html>
<html>
<head>
 <style>
    table.stats {
     table-layout: fixed;
     width: 80%;
    }
    .nren, .country {
        width: 20%;
    }
    .link, .rtt, .loss {
        width : 10%;
    }
    .status {
        width: 4%;
        text-align: center;
    }
    svg {
        display: block;
        margin: auto;
    }
 </style>
  <script src="https://d3js.org/d3.v3.min.js" charset="utf-8"></script>
  <script src="world_map_geo.json"></script>
</head>
 
<body>
   <div id="statusMap"></div>
   <script>
              
    var width = 800,
        height = 580;
    var svg = d3.select( "div" )
                 .attr( "class", "statusMap" )
                .append( "svg" )
                 .attr( "width", width )
                 .attr( "height", height );
                
    var g = svg.append( "g" );
    var routers = svg.append("g");
                 
    var mercatorProjection = d3.geo.mercator()
                                 .scale( 120 ) 
                                 .rotate( [0,0] )
                                 .center( [0, 25] )
                                 .translate( [width/2,height/2] );
    var geoPath = d3.geo.path()                        
                        .projection( mercatorProjection );
                        
    g.selectAll( "path" )
     .data( worldmap_json.features )
     .enter()
     .append( "path" )
     .attr( "fill", "#ffc966" )
     .attr( "d", geoPath )
     .append("text")
     .text(function (d) {return d.id});   
     
    d3.json("status.json", function(router_data){
        var router_nodes = router_data;
    
        routers.selectAll( "path" )
                .data( router_nodes.nren )
                .enter()
                .append( "path" )
                 .attr( "fill", function(d) {
                    if (d.results.status == "OK") {
                      return "green";
                    } else if (d.results.status == "WARN") {
                      return "orange";
                    }
                    return "red";
                  })
                 .attr( "stroke", "#000" )
                 .attr( "d", geoPath );          
                 
        routers.selectAll("text")
                .data( router_nodes.nren)
                .enter()
                    .append("svg:text")
                    .text(function(d){
                        return d.properties.name;
                    })
                    .attr("x", function(d){
                        return geoPath.centroid(d)[0] + 5;
                    })
                    .attr("y", function(d){
                        return  geoPath.centroid(d)[1] - 2;
                    })
                    //.attr("text-anchor","left")
                    .attr('font-size','10pt')
                    .attr('font-weight','bold');
    });
     
  </script>  
</body>
</html>
