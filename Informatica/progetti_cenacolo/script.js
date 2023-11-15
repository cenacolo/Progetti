// Puoi usare JavaScript per aggiungere dinamicamente immagini al riquadro
const riquadro = document.getElementById('riquadro');

// Esempio di come aggiungere un'immagine
const nuovaImmagine = document.createElement('img');
nuovaImmagine.src = 'path/della/tua/immagine.jpg'; // Sostituisci con il percorso della tua immagine
riquadro.appendChild(nuovaImmagine);
