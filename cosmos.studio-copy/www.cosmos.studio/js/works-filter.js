(function () {
  function ready(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }

  ready(function () {
    var form = document.querySelector(".works-filter_list");
    var items = Array.prototype.slice.call(document.querySelectorAll(".works-list .work"));
    if (!form || !items.length) return;

    function setActive(label) {
      form.querySelectorAll(".filter-button").forEach(function (btn) {
        btn.classList.toggle("is--active", btn.getAttribute("data-filter") === label);
        var input = btn.querySelector('input[type="radio"]');
        if (input) input.checked = btn.getAttribute("data-filter") === label;
      });
      items.forEach(function (item) {
        var cat = item.getAttribute("data-category") || "";
        var show = label === "all" || cat === label;
        item.style.display = show ? "" : "none";
      });
      var visible = items.filter(function (item) {
        return item.style.display !== "none";
      }).length;
      var allCount = form.querySelector(".filter-count_all-works");
      if (allCount) allCount.innerHTML = String(items.length) + "<br/>";
      form.querySelectorAll(".filter-button[data-filter]").forEach(function (btn) {
        var key = btn.getAttribute("data-filter");
        var countEl = btn.querySelector(".filter-count");
        if (!countEl || key === "all") return;
        var n = items.filter(function (item) {
          return item.getAttribute("data-category") === key;
        }).length;
        countEl.innerHTML = String(n) + "<br/>";
      });
    }

    form.addEventListener("click", function (e) {
      var btn = e.target.closest(".filter-button");
      if (!btn) return;
      e.preventDefault();
      setActive(btn.getAttribute("data-filter") || "all");
    });

    setActive("all");
  });
})();
