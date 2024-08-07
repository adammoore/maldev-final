/**
 * Fetches lifecycle data from the server and creates a D3.js visualization.
 */
async function createLifecycleVisualization() {
    try {
        const response = await fetch('/api/lifecycle');
        const data = await response.json();

        const width = 800;
        const height = 600;
        const radius = Math.min(width, height) / 2 - 50;

        const svg = d3.select("#lifecycle-container")
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("transform", `translate(${width / 2},${height / 2})`);

        const color = d3.scaleOrdinal(d3.schemeCategory10);

        const pie = d3.pie()
            .value(d => 1)
            .sort(null);

        const arc = d3.arc()
            .innerRadius(radius * 0.5)
            .outerRadius(radius * 0.8);

        const outerArc = d3.arc()
            .innerRadius(radius * 0.9)
            .outerRadius(radius * 0.9);

        const arcs = svg.selectAll(".arc")
            .data(pie(data))
            .enter()
            .append("g")
            .attr("class", "arc");

        arcs.append("path")
            .attr("d", arc)
            .attr("fill", d => color(d.data.name))
            .attr("stroke", "white")
            .style("stroke-width", "2px");

        arcs.append("text")
            .attr("transform", d => {
                const pos = outerArc.centroid(d);
                return `translate(${pos[0]},${pos[1]})`;
            })
            .attr("dy", ".35em")
            .style("text-anchor", "middle")
            .text(d => d.data.name);

        arcs.on("click", async function (event, d) {
            const substagesResponse = await fetch(`/api/substages/${d.data.id}`);
            const substages = await substagesResponse.json();
            console.log("Substages:", substages);
            // TODO: Implement substage visualization
        });
    } catch (error) {
        console.error("Error fetching lifecycle data:", error);
    }
}

document.addEventListener("DOMContentLoaded", createLifecycleVisualization);