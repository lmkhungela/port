(function () {
  // Original Slater globe is aimed at Kyiv. Offset the earth mesh so South Africa
  // sits in the same view. Do not override canvas opacity/display — GSAP owns that.
  var KYIV_LAT = 50.4501;
  var KYIV_LNG = 30.5234;
  var JNB_LAT = -26.2041;
  var JNB_LNG = 28.0473;
  var LAT_OFFSET = ((JNB_LAT - KYIV_LAT) * Math.PI) / 180;
  var LNG_OFFSET = ((JNB_LNG - KYIV_LNG) * Math.PI) / 180;

  function canvasEl() {
    return document.querySelector("canvas.webgl");
  }

  function ensureOnContact() {
    var canvas = canvasEl();
    if (!canvas) return;
    var contact = document.querySelector(".contact, .section.cc--contact, [data-wf--contact], .footer-coll");
    var page = document.querySelector(".page-wrapper");
    var show = false;
    if (contact) {
      var r = contact.getBoundingClientRect();
      show = r.bottom > 0 && r.top < (window.innerHeight || 800) * 1.15;
    }
    // Contact chrome is on every Cosmos page; keep the canvas in the tree.
    canvas.style.pointerEvents = "none";
    if (canvas.style.display === "none") canvas.style.display = "";
    if (show && canvas.style.visibility === "hidden") canvas.style.visibility = "";
  }

  function hookEarth(mesh) {
    if (!mesh || mesh.userData.saHooked) return;
    mesh.userData.saHooked = true;
    var euler = mesh.rotation;
    var rawX = euler.x;
    var rawY = euler.y;
    Object.defineProperty(euler, "x", {
      configurable: true,
      get: function () {
        return rawX + LAT_OFFSET;
      },
      set: function (v) {
        rawX = v;
      },
    });
    Object.defineProperty(euler, "y", {
      configurable: true,
      get: function () {
        return rawY + LNG_OFFSET;
      },
      set: function (v) {
        rawY = v;
      },
    });
  }

  function findEarth() {
    if (!window.scene) return null;
    var found = null;
    window.scene.traverse(function (obj) {
      if (found) return;
      var g = obj.geometry;
      if (obj.isMesh && g && g.type === "SphereGeometry" && g.parameters && Math.abs(g.parameters.radius - 6) < 0.01) {
        found = obj;
      }
    });
    return found;
  }

  function tick() {
    hookEarth(findEarth());
    ensureOnContact();
  }

  function start() {
    var n = 0;
    var id = setInterval(function () {
      tick();
      n += 1;
      if (n > 160) clearInterval(id);
    }, 250);
    window.addEventListener("scroll", ensureOnContact, { passive: true });
    window.addEventListener("resize", ensureOnContact);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
  window.addEventListener("load", function () {
    tick();
  });
})();
