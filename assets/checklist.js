(function () {
  document.querySelectorAll("[data-check-key]").forEach(function (form) {
    var key = "htf-check:" + form.getAttribute("data-check-key");
    var saved = {};
    try {
      saved = JSON.parse(localStorage.getItem(key) || "{}");
    } catch (e) {
      saved = {};
    }
    form.querySelectorAll("[data-check]").forEach(function (box) {
      var id = box.getAttribute("data-check");
      box.checked = !!saved[id];
      box.addEventListener("change", function () {
        saved[id] = box.checked;
        localStorage.setItem(key, JSON.stringify(saved));
      });
    });
  });
})();
