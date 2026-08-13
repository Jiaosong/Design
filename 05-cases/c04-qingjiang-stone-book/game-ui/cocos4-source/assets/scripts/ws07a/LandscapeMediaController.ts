import {
  _decorator,
  Color,
  Component,
  find,
  ImageAsset,
  JsonAsset,
  Label,
  Node,
  resources,
  Sprite,
  SpriteFrame,
  UITransform,
  Vec2,
  warn,
} from 'cc';
import { RuntimeStore } from './RuntimeStore';

const { ccclass } = _decorator;
const MEDIA_MANIFEST_PATH = 'c04/ws07a/visual-media-manifest';
const MEDIA_BRIDGE_KEY = '__OLEANDER_C04_MEDIA__';

interface VisualMediaAsset {
  assetId: string;
  pageId: string;
  resourcePath: string;
  sourceWidth: number;
  sourceHeight: number;
  rightsGate: string;
  nodeGate: string;
  techGate: string;
  usageGate: string;
}

interface VisualMediaManifest {
  version: string;
  status: string;
  activeExperiment: {
    id: string;
    pageId: string;
    screenId: string;
    variant: string;
    assetId: string;
  };
  assets: VisualMediaAsset[];
}

interface TextProtectionSnapshot {
  applied: boolean;
  titleShadow: boolean;
  observationShadow: boolean;
  returnGuardShadow: boolean;
  returnGuardColor: [number, number, number, number];
}

interface MediaSnapshot {
  ready: boolean;
  manifestStatus: string;
  experimentId: string;
  variant: string;
  assetId: string;
  pageId: string;
  currentPageId?: string;
  visible: boolean;
  usageGate: string;
  techGate: string;
  nodeGate: string;
  sourceWidth: number;
  sourceHeight: number;
  renderedWidth: number;
  renderedHeight: number;
  textProtection: TextProtectionSnapshot;
}

interface MediaBridge {
  ready: boolean;
  showActiveExperiment: () => MediaSnapshot;
  snapshot: () => MediaSnapshot;
}

interface LabelStyleSnapshot {
  color: Color;
  enableShadow: boolean;
  shadowColor: Color;
  shadowOffset: Vec2;
  shadowBlur: number;
}

function loadJson<T>(path: string): Promise<T> {
  return new Promise<T>((resolve, reject) => {
    resources.load(path, JsonAsset, (err, asset) => {
      if (err) { reject(err); return; }
      if (!asset?.json) { reject(new Error(`JSON asset has no payload: ${path}`)); return; }
      resolve(asset.json as T);
    });
  });
}

function loadImage(path: string): Promise<ImageAsset> {
  return new Promise<ImageAsset>((resolve, reject) => {
    resources.load(path, ImageAsset, (err, asset) => {
      if (err) { reject(err); return; }
      if (!asset) { reject(new Error(`Image asset missing: ${path}`)); return; }
      resolve(asset);
    });
  });
}

@ccclass('C04WS07ALandscapeMediaController')
export class LandscapeMediaController extends Component {
  private imageNode: Node | null = null;
  private hintNode: Node | null = null;
  private sprite: Sprite | null = null;
  private manifest: VisualMediaManifest | null = null;
  private activeAsset: VisualMediaAsset | null = null;
  private ready = false;
  private lastLayoutSignature = '';
  private textStyleBaselines = new Map<Label, LabelStyleSnapshot>();
  private textProtectionApplied = false;

  protected start(): void {
    this.imageNode = find('S0_OneLineSky/LandscapeImage', this.node);
    this.hintNode = find('S0_OneLineSky/ScreenHint', this.node);
    if (this.imageNode) {
      this.sprite = this.imageNode.getComponent(Sprite) ?? this.imageNode.addComponent(Sprite);
      this.imageNode.setSiblingIndex(0);
      this.imageNode.active = false;
    }
    this.installBridge();
    void this.bootstrap();
  }

  protected lateUpdate(): void {
    this.ensureTextStyleBaselines();
    this.syncVisibility();
    this.applyCoverLayout(false);
  }

  protected onDestroy(): void {
    this.applyPhotoTextProtection(false);
    const root = globalThis as unknown as Record<string, unknown>;
    delete root[MEDIA_BRIDGE_KEY];
  }

