(function () {
  function toLocal(url) {
    if (!url || typeof url !== "string") return url;
    var raw = url.trim();
    if (raw.charAt(0) === "#" || raw.indexOf("mailto:") === 0 || raw.indexOf("tel:") === 0) return url;
    if (raw.indexOf("javascript:") === 0) return url;

    var cosmos = /^(https?:)?\/\/(www\.)?cosmos\.studio/i;
    if (cosmos.test(raw)) {
      try {
        var abs = raw.indexOf("//") === 0 ? location.protocol + raw : raw;
        var parsed = new URL(abs);
        raw = parsed.pathname + parsed.search + parsed.hash;
      } catch (e) {
        raw = raw.replace(cosmos, "");
      }
    }

    var pathOnly = raw.split("?")[0].split("#")[0];
    var suffix = raw.slice(pathOnly.length);
    var file = pathOnly.replace(/\/+$/, "");
    var base = document.querySelector("base");
    var rootHint = (base && base.href) || location.href;

    function join(rel) {
      try {
        return new URL(rel + suffix, rootHint).href;
      } catch (e) {
        return rel + suffix;
      }
    }

    if (/\/works\/?$/.test(file) || file === "works" || file === "/works") {
      return join(file.indexOf("/") === 0 || file.indexOf("http") === 0 ? "works.html" : "works.html");
    }

    var proj = file.match(/\/projects\/([^/.]+)\/?$/);
    if (proj) {
      var fromProjects = /\/projects\//.test(location.pathname);
      return join((fromProjects ? "" : "projects/") + proj[1] + ".html");
    }

    if (file === "/projects" || /\/projects\/?$/.test(file)) {
      return join("works.html");
    }

    return url;
  }

  function patchAnchor(a) {
    if (!a || !a.getAttribute) return;
    var href = a.getAttribute("href");
    if (!href) return;
    var next = toLocal(href);
    if (next && next !== href) a.setAttribute("href", next);
  }

  function scan(root) {
    (root || document).querySelectorAll("a[href]").forEach(patchAnchor);
  }

  document.addEventListener(
    "click",
    function (e) {
      var a = e.target && e.target.closest ? e.target.closest("a[href]") : null;
      if (!a) return;
      patchAnchor(a);
      var href = a.getAttribute("href");
      if (!href) return;
      if (/cosmos\.studio/i.test(href) || /\/works\/?$/.test(href.split("?")[0]) || /\/projects\/[^/.]+\/?$/.test(href.split("?")[0])) {
        e.preventDefault();
        location.href = toLocal(href);
      }
    },
    true
  );

  if (window.fetch) {
    var origFetch = window.fetch;
    window.fetch = function (input, init) {
      if (typeof input === "string") input = toLocal(input);
      else if (input && typeof Request !== "undefined" && input instanceof Request) {
        input = new Request(toLocal(input.url), input);
      }
      return origFetch.call(this, input, init);
    };
  }

  if (window.XMLHttpRequest) {
    var open = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function (method, url) {
      if (typeof url === "string") arguments[1] = toLocal(url);
      return open.apply(this, arguments);
    };
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      scan(document);
    });
  } else {
    scan(document);
  }

  new MutationObserver(function (muts) {
    muts.forEach(function (m) {
      m.addedNodes.forEach(function (n) {
        if (n.nodeType !== 1) return;
        if (n.matches && n.matches("a[href]")) patchAnchor(n);
        if (n.querySelectorAll) scan(n);
      });
    });
  }).observe(document.documentElement, { childList: true, subtree: true });
})();
