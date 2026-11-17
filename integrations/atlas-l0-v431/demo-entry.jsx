/* V4.31 localhost-only React smoke entry. Do not copy this payload import into a public app. */
import React from "react";
import {createRoot} from "react-dom/client";
import AtlasL0Panel from "./AtlasL0Panel.jsx";
import payload from "../../handoff/V429_AI_STUDIO_PRIVATE_L0_CONTENT_IMPORT.json";

const privateLocalDemo = ["127.0.0.1","localhost"].includes(location.hostname);
const show = privateLocalDemo && !new URLSearchParams(location.search).has("blocked");
createRoot(document.querySelector("#app-root")).render(
  <AtlasL0Panel payload={payload} stagingGranted={show}/>
);
