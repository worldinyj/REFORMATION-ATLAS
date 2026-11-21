import React from "react";
import {createRoot} from "react-dom/client";
import AtlasCrossVolumeResearchPanel from "./AtlasCrossVolumeResearchPanel.jsx";
import fourth from "../../research/data/ATLAS_V475_CROSS_VOLUME_REVIEW_BUNDLE.json";
import fifth from "../../research/data/ATLAS_V476_VOL05_REVIEW_BUNDLE.json";
import routes from "../../research/data/ATLAS_V477_CROSS_VOLUME_READING_LINKS.json";
// Browser-test fixture ONLY. A boolean in a page is not server authentication.
const access=window.__V477_ACCESS__===true;
const corrupt=window.__V477_CORRUPT_SOURCE__===true;
const tamper=window.__V477_TAMPER_PATH__===true;
const mockFifth=corrupt?{...fifth,releaseGate:{...fifth.releaseGate,canShip:true}}:fifth;
const mockLinks=tamper?{...routes,editorialComparisons:routes.editorialComparisons.map((x,i)=>
 i===0?{...x,to:{...x.to,sourceIds:["UNKNOWN"]}}:x)}:routes;
createRoot(document.getElementById("root")).render(
 <AtlasCrossVolumeResearchPanel bundles={[fourth,mockFifth]}
  readingPaths={mockLinks} privatePreviewGranted={access}/>
);
