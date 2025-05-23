function convertToCelsius() {
  let fahrenheit = parseFloat(document.getElementById("fahrenheit").value);
  if (!isNaN(fahrenheit)) {
    let celsius = (fahrenheit - 32) * 5 / 9;
    document.getElementById("celsius").innerText = celsius;
  } else {
    document.getElementById("celsius").innerText = "Please enter a valid number.";
  }
}