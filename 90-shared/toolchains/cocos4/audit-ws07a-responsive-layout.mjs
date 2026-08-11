#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const reportPath = path.resolve(process.argv[2] ?? '');
const outputPath = path.resolve(process.argv[3] ?? '');
if (!reportPath || !fs.existsSync(reportPath)) throw new Error(`runtime capture report missing: ${reportPath}`);
if (!outputPath) throw new Error('responsive audit output path required');

const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
const failures = [];
const observations = [];
const EPS = 0.75;
const MIN_TOUCH_PX = 44;

const navPaths = [
  'PrototypeNav/NavS0',
  'PrototypeNav/NavS1',
  'PrototypeNav/NavS2',
  'PrototypeNav/NavRoute',
  'PrototypeNav/NavBook',
];
const actionPaths = [
  'ReadingOverlay/RecordButton',
  'ReadingOverlay/RevealButton',
  'S2_RiverValley/RevealRoot/CloseReveal',
];
const interactivePaths = [...navPaths, ...actionPaths];

function rectOverlap(a, b) {
  if (!a?.rect || !b?.rect || !a.active || !b.active) return false;
  const ar = a.rect; const br = b.rect;
  return ar.x < br.x + br.width && ar.x + ar.width > br.x && ar.y < br.y + br.height && ar.y + ar.height > br.y;
}

function addFailure(code, viewport, state, detail) {
  failures.push({ code, viewport, state, detail });
}

function pairwiseActiveOverlap(byPath, paths, viewport, state) {
  for (let i = 0; i < paths.length; i += 1) {
    for (let j = i + 1; j < paths.length; j += 1) {
      const a = byPath.get(paths[i]);
      const b = byPath.get(paths[j]);
      if (rectOverlap(a, b)) addFailure('INTERACTIVE_HITBOX_OVERLAP', viewport, state, { a: paths[i], b: paths[j] });
    }
  }
}

if (report.gate !== 'RUNTIME_CAPTURE_PASS') failures.push({ code: 'RUNTIME_CAPTURE_NOT_PASS', gate: report.gate });
if ((report.failures ?? []).length) failures.push({ code: 'RUNTIME_CAPTURE_FAILURES_PRESENT', failures: report.failures });

for (const viewport of report.viewports ?? []) {
  for (const [stateName, state] of Object.entries(viewport.states ?? {})) {
    const canvas = state.canvas ?? {};
    const pxPerUnit = Number(canvas.pxPerUnit ?? 0);
    const canvasWidth = Number(canvas.width ?? 0);
    const canvasHeight = Number(canvas.height ?? 0);
    const byPath = new Map((state.layout ?? []).map((item) => [item.path, item]));

    if (!(pxPerUnit > 0 && canvasWidth > 0 && canvasHeight > 0)) {
      addFailure('CANVAS_METRICS_INVALID', viewport.id, stateName, canvas);
      continue;
    }

    pairwiseActiveOverlap(byPath, navPaths, viewport.id, stateName);
    pairwiseActiveOverlap(byPath, actionPaths, viewport.id, stateName);

    for (const pathValue of interactivePaths) {
      const item = byPath.get(pathValue);
      if (!item?.active || !item.rect) continue;
      const rect = item.rect;
      const outside = rect.x < -EPS || rect.y < -EPS || rect.x + rect.width > canvasWidth + EPS || rect.y + rect.height > canvasHeight + EPS;
      if (outside) addFailure('INTERACTIVE_OUT_OF_CANVAS', viewport.id, stateName, { path: pathValue, rect, canvasWidth, canvasHeight });
      const physicalWidth = rect.width * pxPerUnit;
      const physicalHeight = rect.height * pxPerUnit;
      if (physicalWidth + EPS < MIN_TOUCH_PX || physicalHeight + EPS < MIN_TOUCH_PX) {
        addFailure('INTERACTIVE_TOUCH_TARGET_LT_44PX', viewport.id, stateName, { path: pathValue, physicalWidth, physicalHeight });
      }
    }

    if (stateName === 's2Reveal' && canvas.profile === 'LANDSCAPE') {
      if (state.readingOverlayActive) addFailure('LANDSCAPE_REVEAL_READING_OVERLAY_VISIBLE', viewport.id, stateName, true);
      observations.push({ viewport: viewport.id, state: stateName, code: 'LANDSCAPE_REVEAL_RECLAIMS_READING_OVERLAY_SPACE', pass: !state.readingOverlayActive });
    }
  }
}

const audit = {
  gate: failures.length === 0 ? 'RESPONSIVE_INTERACTION_LAYOUT_PASS' : 'RESPONSIVE_INTERACTION_LAYOUT_FAIL',
  runtimeGate: report.gate,
  viewportCount: report.viewports?.length ?? 0,
  screenshotCount: (report.viewports ?? []).reduce((sum, viewport) => sum + (viewport.captures?.length ?? 0), 0),
  touchTargetMinimumPx: MIN_TOUCH_PX,
  rawLabelAabbDiagnostics: report.visualIssues?.length ?? 0,
  note: 'Raw Label/UITransform AABB overlap diagnostics are retained as non-gating evidence because Cocos Label layout boxes can exceed rendered glyph bounds. Screenshot visual review remains required for text hierarchy/occlusion.',
  observations,
  failures,
};

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, `${JSON.stringify(audit, null, 2)}\n`);
console.log(`${audit.gate}: viewports=${audit.viewportCount} screenshots=${audit.screenshotCount} rawLabelAabbDiagnostics=${audit.rawLabelAabbDiagnostics}`);
if (failures.length) {
  console.error(JSON.stringify(failures, null, 2));
  process.exitCode = 65;
}
