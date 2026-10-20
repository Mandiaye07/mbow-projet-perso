function ChangementCouleur() {
  var red = getRandomValue();
  var green = getRandomValue();
  var blue = getRandomValue();
  var randomColor = 'rgb(' + red + ',' + green + ',' + blue + ')';
  document.body.style.backgroundColor = randomColor;
  alert("Vous avez changé la couleur du fond !")
}
function getRandomValue() {
  return Math.floor(Math.random() * 256);
}

function sauvegarderChiffre() {
  const userInput = parseFloat(document.getElementById("userInput").value);
  if (!isNaN(userInput)) {
      //ajoute le chiffre à la liste des chiffres sauvegardés
      const chiffresSauvegardes = JSON.parse(localStorage.getItem("chiffresSaisis")) || [];
      chiffresSauvegardes.push(userInput);
      chiffresSauvegardes.sort((a, b) => b - a); //trie du plus grand au plus petit
      localStorage.setItem("chiffresSaisis", JSON.stringify(chiffresSauvegardes));
      afficherChiffres();
  }
}

function afficherChiffres() {
  const chiffresSauvegardes = JSON.parse(localStorage.getItem("chiffresSaisis")) || [];
  const affichageChiffres = document.getElementById("affichageChiffres");
  affichageChiffres.innerHTML = "<h2>Scores sauvegardés 👇:</h2>";
  chiffresSauvegardes.forEach((chiffre, index) => {
      affichageChiffres.innerHTML += `<p>${index + 1}. ${chiffre}</p>`;
  });
}

window.onload = function () {
  afficherChiffres();
};

