async function buscarHumor(tipo) {
  const url = `/api/humor?tipo=${encodeURIComponent(tipo)}`;
  const r = await fetch(url);
  if (!r.ok) {
    throw new Error("Falha ao obter humor");
  }
  return await r.json();
}

function renderResultado(data) {
  const div = document.getElementById("resultado");
  div.innerHTML = `<div class="card"><span class="emoji">${data.emoji}</span><span class="tipo">${data.tipo}</span><p>${data.texto}</p></div>`;
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("button[data-tipo]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const tipo = btn.getAttribute("data-tipo");
      try {
        const data = await buscarHumor(tipo);
        renderResultado(data);
      } catch (e) {
        alert(e.message);
      }
    });
  });
});
