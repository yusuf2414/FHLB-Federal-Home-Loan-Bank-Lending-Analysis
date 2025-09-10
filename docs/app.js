async function loadManifest() {
  const res = await fetch("./images/manifest.json");
  if (!res.ok) throw new Error("manifest.json not found under docs/images/");
  return res.json();
}

function byId(id){ return document.getElementById(id); }

function filenameToCaption(path) {
  // path like "Boston/ltv_hist.png" or "Des%20Moines/Distributions...png"
  const base = decodeURIComponent(path.split("/").slice(-1)[0]);
  return base.replace(/[_-]/g, " ").replace(/\.png$/i, "");
}

function renderBankList(banks) {
  const sel = byId("bankSelect");
  sel.innerHTML = "";
  banks.forEach(b => sel.append(new Option(b, b)));
}

function renderImages(bank, images) {
  const root = byId("gallery");
  root.innerHTML = "";
  const note = byId("note");

  const list = (images[bank] || []).map(p => `./images/${p}`);
  if (!list.length) {
    note.textContent = `No images available for ${bank}.`;
    return;
  }
  note.textContent = "";

  // make a 2-col grid of figures
  for (const src of list) {
    const fig = document.createElement("figure");
    const img = document.createElement("img");
    img.src = src;
    img.alt = filenameToCaption(src);
    img.style.width = "100%";
    img.loading = "lazy";
    img.onerror = () => { fig.remove(); }; // hide broken links

    const cap = document.createElement("figcaption");
    cap.textContent = filenameToCaption(src);

    fig.appendChild(img);
    fig.appendChild(cap);
    root.appendChild(fig);
  }
}

async function bootstrap(){
  const manifest = await loadManifest();
  renderBankList(manifest.banks);

  const sel = byId("bankSelect");
  sel.addEventListener("change", () => renderImages(sel.value, manifest.images));

  // default to first bank
  if (manifest.banks.length) {
    sel.value = manifest.banks[0];
    renderImages(sel.value, manifest.images);
  }
}

bootstrap();
