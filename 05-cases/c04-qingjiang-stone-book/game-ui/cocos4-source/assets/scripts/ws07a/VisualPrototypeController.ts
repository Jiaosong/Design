import {
  _decorator,
  Button,
  Color,
  Component,
  find,
  HorizontalTextAlignment,
  Label,
  Node,
  Overflow,
  profiler,
  screen,
  UITransform,
  VerticalTextAlignment,
  warn,
} from 'cc';
import { RuntimeCatalog } from './RuntimeCatalog';
import { RuntimeStore } from './RuntimeStore';
import type { ClaimType, PrototypeScreenId, ReadingPage } from './RuntimeTypes';

const { ccclass } = _decorator;

interface RectSnapshot { x: number; y: number; width: number; height: number; }
interface NodeSnapshot { path: string; active: boolean; rect: RectSnapshot | null; }
interface CanvasSnapshot { width: number; height: number; pxPerUnit: number; profile: 'PORTRAIT' | 'LANDSCAPE'; }
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
  canvas: CanvasSnapshot;
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

interface LayoutMetrics {
  width: number;
  height: number;
  pxPerUnit: number;
  profile: 'PORTRAIT' | 'LANDSCAPE';
  marginX: number;
  marginY: number;
  gap: number;
  titleFont: number;
  bodyFont: number;
  navFont: number;
  metaFont: number;
  navHeight: number;
  actionHeight: number;
  actionWidth: number;
  navY: number;
  returnY: number;
  returnHeight: number;
  footerTop: number;
  titleY: number;
  titleHeight: number;
  observationY: number;
  observationHeight: number;
  contentTop: number;
}