  private async bootstrap(): Promise<void> {
    try {
      const manifest = await loadJson<VisualMediaManifest>(MEDIA_MANIFEST_PATH);
      const active = manifest.assets.find((asset) => asset.assetId === manifest.activeExperiment.assetId);
      if (!active) throw new Error(`active visual media asset missing: ${manifest.activeExperiment.assetId}`);
      if (active.pageId !== manifest.activeExperiment.pageId) throw new Error('visual media page/experiment mismatch');
      if (active.usageGate !== 'RESEARCH_PROTOTYPE_ONLY') throw new Error(`unsupported visual media usage gate: ${active.usageGate}`);

      const image = await loadImage(active.resourcePath);
      if (!this.sprite) throw new Error('LandscapeImage Sprite component missing');
      this.sprite.spriteFrame = SpriteFrame.createWithImage(image);
      this.sprite.sizeMode = Sprite.SizeMode.CUSTOM;
      this.manifest = manifest;
      this.activeAsset = active;
      this.ready = true;
      const bridge = this.getBridge();
      if (bridge) bridge.ready = true;
      this.syncVisibility();
      this.applyCoverLayout(true);
    } catch (error) {
      warn('[C04 Case Exploration] landscape media bootstrap failed', error);
    }
  }

  private showActiveExperiment(): MediaSnapshot {
    if (!this.ready || !this.manifest || !this.activeAsset) return this.snapshot();
    const page = RuntimeStore.getPage(this.activeAsset.pageId);
    if (!page) {
      warn(`[C04 Case Exploration] visual experiment page missing: ${this.activeAsset.pageId}`);
      return this.snapshot();
    }

    RuntimeStore.setScreen('S0_ONE_LINE_SKY');
    RuntimeStore.setCurrentPage(page.id);
    RuntimeStore.setReveal(false);

    const roots = ['S0_OneLineSky', 'S1_RedRockMouth', 'S2_RiverValley', 'Route', 'MyBook'];
    for (const rootName of roots) {
      const root = find(rootName, this.node);
      if (root) root.active = rootName === 'S0_OneLineSky';
    }
    const overlay = find('ReadingOverlay', this.node);
    if (overlay) overlay.active = true;
    const title = find('ReadingOverlay/PageTitle', this.node)?.getComponent(Label);
    const observation = find('ReadingOverlay/Observation', this.node)?.getComponent(Label);
    if (title) title.string = page.title;
    if (observation) observation.string = page.observation ?? '';
    const record = find('ReadingOverlay/RecordButton', this.node);
    const reveal = find('ReadingOverlay/RevealButton', this.node);
    const revealRoot = find('S2_RiverValley/RevealRoot', this.node);
    if (record) record.active = false;
    if (reveal) reveal.active = false;
    if (revealRoot) revealRoot.active = false;

    this.syncVisibility();
    this.applyCoverLayout(true);
    return this.snapshot();
  }

  private syncVisibility(): void {
    if (!this.imageNode || !this.activeAsset) return;
    const visible = this.ready
      && RuntimeStore.snapshot.currentPageId === this.activeAsset.pageId
      && RuntimeStore.snapshot.currentScreen === 'S0_ONE_LINE_SKY';
    this.imageNode.active = visible;
    if (this.hintNode) this.hintNode.active = !visible;
    this.applyPhotoTextProtection(visible);
  }

  private ensureTextStyleBaselines(): void {
    if (this.textStyleBaselines.size > 0) return;
    for (const path of ['ReadingOverlay/PageTitle', 'ReadingOverlay/Observation', 'ReturnGuard/Label']) {
      const label = find(path, this.node)?.getComponent(Label);
      if (!label) continue;
      this.textStyleBaselines.set(label, {
        color: new Color(label.color.r, label.color.g, label.color.b, label.color.a),
        enableShadow: label.enableShadow,
        shadowColor: new Color(label.shadowColor.r, label.shadowColor.g, label.shadowColor.b, label.shadowColor.a),
        shadowOffset: new Vec2(label.shadowOffset.x, label.shadowOffset.y),
        shadowBlur: label.shadowBlur,
      });
    }
  }

