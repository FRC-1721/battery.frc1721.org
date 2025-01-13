// Dylan originally wrote this
document.addEventListener("DOMContentLoaded", function () {
    // Color condition cells
    let conditions = document.getElementsByClassName("condition");
    Array.from(conditions).forEach(function (condition) {
        if (condition.innerText == "Good") {
            condition.style.background = "lime";
        } else if (condition.innerText == "Fair") {
            condition.style.background = "yellow";
        } else if (condition.innerText == "Poor") {
            condition.style.background = "red";
        } else {
            condition.style.background = "gray";
        }
    });

    // Color ready cells
    let readyvalues = document.getElementsByClassName("ready");
    Array.from(readyvalues).forEach(function (readyvalue) {
        if (readyvalue.innerText == "True") {
            readyvalue.style.background = "lime";
        } else {
            readyvalue.style.background = "red";
        }
    });

    // Color charge cells
    let charges = document.getElementsByClassName("charge");
    Array.from(charges).forEach(function (charge) {
        if (charge.innerText == -1) {
            charge.style.background = "gray";
        } else {
            charge.style.background = "hsl(" + charge.innerText + " 100% 50%)";
        }
    });
});
