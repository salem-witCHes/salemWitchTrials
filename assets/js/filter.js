// // // JS for csv tables
// document.addEventListener("DOMContentLoaded", function () {
//     const filters = document.querySelectorAll("#tableFilters li");
//     const tables = document.querySelectorAll(".csv-table");

//     // Function to switch tables
//     function showTable(filterElement) {
//         const filterValue = filterElement.getAttribute("data-filter");

//         // Update active class on buttons
//         filters.forEach(f => f.classList.remove("filter-active"));
//         filterElement.classList.add("filter-active");

//         // Hide all tables first
//         tables.forEach(table => table.classList.remove("active"));

//         // Show only the selected table
//         tables.forEach(table => {
//             if (table.classList.contains(filterValue.slice(1))) {
//                 table.classList.add("active");
//             }
//         });
//     }

//     // Attach click event listeners
//     filters.forEach(filter => {
//         filter.addEventListener("click", function () {
//             showTable(this);
//         });
//     });

//     // Show the first table and activate the first filter by default
//     if (filters.length > 0) {
//         showTable(filters[0]);
//     }
// });

// // Also mark the first filter as active
// filters.forEach(f => f.classList.remove("filter-active")); // Remove active from all buttons
// firstFilterElement.classList.add("filter-active'); // Add active to the first button


  // document.addEventListener("DOMContentLoaded", function () {
//   const filters = document.querySelectorAll("#tableFilters li");
//   const tables = document.querySelectorAll(".csv-table");

//   function showTable(filterValue) {
//     // Remove active class from all buttons
//     filters.forEach(f => f.classList.remove("filter-active"));

//     // Add active to clicked filter
//     const activeFilter = [...filters].find(f => f.getAttribute("data-filter") === filterValue);
//     if (activeFilter) activeFilter.classList.add("filter-active");

//     // Hide all tables
//     tables.forEach(table => table.classList.remove("active"));

//     // Show matching table
//     const matchedTable = document.querySelector(`.csv-table${filterValue}`);
//     if (matchedTable) matchedTable.classList.add("active");
//   }

//   // Set default table (first filter)
//   const initialFilter = filters[0].getAttribute("data-filter"); // includes dot
//   showTable(initialFilter);

//   // Set up click events
//   filters.forEach(filter => {
//     filter.addEventListener("click", function () {
//       const filterValue = this.getAttribute("data-filter");
//       showTable(filterValue);
//     });
//   });
// });

// // Assuming you initialized Isotope like this:
// var iso = new Isotope('.isotope-container', {
//   itemSelector: '.isotope-item',
//   layoutMode: 'fitRows' // or 'masonry'
// });

// // Trigger filter manually on page load
// iso.arrange({ filter: '.filter-painting' });


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
