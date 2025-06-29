async function loadAppointments() {
    const res = await fetch('/api/appointments');
    const data = await res.json();
    const tbody = document.querySelector('#appointments tbody');
    tbody.innerHTML = '';
    data.forEach(app => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${app.name}</td><td>${app.email}</td><td>${app.datetime}</td><td>${app.message}</td>`;
        tbody.appendChild(row);
    });
}

document.getElementById('appointment-form').addEventListener('submit', async e => {
    e.preventDefault();
    const formData = new FormData(e.target);
    await fetch('/api/appointments', { method: 'POST', body: formData });
    e.target.reset();
    loadAppointments();
});

window.addEventListener('DOMContentLoaded', loadAppointments);
