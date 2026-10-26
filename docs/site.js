(() => {
  "use strict";
  const data = window.BEYONDSUMI;
  const root = document;
  const byId = (id) => root.getElementById(id);
  const video = byId("demo-video");
  const music = byId("music-player");
  const local = ["localhost", "127.0.0.1", ""].includes(location.hostname);
  const base = local ? "demo-media/" : data.mediaBase;
  const tabs = [...root.querySelectorAll("[data-demo]")];
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function selectDemo(id, focus = false, updateHash = false) {
    const demo = data.demos.find((item) => item.id === id) || data.demos[0];
    video.pause();
    video.poster = demo.poster;
    video.src = base + demo.file;
    video.setAttribute("aria-label", `${demo.name} — ${demo.style} demo`);
    byId("video-error").hidden = true;
    for (const [name, value] of Object.entries({
      "film-style": demo.style,
      "film-name": demo.name,
      "film-kind": demo.format,
      "film-purpose": demo.purpose,
      "film-description": demo.description,
      "film-duration": demo.duration,
      "film-language": demo.language,
      "film-best": demo.best,
      "film-technique": demo.technique,
      "film-format":
        demo.id === "svg"
          ? "Full HD · music, SFX & captions"
          : "Full HD · narration & sound",
    }))
      byId(name).textContent = value;
    byId("demo-note").textContent = ["original", "dark"].includes(demo.id)
      ? "Dramatized storytelling demo. Historical scenes include creative reconstruction."
      : demo.id === "svg"
        ? "SVG artwork route shown in Sumi Dark. No narration. Story captions and sound."
        : "A fable with narrator and character dialogue. Story captions are included.";
    byId("film-download").href = base + demo.file;
    byId("film-download").download = demo.file;
    byId("error-download").href = base + demo.file;
    byId("film-panel").setAttribute("aria-labelledby", `tab-${demo.id}`);
    for (const tab of tabs) {
      const selected = tab.dataset.demo === demo.id;
      tab.setAttribute("aria-selected", String(selected));
      tab.tabIndex = selected ? 0 : -1;
      if (selected && focus) tab.focus();
    }
    if (updateHash) history.replaceState(null, "", "#watch-" + demo.id);
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () =>
      selectDemo(tab.dataset.demo, false, true),
    );
    tab.addEventListener("keydown", (event) => {
      let next;
      if (event.key === "ArrowRight") next = (index + 1) % tabs.length;
      if (event.key === "ArrowLeft")
        next = (index - 1 + tabs.length) % tabs.length;
      if (event.key === "Home") next = 0;
      if (event.key === "End") next = tabs.length - 1;
      if (next !== undefined) {
        event.preventDefault();
        selectDemo(tabs[next].dataset.demo, true, true);
      }
    });
  });
  root.querySelectorAll("[data-watch]").forEach((button) =>
    button.addEventListener("click", () => {
      selectDemo(button.dataset.watch, false, true);
      byId("films").scrollIntoView({ behavior: reduced ? "auto" : "smooth" });
    }),
  );
  video.addEventListener("error", () => {
    byId("video-error").hidden = false;
  });
  video.addEventListener("play", () => music.pause());
  music.addEventListener("play", () => video.pause());
  root.querySelectorAll("[data-mood]").forEach((button) =>
    button.addEventListener("click", () => {
      const wasPlaying = !music.paused;
      music.pause();
      const mood = button.dataset.mood;
      music.src = "assets/music/" + mood + ".mp3";
      music.setAttribute(
        "aria-label",
        `${mood} — original Python music excerpt`,
      );
      byId("music-description").textContent =
        `An 18-second excerpt from the bundled ${mood[0].toUpperCase() + mood.slice(1)} theme.`;
      root
        .querySelectorAll("[data-mood]")
        .forEach((item) =>
          item.setAttribute("aria-pressed", String(item === button)),
        );
      if (wasPlaying) music.play().catch(() => {});
    }),
  );
  byId("assistant").addEventListener("change", (event) => {
    byId("install-guide").href =
      data.repository +
      "/blob/main/skills/sumi/references/install/" +
      event.target.value +
      ".md";
  });
  byId("copy-prompt").addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(byId("starter-prompt").textContent);
      byId("copy-status").textContent = "Copied. Paste it into your assistant.";
    } catch {
      byId("copy-status").textContent =
        "Select the request above and copy it, then paste it into your assistant.";
      byId("starter-prompt").focus();
    }
  });
  const requested = location.hash.match(
    /^#watch-(original|light|dark|svg)$/,
  )?.[1];
  selectDemo(requested || "original");
  if (requested) byId("films").scrollIntoView({ behavior: "auto" });
})();
