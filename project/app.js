// Démo JS: petite logique + export
function sum(a, b) {
  return a + b;
}

function formatUser(user) {
  return `${user.name} (${user.age})`;
}

module.exports = { sum, formatUser };
