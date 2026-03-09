let allJobs = [];

async function loadData() {
  const [jobsRes, metaRes] = await Promise.all([fetch("data/jobs.json"), fetch("data/meta.json")]);
  allJobs = await jobsRes.json();
  const meta = await metaRes.json();
  document.getElementById("updatedAt").textContent = `Last update (Beijing): ${meta.last_update_bj || "N/A"}`;
  buildFilters(allJobs);
  render();
}

function uniq(values) { return [...new Set(values.filter(Boolean))].sort(); }

function buildFilters(rows) {
  const orgFilter = document.getElementById("orgFilter");
  const typeFilter = document.getElementById("typeFilter");
  uniq(rows.map((r) => r.org_name)).forEach((v) => addOpt(orgFilter, v));
  uniq(rows.map((r) => r.job_type)).forEach((v) => addOpt(typeFilter, v));
}

function addOpt(select, value) {
  const opt = document.createElement("option");
  opt.value = value;
  opt.textContent = value;
  select.appendChild(opt);
}

function applyFilters(rows) {
  const q = document.getElementById("searchInput").value.trim().toLowerCase();
  const org = document.getElementById("orgFilter").value;
  const typ = document.getElementById("typeFilter").value;
  const newOnly = document.getElementById("newOnly").checked;
  return rows.filter((r) => {
    const hay = `${r.org_name} ${r.job_title} ${r.location}`.toLowerCase();
    if (q && !hay.includes(q)) return false;
    if (org && r.org_name !== org) return false;
    if (typ && r.job_type !== typ) return false;
    if (newOnly && !r.is_new_today) return false;
    return true;
  });
}

function render() {
  const container = document.getElementById("jobList");
  container.innerHTML = "";
  const rows = applyFilters(allJobs);
  document.getElementById("countLabel").textContent = `${rows.length} positions shown`;
  rows.forEach((r) => {
    const el = document.createElement("article");
    el.className = `card ${r.is_new_today ? "new" : ""}`;
    el.innerHTML = `
      <h3><a href="${r.job_url}" target="_blank" rel="noopener">${esc(r.job_title || "Untitled")}</a></h3>
      <div class="meta">${esc(r.org_name)} | ${esc(r.location || "N/A")}</div>
      <div class="meta">Type: ${esc(r.job_type || "N/A")}</div>
      <div class="meta">Deadline: ${esc(r.deadline || "N/A")}</div>
      ${r.is_new_today ? '<span class="badge">New Today</span>' : ""}
    `;
    container.appendChild(el);
  });
}

function esc(s) {
  return String(s).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#39;");
}

["searchInput", "orgFilter", "typeFilter", "newOnly"].forEach((id) => {
  document.getElementById(id)?.addEventListener("input", render);
  document.getElementById(id)?.addEventListener("change", render);
});

loadData().catch((e) => {
  document.getElementById("updatedAt").textContent = `Failed to load data: ${e}`;
});
