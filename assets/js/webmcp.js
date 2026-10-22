/**
 * WebMCP — exposes this site's actions as tools to an in-browser AI agent.
 * https://webmachinelearning.github.io/webmcp/
 *
 * Deliberately standalone rather than part of app.js: app.js returns early if
 * GSAP is missing, and tool registration shouldn't depend on an animation
 * library loading.
 *
 * The API is young and still changing, so every call is feature-detected and
 * wrapped — a browser without it, or a future rename, degrades to doing
 * nothing rather than throwing on page load.
 */
(function () {
  "use strict";

  var ctx = typeof document !== "undefined" && document.modelContext;
  if (!ctx || typeof ctx.registerTool !== "function") return;

  // Tools live as long as the page does. The spec takes an AbortSignal for
  // unregistration, so wire one to pagehide rather than leaking registrations
  // across bfcache navigations.
  var controller = new AbortController();
  addEventListener("pagehide", function () { controller.abort(); }, { once: true });
  var options = { signal: controller.signal };

  var DATA_URL = "/agent-data.json";
  var cache = null;
  function data() {
    if (!cache) {
      cache = fetch(DATA_URL, { headers: { Accept: "application/json" } })
        .then(function (r) {
          if (!r.ok) throw new Error("agent-data unavailable");
          return r.json();
        })
        .catch(function (err) { cache = null; throw err; });
    }
    return cache;
  }

  /** MCP tool results are a content array, not a bare value. */
  function text(value) {
    return {
      content: [{
        type: "text",
        text: typeof value === "string" ? value : JSON.stringify(value, null, 2),
      }],
    };
  }

  function fail(message) {
    return { content: [{ type: "text", text: message }], isError: true };
  }

  var tools = [
    {
      name: "list_projects",
      description:
        "List the projects in this portfolio, with the stack used, the year, " +
        "and a link to the full write-up. Optionally filter by technology.",
      inputSchema: {
        type: "object",
        properties: {
          technology: {
            type: "string",
            description:
              "Case-insensitive filter, matched against the stack and " +
              "category, e.g. 'React', 'Django', 'PostgreSQL'.",
          },
        },
      },
      execute: async function (args) {
        var site = await data();
        var q = (args && args.technology ? String(args.technology) : "").toLowerCase();
        var hits = site.projects.filter(function (p) {
          if (!q) return true;
          return (p.stack + " " + p.category).toLowerCase().indexOf(q) !== -1;
        });
        if (!hits.length) {
          return text("No projects match \"" + args.technology + "\". " +
            "Known stacks: " + site.projects.map(function (p) { return p.stack; }).join("; "));
        }
        return text(hits);
      },
    },

    {
      name: "get_profile",
      description:
        "Who this site belongs to: name, current role, location, contact " +
        "details, work history and technical skills.",
      inputSchema: { type: "object", properties: {} },
      execute: async function () {
        var site = await data();
        return text({
          profile: site.profile,
          skills: site.skills,
          experience: site.experience,
        });
      },
    },

    {
      name: "read_page",
      description:
        "Read any page of this site as clean markdown — no navigation or " +
        "styling. Use list_pages first if unsure which pages exist.",
      inputSchema: {
        type: "object",
        required: ["page"],
        properties: {
          page: {
            type: "string",
            description:
              "Page name, e.g. 'about', 'resume', 'skills', 'work', " +
              "'contact', or a project slug such as 'consentx'.",
          },
        },
      },
      execute: async function (args) {
        var site = await data();
        var want = String((args && args.page) || "").toLowerCase().trim()
          .replace(/\.(html|md)$/, "");
        var match = site.pages.find(function (p) {
          return p.title.toLowerCase() === want ||
                 p.url.toLowerCase().indexOf("/" + want + ".html") !== -1;
        });
        if (!match) {
          var project = site.projects.find(function (p) {
            return p.slug === want || p.name.toLowerCase() === want;
          });
          if (project) match = { markdown: project.url.replace(/\.html$/, ".md") };
        }
        if (!match) {
          return fail("No page named \"" + want + "\". Available: " +
            site.pages.map(function (p) { return p.title.toLowerCase(); }).join(", ") +
            ", or a project slug: " +
            site.projects.map(function (p) { return p.slug; }).join(", "));
        }
        var res = await fetch(match.markdown, { headers: { Accept: "text/markdown" } });
        if (!res.ok) return fail("Could not read that page.");
        return text(await res.text());
      },
    },

    {
      name: "send_message",
      description:
        "Send a message to the owner of this site via the contact form. " +
        "Only use this when the person has explicitly asked to get in touch, " +
        "and confirm the wording with them first — it delivers a real email.",
      inputSchema: {
        type: "object",
        required: ["name", "email", "message"],
        properties: {
          name: { type: "string", description: "Sender's name." },
          email: { type: "string", description: "Sender's email — used as reply-to." },
          company: { type: "string", description: "Optional company name." },
          message: { type: "string", description: "The message body." },
        },
      },
      execute: async function (args) {
        var res = await fetch("/api/contact", {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify({
            name: args.name,
            email: args.email,
            company: args.company || "",
            message: args.message,
          }),
        });
        var body = await res.json().catch(function () { return {}; });
        if (res.ok) return text("Message sent. Pradeep replies within 24 hours.");
        if (res.status === 400) return fail("Rejected: " + (body.error || "invalid input"));
        return fail(
          "Could not send right now. Email " +
          "pradeepmaurya2002@gmail.com directly instead."
        );
      },
    },
  ];

  tools.forEach(function (tool) {
    try {
      var result = ctx.registerTool(tool, options);
      if (result && typeof result.catch === "function") {
        result.catch(function (err) {
          console.warn("[webmcp] could not register", tool.name, err);
        });
      }
    } catch (err) {
      console.warn("[webmcp] registerTool threw for", tool.name, err);
    }
  });
})();
