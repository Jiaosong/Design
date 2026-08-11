export type ExperienceMode = 'S0' | 'S1' | 'S2';
export type PageRole = 'CORE' | 'COMPANION';
export type ClaimType = 'FACT' | 'LOCAL_NARRATIVE' | 'DESIGN_READING';
export type PrototypeScreenId = 'S0_ONE_LINE_SKY' | 'S1_RED_ROCK_MOUTH' | 'S2_RIVER_VALLEY' | 'ROUTE' | 'MY_BOOK';

export interface ClaimLayer { type: ClaimType; text: string; evidenceStatus: string; }
export interface ReadingPage { id: string; title: string; markName?: string; chapter?: string; mode: ExperienceMode; role: PageRole; observation?: string; status: string; claimLayers?: ClaimLayer[]; }
export interface PrototypeScreen { id: PrototypeScreenId; kind: 'PAGE' | 'ROUTE' | 'BOOK'; pageId?: string; density?: ExperienceMode; }
export interface RuntimeManifest {
  version: string; authority: string[]; status: string; principles: string[];
  corePages: ReadingPage[]; companionPages: ReadingPage[]; prototypeScreens: PrototypeScreen[];
  route: { layers: string[]; priority: string[]; autoGpsRequired: boolean; offlineFirst: boolean; };
  myBook: { partialIsComplete: boolean; requiresThirteenOfThirteen: boolean; completionReward: boolean; unreadPagesBecomeRevisitInvitation: boolean; };
  returnGuard: { message: string; realTimeClaim: boolean; };
}
export interface UiTokens {
  version: string; systemName: string; colorRoles: Record<string, string>;
  densityTargets: Record<ExperienceMode, { landscapeMin: number; landscapeMax: number }>;
  hierarchy: string[]; functionalLines: string[]; claimTypes: ClaimType[];
  accessibilityTargets: { functionalTextPxMin: number; mainActionPxMin: number; colorAloneForbidden: boolean; textureBehindSmallTextForbidden: boolean; };
  forbidden: string[];
}
export interface RuntimeBundle { manifest: RuntimeManifest; tokens: UiTokens; }
