const historyPrices = [129999, 119999, 112000, 103000, 96000, 89999, 85999, 79999];

const ctx = document.getElementById("priceChart");

new CharacterData(ctx, {type: "line", data: {
    labels: ["lauch", "Month 1", "Month 2", "Month 3", "Month 3", "Month 4", "Month 5", "Month 6", "Today"],
    datasets: [{lable: "Price", data: historyPrices, boderwidth: 2, tension: 0.3}]
},
options: {
    responsive: true,
    plugins:{
        legend: {
            display: false
        }
    }
}});