import { _decorator, Button, Component, find, Label, Node, UITransform, warn } from 'cc';
import { RuntimeCatalog } from './RuntimeCatalog';
import { RuntimeStore } from './RuntimeStore';
import type { ClaimType, PrototypeScreenId, ReadingPage } from './RuntimeTypes';

const { ccclass } = _decorator;

interface RectSnapshot { x: number; y: number; width: number; height: number; }
interface NodeSnapshot { path: string; active: boolean; rect: RectSnapshot | null; }
interface RuntimeAuditSnapshot {
  ready: boolean;
  currentScreen: PrototypeScreenId;
  currentPageId?: string;
  recordedPageIds: string[];
  revealOpen: boolean;
  activeScreens: string[];
  readingOverlayActive: boolean;
  recordButtonActive: boolean;
  revealButtonActive: boolean;
  revealRootActive: boolean;
  returnGuardActive: boolean;
  pageTitle: string;
  observation: string;
  evidenceStatus: string;
  claims: Record<ClaimType, { active: boolean; text: string }>;
  bookSummary: string;
  layout: NodeSnapshot[];
}

interface RuntimeBridge {
  ready: boolean;
  showS0: () => RuntimeAuditSnapshot;
  showS1: () => RuntimeAuditSnapshot;
  showS2: () => RuntimeAuditSnapshot;
  showRoute: () => RuntimeAuditSnapshot;
  showMyBook: () => RuntimeAuditSnapshot;
  recordCurrentPage: () => RuntimeAuditSnapshot;
  openReveal: () => RuntimeAuditSnapshot;
  closeReveal: () => RuntimeAuditSnapshot;
  snapshot: () => RuntimeAuditSnapshot;
}

const BRIDGE_KEY = '__OLEANDER_WS07A__';

@ccclass('C04WS07AVisualPrototypeController')
export class VisualPrototypeController extends Component {
  private s0Root: Node | null = null;
  private s1Root: Node | null = null;
  private s2Root: Node | null = null;
  private routeRoot: Node | null = null;
  private myBookRoot: Node | null = null;
  private readingOverlayRoot: Node | null = null;
  private revealRoot: Node | null = null;
  private recordButtonNode: Node | null = null;
  private revealButtonNode: Node | null = null;
  private pageTitleLabel: Label | null = null;
  private observationLabel: Label | null = null;
  private evidenceStatusLabel: Label | null = null;
  private factLabel: Label | null = null;
  private narrativeLabel: Label | null = null;
  private designReadingLabel: Label | null = null;
  private bookSummaryLabel: Label | null = null;
  private returnGuardLabel: Label | null = null;
  private runtimeReady = false;

  protected start(): void {
    this.resolveSceneContract();
    this.wireInteraction();
    this.installRuntimeBridge();
    void this.bootstrap();
  }

  protected onDestroy(): void {
    const root = globalThis as unknown as Record<string, unknown>;
    delete root[BRIDGE_KEY];
  }

  private async bootstrap(): Promise<void> {
    try {
      const bundle = await RuntimeCatalog.load();
      RuntimeStore.hydrate(bundle);
      if (this.returnGuardLabel) this.returnGuardLabel.string = bundle.manifest.returnGuard.message;
      this.showS0();
      this.runtimeReady = true;
      const bridge = this.getRuntimeBridge();
      if (bridge) bridge.ready = true;
    } catch (error) {
      warn('[C04 WS-07A] runtime bootstrap failed', error);
    }
  }

  public showS0(): void { this.showPageScreen('S0_ONE_LINE_SKY', 'R13'); }
  public showS1(): void { this.showPageScreen('S1_RED_ROCK_MOUTH', 'R01'); }
  public showS2(): void { this.showPageScreen('S2_RIVER_VALLEY', 'R06'); }
  public showRoute(): void {
    this.setScreen('ROUTE');
    RuntimeStore.setCurrentPage(undefined);
  }
  public showMyBook(): void {
    this.setScreen('MY_BOOK');
    RuntimeStore.setCurrentPage(undefined);
    this.renderBookSummary();
  }

  public recordCurrentPage(): void {
    const pageId = RuntimeStore.snapshot.currentPageId;
    if (!pageId) return;
    RuntimeStore.record(pageId);
    this.renderBookSummary();
  }

  public openReveal(): void {
    const pageId = RuntimeStore.snapshot.currentPageId;
    const page = pageId ? RuntimeStore.getPage(pageId) : undefined;
    if (!page || page.mode !== 'S2') return;
    RuntimeStore.setReveal(true);
    if (this.revealRoot) this.revealRoot.active = true;
  }

  public closeReveal(): void {
    RuntimeStore.setReveal(false);
    if (this.revealRoot) this.revealRoot.active = false;
  }

