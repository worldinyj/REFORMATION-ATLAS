import React from "react";
import {createRoot} from "react-dom/client";
import AtlasFlagship1529Panel from "./AtlasFlagship1529Panel.jsx";
import scene from "../../research/data/ATLAS_PHASE0_FLAGSHIP_SCENE_1529_1540_PRIVATE_MODEL.json";
import sourcePack from "../../research/data/ATLAS_V474_REACT_READER_PACK.json";
const atlas={
  meta:{canShip:false},
  getVolume:()=>({title:"제4권 기존 연구 개요",bodyMarkdown:"구형 연구 개요"}),
  getChapter:()=>({title:"제4권 기존 연구 해설",bodyMarkdown:"구형 연구 해설"})
};
// This fixture is ONLY a browser test; it is not a deployable host authentication gate.
const granted=window.__ATLAS_V474_TEST_GRANT__===true;
const corrupt=window.__ATLAS_V474_CORRUPT_PACK__===true;
const pack=corrupt?{...sourcePack,releaseGate:{...sourcePack.releaseGate,canShip:true}}:sourcePack;
createRoot(document.getElementById("root")).render(
  <AtlasFlagship1529Panel scene={scene} atlas={atlas} readerPack={pack}
    privatePreviewGranted={granted}/>
);
