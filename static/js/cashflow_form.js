document.addEventListener("DOMContentLoaded", function () {
  const typeSelect = document.getElementById("id_type");
  const categorySelect = document.getElementById("id_category");
  const subcategorySelect = document.getElementById("id_subcategory");

  // 🧩 При изменении типа — обновить категории
  typeSelect.addEventListener("change", function () {
    const typeId = this.value;

    categorySelect.innerHTML = '<option value="">---------</option>';
    subcategorySelect.innerHTML = '<option value="">---------</option>'; // сброс подкатегорий тоже

    if (!typeId) return;

    fetch(`/ajax/load-categories/?type_id=${typeId}`)
      .then(response => response.json())
      .then(data => {
        data.categories.forEach(cat => {
          const option = document.createElement("option");
          option.value = cat.id;
          option.textContent = cat.name;
          categorySelect.appendChild(option);
        });
      });
  });

  // 🧩 При изменении категории — обновить подкатегории
  categorySelect.addEventListener("change", function () {
    const categoryId = this.value;

    subcategorySelect.innerHTML = '<option value="">---------</option>';
    if (!categoryId) return;

    fetch(`/ajax/load-subcategories/?category_id=${categoryId}`)
      .then(response => response.json())
      .then(data => {
        data.subcategories.forEach(sub => {
          const option = document.createElement("option");
          option.value = sub.id;
          option.textContent = sub.name;
          subcategorySelect.appendChild(option);
        });
      });
  });
});