  private resolveSceneContract(): void {
    this.s0Root = this.getNode('S0_OneLineSky');
    this.s1Root = this.getNode('S1_RedRockMouth');
    this.s2Root = this.getNode('S2_RiverValley');
    this.routeRoot = this.getNode('Route');
    this.myBookRoot = this.getNode('MyBook');
    this.readingOverlayRoot = this.getNode('ReadingOverlay');
    this.revealRoot = this.getNode('S2_RiverValley/RevealRoot');
    this.recordButtonNode = this.getNode('ReadingOverlay/RecordButton');
    this.revealButtonNode = this.getNode('ReadingOverlay/RevealButton');
    this.pageTitleLabel = this.getLabel('ReadingOverlay/PageTitle');
    this.observationLabel = this.getLabel('ReadingOverlay/Observation');
    this.evidenceStatusLabel = this.getLabel('S2_RiverValley/RevealRoot/EvidenceStatus');
    this.factLabel = this.getLabel('S2_RiverValley/RevealRoot/Fact');
    this.narrativeLabel = this.getLabel('S2_RiverValley/RevealRoot/Narrative');
    this.designReadingLabel = this.getLabel('S2_RiverValley/RevealRoot/DesignReading');
    this.bookSummaryLabel = this.getLabel('MyBook/BookSummary');
    this.returnGuardLabel = this.getLabel('ReturnGuard/Label');
  }

  private wireInteraction(): void {
    this.bindClick('PrototypeNav/NavS0', this.showS0);
    this.bindClick('PrototypeNav/NavS1', this.showS1);
    this.bindClick('PrototypeNav/NavS2', this.showS2);
    this.bindClick('PrototypeNav/NavRoute', this.showRoute);
    this.bindClick('PrototypeNav/NavBook', this.showMyBook);
    this.bindClick('ReadingOverlay/RecordButton', this.recordCurrentPage);
    this.bindClick('ReadingOverlay/RevealButton', this.openReveal);
    this.bindClick('S2_RiverValley/RevealRoot/CloseReveal', this.closeReveal);
  }

  private bindClick(path: string, handler: () => void): void {
    const node = this.getNode(path);
    if (!node) {
      warn(`[C04 WS-07A] interaction node missing: ${path}`);
      return;
    }
    node.on(Button.EventType.CLICK, handler, this);
  }

  private showPageScreen(screen: PrototypeScreenId, pageId: string): void {
    this.setScreen(screen);
    const page = RuntimeStore.getPage(pageId);
    if (!page) {
      warn(`[C04 WS-07A] page missing: ${pageId}`);
      return;
    }
    RuntimeStore.setCurrentPage(pageId);
    this.bindPage(page);
  }

  private setScreen(screen: PrototypeScreenId): void {
    RuntimeStore.setScreen(screen);
    const roots: Array<[PrototypeScreenId, Node | null]> = [
      ['S0_ONE_LINE_SKY', this.s0Root],
      ['S1_RED_ROCK_MOUTH', this.s1Root],
      ['S2_RIVER_VALLEY', this.s2Root],
      ['ROUTE', this.routeRoot],
      ['MY_BOOK', this.myBookRoot],
    ];
    roots.forEach(([id, root]) => { if (root) root.active = id === screen; });
    if (this.readingOverlayRoot) {
      this.readingOverlayRoot.active = screen === 'S0_ONE_LINE_SKY' || screen === 'S1_RED_ROCK_MOUTH' || screen === 'S2_RIVER_VALLEY';
    }
    this.closeReveal();
  }

  private bindPage(page: ReadingPage): void {
    if (this.pageTitleLabel) this.pageTitleLabel.string = page.title;
    if (this.observationLabel) this.observationLabel.string = page.observation ?? '';
    if (this.recordButtonNode) this.recordButtonNode.active = page.mode !== 'S0';
    if (this.revealButtonNode) this.revealButtonNode.active = page.mode === 'S2';
    if (this.evidenceStatusLabel) this.evidenceStatusLabel.string = page.status;
    this.setClaimText('FACT', page, this.factLabel);
    this.setClaimText('LOCAL_NARRATIVE', page, this.narrativeLabel);
    this.setClaimText('DESIGN_READING', page, this.designReadingLabel);
  }

  private setClaimText(type: ClaimType, page: ReadingPage, label: Label | null): void {
    if (!label) return;
    const claim = page.claimLayers?.find((item) => item.type === type);
    label.string = claim ? claim.text : '';
    label.node.active = Boolean(claim);
  }

  private renderBookSummary(): void {
    if (!this.bookSummaryLabel) return;
    const pages = RuntimeStore.getRecordedPages();
    this.bookSummaryLabel.string = pages.length === 0
      ? '本次还没有留下印记；未完成也可以成为一本石书。'
      : `本次石书已留下 ${pages.length} 页：${pages.map((page) => page.title).join('、')}`;
  }

