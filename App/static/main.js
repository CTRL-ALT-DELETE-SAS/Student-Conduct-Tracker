async function getUserData() {
  const response = await fetch('/api/users');
  return response.json();
}

function loadTable(users) {
  const table = document.querySelector('#result');
  for (let user of users) {
    table.innerHTML += `<tr>
            <td>${user.ID}</td>
            <td>${user.firstname}</td>
            <td>${user.lastname}</td>
        </tr>`;
  }
}

async function main() {
  const users = await getUserData();
  loadTable(users);
}

main();
