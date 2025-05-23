    const person = {
      firstName: "Ahmed",
      lastName: "Kamilov",
      age: 22,
      eyeColor: "brown"
    };

    const table = document.getElementById("infoTable");

    for (let key in person) {
      let row = table.insertRow();
      let cell1 = row.insertCell(0);
      let cell2 = row.insertCell(1);
      cell1.textContent = key;
      cell2.textContent = person[key];
    }