  private installRuntimeBridge(): void {
    const bridge: RuntimeBridge = {
      ready: false,
      showS0: () => { this.showS0(); return this.getAuditSnapshot(); },
      showS1: () => { this.showS1(); return this.getAuditSnapshot(); },
      showS2: () => { this.showS2(); return this.getAuditSnapshot(); },
      showRoute: () => { this.showRoute(); return this.getAuditSnapshot(); },
      showMyBook: () => { this.showMyBook(); return this.getAuditSnapshot(); },
      recordCurrentPage: () => { this.recordCurrentPage(); return this.getAuditSnapshot(); },
      openReveal: () => { this.openReveal(); return this.getAuditSnapshot(); },
      closeReveal: () => { this.closeReveal(); return this.getAuditSnapshot(); },
      snapshot: () => this.getAuditSnapshot(),
    };
    const root = globalThis as unknown as Record<string, unknown>;
    root[BRIDGE_KEY] = bridge;
  }

  private getRuntimeBridge(): RuntimeBridge | null {
    const root = globalThis as unknown as Record<string, unknown>;
    return (root[BRIDGE_KEY] as RuntimeBridge | undefined) ?? null;
  }

  private getAuditSnapshot(): RuntimeAuditSnapshot {
    const state = RuntimeStore.snapshot;
    const screenRoots: Array<[string, Node | null]> = [
      ['S0_ONE_LINE_SKY', this.s0Root],
      ['S1_RED_ROCK_MOUTH', this.s1Root],
      ['S2_RIVER_VALLEY', this.s2Root],
      ['ROUTE', this.routeRoot],
      ['MY_BOOK', this.myBookRoot],
    ];
    return {
      ready: this.runtimeReady,
      currentScreen: state.currentScreen,
      currentPageId: state.currentPageId,
      recordedPageIds: [...state.recordedPageIds],
      revealOpen: state.revealOpen,
      activeScreens: screenRoots.filter(([, node]) => Boolean(node?.activeInHierarchy)).map(([id]) => id),
      readingOverlayActive: Boolean(this.readingOverlayRoot?.activeInHierarchy),
      recordButtonActive: Boolean(this.recordButtonNode?.activeInHierarchy),
      revealButtonActive: Boolean(this.revealButtonNode?.activeInHierarchy),
      revealRootActive: Boolean(this.revealRoot?.activeInHierarchy),
      returnGuardActive: Boolean(this.returnGuardLabel?.node.activeInHierarchy),
      pageTitle: this.pageTitleLabel?.string ?? '',
      observation: this.observationLabel?.string ?? '',
      evidenceStatus: this.evidenceStatusLabel?.string ?? '',
      claims: {
        FACT: this.labelState(this.factLabel),
        LOCAL_NARRATIVE: this.labelState(this.narrativeLabel),
        DESIGN_READING: this.labelState(this.designReadingLabel),
      },
      bookSummary: this.bookSummaryLabel?.string ?? '',
      layout: this.captureLayout([
        'PrototypeNav', 'PrototypeNav/NavS0', 'PrototypeNav/NavS1', 'PrototypeNav/NavS2', 'PrototypeNav/NavRoute', 'PrototypeNav/NavBook',
        'ReadingOverlay/PageTitle', 'ReadingOverlay/Observation', 'ReadingOverlay/RecordButton', 'ReadingOverlay/RevealButton',
        'S2_RiverValley/RevealRoot', 'S2_RiverValley/RevealRoot/Fact', 'S2_RiverValley/RevealRoot/Narrative', 'S2_RiverValley/RevealRoot/DesignReading',
        'Route/Title', 'Route/Priority', 'MyBook/Title', 'MyBook/BookSummary', 'ReturnGuard/Label',
      ]),
    };
  }

  private labelState(label: Label | null): { active: boolean; text: string } {
    return { active: Boolean(label?.node.activeInHierarchy), text: label?.string ?? '' };
  }

  private captureLayout(paths: string[]): NodeSnapshot[] {
    return paths.map((path) => {
      const node = find(path, this.node);
      if (!node) return { path, active: false, rect: null };
      const transform = node.getComponent(UITransform);
      const rect = transform?.getBoundingBoxToWorld();
      return {
        path,
        active: node.activeInHierarchy,
        rect: rect ? { x: rect.x, y: rect.y, width: rect.width, height: rect.height } : null,
      };
    });
  }

  private getNode(path: string): Node | null {
    const node = find(path, this.node);
    if (!node) warn(`[C04 WS-07A] scene contract node missing: ${path}`);
    return node;
  }

  private getLabel(path: string): Label | null {
    const node = this.getNode(path);
    const label = node?.getComponent(Label) ?? null;
    if (node && !label) warn(`[C04 WS-07A] Label component missing: ${path}`);
    return label;
  }
}
