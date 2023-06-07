function startCounter() {
    var endDate = new Date("2023-12-31");
    var todayDate = new Date();
    var diffDate = endDate - todayDate;
    
    if(diffDate <= 0) {
        clearInterval(interval);
        return;
    }


    var seconds = Math.floor(diffDate / 1000) % 60;
    var minutes = Math.floor(diffDate / 1000 / 60) % 60;
    var hours = Math.floor(diffDate / 1000 / 60 / 60) % 24;
    var days = Math.floor(diffDate / 1000 / 60 / 60 / 24);

    const counterText = `- ${days} days ${hours} hours ${minutes} minutes ${seconds} seconds -`;
    document.getElementById('counter').innerHTML =  counterText;
}


const interval = setInterval(startCounter, 1000);