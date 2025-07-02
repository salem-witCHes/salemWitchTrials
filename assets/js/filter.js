// JS for csv tables
document.addEventListener("DOMContentLoaded", function () {
const filters = document.querySelectorAll("#tableFilters li");
const tables = document.querySelectorAll(".csv-table");

filters.forEach(filter => {
    filter.addEventListener("click", function () {
    const filterValue = this.getAttribute("data-filter");

    // Update active class on buttons
    filters.forEach(f => f.classList.remove("filter-active"));
    this.classList.add("filter-active");

    // Hide all tables first
    tables.forEach(table => {
        table.classList.remove("active");
    });

    // Show only the selected one
    tables.forEach(table => {
        if (table.classList.contains(filterValue.slice(1))) {
        table.classList.add("active");
        }
    });
    });
});

// Show the first table by default
tables.forEach(table => table.classList.remove("active"));
const firstFilter = filters[0].getAttribute("data-filter").slice(1);
const firstTable = document.querySelector(`.csv-table.${firstFilter}`);
if (firstTable) firstTable.classList.add("active");
});


// JS for models
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".zoom-container").forEach(function (container) {
    const img = container.querySelector(".zoom-img");

    let scale = 1;
    let pos = { x: 0, y: 0 };
    let start = { x: 0, y: 0 };
    let isDragging = false;

    container.addEventListener("wheel", function (e) {
      e.preventDefault();
      const delta = e.deltaY > 0 ? -0.1 : 0.1;
      scale = Math.min(Math.max(1, scale + delta), 5);
      updateTransform();
    });

    container.addEventListener("mousedown", function (e) {
      isDragging = true;
      start = { x: e.clientX - pos.x, y: e.clientY - pos.y };
      container.style.cursor = "grabbing";
    });

    window.addEventListener("mouseup", function () {
      isDragging = false;
      container.style.cursor = "grab";
    });

    window.addEventListener("mousemove", function (e) {
      if (!isDragging) return;
      pos = { x: e.clientX - start.x, y: e.clientY - start.y };
      updateTransform();
    });

    function updateTransform() {
      img.style.transform = `translate(${pos.x}px, ${pos.y}px) scale(${scale})`;
    }
  });
});
