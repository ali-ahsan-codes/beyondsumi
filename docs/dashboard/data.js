(() => {
  const config = window.BEYONDSUMI;
  const demo = config.demos.find((d) => d.id === "svg");
  const local = ["localhost", "127.0.0.1", ""].includes(location.hostname);
  window.SUMI_DELIVERY = {
    brand: "Beyondsumi",
    title: "The Last Blossom",
    subtitle:
      "A Sumi Dark story made with SVG artwork, music, sound effects and captions.",
    catalogue: config.demos
      .filter((d) => d.id !== "svg")
      .map((d) => ({ name: d.style, description: d.purpose })),
    recreation_context:
      "Public showcase only. The editable film project and personal production history are not included. Ask the viewer for their own story and duration before producing a new film.",
    films: [
      {
        width: demo.width,
        height: demo.height,
        fps: demo.fps,
        duration: demo.seconds,
        bytes: demo.bytes,
        audio: true,
        sha256: demo.sha256,
        style: "Sumi Dark",
        description:
          "Original SVG scenes and a sound-led story. No image-generation or video-generation API.",
        status: "demo",
        review_note:
          "A finished showcase film. Start your own project with the included skill and guides.",
        file: local ? "media/beyondsumi-svg.mp4" : config.mediaBase + demo.file,
        download_name: demo.file,
        poster: "media/last-blossom.jpg",
      },
    ],
  };
})();