  private applyPhotoTextProtection(visible: boolean): void {
    this.ensureTextStyleBaselines();
    if (visible && this.textProtectionApplied) return;
    if (!visible && !this.textProtectionApplied) return;

    const title = find('ReadingOverlay/PageTitle', this.node)?.getComponent(Label) ?? null;
    const observation = find('ReadingOverlay/Observation', this.node)?.getComponent(Label) ?? null;
    const returnGuard = find('ReturnGuard/Label', this.node)?.getComponent(Label) ?? null;

    if (visible) {
      for (const label of [title, observation]) {
        if (!label) continue;
        label.enableShadow = true;
        label.shadowColor = new Color(0, 0, 0, 180);
        label.shadowOffset = new Vec2(0, -2);
        label.shadowBlur = 2;
      }
      if (returnGuard) {
        returnGuard.color = new Color(255, 255, 255, 225);
        returnGuard.enableShadow = true;
        returnGuard.shadowColor = new Color(0, 0, 0, 215);
        returnGuard.shadowOffset = new Vec2(0, -1);
        returnGuard.shadowBlur = 2;
      }
      this.textProtectionApplied = true;
      return;
    }

    for (const [label, baseline] of this.textStyleBaselines) {
      label.color = new Color(baseline.color.r, baseline.color.g, baseline.color.b, baseline.color.a);
      label.enableShadow = baseline.enableShadow;
      label.shadowColor = new Color(baseline.shadowColor.r, baseline.shadowColor.g, baseline.shadowColor.b, baseline.shadowColor.a);
      label.shadowOffset = new Vec2(baseline.shadowOffset.x, baseline.shadowOffset.y);
      label.shadowBlur = baseline.shadowBlur;
    }
    this.textProtectionApplied = false;
  }

  private applyCoverLayout(force: boolean): void {
    if (!this.ready || !this.imageNode || !this.activeAsset || !this.imageNode.active) return;
    const canvas = this.node.getComponent(UITransform);
    if (!canvas) return;
    const width = canvas.contentSize.width;
    const height = canvas.contentSize.height;
    if (width <= 0 || height <= 0) return;
    const signature = `${width.toFixed(2)}x${height.toFixed(2)}:${this.activeAsset.assetId}`;
    if (!force && signature === this.lastLayoutSignature) return;
    this.lastLayoutSignature = signature;

    const sourceAspect = this.activeAsset.sourceWidth / this.activeAsset.sourceHeight;
    const canvasAspect = width / height;
    let renderedWidth: number;
    let renderedHeight: number;
    if (canvasAspect > sourceAspect) {
      renderedWidth = width;
      renderedHeight = width / sourceAspect;
    } else {
      renderedHeight = height;
      renderedWidth = height * sourceAspect;
    }
    const transform = this.imageNode.getComponent(UITransform) ?? this.imageNode.addComponent(UITransform);
    transform.setContentSize(renderedWidth, renderedHeight);
    this.imageNode.setPosition(0, 0, 0);
  }

  private installBridge(): void {
    const bridge: MediaBridge = {
      ready: false,
      showActiveExperiment: () => this.showActiveExperiment(),
      snapshot: () => this.snapshot(),
    };
    const root = globalThis as unknown as Record<string, unknown>;
    root[MEDIA_BRIDGE_KEY] = bridge;
  }

  private getBridge(): MediaBridge | null {
    const root = globalThis as unknown as Record<string, unknown>;
    return (root[MEDIA_BRIDGE_KEY] as MediaBridge | undefined) ?? null;
  }

  private textProtectionSnapshot(): TextProtectionSnapshot {
    const title = find('ReadingOverlay/PageTitle', this.node)?.getComponent(Label) ?? null;
    const observation = find('ReadingOverlay/Observation', this.node)?.getComponent(Label) ?? null;
    const returnGuard = find('ReturnGuard/Label', this.node)?.getComponent(Label) ?? null;
    const guardColor = returnGuard?.color ?? new Color(0, 0, 0, 0);
    return {
      applied: this.textProtectionApplied,
      titleShadow: Boolean(title?.enableShadow),
      observationShadow: Boolean(observation?.enableShadow),
      returnGuardShadow: Boolean(returnGuard?.enableShadow),
      returnGuardColor: [guardColor.r, guardColor.g, guardColor.b, guardColor.a],
    };
  }

  private snapshot(): MediaSnapshot {
    const transform = this.imageNode?.getComponent(UITransform);
    return {
      ready: this.ready,
      manifestStatus: this.manifest?.status ?? '',
      experimentId: this.manifest?.activeExperiment.id ?? '',
      variant: this.manifest?.activeExperiment.variant ?? '',
      assetId: this.activeAsset?.assetId ?? '',
      pageId: this.activeAsset?.pageId ?? '',
      currentPageId: RuntimeStore.snapshot.currentPageId,
      visible: Boolean(this.imageNode?.activeInHierarchy),
      usageGate: this.activeAsset?.usageGate ?? '',
      techGate: this.activeAsset?.techGate ?? '',
      nodeGate: this.activeAsset?.nodeGate ?? '',
      sourceWidth: this.activeAsset?.sourceWidth ?? 0,
      sourceHeight: this.activeAsset?.sourceHeight ?? 0,
      renderedWidth: transform?.contentSize.width ?? 0,
      renderedHeight: transform?.contentSize.height ?? 0,
      textProtection: this.textProtectionSnapshot(),
    };
  }
}
