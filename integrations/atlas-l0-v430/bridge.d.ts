/**
 * ATLAS V4.30 private L0 data bridge. Types describe consumer output ONLY.
 * Host authentication and access control must be implemented in the actual app.
 */
export const CONTRACT_VERSION: "V4.30";
export type AtlasVolumeId = "VOL-01"|"VOL-02"|"VOL-03"|"VOL-04"|"VOL-05"|"VOL-06"|"VOL-07"|"VOL-08";
export type AtlasThemeId = "T415-01"|"T415-02"|"T415-03"|"T415-04"|"T415-05"|"T415-06";
export type AtlasChapterId = "INTRO-1"|"INTRO-2"|"INTRO-3"|"INTRO-4"|"INTRO-5"|"INTRO-6";
export type AtlasRoute = Readonly<{kind:"VOLUME"|"THEME"|"CHAPTER",id:string}>;
export interface AtlasVolume {
  readonly kind:"VOLUME"; readonly id:AtlasVolumeId; readonly order:number; readonly title:string;
  readonly period:string; readonly leadQuestion:string; readonly description:string; readonly bodyMarkdown:string;
  readonly isThematicArchive:boolean; readonly relatedThemeIds:readonly AtlasThemeId[];
}
export interface AtlasThemeLink {
  readonly targetKind:"VOLUME";readonly targetId:Exclude<AtlasVolumeId,"VOL-08">;
  readonly title:string;readonly relation:"CORE_CASE"|"CONTEXT_BRIDGE"|"LIMITED_CONTEXT_NOT_DOCTRINE";
  readonly relationLabel:string;
}
export interface AtlasTheme {
  readonly kind:"THEME";readonly id:AtlasThemeId;readonly order:number;readonly title:string;
  readonly leadQuestion:string;readonly bodyMarkdown:string;readonly links:readonly AtlasThemeLink[];
}
export interface AtlasChapter {
  readonly kind:"CHAPTER";readonly id:AtlasChapterId;readonly order:number;
  readonly title:string;readonly bodyMarkdown:string;
}
export interface AtlasSearchResult {
  readonly kind:"VOLUME"|"THEME"|"CHAPTER";readonly id:string;readonly title:string;readonly excerpt:string;
  readonly navigation:AtlasRoute;
}
export interface AtlasL0Bridge {
  readonly contractVersion:"V4.30";
  readonly contentVersion:"V4.23";
  readonly importVersion:"V4.29";
  readonly sourceGitBlobSha:string;
  readonly runtimeMode:"PRIVATE_STAGING_ONLY";
  readonly canPublish:false;
  readonly canMergeMain:false;
  readonly mayCollectResponses:false;
  readonly hostAccessControlNotImplementedByAdapter:true;
  readonly counts:Readonly<{volumes:8,themes:6,chapters:6,themeToVolumeLinks:42}>;
  readonly catalog:Readonly<{
    volumes:readonly Readonly<{id:AtlasVolumeId,kind:string,title:string,period:string,description:string,isThematicArchive:boolean}>[];
    themes:readonly Readonly<{id:AtlasThemeId,title:string,leadQuestion:string}>[];
    chapters:readonly Readonly<{id:AtlasChapterId,title:string,order:number}>[];
  }>;
  readonly readerIntro:Readonly<{id:"INTRO-V421",title:string,readingTimeTargetMinutes:10,readingTimeMeasured:false,prefaceMarkdown:string}>;
  getVolume(id:string):AtlasVolume|null;
  getTheme(id:string):AtlasTheme|null;
  getChapter(id:string):AtlasChapter|null;
  resolve(target:AtlasRoute):AtlasVolume|AtlasTheme|AtlasChapter|null;
  search(query:string,options?:{limit?:number}):readonly AtlasSearchResult[];
}
/**
 * The hostDeclaration flag states a prerequisite; it does NOT check authentication.
 * Real app must enforce private access before calling the bridge or rendering any output.
 * Never expose the JSON or the adapter from a publicly deployed route.
 */
export function createAtlasL0ReadOnlyBridge(
  packageObject:unknown,
  hostDeclaration:{environment:"PRIVATE_STAGING",accessControlDeclared:true}
):AtlasL0Bridge;
