// Lista droni
axios.get("http://127.0.0.1:5000/droni")
.then(res => {
    const droniList = document.getElementById("droni-list");
    res.data.forEach(d => {
        const li = document.createElement("li");
        li.textContent = `${d.Modello} - Capacità: ${d.Capacità}, Batteria: ${d.Batteria}%`;
        droniList.appendChild(li);
    });
})
.catch(err => console.error(err));

// Lista piloti
axios.get("http://127.0.0.1:5000/piloti")
.then(res => {
    const pilotiList = document.getElementById("piloti-list");
    res.data.forEach(p => {
        const li = document.createElement("li");
        li.textContent = `${p.Nome} ${p.Cognome} - Brevetto: ${p.Brevetto}, Turno: ${p.Turno}`;
        pilotiList.appendChild(li);
    });
})
.catch(err => console.error(err));
