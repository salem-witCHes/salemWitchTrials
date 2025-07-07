// // // JS for csv tables
document.addEventListener("DOMContentLoaded", function () {
  const filters = document.querySelectorAll("#tableFilters li");
  const csvContainer = document.querySelector("#csv .isotope-container");
  const metadataContainer = document.querySelector("#metadata .isotope-container");
  const csvTables = csvContainer.querySelectorAll(".csv-table");

  // Separate Isotope instances
  const csvIsotope = new Isotope(csvContainer, {
    itemSelector: '.isotope-item',
    layoutMode: 'fitRows'
  });

  // Metadata Isotope setup
  const metadataIsotope = new Isotope('#metadata .metadata-container', {
    itemSelector: '.metadata-item',
    layoutMode: 'fitRows'
  });

  function showTable(filterValue) {
    // Update active filter button
    filters.forEach(f => f.classList.remove("filter-active"));
    const activeFilter = [...filters].find(f => f.getAttribute("data-filter") === filterValue);
    if (activeFilter) activeFilter.classList.add("filter-active");

    // Show/hide tables
    csvTables.forEach(table => {
      if (table.classList.contains(filterValue.slice(1))) {
        table.classList.add("active");
      } else {
        table.classList.remove("active");
      }
    });

    // Keep images always visible when filtering tables
    csvIsotope.arrange({ filter: filterValue });
  }

  // Show the first table on load
  const defaultFilter = filters[0].getAttribute("data-filter");
  showTable(defaultFilter);

  // Set up click listeners
  filters.forEach(filter => {
    filter.addEventListener("click", function () {
      const filterValue = this.getAttribute("data-filter");
      showTable(filterValue);
    });
  });
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