const BRIDGE_KEY = '__OLEANDER_WS07A__';
const FONT_FAMILY = 'Noto Sans CJK SC';
const COLORS = {
  landscapeNeutral: new Color(241, 239, 232, 255),
  inkRock: new Color(32, 37, 35, 255),
  mistGray: new Color(168, 174, 170, 255),
  deepQing: new Color(23, 61, 57, 255),
  oldBronze: new Color(138, 104, 68, 255),
  evidenceGray: new Color(111, 118, 114, 255),
  evidenceQuiet: new Color(111, 118, 114, 150),
};

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
  private lastLayoutSignature = '';
  private currentMetrics: LayoutMetrics | null = null;

  protected start(): void {
    profiler.hideStats();
    this.resolveSceneContract();
    this.suppressUnexpectedTemplateChildren();
    this.wireInteraction();
    this.installRuntimeBridge();
    this.applyResponsiveLayout(true);
    void this.bootstrap();
  }

  protected lateUpdate(): void {
    this.applyResponsiveLayout(false);
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
    this.applyResponsiveLayout(true);
  }
  public showMyBook(): void {
    this.setScreen('MY_BOOK');
    RuntimeStore.setCurrentPage(undefined);
    this.renderBookSummary();
    this.applyResponsiveLayout(true);
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
    this.syncPageActions(page);
    this.applyResponsiveLayout(true);
  }

  public closeReveal(): void {
    RuntimeStore.setReveal(false);
    if (this.revealRoot) this.revealRoot.active = false;
    const pageId = RuntimeStore.snapshot.currentPageId;
    this.syncPageActions(pageId ? RuntimeStore.getPage(pageId) : undefined);
    this.applyResponsiveLayout(true);
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

  private suppressUnexpectedTemplateChildren(): void {
    const buttonPaths = [
      'PrototypeNav/NavS0', 'PrototypeNav/NavS1', 'PrototypeNav/NavS2', 'PrototypeNav/NavRoute', 'PrototypeNav/NavBook',
      'ReadingOverlay/RecordButton', 'ReadingOverlay/RevealButton', 'S2_RiverValley/RevealRoot/CloseReveal',
    ];
    for (const path of buttonPaths) {
      const button = this.getNode(path);
      for (const child of button?.children ?? []) {
        if (child.name !== 'Text') child.active = false;
      }
    }
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

  private showPageScreen(screenId: PrototypeScreenId, pageId: string): void {
    this.setScreen(screenId);
    const page = RuntimeStore.getPage(pageId);
    if (!page) {
      warn(`[C04 WS-07A] page missing: ${pageId}`);
      return;
    }
    RuntimeStore.setCurrentPage(pageId);
    this.bindPage(page);
    this.applyResponsiveLayout(true);
  }

  private setScreen(screenId: PrototypeScreenId): void {
    RuntimeStore.setScreen(screenId);
    const roots: Array<[PrototypeScreenId, Node | null]> = [
      ['S0_ONE_LINE_SKY', this.s0Root],
      ['S1_RED_ROCK_MOUTH', this.s1Root],
      ['S2_RIVER_VALLEY', this.s2Root],
      ['ROUTE', this.routeRoot],
      ['MY_BOOK', this.myBookRoot],
    ];
    roots.forEach(([id, root]) => { if (root) root.active = id === screenId; });
    if (this.readingOverlayRoot) {
      this.readingOverlayRoot.active = screenId === 'S0_ONE_LINE_SKY' || screenId === 'S1_RED_ROCK_MOUTH' || screenId === 'S2_RIVER_VALLEY';
    }
    RuntimeStore.setReveal(false);
    if (this.revealRoot) this.revealRoot.active = false;
    this.updateNavState(screenId);
  }

  private bindPage(page: ReadingPage): void {
    if (this.pageTitleLabel) this.pageTitleLabel.string = page.title;
    if (this.observationLabel) this.observationLabel.string = page.observation ?? '';
    if (this.evidenceStatusLabel) this.evidenceStatusLabel.string = `EVIDENCE｜${page.status}`;
    this.setClaimText('FACT', page, this.factLabel);
    this.setClaimText('LOCAL_NARRATIVE', page, this.narrativeLabel);
    this.setClaimText('DESIGN_READING', page, this.designReadingLabel);
    this.syncPageActions(page);
  }

  private syncPageActions(page?: ReadingPage): void {
    const revealOpen = RuntimeStore.snapshot.revealOpen;
    if (this.recordButtonNode) this.recordButtonNode.active = Boolean(page && page.mode !== 'S0' && !revealOpen);
    if (this.revealButtonNode) this.revealButtonNode.active = Boolean(page && page.mode === 'S2' && !revealOpen);
  }

  private setClaimText(type: ClaimType, page: ReadingPage, label: Label | null): void {
    if (!label) return;
    const claim = page.claimLayers?.find((item) => item.type === type);
    const prefix: Record<ClaimType, string> = {
      FACT: 'FACT｜事实',
      LOCAL_NARRATIVE: 'LOCAL NARRATIVE｜地方叙事',
      DESIGN_READING: 'DESIGN READING｜设计阅读',
    };
    label.string = claim ? `${prefix[type]}\n${claim.text}` : '';
    label.node.active = Boolean(claim);
  }

  private renderBookSummary(): void {
    if (!this.bookSummaryLabel) return;
    const pages = RuntimeStore.getRecordedPages();
    this.bookSummaryLabel.string = pages.length === 0
      ? '本次还没有留下印记；未完成也可以成为一本石书。'
      : `本次石书已留下 ${pages.length} 页：${pages.map((page) => page.title).join('、')}`;
  }

  private updateNavState(screenId: PrototypeScreenId): void {
    const nav: Array<[PrototypeScreenId, string]> = [
      ['S0_ONE_LINE_SKY', 'PrototypeNav/NavS0/Text'],
      ['S1_RED_ROCK_MOUTH', 'PrototypeNav/NavS1/Text'],
      ['S2_RIVER_VALLEY', 'PrototypeNav/NavS2/Text'],
      ['ROUTE', 'PrototypeNav/NavRoute/Text'],
      ['MY_BOOK', 'PrototypeNav/NavBook/Text'],
    ];
    for (const [id, path] of nav) {
      const label = this.getLabel(path);
      if (label) label.color = id === screenId ? COLORS.oldBronze : COLORS.mistGray;
    }
  }

  private applyResponsiveLayout(force: boolean): void {
    const metrics = this.computeLayoutMetrics();
    if (!metrics) return;
    const signature = `${metrics.width.toFixed(2)}x${metrics.height.toFixed(2)}:${metrics.profile}`;
    if (!force && signature === this.lastLayoutSignature) return;
    this.lastLayoutSignature = signature;
    this.currentMetrics = metrics;

    const m = metrics;
    const navPaths = ['PrototypeNav/NavS0', 'PrototypeNav/NavS1', 'PrototypeNav/NavS2', 'PrototypeNav/NavRoute', 'PrototypeNav/NavBook'];
    const navTextPaths = navPaths.map((path) => `${path}/Text`);
    const navWidth = (m.width - (2 * m.marginX) - (4 * m.gap)) / 5;
    navPaths.forEach((path, index) => {
      const x = -m.width / 2 + m.marginX + navWidth / 2 + index * (navWidth + m.gap);
      this.place(path, x, m.navY, navWidth, m.navHeight);
      this.place(navTextPaths[index], 0, 0, navWidth, m.navHeight);
      this.styleLabel(navTextPaths[index], m.navFont, COLORS.mistGray, HorizontalTextAlignment.CENTER, VerticalTextAlignment.CENTER, false);
    });

    this.place('ReturnGuard/Label', 0, m.returnY, m.width - 2 * m.marginX, m.returnHeight);
    this.styleLabel('ReturnGuard/Label', m.metaFont, COLORS.evidenceGray, HorizontalTextAlignment.LEFT, VerticalTextAlignment.CENTER, true);

    this.place('ReadingOverlay/PageTitle', 0, m.titleY, m.width - 2 * m.marginX, m.titleHeight);
    this.styleLabel('ReadingOverlay/PageTitle', m.titleFont, COLORS.landscapeNeutral, HorizontalTextAlignment.LEFT, VerticalTextAlignment.CENTER, true);
    this.place('ReadingOverlay/Observation', 0, m.observationY, m.width - 2 * m.marginX, m.observationHeight);
    this.styleLabel('ReadingOverlay/Observation', m.bodyFont, COLORS.landscapeNeutral, HorizontalTextAlignment.LEFT, VerticalTextAlignment.TOP, true);

    const actionY = m.footerTop + m.gap + m.actionHeight / 2;
    const actionGap = m.gap;
    this.place('ReadingOverlay/RecordButton', m.width / 2 - m.marginX - m.actionWidth / 2, actionY, m.actionWidth, m.actionHeight);
    this.place('ReadingOverlay/RecordButton/Text', 0, 0, m.actionWidth, m.actionHeight);
    this.styleLabel('ReadingOverlay/RecordButton/Text', m.navFont, COLORS.oldBronze, HorizontalTextAlignment.CENTER, VerticalTextAlignment.CENTER, false);
    this.place('ReadingOverlay/RevealButton', m.width / 2 - m.marginX - (m.actionWidth * 1.5) - actionGap, actionY, m.actionWidth, m.actionHeight);
    this.place('ReadingOverlay/RevealButton/Text', 0, 0, m.actionWidth, m.actionHeight);
    this.styleLabel('ReadingOverlay/RevealButton/Text', m.navFont, COLORS.oldBronze, HorizontalTextAlignment.CENTER, VerticalTextAlignment.CENTER, false);

    const landscapeCenterY = (m.contentTop + m.footerTop) / 2;
    const landscapeHeight = Math.max(60, m.contentTop - m.footerTop - 2 * m.gap);
    for (const path of ['S0_OneLineSky/ScreenHint', 'S1_RedRockMouth/ScreenHint', 'S2_RiverValley/ScreenHint']) {
      this.place(path, 0, landscapeCenterY, m.width - 2 * m.marginX, Math.min(landscapeHeight, m.bodyFont * 2.4));
      this.styleLabel(path, m.metaFont, COLORS.evidenceQuiet, HorizontalTextAlignment.CENTER, VerticalTextAlignment.CENTER, true);
    }

    this.layoutReveal(m);
    this.layoutRouteAndBook(m);
    this.applyResponsiveLayoutToActiveState();
  }

  private layoutReveal(m: LayoutMetrics): void {
    this.place('S2_RiverValley/RevealRoot', 0, 0, m.width, m.height);
    const evidenceHeight = m.metaFont * 2.2;
    const closeYBase = m.footerTop + m.gap + m.actionHeight / 2;
    this.place('S2_RiverValley/RevealRoot/CloseReveal', m.width / 2 - m.marginX - m.actionWidth / 2, closeYBase, m.actionWidth, m.actionHeight);
    this.place('S2_RiverValley/RevealRoot/CloseReveal/Text', 0, 0, m.actionWidth, m.actionHeight);
    this.styleLabel('S2_RiverValley/RevealRoot/CloseReveal/Text', m.navFont, COLORS.oldBronze, HorizontalTextAlignment.CENTER, VerticalTextAlignment.CENTER, false);

    if (m.profile === 'LANDSCAPE') {
      const panelTop = m.contentTop;
      const panelBottom = closeYBase + m.actionHeight / 2 + m.gap;
      const evidenceY = panelTop - evidenceHeight / 2;
      this.place('S2_RiverValley/RevealRoot/EvidenceStatus', 0, evidenceY, m.width - 2 * m.marginX, evidenceHeight);
      this.styleLabel('S2_RiverValley/RevealRoot/EvidenceStatus', m.metaFont, COLORS.evidenceGray, HorizontalTextAlignment.LEFT, VerticalTextAlignment.CENTER, true);
      const claimTop = evidenceY - evidenceHeight / 2 - m.gap;
      const claimHeight = Math.max(64, claimTop - panelBottom);
      const claimWidth = (m.width - 2 * m.marginX - 2 * m.gap) / 3;
      const paths = ['S2_RiverValley/RevealRoot/Fact', 'S2_RiverValley/RevealRoot/Narrative', 'S2_RiverValley/RevealRoot/DesignReading'];
      paths.forEach((path, index) => {
        const x = -m.width / 2 + m.marginX + claimWidth / 2 + index * (claimWidth + m.gap);
        this.place(path, x, panelBottom + claimHeight / 2, claimWidth, claimHeight);
      });
    } else {
      const panelTop = m.contentTop;
      this.place('S2_RiverValley/RevealRoot/EvidenceStatus', 0, panelTop - evidenceHeight / 2, m.width - 2 * m.marginX, evidenceHeight);
      this.styleLabel('S2_RiverValley/RevealRoot/EvidenceStatus', m.metaFont, COLORS.evidenceGray, HorizontalTextAlignment.LEFT, VerticalTextAlignment.CENTER, true);
      const claimHeight = Math.min(180, Math.max(110, m.bodyFont * 4.4));
      const claimWidth = m.width - 2 * m.marginX;
      const firstY = panelTop - evidenceHeight - m.gap - claimHeight / 2;
      this.place('S2_RiverValley/RevealRoot/Fact', 0, firstY, claimWidth, claimHeight);
      this.place('S2_RiverValley/RevealRoot/Narrative', 0, firstY - claimHeight - m.gap, claimWidth, claimHeight);
      this.place('S2_RiverValley/RevealRoot/DesignReading', 0, firstY - 2 * (claimHeight + m.gap), claimWidth, claimHeight);
      const lastBottom = firstY - 2 * (claimHeight + m.gap) - claimHeight / 2;
      this.place('S2_RiverValley/RevealRoot/CloseReveal', m.width / 2 - m.marginX - m.actionWidth / 2, Math.max(closeYBase, lastBottom - m.gap - m.actionHeight / 2), m.actionWidth, m.actionHeight);
    }

    this.styleLabel('S2_RiverValley/RevealRoot/Fact', m.bodyFont, COLORS.landscapeNeutral, HorizontalTextAlignment.LEFT, VerticalTextAlignment.TOP, true);
    this.styleLabel('S2_RiverValley/RevealRoot/Narrative', m.bodyFont, COLORS.mistGray, HorizontalTextAlignment.LEFT, VerticalTextAlignment.TOP, true);
    this.styleLabel('S2_RiverValley/RevealRoot/DesignReading', m.bodyFont, COLORS.oldBronze, HorizontalTextAlignment.LEFT, VerticalTextAlignment.TOP, true);
  }

  private layoutRouteAndBook(m: LayoutMetrics): void {
    const wide = m.width - 2 * m.marginX;
    const supportY = m.observationY;
    this.place('Route/Title', 0, m.titleY, wide, m.titleHeight);
    this.styleLabel('Route/Title', m.titleFont, COLORS.landscapeNeutral, HorizontalTextAlignment.LEFT, VerticalTextAlignment.CENTER, true);
    this.place('Route/Priority', 0, supportY, wide, m.observationHeight);
    this.styleLabel('Route/Priority', m.bodyFont, COLORS.mistGray, HorizontalTextAlignment.LEFT, VerticalTextAlignment.TOP, true);
    this.place('MyBook/Title', 0, m.titleY, wide, m.titleHeight);
    this.styleLabel('MyBook/Title', m.titleFont, COLORS.landscapeNeutral, HorizontalTextAlignment.LEFT, VerticalTextAlignment.CENTER, true);
    this.place('MyBook/BookSummary', 0, supportY, wide, Math.max(m.observationHeight, m.bodyFont * 3));
    this.styleLabel('MyBook/BookSummary', m.bodyFont, COLORS.mistGray, HorizontalTextAlignment.LEFT, VerticalTextAlignment.TOP, true);
  }

  private applyResponsiveLayoutToActiveState(): void {
    const pageId = RuntimeStore.snapshot.currentPageId;
    if (pageId) this.syncPageActions(RuntimeStore.getPage(pageId));
    this.updateNavState(RuntimeStore.snapshot.currentScreen);
  }

  private computeLayoutMetrics(): LayoutMetrics | null {
    const canvasTransform = this.ensureTransform(this.node);
    const width = canvasTransform.contentSize.width;
    const height = canvasTransform.contentSize.height;
    if (width <= 0 || height <= 0) return null;
    const pxPerUnit = Math.max(0.1, screen.windowSize.width / width);
    const profile: 'PORTRAIT' | 'LANDSCAPE' = height < width * 0.8 ? 'LANDSCAPE' : 'PORTRAIT';
    const unit = (px: number, min: number, max: number): number => this.clamp(px / pxPerUnit, min, max);
    const marginX = unit(24, 28, 64);
    const marginY = profile === 'LANDSCAPE' ? unit(16, 16, 34) : unit(28, 28, 72);
    const gap = unit(10, 10, 26);
    const titleFont = unit(28, 30, 64);
    const bodyFont = unit(17, 18, 42);
    const navFont = unit(14, 16, 36);
    const metaFont = unit(14, 14, 34);
    const navHeight = unit(48, 52, 112);
    const actionHeight = navHeight;
    const actionWidth = unit(132, 160, 300);
    const bottom = -height / 2 + marginY;
    const navY = bottom + navHeight / 2;
    const returnHeight = Math.max(metaFont * 2.2, unit(34, 36, 82));
    const returnY = bottom + navHeight + gap + returnHeight / 2;
    const footerTop = bottom + navHeight + gap + returnHeight + gap;
    const titleHeight = Math.max(titleFont * 1.45, unit(46, 50, 108));
    const observationHeight = profile === 'LANDSCAPE' ? Math.max(bodyFont * 2.2, 48) : Math.max(bodyFont * 3, 72);
    const titleY = height / 2 - marginY - titleHeight / 2;
    const observationY = titleY - titleHeight / 2 - gap - observationHeight / 2;
    const contentTop = observationY - observationHeight / 2 - gap;
    return {
      width, height, pxPerUnit, profile, marginX, marginY, gap, titleFont, bodyFont, navFont, metaFont,
      navHeight, actionHeight, actionWidth, navY, returnY, returnHeight, footerTop,
      titleY, titleHeight, observationY, observationHeight, contentTop,
    };
  }

  private place(path: string, x: number, y: number, width: number, height: number): void {
    const node = find(path, this.node);
    if (!node) return;
    const transform = this.ensureTransform(node);
    transform.setContentSize(Math.max(1, width), Math.max(1, height));
    node.setPosition(x, y, 0);
  }

  private styleLabel(
    path: string,
    fontSize: number,
    color: Color,
    horizontal: HorizontalTextAlignment,
    vertical: VerticalTextAlignment,
    wrap: boolean,
  ): void {
    const label = this.getLabel(path);
    if (!label) return;
    label.useSystemFont = true;
    label.fontFamily = FONT_FAMILY;
    label.fontSize = Math.max(1, Math.round(fontSize));
    label.lineHeight = Math.max(label.fontSize + 4, Math.round(label.fontSize * 1.35));
    label.horizontalAlign = horizontal;
    label.verticalAlign = vertical;
    label.enableWrapText = wrap;
    label.overflow = Overflow.SHRINK;
    label.color = color;
  }

  private ensureTransform(node: Node): UITransform {
    return node.getComponent(UITransform) ?? node.addComponent(UITransform);
  }

  private clamp(value: number, min: number, max: number): number {
    return Math.min(max, Math.max(min, value));
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
    const metrics = this.currentMetrics ?? this.computeLayoutMetrics();
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
      canvas: {
        width: metrics?.width ?? 0,
        height: metrics?.height ?? 0,
        pxPerUnit: metrics?.pxPerUnit ?? 0,
        profile: metrics?.profile ?? 'PORTRAIT',
      },
      layout: this.captureLayout([
        'PrototypeNav/NavS0', 'PrototypeNav/NavS1', 'PrototypeNav/NavS2', 'PrototypeNav/NavRoute', 'PrototypeNav/NavBook',
        'ReadingOverlay/PageTitle', 'ReadingOverlay/Observation', 'ReadingOverlay/RecordButton', 'ReadingOverlay/RevealButton',
        'S2_RiverValley/RevealRoot/EvidenceStatus', 'S2_RiverValley/RevealRoot/Fact', 'S2_RiverValley/RevealRoot/Narrative', 'S2_RiverValley/RevealRoot/DesignReading', 'S2_RiverValley/RevealRoot/CloseReveal',
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
    const node = find(path, this.node);
    if (!node) return null;
    const label = node.getComponent(Label) ?? null;
    if (!label) warn(`[C04 WS-07A] Label component missing: ${path}`);
    return label;
  }
}
