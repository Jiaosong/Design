import type { RuntimeManifest, UiTokens } from './RuntimeTypes';

export interface AuditIssue { code: string; message: string; }

export function auditRuntimeSource(manifest: RuntimeManifest, tokens: UiTokens): AuditIssue[] {
  const issues: AuditIssue[] = [];
  if (manifest.corePages.length !== 8) issues.push({ code: 'CORE_COUNT', message: 'Core pages must remain 8.' });
  if (manifest.companionPages.length !== 5) issues.push({ code: 'COMPANION_COUNT', message: 'Companion pool must remain 5.' });
  if (manifest.myBook.requiresThirteenOfThirteen) issues.push({ code: 'NO_13_OF_13', message: '13/13 completion must remain disabled.' });
  if (manifest.myBook.completionReward) issues.push({ code: 'NO_REWARD', message: 'Completion reward economy is forbidden.' });
  if (manifest.route.autoGpsRequired) issues.push({ code: 'NO_AUTO_GPS', message: 'Auto GPS cannot be required by the core flow.' });
  if (!manifest.route.offlineFirst) issues.push({ code: 'OFFLINE_FIRST', message: 'Core flow must remain offline-first.' });
  const s0 = tokens.densityTargets.S0; const s1 = tokens.densityTargets.S1; const s2 = tokens.densityTargets.S2;
  if (s0.landscapeMin < 0.85) issues.push({ code: 'S0_DENSITY', message: 'S0 landscape minimum must remain at least 85%.' });
  if (s1.landscapeMin < 0.60 || s1.landscapeMax > 0.75) issues.push({ code: 'S1_DENSITY', message: 'S1 landscape target must stay within 60–75%.' });
  if (s2.landscapeMin < 0.40 || s2.landscapeMax > 0.60) issues.push({ code: 'S2_DENSITY', message: 'S2 landscape target must stay within 40–60%.' });
  return issues;
}
