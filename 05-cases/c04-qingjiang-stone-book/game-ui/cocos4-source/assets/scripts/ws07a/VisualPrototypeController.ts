import { _decorator, Component, Label, Node, warn } from 'cc';
import { RuntimeCatalog } from './RuntimeCatalog';
import { RuntimeStore } from './RuntimeStore';
import type { ClaimType, PrototypeScreenId, ReadingPage } from './RuntimeTypes';

const { ccclass, property } = _decorator;

@ccclass('C04WS07AVisualPrototypeController')
export class VisualPrototypeController extends Component {
  @property(Node) s0Root: Node | null = null;
  @property(Node) s1Root: Node | null = null;
  @property(Node) s2Root: Node | null = null;
  @property(Node) routeRoot: Node | null = null;
  @property(Node) myBookRoot: Node | null = null;
  @property(Node) revealRoot: Node | null = null;
  @property(Label) pageTitleLabel: Label | null = null;
  @property(Label) observationLabel: Label | null = null;
  @property(Label) evidenceStatusLabel: Label | null = null;
  @property(Label) factLabel: Label | null = null;
  @property(Label) narrativeLabel: Label | null = null;
  @property(Label) designReadingLabel: Label | null = null;
  @property(Label) bookSummaryLabel: Label | null = null;
  @property(Label) returnGuardLabel: Label | null = null;

  protected start(): void { void this.bootstrap(); }

  private async bootstrap(): Promise<void> {
    try {
      const bundle = await RuntimeCatalog.load();
      RuntimeStore.hydrate(bundle);
      if (this.returnGuardLabel) this.returnGuardLabel.string = bundle.manifest.returnGuard.message;
      this.showS0();
    } catch (error) {
      warn('[C04 WS-07A] runtime bootstrap failed', error);
    }
  }

  public showS0(): void { this.showPageScreen('S0_ONE_LINE_SKY', 'R13'); }
  public showS1(): void { this.showPageScreen('S1_RED_ROCK_MOUTH', 'R01'); }
  public showS2(): void { this.showPageScreen('S2_RIVER_VALLEY', 'R06'); }
  public showRoute(): void { this.setScreen('ROUTE'); RuntimeStore.setCurrentPage(undefined); }
  public showMyBook(): void { this.setScreen('MY_BOOK'); RuntimeStore.setCurrentPage(undefined); this.renderBookSummary(); }

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

  public closeReveal(): void { RuntimeStore.setReveal(false); if (this.revealRoot) this.revealRoot.active = false; }

  private showPageScreen(screen: PrototypeScreenId, pageId: string): void {
    this.setScreen(screen);
    const page = RuntimeStore.getPage(pageId);
    if (!page) { warn(`[C04 WS-07A] page missing: ${pageId}`); return; }
    RuntimeStore.setCurrentPage(pageId);
    this.bindPage(page);
  }

  private setScreen(screen: PrototypeScreenId): void {
    RuntimeStore.setScreen(screen);
    const roots: Array<[PrototypeScreenId, Node | null]> = [
      ['S0_ONE_LINE_SKY', this.s0Root], ['S1_RED_ROCK_MOUTH', this.s1Root], ['S2_RIVER_VALLEY', this.s2Root], ['ROUTE', this.routeRoot], ['MY_BOOK', this.myBookRoot],
    ];
    roots.forEach(([id, root]) => { if (root) root.active = id === screen; });
    this.closeReveal();
  }

  private bindPage(page: ReadingPage): void {
    if (this.pageTitleLabel) this.pageTitleLabel.string = page.title;
    if (this.observationLabel) this.observationLabel.string = page.observation ?? '';
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
}
